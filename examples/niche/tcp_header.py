"""TCP header (minimal, big-endian).

Shows bitfields for flags and options length.
"""
from construct import Struct, Int16ub, Int32ub, BitStruct, BitsInteger, Flag

fmt = Struct(
    "src_port" / Int16ub,
    "dst_port" / Int16ub,
    "seq" / Int32ub,
    "ack" / Int32ub,
    "data_offset_flags" / BitStruct(
        "data_offset" / BitsInteger(4),
        "reserved" / BitsInteger(3),
        "ns" / Flag,
        "cwr" / Flag,
        "ece" / Flag,
        "urg" / Flag,
        "ack_flag" / Flag,
        "psh" / Flag,
        "rst" / Flag,
        "syn" / Flag,
        "fin" / Flag,
    ),
    "window" / Int16ub,
    "checksum" / Int16ub,
    "urgent" / Int16ub,
)
