"""Simple CAN-like frame (embedded).

Niche automotive/industrial case.
"""
from construct import Struct, Const, Int32ul, Int8ul, Bytes, this

fmt = Struct(
    "magic" / Const(b"CAN1"),
    "id" / Int32ul,
    "dlc" / Int8ul,
    "data" / Bytes(this.dlc),
)
