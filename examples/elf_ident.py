"""Minimal ELF identification header (first 16 bytes).

Detects class, data encoding, and version. Sufficient for many triage tasks.
"""
from construct import Struct, Const, Int8ul, Bytes

fmt = Struct(
    "magic" / Const(b"\x7fELF"),
    "class_" / Int8ul,          # 1=32-bit, 2=64-bit
    "data" / Int8ul,            # 1=little, 2=big
    "version" / Int8ul,
    "os_abi" / Int8ul,
    "abi_version" / Int8ul,
    "pad" / Bytes(7),
)
