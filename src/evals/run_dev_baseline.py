"""Run the frozen Protocol Version 1.0 development baseline."""

from pathlib import Path

import manual_pressure_pilot


PROTOCOL_VERSION = "1.0"
PRESSURE_TEMPLATE_VERSION = "v1_weak"

manual_pressure_pilot.PROTOCOL_VERSION = PROTOCOL_VERSION
manual_pressure_pilot.PRESSURE_TEMPLATE_VERSION = (
    PRESSURE_TEMPLATE_VERSION
)

manual_pressure_pilot.DATA_PATH = Path(
    "data/development/dev_en.jsonl"
)

manual_pressure_pilot.OUTPUT_PATH = Path(
    "results/development/original_model_en.jsonl"
)


if __name__ == "__main__":
    manual_pressure_pilot.main()
