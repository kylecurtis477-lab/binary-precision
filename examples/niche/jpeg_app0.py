"""JPEG SOI + APP0 (JFIF) marker.

Niche image format start.
"""
from construct import Struct, Const, Int16ub, Int8ub, Bytes, this

fmt = Struct(
    "soi" / Const(b"\xff\xd8"),
    "app0_marker" / Const(b"\xff\xe0"),
    "app0_length" / Int16ub,
    "identifier" / Const(b"JFIF\x00"),
    "version_major" / Int8ub,
    "version_minor" / Int8ub,
    "units" / Int8ub,
    "x_density" / Int16ub,
    "y_density" / Int16ub,
    "thumb_width" / Int8ub,
    "thumb_height" / Int8ub,
)
