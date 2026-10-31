"""DHCP option header (code + length).

Niche network configuration.
"""
from construct import Struct, Int8ul, Bytes, this

fmt = Struct(
    "code" / Int8ul,
    "length" / Int8ul,
    "value" / Bytes(this.length),
)
