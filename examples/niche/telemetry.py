"""Telemetry frame with bit-packed status.

Niche IoT/sensor case with mixed dense and sparse fields.
"""
from construct import Struct, Const, Int32ul, Float32l, BitStruct, BitsInteger, Flag, this

fmt = Struct(
    "magic" / Const(b"TLM1"),
    "timestamp" / Int32ul,
    "status" / BitStruct(
        "ok" / Flag,
        "error" / Flag,
        "calibrated" / Flag,
        "reserved" / BitsInteger(5),
    ),
    "temp" / Float32l,
    "humidity" / Float32l,
    "pressure" / Float32l,
)
