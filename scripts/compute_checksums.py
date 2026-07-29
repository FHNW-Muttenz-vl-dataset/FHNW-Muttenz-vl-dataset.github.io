"""
Compute SHA-256 checksums and file sizes for the dataset's release zip
bundles, and write them into the checksums data files used by the
documentation site.

Usage
-----
    python compute_checksums.py --bundles-dir /path/to/zips

This updates two files, kept identical on every run:
  - docs/_data/checksums.json        (read by download.md to render the
                                       checksum tables via Liquid)
  - docs/assets/data/checksums.json  (public copy, directly downloadable
                                       from the Download page)

Bundles listed in the checksums file but not found in --bundles-dir are
left unchanged (with a warning); files found in --bundles-dir that
aren't listed in the checksums file are reported but not added
automatically.
"""

import argparse
import json
from pathlib import Path

from compute_sha256 import compute_sha256

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHECKSUMS_FILE = REPO_ROOT / "docs" / "_data" / "checksums.json"
DEFAULT_PUBLIC_COPY = REPO_ROOT / "docs" / "assets" / "data" / "checksums.json"


def size_gb(path: Path) -> float:
    """Return the file size in GB (decimal, 1 GB = 1e9 bytes), rounded to 2 decimals."""
    return round(path.stat().st_size / 1_000_000_000, 2)


def update_checksums(bundles_dir: Path, checksums_file: Path, public_copy: Path) -> None:
    with open(checksums_file, "r") as f:
        data = json.load(f)

    available = {p.name: p for p in bundles_dir.glob("*.zip")}
    listed_names = {bundle["file"] for bundle in data["bundles"]}

    for bundle in data["bundles"]:
        path = available.get(bundle["file"])
        if path is None:
            print(f"Warning: '{bundle['file']}' not found in {bundles_dir}, leaving unchanged.")
            continue
        bundle["size_gb"] = size_gb(path)
        bundle["sha256"] = compute_sha256(path)
        print(f"Updated {bundle['file']}: {bundle['size_gb']} GB, {bundle['sha256']}")

    unlisted = sorted(set(available) - listed_names)
    for name in unlisted:
        print(f"Note: '{name}' found in {bundles_dir} but not listed in {checksums_file}.")

    for output_path in (checksums_file, public_copy):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundles-dir",
        type=Path,
        required=True,
        help="Directory containing the release .zip bundles.",
    )
    parser.add_argument(
        "--checksums-file",
        type=Path,
        default=DEFAULT_CHECKSUMS_FILE,
        help=f"Path to the Liquid-facing checksums JSON file (default: {DEFAULT_CHECKSUMS_FILE}).",
    )
    parser.add_argument(
        "--public-copy",
        type=Path,
        default=DEFAULT_PUBLIC_COPY,
        help=f"Path to the publicly downloadable copy (default: {DEFAULT_PUBLIC_COPY}).",
    )
    args = parser.parse_args()
    update_checksums(args.bundles_dir, args.checksums_file, args.public_copy)


if __name__ == "__main__":
    main()
