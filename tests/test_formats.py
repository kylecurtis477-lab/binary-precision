"""Tests for additional example formats."""

from pathlib import Path

import pytest

from binary_precision import load_format, round_trip, build, parse


EXAMPLES = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize("name,obj", [
    ("bmp_header.py", {
        "signature": "BM",
        "file_size": 54,
        "reserved": 0,
        "data_offset": 54,
        "header_size": 40,
        "width": 100,
        "height": 50,
        "planes": 1,
        "bpp": 24,
        "compression": 0,
    }),
    ("elf_ident.py", {
        "magic": "\x7fELF",
        "class_": 2,
        "data": 1,
        "version": 1,
        "os_abi": 0,
        "abi_version": 0,
        "pad": "\x00" * 7,
    }),
    ("wav_header.py", {
        "riff": "RIFF",
        "file_size": 36,
        "wave": "WAVE",
        "fmt_": "fmt ",
        "fmt_size": 16,
        "audio_format": 1,
        "channels": 2,
        "sample_rate": 44100,
        "byte_rate": 176400,
        "block_align": 4,
        "bits_per_sample": 16,
    }),
])
def test_format_roundtrip(name, obj):
    fmt = load_format(EXAMPLES / name)
    assert round_trip(fmt, obj)


def test_sensor_soa_roundtrip():
    fmt = load_format(EXAMPLES / "sensor_soa.py")
    obj = {
        "magic": "SNS1",
        "count": 2,
        "timestamps": [1000, 2000],
        "values": [1.5, 2.5],
        "flags": [1, 0],
    }
    assert round_trip(fmt, obj)
    data = build(fmt, obj)
    parsed = parse(fmt, data)
    assert parsed["count"] == 2
    assert len(parsed["values"]) == 2
