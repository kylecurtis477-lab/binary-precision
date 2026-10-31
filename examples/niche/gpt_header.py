"""GPT header (EFI partition table start).

Niche disk format.
"""
from construct import Struct, Const, Int32ul, Int64ul, Bytes

fmt = Struct(
    "signature" / Const(b"EFI PART"),
    "revision" / Int32ul,
    "header_size" / Int32ul,
    "crc32" / Int32ul,
    "reserved" / Int32ul,
    "current_lba" / Int64ul,
    "backup_lba" / Int64ul,
    "first_usable" / Int64ul,
    "last_usable" / Int64ul,
    "disk_guid" / Bytes(16),
    "part_entry_lba" / Int64ul,
    "num_entries" / Int32ul,
    "entry_size" / Int32ul,
    "entries_crc" / Int32ul,
)
