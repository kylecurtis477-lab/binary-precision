# Data-Oriented Layout Example

Contiguous arrays beat pointer-chasing for cache efficiency.

## Array-of-Structs (AoS) vs Struct-of-Arrays (SoA)

```python
from construct import Struct, Int32ul, Array

# AoS: each record is contiguous but fields are interleaved
aos = Struct(
    "records" / Array(1000, Struct(
        "id" / Int32ul,
        "value" / Int32ul,
        "flag" / Int32ul,
    ))
)

# SoA: each field is a contiguous array (better for SIMD / sequential scans)
soa = Struct(
    "ids" / Array(1000, Int32ul),
    "values" / Array(1000, Int32ul),
    "flags" / Array(1000, Int32ul),
)
```

Measure both with the round-trip tool and a profiler. SoA often wins when you process one field across many records.
