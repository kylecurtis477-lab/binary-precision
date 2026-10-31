"""Versioned protocol with Switch.

Demonstrates conditional body based on version.
"""
from construct import Struct, Const, Int8ul, Int16ul, Switch, this, Bytes

BodyV1 = Struct("value" / Int16ul)
BodyV2 = Struct("value" / Int16ul, "extra" / Bytes(4))

fmt = Struct(
    "magic" / Const(b"VER"),
    "version" / Int8ul,
    "body" / Switch(this.version, {
        1: BodyV1,
        2: BodyV2,
    }),
)
