"""GIF header (signature + logical screen descriptor start).

Niche image format.
"""
from construct import Struct, Const, Int16ul, Int8ul, BitStruct, BitsInteger, Flag

fmt = Struct(
    "signature" / Const(b"GIF89a"),
    "width" / Int16ul,
    "height" / Int16ul,
    "packed" / BitStruct(
        "gct_flag" / Flag,
        "color_res" / BitsInteger(3),
        "sort" / Flag,
        "gct_size" / BitsInteger(3),
    ),
    "bg_index" / Int8ul,
    "aspect" / Int8ul,
)
