"""Columnar log entry (data-oriented, SoA-style single record).

Useful for high-volume structured logging.
"""
from construct import Struct, Const, Int64ul, Int32ul, Float64l, Bytes

fmt = Struct(
    "magic" / Const(b"LOG1"),
    "timestamp_ns" / Int64ul,
    "level" / Int32ul,
    "code" / Int32ul,
    "value" / Float64l,
    "tag" / Bytes(8),
)
