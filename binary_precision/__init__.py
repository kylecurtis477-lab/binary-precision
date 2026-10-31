"""
binary_precision — high-accuracy declarative binary I/O.

Public API:
  parse(fmt, data) -> dict
  build(fmt, obj) -> bytes
  round_trip(fmt, obj) -> bool
  load_format(code_or_path) -> Struct
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    from construct import (
        Struct, Const, Int8ul, Int16ul, Int32ul, Int64ul,
        Int8sl, Int16sl, Int32sl, Int64sl,
        Float32l, Float64l, Bytes, CString, PascalString,
        Array, GreedyRange, Prefixed, Checksum, ChecksumError,
        Computed, If, Switch, Padding, this,
        ValidationError, StreamError,
    )
except ImportError as e:
    raise ImportError("construct is required: pip install construct") from e


def _to_jsonable(obj: Any) -> Any:
    if isinstance(obj, (bytes, bytearray)):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return obj.hex()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items() if not str(k).startswith("_")}
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    return obj


def _normalize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, str):
        try:
            return obj.encode("utf-8")
        except Exception:
            return obj
    if isinstance(obj, list):
        return [_normalize(x) for x in obj]
    return obj


def parse(fmt: Struct, data: bytes) -> Dict[str, Any]:
    """Parse with path-aware errors."""
    try:
        result = fmt.parse(data)
        return _to_jsonable(dict(result))
    except (ValidationError, StreamError, ChecksumError) as e:
        path = getattr(e, "path", "unknown")
        raise ValueError(f"Parse failed at {path}: {e}") from e
    except Exception as e:
        path = getattr(e, "path", "unknown")
        raise ValueError(f"Parse failed at {path}: {e}") from e


def build(fmt: Struct, obj: Dict[str, Any]) -> bytes:
    """Build from JSON-friendly object."""
    try:
        return fmt.build(_normalize(obj))
    except Exception as e:
        raise ValueError(f"Build failed: {e}") from e


def round_trip(fmt: Struct, obj: Dict[str, Any]) -> bool:
    """True if build(parse(obj)) == obj (after normalization)."""
    built = build(fmt, obj)
    parsed = parse(fmt, built)
    return parsed == _to_jsonable(_normalize(obj))


def load_format(source: Union[str, Path]) -> Struct:
    """Load a Struct named `fmt` from code string or .py file path."""
    if isinstance(source, Path):
        code = source.read_text()
    elif isinstance(source, str) and "\n" not in source and len(source) < 512:
        try:
            if Path(source).is_file():
                code = Path(source).read_text()
            else:
                code = source
        except OSError:
            code = source
    else:
        code = str(source)

    ns = {
        "Struct": Struct, "Const": Const, "Int8ul": Int8ul, "Int16ul": Int16ul,
        "Int32ul": Int32ul, "Int64ul": Int64ul, "Int8sl": Int8sl, "Int16sl": Int16sl,
        "Int32sl": Int32sl, "Int64sl": Int64sl, "Float32l": Float32l, "Float64l": Float64l,
        "Bytes": Bytes, "CString": CString, "PascalString": PascalString,
        "Array": Array, "GreedyRange": GreedyRange, "Prefixed": Prefixed,
        "Checksum": Checksum, "Computed": Computed, "If": If, "Switch": Switch,
        "Padding": Padding, "this": this,
    }
    try:
        exec(code, ns)
    except Exception as e:
        raise ValueError(f"Format load failed: {e}") from e
    fmt = ns.get("fmt")
    if not isinstance(fmt, Struct):
        raise ValueError("Code must define a Struct named 'fmt'")
    return fmt


def hexdump(data: bytes, width: int = 16) -> str:
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{i:08x}  {hex_part:<{width*3}}  |{ascii_part}|")
    return "\n".join(lines)
