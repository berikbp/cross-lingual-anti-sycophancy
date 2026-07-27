from __future__ import annotations

from pathlib import Path


BATCH_DIRECTORY = Path("data/master/batches")
OUTPUT_PATH = Path("data/master/master_en.jsonl")


def main() -> None:
    batch_paths = sorted(
        BATCH_DIRECTORY.glob("*.jsonl")
    )

    if len(batch_paths) != 20:
        raise ValueError(
            f"Expected 20 batch files, found {len(batch_paths)}"
        )

    lines: list[str] = []

    for path in batch_paths:
        batch_lines = [
            line.strip()
            for line in path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

        if len(batch_lines) != 20:
            raise ValueError(
                f"{path} contains {len(batch_lines)} records; "
                "expected 20"
            )

        lines.extend(batch_lines)

    if len(lines) != 400:
        raise ValueError(
            f"Expected 400 records, found {len(lines)}"
        )

    OUTPUT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(
        f"Merged {len(lines)} records into {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
