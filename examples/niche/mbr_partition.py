"""Simple MBR partition table entry (one of 16-byte records).

Niche but useful for disk tools.
"""
from construct import Struct, Int8ul, Int32ul, Bytes

fmt = Struct(
    "status" / Int8ul,
    "chs_start" / Bytes(3),
    "type_" / Int8ul,
    "chs_end" / Bytes(3),
    "lba_start" / Int32ul,
    "sectors" / Int32ul,
)
