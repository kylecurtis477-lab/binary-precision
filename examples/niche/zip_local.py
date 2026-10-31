"""ZIP local file header (signature + metadata).

Common in archive tools. Shows fixed fields + variable filename.
"""
from construct import Struct, Const, Int16ul, Int32ul, Bytes, this

fmt = Struct(
    "signature" / Const(b"PK\x03\x04"),
    "version_needed" / Int16ul,
    "flags" / Int16ul,
    "compression" / Int16ul,
    "mod_time" / Int16ul,
    "mod_date" / Int16ul,
    "crc32" / Int32ul,
    "compressed_size" / Int32ul,
    "uncompressed_size" / Int32ul,
    "filename_len" / Int16ul,
    "extra_len" / Int16ul,
    "filename" / Bytes(this.filename_len),
    "extra" / Bytes(this.extra_len),
)
