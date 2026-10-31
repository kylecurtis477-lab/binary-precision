from construct import Struct, Const, Int32ul, Bytes, this

fmt = Struct(
    "magic" / Const(b"DEMO"),
    "count" / Int32ul,
    "payload" / Bytes(this.count),
)
