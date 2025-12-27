#!/usr/bin/env python3
"""
rot13 — ROT13 encoder/decoder

Author: Supun Hewagamage
"""

VERSION = "1.0.0"
AUTHOR = "Supun Hewagamage"

import argparse
import sys
import codecs
from pathlib import Path


def rot13(text: str) -> str:
    return codecs.encode(text, "rot_13")


def process_file(path: Path) -> str:
    try:
        return rot13(path.read_text())
    except Exception as e:
        sys.exit(f"[!] Error reading file '{path}': {e}")


def main():
    parser = argparse.ArgumentParser(
        prog="rot13",
        description="ROT13 encode/decode strings, files, or stdin",
        epilog="Examples:\n"
               "  rot13 hello\n"
               "  rot13 file.txt\n"
               "  echo hello | rot13\n"
               "  rot13 hello file.txt -o out.txt\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "inputs",
        nargs="*",
        help="Strings or files"
    )

    parser.add_argument(
        "-o", "--output",
        help="Write output to file"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"rot13 {VERSION}\nAuthor: {AUTHOR}",
    )

    args = parser.parse_args()

    output = []

    # ── stdin support ─────────────────────────────
    if not sys.stdin.isatty():
        output.append(rot13(sys.stdin.read()))

    # ── args/files ────────────────────────────────
    for item in args.inputs:
        path = Path(item)
        if path.exists() and path.is_file():
            output.append(process_file(path))
        else:
            output.append(rot13(item))

    if not output:
        parser.print_help()
        sys.exit(0)

    final_output = "\n".join(o.rstrip("\n") for o in output)

    if args.output:
        try:
            Path(args.output).write_text(final_output + "\n")
        except Exception as e:
            sys.exit(f"[!] Could not write to output file: {e}")
    else:
        print(final_output)


if __name__ == "__main__":
    main()
