"""Tests for niche formats."""

from pathlib import Path

import pytest

from binary_precision import load_format, round_trip


NICHE = Path(__file__).parent.parent / "examples" / "niche"


@pytest.mark.parametrize("name,obj", [
    ("ipv4_header.py", {
        "version_ihl": {"version": 4, "ihl": 5},
        "dscp_ecn": {"dscp": 0, "ecn": 0},
        "total_length": 20,
        "identification": 1,
        "flags_frag": {"flags": 2, "fragment_offset": 0},
        "ttl": 64,
        "protocol": 6,
        "checksum": 0,
        "src": 0x7f000001,
        "dst": 0x08080808,
    }),
    ("dns_header.py", {
        "id": 0x1234,
        "flags": {"qr": 1, "opcode": 0, "aa": 0, "tc": 0, "rd": 1, "ra": 1, "z": 0, "rcode": 0},
        "qdcount": 1,
        "ancount": 1,
        "nscount": 0,
        "arcount": 0,
    }),
    ("versioned_protocol.py", {
        "magic": "VER",
        "version": 1,
        "body": {"value": 42},
    }),
    ("telemetry.py", {
        "magic": "TLM1",
        "timestamp": 1234567890,
        "status": {"ok": 1, "error": 0, "calibrated": 1, "reserved": 0},
        "temp": 23.5,
        "humidity": 45.0,
        "pressure": 1013.25,
    }),
    ("pcap_packet.py", {
        "ts_sec": 1700000000,
        "ts_usec": 123456,
        "incl_len": 64,
        "orig_len": 64,
    }),
    ("mesh_header.py", {
        "magic": "MESH",
        "version": 1,
        "vertex_count": 1000,
        "index_count": 3000,
        "vertex_offset": 32,
        "index_offset": 1232,
    }),
    ("gif_header.py", {
        "signature": "GIF89a",
        "width": 320,
        "height": 240,
        "packed": {"gct_flag": 1, "color_res": 7, "sort": 0, "gct_size": 7},
        "bg_index": 0,
        "aspect": 0,
    }),
    ("can_frame.py", {
        "magic": "CAN1",
        "id": 0x123,
        "dlc": 8,
        "data": "\x01\x02\x03\x04\x05\x06\x07\x08",
    }),
])
def test_niche_roundtrip(name, obj):
    fmt = load_format(NICHE / name)
    assert round_trip(fmt, obj)
