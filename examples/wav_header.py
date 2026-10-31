"""Minimal WAV/RIFF header.

Extracts sample rate, channels, and bit depth.
"""
from construct import Struct, Const, Int32ul, Int16ul, Bytes

fmt = Struct(
    "riff" / Const(b"RIFF"),
    "file_size" / Int32ul,
    "wave" / Const(b"WAVE"),
    "fmt_" / Const(b"fmt "),
    "fmt_size" / Int32ul,
    "audio_format" / Int16ul,
    "channels" / Int16ul,
    "sample_rate" / Int32ul,
    "byte_rate" / Int32ul,
    "block_align" / Int16ul,
    "bits_per_sample" / Int16ul,
)
