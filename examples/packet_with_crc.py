from construct import Struct, Const, Int32ul, Bytes, this, Checksum
import zlib

fmt = Struct(
    "magic" / Const(b"PKT1"),
    "length" / Int32ul,
    "payload" / Bytes(this.length),
    "crc" / Checksum(
        Int32ul,
        lambda data: zlib.crc32(data) & 0xffffffff,
        this.payload,
    ),
)
