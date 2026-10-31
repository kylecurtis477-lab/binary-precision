"""Modbus RTU frame (simple function code + data).

Niche industrial protocol.
"""
from construct import Struct, Int8ul, Int16ul, Bytes, this

fmt = Struct(
    "slave" / Int8ul,
    "function" / Int8ul,
    "data_len" / Int8ul,
    "data" / Bytes(this.data_len),
    "crc" / Int16ul,
)
