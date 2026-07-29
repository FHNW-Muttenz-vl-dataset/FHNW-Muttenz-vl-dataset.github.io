"""
Compute the SHA-256 checksum of one or more files.

Useful for verifying a downloaded dataset bundle against the checksums
published on the Download page.

Usage
-----
    python compute_sha256.py file1.zip [file2.zip ...]
"""

import argparse
from pathlib import Path
import hashlib

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MiB


def compute_sha256(path: Path) -> str:
    """Compute the SHA-256 checksum of a file, reading it in chunks."""
    with open(path, "rb") as f:
        if hasattr(
            hashlib, "file_digest"
        ):  # Python >= 3.11: optimized read/hash loop
            return hashlib.file_digest(f, "sha256").hexdigest()
        digest = hashlib.sha256()
        buf = bytearray(CHUNK_SIZE)
        view = memoryview(buf)
        while True:
            n = f.readinto(buf)
            if not n:
                break
            digest.update(view[:n])
        return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files", type=Path, nargs="+", help="File(s) to checksum."
    )
    args = parser.parse_args()

    for path in args.files:
        print(f"{compute_sha256(path)}  {path.name}")


if __name__ == "__main__":
    main()
