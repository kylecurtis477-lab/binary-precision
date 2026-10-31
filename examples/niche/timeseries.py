"""Simple time-series record (data-oriented, fixed stride).

Niche analytics / logging.
"""
from construct import Struct, Const, Int64ul, Float64l, Int32ul

fmt = Struct(
    "magic" / Const(b"TS01"),
    "timestamp" / Int64ul,
    "value" / Float64l,
    "quality" / Int32ul,
)
