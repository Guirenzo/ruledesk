from __future__ import annotations

import argparse
import re
import sys
import zlib
from pathlib import Path


def pdf_unescape(value: bytes) -> str:
    out = bytearray()
    i = 0
    while i < len(value):
        c = value[i]
        if c != 0x5C:
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= len(value):
            break
        esc = value[i]
        i += 1
        mapping = {
            ord("n"): ord("\n"),
            ord("r"): ord("\r"),
            ord("t"): ord("\t"),
            ord("b"): ord("\b"),
            ord("f"): ord("\f"),
            ord("("): ord("("),
            ord(")"): ord(")"),
            ord("\\"): ord("\\"),
        }
        if esc in mapping:
            out.append(mapping[esc])
        elif 48 <= esc <= 55:
            digits = bytes([esc])
            for _ in range(2):
                if i < len(value) and 48 <= value[i] <= 55:
                    digits += bytes([value[i]])
                    i += 1
                else:
                    break
            out.append(int(digits, 8))
        elif esc in (10, 13):
            if esc == 13 and i < len(value) and value[i] == 10:
                i += 1
        else:
            out.append(esc)
    for encoding in ("utf-16-be", "utf-8", "cp1252", "latin-1"):
        try:
            return out.decode(encoding)
        except UnicodeDecodeError:
            pass
    return out.decode("latin-1", errors="replace")


def extract_streams(data: bytes) -> list[tuple[bytes, bytes]]:
    streams: list[tuple[bytes, bytes]] = []
    for match in re.finditer(rb"<<(?P<dict>.*?)>>\s*stream\r?\n(?P<stream>.*?)\r?\nendstream", data, re.S):
        dictionary = match.group("dict")
        stream = match.group("stream")
        if b"FlateDecode" in dictionary:
            try:
                stream = zlib.decompress(stream)
            except zlib.error:
                pass
        streams.append((dictionary, stream))
    return streams


def extract_strings_from_stream(stream: bytes) -> list[str]:
    strings: list[str] = []
    for literal in re.finditer(rb"\((?:\\.|[^\\()])*\)", stream, re.S):
        text = pdf_unescape(literal.group(0)[1:-1])
        if text.strip():
            strings.append(text)
    for hex_string in re.finditer(rb"<([0-9A-Fa-f\s]+)>", stream):
        raw_hex = re.sub(rb"\s+", b"", hex_string.group(1))
        if len(raw_hex) < 2:
            continue
        if len(raw_hex) % 2:
            raw_hex += b"0"
        try:
            raw = bytes.fromhex(raw_hex.decode("ascii"))
        except ValueError:
            continue
        for encoding in ("utf-16-be", "utf-8", "cp1252", "latin-1"):
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                text = raw.decode("latin-1", errors="replace")
        if text.strip() and any(ch.isalnum() for ch in text):
            strings.append(text)
    return strings


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--dump-streams", action="store_true")
    args = parser.parse_args()

    data = args.pdf.read_bytes()
    print(f"bytes: {len(data)}")
    print(f"pages markers: {len(re.findall(rb'/Type\\s*/Page\\b', data))}")
    streams = extract_streams(data)
    print(f"streams: {len(streams)}")

    all_text: list[str] = []
    for index, (dictionary, stream) in enumerate(streams):
        strings = extract_strings_from_stream(stream)
        if args.dump_streams:
            print(f"\n--- stream {index} dict ---")
            print(dictionary[:500].decode("latin-1", errors="replace"))
            print(f"--- stream {index} sample ---")
            print(stream[:2000].decode("latin-1", errors="replace"))
        if strings:
            all_text.append(f"\n[stream {index}]")
            all_text.extend(strings)

    print("\n=== Extracted strings ===")
    print("\n".join(all_text))


if __name__ == "__main__":
    main()
