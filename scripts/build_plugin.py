"""Create a deterministic local-only Cyclizer Plugin Package v2."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"
COMPONENT = "third-party.development-journal"
FILES = (
    "plugin.json",
    f"components/{COMPONENT}/component.json",
    f"components/{COMPONENT}/process.py",
)


def build_package(output: Path) -> str:
    if not output.name.endswith(".cyclizer.plugin.zip"):
        raise ValueError("Package filename must end with .cyclizer.plugin.zip")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for name in FILES:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (PLUGIN / name).read_bytes())
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist/packages/development-journal-0.2.0.cyclizer.plugin.zip",
    )
    args = parser.parse_args()
    print(f"Package: {args.output.resolve()}\nSHA-256: {build_package(args.output)}")


if __name__ == "__main__":
    main()
