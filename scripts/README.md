# Scripts

Utility scripts for working with the FHNW Muttenz visual localization dataset. See the [dataset documentation](../docs/dataset.md) for the underlying file formats and conventions.

## Requirements

Python >= 3.9, plus the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Scripts

### `pose_conversion.py`

Load `poses.json` / `camera_system.json` and convert image poses and relative orientations between the photogrammetric and computer vision camera coordinate conventions described in [Changing camera coordinate convention](../docs/dataset.md#changing-camera-coordinate-convention).

### `compute_sha256.py`

Compute the SHA-256 checksum of one or more files, e.g. to verify a downloaded bundle against the checksums published on [Download](../docs/download.md):

```bash
python compute_sha256.py 2023_panorama_camera.zip
```

### `compute_checksums.py` (maintainers only)

Compute SHA-256 checksums and sizes for the release `.zip` bundles and write them into [`docs/_data/checksums.json`](../docs/_data/checksums.json) (renders the checksum tables on [Download](../docs/download.md) via Liquid) and its public copy [`docs/assets/data/checksums.json`](../docs/assets/data/checksums.json) (linked from the same page for direct download), keeping both identical. Run it against the directory holding the prepared bundles before publishing a release; uses `compute_sha256.py` internally.

```bash
python compute_checksums.py --bundles-dir /path/to/zips
```
