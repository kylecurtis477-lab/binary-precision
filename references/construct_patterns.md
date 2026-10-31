# Construct Patterns for High-Accuracy Binary

Use these patterns to maximize reliability when defining formats with Construct.

## Core Principles for 99%+ Accuracy

1. **Always validate** — Use `Const`, `Checksum`, length checks, and range assertions.
2. **Round-trip every format** — Build → parse → compare before trusting.
3. **Explicit endianness** — Prefer `*l` (little) or `*b` (big) variants; never rely on defaults for portable data.
4. **Document offsets** — Comment field offsets in the format definition.
5. **Fail loudly** — Catch `ValidationError` / `ChecksumError` and report the offset.

## Essential Constructs

| Need | Construct | Example |
|------|-----------|---------|
| Unsigned 32-bit LE | `Int32ul` | `Int32ul` |
| Signed 16-bit BE | `Int16sb` | `Int16sb` |
| Fixed bytes | `Bytes(n)` | `Bytes(4)` |
| Null-terminated | `CString("utf8")` | `CString("utf8")` |
| Length-prefixed | `PascalString(Int8ul, "utf8")` | — |
| Array of fixed size | `Array(n, type)` | `Array(4, Int16ul)` |
| Until end | `GreedyRange(type)` | `GreedyRange(Int32ul)` |
| Conditional | `If(this.flag, type)` | — |
| Magic / constant | `Const(b"PNG")` | `Const(b"\x89PNG")` |
| Checksum | `Checksum(Int32ul, lambda data: zlib.crc32(data))` | See below |

## Checksum Pattern

```python
import zlib
from construct import Struct, Int32ul, Bytes, Checksum, this

fmt = Struct(
    "payload" / Bytes(this._.payload_len),
    "crc" / Checksum(Int32ul, lambda data: zlib.crc32(data) & 0xffffffff,
                     this.payload),
)
```

## Versioned Format Pattern

```python
fmt = Struct(
    "magic" / Const(b"FMT1"),
    "version" / Int16ul,
    "body" / Switch(this.version, {
        1: BodyV1,
        2: BodyV2,
    }),
)
```

## Alignment / Padding

```python
"pad" / Padding(4),          # fixed
"align" / Padding(lambda ctx: (4 - (ctx.offset % 4)) % 4),
```

## Best Practices Checklist

- [ ] Magic number or signature present
- [ ] All multi-byte fields specify endianness
- [ ] Length fields validated against actual data
- [ ] Checksums or CRCs on critical sections
- [ ] Round-trip test passes on golden samples
- [ ] Edge cases tested (empty, max size, truncated)
- [ ] Error messages include byte offset when possible

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Implicit endianness | Always use `ul`/`ub`/`sl`/`sb` |
| Missing length validation | Use `Prefixed` or explicit checks |
| Float equality in round-trips | Use approximate compare or store as integers |
| Unaligned access assumptions | Explicit `Padding` |
| Silent truncation | Use `ValidationError` handlers |

See Construct docs for full API: https://construct.readthedocs.io/
