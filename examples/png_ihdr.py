"""Minimal PNG signature + IHDR chunk.

Useful for quickly validating PNG files and extracting dimensions.
"""
from construct import Struct, Const, Int32ub, Int8ul, Bytes, this

fmt = Struct(
    "signature" / Const(b"\x89PNG\r\n\x1a\n"),
    "ihdr_length" / Int32ub,
    "ihdr_type" / Const(b"IHDR"),
    "width" / Int32ub,
    "height" / Int32ub,
    "bit_depth" / Int8ul,
    "color_type" / Int8ul,
    "compression" / Int8ul,
    "filter" / Int8ul,
    "interlace" / Int8ul,
    "ihdr_crc" / Int32ub,
)
