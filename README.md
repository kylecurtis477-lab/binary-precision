# binary-precision

**High-accuracy declarative binary I/O.**  
Define formats once with Construct, get reliable parse/build, round-trip guarantees, and production-grade error reporting.

Target: 99%+ accuracy on specified formats. Ideal for protocols, file headers, embedded data, and data-oriented layouts.

## Install

```bash
pip install -e .
# or
pip install construct && python -m binary_precision.cli ...
```

## Quick Start

```bash
# Round-trip a format
binary-precision roundtrip \
  --format-file examples/demo_format.py \
  --json-input '{"magic":"DEMO","count":5,"payload":"hello"}'

# Parse
binary-precision parse data.bin --format-file examples/packet_with_crc.py --json

# Hex dump
binary-precision hex data.bin
```

## Examples

| File | What it covers |
|------|----------------|
| `examples/demo_format.py` | Basic magic + length-prefixed payload |
| `examples/packet_with_crc.py` | Magic + length + CRC32 |
| `examples/png_ihdr.py` | PNG signature + IHDR (width/height) |
| `examples/bmp_header.py` | BMP file + info header |
| `examples/elf_ident.py` | ELF identification (class, endianness) |
| `examples/wav_header.py` | WAV/RIFF header (sample rate, channels) |
| `examples/sensor_soa.py` | Data-oriented sensor frame (SoA arrays) |

## Niche Formats (`examples/niche/`)

| File | What it covers |
|------|----------------|
| `ipv4_header.py` | IPv4 header with bitfields |
| `zip_local.py` | ZIP local file header |
| `dns_header.py` | DNS header with flag bitfields |
| `versioned_protocol.py` | Versioned body via Switch |
| `mbr_partition.py` | MBR partition table entry |
| `telemetry.py` | IoT telemetry with bit-packed status |
| `pcap_packet.py` | PCAP packet record header |
| `mesh_header.py` | Simple mesh/asset header |
| `columnar_log.py` | Data-oriented log record |
| `auth_header.py` | Authenticated payload + MAC |
| `gif_header.py` | GIF logical screen descriptor |
| `can_frame.py` | CAN-like embedded frame |
| `tcp_header.py` | TCP header with flag bitfields |
| `jpeg_app0.py` | JPEG SOI + JFIF APP0 |
| `gpt_header.py` | GPT (EFI) partition header |
| `modbus_rtu.py` | Modbus RTU frame |
| `pe_optional.py` | PE optional header start |
| `timeseries.py` | Fixed-stride time-series record |
| `dhcp_option.py` | DHCP option (code + length) |

## Features

- Declarative formats (Construct)
- Path-aware error messages
- Round-trip validation
- `--format-file` for reusable definitions
- Checksum / magic / version patterns
- Data-oriented layout guidance (AoS vs SoA)
- Installable CLI + Python API
- CI tested

## Skill

This repo is also a Grok skill. See `SKILL.md`.

## Production Checklist

1. Define format in a `.py` file.
2. Add magic, length, checksum.
3. Run `roundtrip` on real + edge data.
4. Add size limits for untrusted input.
5. (Optional) `fmt.compile()` after validation for speed.

## License

MIT
