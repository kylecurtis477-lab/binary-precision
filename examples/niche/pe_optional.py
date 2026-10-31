"""Minimal PE optional header signature + key fields.

Niche Windows executable.
"""
from construct import Struct, Int16ul, Int8ul, Int32ul, Int64ul

fmt = Struct(
    "magic" / Int16ul,  # 0x10b = PE32, 0x20b = PE32+
    "major_linker" / Int8ul,
    "minor_linker" / Int8ul,
    "size_of_code" / Int32ul,
    "size_of_initialized_data" / Int32ul,
    "size_of_uninitialized_data" / Int32ul,
    "address_of_entry_point" / Int32ul,
    "base_of_code" / Int32ul,
)
