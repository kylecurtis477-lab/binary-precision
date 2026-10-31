"""Authenticated header with simple HMAC-style length prefix.

Niche security pattern: magic + length + payload + mac placeholder.
"""
from construct import Struct, Const, Int32ul, Bytes, this

fmt = Struct(
    "magic" / Const(b"AUTH"),
    "payload_len" / Int32ul,
    "payload" / Bytes(this.payload_len),
    "mac" / Bytes(16),  # placeholder for HMAC/SHA256 truncated
)
