"""Minimal BMP file header (BITMAPFILEHEADER + BITMAPINFOHEADER start).

Extracts dimensions and basic metadata from common BMPs.
"""
from construct import Struct, Const, Int32ul, Int16ul, Int8ul

fmt = Struct(
    "signature" / Const(b"BM"),
    "file_size" / Int32ul,
    "reserved" / Int32ul,
    "data_offset" / Int32ul,
    "header_size" / Int32ul,
    "width" / Int32ul,
    "height" / Int32ul,
    "planes" / Int16ul,
    "bpp" / Int16ul,
    "compression" / Int32ul,
)
