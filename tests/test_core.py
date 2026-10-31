"""Tests for binary_precision."""

import json
from pathlib import Path

import pytest

from binary_precision import parse, build, round_trip, load_format


@pytest.fixture
def demo_fmt():
    return load_format(Path(__file__).parent.parent / "examples" / "demo_format.py")


def test_round_trip_demo(demo_fmt):
    obj = {"magic": "DEMO", "count": 5, "payload": "hello"}
    assert round_trip(demo_fmt, obj)


def test_parse_build_identity(demo_fmt):
    obj = {"magic": "DEMO", "count": 3, "payload": "abc"}
    data = build(demo_fmt, obj)
    parsed = parse(demo_fmt, data)
    assert parsed["count"] == 3
    assert parsed["payload"] == "abc"


def test_bad_magic_fails(demo_fmt):
    with pytest.raises(ValueError, match="Parse failed"):
        parse(demo_fmt, b"BADX" + b"\x00\x00\x00\x00")


def test_load_from_code():
    code = '''
from construct import Struct, Const, Int32ul
fmt = Struct("magic" / Const(b"OK"), "n" / Int32ul)
'''
    fmt = load_format(code)
    data = build(fmt, {"magic": "OK", "n": 42})
    assert parse(fmt, data)["n"] == 42
