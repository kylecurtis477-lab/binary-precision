#!/usr/bin/env python3
"""CLI for binary_precision. Run with: python -m binary_precision or binary-precision after install."""

import argparse
import json
import sys
from pathlib import Path

from . import parse, build, round_trip, load_format, hexdump


def main(argv=None):
    p = argparse.ArgumentParser(prog="binary-precision", description="High-accuracy binary I/O")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_fmt(sp):
        sp.add_argument("--format-file", type=Path, help="Path to .py defining fmt")
        sp.add_argument("--format-code", help="Inline Python code defining fmt")

    # parse
    sp = sub.add_parser("parse")
    sp.add_argument("file", type=Path)
    add_fmt(sp)
    sp.add_argument("--json", action="store_true")

    # build
    sp = sub.add_parser("build")
    sp.add_argument("output", type=Path)
    add_fmt(sp)
    sp.add_argument("--json-input", required=True, help="JSON string or @file.json")

    # roundtrip
    sp = sub.add_parser("roundtrip")
    add_fmt(sp)
    sp.add_argument("--json-input", required=True)

    # hex
    sp = sub.add_parser("hex")
    sp.add_argument("file", type=Path)

    # compile (performance)
    sp = sub.add_parser("compile")
    add_fmt(sp)
    sp.add_argument("--out", type=Path, default=Path("compiled_fmt.py"))

    args = p.parse_args(argv)

    def get_fmt():
        if args.format_file:
            return load_format(args.format_file)
        if args.format_code:
            return load_format(args.format_code)
        p.error("Provide --format-file or --format-code")

    if args.cmd == "hex":
        print(hexdump(args.file.read_bytes()))
        return 0

    fmt = get_fmt()

    if args.cmd == "parse":
        result = parse(fmt, args.file.read_bytes())
        print(json.dumps(result, indent=2) if args.json else result)
        return 0

    if args.cmd == "build":
        js = args.json_input
        if js.startswith("@"):
            js = Path(js[1:]).read_text()
        data = build(fmt, json.loads(js))
        args.output.write_bytes(data)
        print(f"Wrote {len(data)} bytes → {args.output}")
        return 0

    if args.cmd == "roundtrip":
        js = args.json_input
        if js.startswith("@"):
            js = Path(js[1:]).read_text()
        ok = round_trip(fmt, json.loads(js))
        print("ROUND-TRIP OK" if ok else "ROUND-TRIP FAILED")
        return 0 if ok else 1

    if args.cmd == "compile":
        compiled = fmt.compile()
        args.out.write_text(
            "# Auto-compiled by binary-precision\n"
            "from construct import Struct\n"
            f"fmt = {compiled!r}\n"
        )
        print(f"Compiled format written to {args.out}")
        print("Note: compiled parsers are faster but less forgiving of corrupt data.")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
