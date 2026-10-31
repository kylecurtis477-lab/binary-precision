"""Minimal DNS header.

Shows flags as bitfields and count fields.
"""
from construct import Struct, Int16ub, BitStruct, BitsInteger, Flag

fmt = Struct(
    "id" / Int16ub,
    "flags" / BitStruct(
        "qr" / Flag,
        "opcode" / BitsInteger(4),
        "aa" / Flag,
        "tc" / Flag,
        "rd" / Flag,
        "ra" / Flag,
        "z" / BitsInteger(3),
        "rcode" / BitsInteger(4),
    ),
    "qdcount" / Int16ub,
    "ancount" / Int16ub,
    "nscount" / Int16ub,
    "arcount" / Int16ub,
)
