"""PCAP packet record header (global + packet).

Common in network capture tools.
"""
from construct import Struct, Int32ul, Int16ul

fmt = Struct(
    "ts_sec" / Int32ul,
    "ts_usec" / Int32ul,
    "incl_len" / Int32ul,
    "orig_len" / Int32ul,
)
