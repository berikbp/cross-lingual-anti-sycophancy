
from __future__ import annotations

import argparse
import tomllib
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    metadata = tomllib.loads(
        (root / "pyproject.toml").read_text(encoding="utf-8")
    )
    release_version = metadata["project"]["version"]
    parser = argparse.ArgumentParser(
        description="Multilingual anti-sycophancy research artifact."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {release_version}",
    )
    parser.parse_args()

    print("Multilingual anti-sycophancy research artifact")
    print(f"Version: {release_version}")
    print(f"Repository: {root}")
    print("Reproducibility guide: docs/reproducibility.md")


if __name__ == "__main__":
    main()
