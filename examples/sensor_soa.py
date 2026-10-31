"""Data-oriented sensor frame (SoA-friendly).

Fixed layout for high-throughput sensor logs.
"""
from construct import Struct, Const, Int32ul, Int16ul, Float32l, Array, this

fmt = Struct(
    "magic" / Const(b"SNS1"),
    "count" / Int32ul,
    "timestamps" / Array(this.count, Int32ul),
    "values" / Array(this.count, Float32l),
    "flags" / Array(this.count, Int16ul),
)
