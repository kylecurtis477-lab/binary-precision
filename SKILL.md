---
name: binary-precision
description: "High-accuracy binary read and write using declarative Construct formats with validation and round-trip checks. Use when parsing, generating, or validating binary files, protocols, or data structures for maximum reliability and efficiency."
type: workflow
lifecycle: active
---

# Binary Precision — Declarative High-Accuracy Binary I/O

Parse and generate binary data with near-100% fidelity using Construct. Focus on validation, round-trips, and data-oriented layouts so programs stay compact and correct without unnecessary translation layers.

## When to Use

- Reading or writing custom binary formats, file headers, protocols, or embedded data.
- Need reliable round-trip (build → parse → identical) guarantees.
- Optimizing memory layout or serialization for performance.
- Inspecting or debugging binary with structured field views.

## Core Workflow

1. **Define the format**  
   Write a Construct `Struct` (or load from code). Prefer explicit endianness, constants, and checksums.  
   See `references/construct_patterns.md` for patterns that raise accuracy.

2. **Validate with round-trip**  
   Use the bundled script to confirm build/parse identity before trusting the format.

3. **Parse or build**  
   Run `scripts/binary_tool.py` or import the helpers.

4. **Inspect when needed**  
   Hex dump with offsets to correlate failures.

## Using the Tool

Script location: `scripts/binary_tool.py` (requires `construct` — `pip install construct`).

### Parse a file
```bash
python3 scripts/binary_tool.py parse data.bin \
  --format-code 'fmt = Struct("magic" / Const(b"TEST"), "value" / Int32ul)' \
  --json
```

### Build from JSON
```bash
python3 scripts/binary_tool.py build out.bin \
  --format-code 'fmt = Struct("magic" / Const(b"TEST"), "value" / Int32ul)' \
  --json-input '{"magic": "TEST", "value": 42}'
```

### Round-trip test
```bash
python3 scripts/binary_tool.py roundtrip \
  --format-code 'fmt = Struct("magic" / Const(b"TEST"), "value" / Int32ul)' \
  --json-input '{"magic": "TEST", "value": 42}'
```

### Hex dump
```bash
python3 scripts/binary_tool.py hex data.bin
```

## Production Notes

- Prefer `--format-file` over inline `--format-code` for reusable, reviewable definitions.
- Always run `roundtrip` on real and edge-case data before trusting a format.
- Once validated, call `fmt.compile()` for faster parse/build in hot paths (Construct 2.10+).
- Do not parse untrusted input without explicit size limits, checksums, and validation.
- For complex types (nested, floats, custom adapters), supply Python objects rather than pure JSON when building.

## Resources

- `scripts/binary_tool.py` — CLI for parse/build/roundtrip/hex.
- `references/construct_patterns.md` — Patterns, checklist, and pitfalls for 99%+ reliability.
- `references/data_oriented.md` — Layout tips for cache-efficient binary structures.

## Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `ValidationError` | Magic/checksum mismatch or truncated data | Check offsets with hex dump; verify format version |
| Round-trip fails | Float precision or missing field | Use integer fixed-point or ensure all fields are in the object |
| Import error | construct missing | `pip install construct` |
| Wrong values | Endianness | Switch `ul` ↔ `ub` and re-test round-trip |
