"""IPv4 header (minimal, big-endian).

Demonstrates bitfields and computed fields.
"""
from construct import Struct, BitStruct, BitsInteger, Int8ub, Int16ub, Int32ub, Computed

fmt = Struct(
    "version_ihl" / BitStruct(
        "version" / BitsInteger(4),
        "ihl" / BitsInteger(4),
    ),
    "dscp_ecn" / BitStruct(
        "dscp" / BitsInteger(6),
        "ecn" / BitsInteger(2),
    ),
    "total_length" / Int16ub,
    "identification" / Int16ub,
    "flags_frag" / BitStruct(
        "flags" / BitsInteger(3),
        "fragment_offset" / BitsInteger(13),
    ),
    "ttl" / Int8ub,
    "protocol" / Int8ub,
    "checksum" / Int16ub,
    "src" / Int32ub,
    "dst" / Int32ub,
)
