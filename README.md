# binary-precision

High-accuracy declarative binary read/write skill and toolkit using [Construct](https://construct.readthedocs.io/).

Designed for production use: validation, round-trip guarantees, explicit endianness, checksums, and data-oriented layout guidance. Target 99%+ accuracy on specified formats.

## Quick Start

```bash
pip install -r requirements.txt
```

```bash
# Parse
python3 scripts/binary_tool.py parse data.bin --format-file examples/demo_format.py --json

# Round-trip test
python3 scripts/binary_tool.py roundtrip --format-file examples/demo_format.py --json-input '{"magic":"DEMO","count":5,"payload":"hello"}'
```

## Skill Usage

This is structured as a Grok skill. See `SKILL.md` for the full workflow.

- `scripts/binary_tool.py` — CLI
- `references/` — patterns and data-oriented advice
- `examples/` — sample formats

## Production Notes

- Always validate with round-trip on real data.
- Prefer `--format-file` for reusable definitions.
- Add magic, checksums, and size limits for untrusted input.
- Use `fmt.compile()` after validation for speed.

MIT License.
