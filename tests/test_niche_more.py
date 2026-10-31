"""Additional niche format tests."""

from pathlib import Path

import pytest

from binary_precision import load_format, round_trip


NICHE = Path(__file__).parent.parent / "examples" / "niche"


@pytest.mark.parametrize("name,obj", [
    ("tcp_header.py", {
        "src_port": 12345,
        "dst_port": 80,
        "seq": 1000,
        "ack": 2000,
        "data_offset_flags": {
            "data_offset": 5, "reserved": 0, "ns": 0, "cwr": 0, "ece": 0,
            "urg": 0, "ack_flag": 1, "psh": 0, "rst": 0, "syn": 0, "fin": 0
        },
        "window": 65535,
        "checksum": 0,
        "urgent": 0,
    }),
    ("gpt_header.py", {
        "signature": "EFI PART",
        "revision": 0x00010000,
        "header_size": 92,
        "crc32": 0,
        "reserved": 0,
        "current_lba": 1,
        "backup_lba": 100,
        "first_usable": 34,
        "last_usable": 66,
        "disk_guid": "\x00" * 16,
        "part_entry_lba": 2,
        "num_entries": 128,
        "entry_size": 128,
        "entries_crc": 0,
    }),
    ("modbus_rtu.py", {
        "slave": 1,
        "function": 3,
        "data_len": 4,
        "data": "\x00\x00\x00\x0a",
        "crc": 0x1234,
    }),
    ("timeseries.py", {
        "magic": "TS01",
        "timestamp": 1700000000000000000,
        "value": 3.14159,
        "quality": 192,
    }),
    ("dhcp_option.py", {
        "code": 53,
        "length": 1,
        "value": "\x01",
    }),
])
def test_more_niche_roundtrip(name, obj):
    fmt = load_format(NICHE / name)
    assert round_trip(fmt, obj)
