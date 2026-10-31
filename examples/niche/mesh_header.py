"""Simple mesh header (graphics/game asset).

Shows counts + offset-style fields.
"""
from construct import Struct, Const, Int32ul, Int16ul, this

fmt = Struct(
    "magic" / Const(b"MESH"),
    "version" / Int16ul,
    "vertex_count" / Int32ul,
    "index_count" / Int32ul,
    "vertex_offset" / Int32ul,
    "index_offset" / Int32ul,
)
