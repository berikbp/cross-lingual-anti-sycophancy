
from __future__ import annotations

import argparse
from pathlib import Path


VERSION = "1.1.0"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multilingual anti-sycophancy research artifact."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    parser.parse_args()

    root = Path(__file__).resolve().parent
    print("Multilingual anti-sycophancy research artifact")
    print(f"Version: {VERSION}")
    print(f"Repository: {root}")
    print("Reproducibility guide: docs/reproducibility.md")


if __name__ == "__main__":
    main()
