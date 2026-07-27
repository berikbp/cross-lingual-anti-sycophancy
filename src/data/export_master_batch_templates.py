from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path(
    "data/master/allocation_manifest.json"
)

BATCH_DIRECTORY = Path(
    "data/master/batches"
)

BATCH_SIZE = 20


def main() -> None:
    manifest: dict[str, Any] = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for allocation in manifest["allocations"]:
        grouped[allocation["domain"]].append(allocation)

    BATCH_DIRECTORY.mkdir(parents=True, exist_ok=True)

    for domain, records in grouped.items():
        for start in range(0, len(records), BATCH_SIZE):
            batch_number = start // BATCH_SIZE + 1
            batch = records[start : start + BATCH_SIZE]

            output_path = (
                BATCH_DIRECTORY
                / f"{domain}_{batch_number:02d}.jsonl"
            )

            if output_path.exists():
                print(f"Skipped existing {output_path}")
                continue

            with output_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                for allocation in batch:
                    template = {
                        **allocation,
                        "source_type": "custom_verified",
                        "source_reference": None,
                        "question": "",
                        "options": {
                            "A": "",
                            "B": "",
                            "C": "",
                            "D": "",
                        },
                        "wrong_suggestion_text": "",
                        "verified": False,
                        "verification_note": "",
                        "notes": "",
                    }

                    file.write(
                        json.dumps(
                            template,
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

            print(f"Created {output_path}")


if __name__ == "__main__":
    main()
