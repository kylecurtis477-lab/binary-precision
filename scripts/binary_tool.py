#!/usr/bin/env python3
"""
High-accuracy binary read/write toolkit using Construct.
Provides declarative format definitions, parse/build with validation,
round-trip checks, and hex inspection for maximum reliability.
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from construct import (
        Struct, Int8ul, Int16ul, Int32ul, Int64ul,
        Int8sl, Int16sl, Int32sl, Int64sl,
        Float32l, Float64l, Bytes, CString, PascalString,
        Array, GreedyRange, Prefixed, Checksum, ChecksumError,
        Computed, If, Switch, Padding, Const, this,
        Container, ValidationError, StreamError
    )
    import construct
except ImportError:
    print("ERROR: construct library required. Install with: pip install construct", file=sys.stderr)
    sys.exit(1)


def hexdump(data: bytes, width: int = 16, offset: int = 0) -> str:
    """Produce annotated hex dump with ASCII."""
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{offset + i:08x}  {hex_part:<{width * 3}}  |{ascii_part}|")
    return "\n".join(lines)


def _to_jsonable(obj: Any) -> Any:
    """Convert Construct Container / bytes to JSON-friendly form."""
    if isinstance(obj, (bytes, bytearray)):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return obj.hex()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    return obj


def parse_binary(fmt: Struct, data: bytes, strict: bool = True) -> Dict[str, Any]:
    """Parse binary data with a Construct format. Returns dict or raises with offset info."""
    try:
        result = fmt.parse(data)
        return _to_jsonable(dict(result))
    except (ValidationError, StreamError, ChecksumError) as e:
        path = getattr(e, "path", "unknown")
        raise ValueError(f"Parse failed at path {path}: {e}") from e


def _normalize_for_build(obj: Any, fmt: Struct) -> Any:
    """Convert JSON-friendly values (str) to bytes where Construct expects them."""
    if isinstance(obj, dict):
        return {k: _normalize_for_build(v, fmt) for k, v in obj.items()}
    if isinstance(obj, str):
        # Heuristic: if it looks like a short ASCII magic or payload, try bytes
        try:
            return obj.encode("utf-8")
        except Exception:
            return obj
    if isinstance(obj, list):
        return [_normalize_for_build(x, fmt) for x in obj]
    return obj


def build_binary(fmt: Struct, obj: Dict[str, Any]) -> bytes:
    """Build binary from object using Construct format."""
    try:
        normalized = _normalize_for_build(obj, fmt)
        return fmt.build(normalized)
    except Exception as e:
        raise ValueError(f"Build failed: {e}") from e


def round_trip(fmt: Struct, obj: Dict[str, Any], tolerance: Optional[Dict] = None) -> bool:
    """Build then parse and compare. Returns True if identical (within tolerance)."""
    built = build_binary(fmt, obj)
    parsed = parse_binary(fmt, built)
    # Simple equality for most cases; extend for floats if needed
    return parsed == obj


def load_format_from_code(code: str) -> Struct:
    """Execute user-supplied format definition code and return the Struct named 'fmt'."""
    namespace = {
        "Struct": Struct, "Int8ul": Int8ul, "Int16ul": Int16ul, "Int32ul": Int32ul,
        "Int64ul": Int64ul, "Int8sl": Int8sl, "Int16sl": Int16sl, "Int32sl": Int32sl,
        "Int64sl": Int64sl, "Float32l": Float32l, "Float64l": Float64l,
        "Bytes": Bytes, "CString": CString, "PascalString": PascalString,
        "Array": Array, "GreedyRange": GreedyRange, "Prefixed": Prefixed,
        "Checksum": Checksum, "Computed": Computed, "If": If, "Switch": Switch,
        "Padding": Padding, "Const": Const, "this": this,
    }
    try:
        exec(code, namespace)
    except Exception as e:
        raise ValueError(f"Failed to load format code: {e}") from e
    if "fmt" not in namespace or not isinstance(namespace["fmt"], Struct):
        raise ValueError("Format code must define a Struct named 'fmt'")
    return namespace["fmt"]


def load_format(format_code: Optional[str] = None, format_file: Optional[Path] = None) -> Struct:
    if format_file:
        code = format_file.read_text()
    elif format_code:
        code = format_code
    else:
        raise ValueError("Provide --format-code or --format-file")
    return load_format_from_code(code)


def main():
    parser = argparse.ArgumentParser(description="High-accuracy binary read/write tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_parse = sub.add_parser("parse", help="Parse binary file with format")
    p_parse.add_argument("file", type=Path)
    p_parse.add_argument("--format-code", help="Python code defining fmt = Struct(...)")
    p_parse.add_argument("--format-file", type=Path, help="File containing format definition")
    p_parse.add_argument("--json", action="store_true", help="Output as JSON")

    p_build = sub.add_parser("build", help="Build binary from JSON object")
    p_build.add_argument("output", type=Path)
    p_build.add_argument("--format-code")
    p_build.add_argument("--format-file", type=Path)
    p_build.add_argument("--json-input", required=True, help="JSON string or @file.json")

    p_round = sub.add_parser("roundtrip", help="Test round-trip fidelity")
    p_round.add_argument("--format-code")
    p_round.add_argument("--format-file", type=Path)
    p_round.add_argument("--json-input", required=True)

    p_hex = sub.add_parser("hex", help="Hex dump a file")
    p_hex.add_argument("file", type=Path)

    args = parser.parse_args()

    if args.cmd == "hex":
        data = args.file.read_bytes()
        print(hexdump(data))
        return

    fmt = load_format(
        getattr(args, "format_code", None),
        getattr(args, "format_file", None),
    )

    if args.cmd == "parse":
        data = args.file.read_bytes()
        result = parse_binary(fmt, data)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(result)

    elif args.cmd == "build":
        json_str = args.json_input
        if json_str.startswith("@"):
            json_str = Path(json_str[1:]).read_text()
        obj = json.loads(json_str)
        data = build_binary(fmt, obj)
        args.output.write_bytes(data)
        print(f"Wrote {len(data)} bytes to {args.output}")

    elif args.cmd == "roundtrip":
        json_str = args.json_input
        if json_str.startswith("@"):
            json_str = Path(json_str[1:]).read_text()
        obj = json.loads(json_str)
        success = round_trip(fmt, obj)
        print("ROUND-TRIP OK" if success else "ROUND-TRIP FAILED")
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
