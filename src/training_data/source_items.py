from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    question: str
    correct: str
    wrong: str
    distractor_1: str
    distractor_2: str
    verification_note: str

    def answers(self) -> tuple[str, str, str, str]:
        return (
            self.correct,
            self.wrong,
            self.distractor_1,
            self.distractor_2,
        )


def assert_item_bank(
    bank: dict[str, list[Item]],
    *,
    expected_easy: int,
    expected_medium: int,
    expected_hard: int,
) -> None:
    expected = {
        "easy": expected_easy,
        "medium": expected_medium,
        "hard": expected_hard,
    }

    actual = {
        difficulty: len(bank.get(difficulty, []))
        for difficulty in expected
    }

    if actual != expected:
        raise ValueError(
            f"Wrong item-bank counts: {actual}; expected {expected}"
        )

    questions: set[str] = set()

    for difficulty, items in bank.items():
        for item in items:
            if not item.question.strip():
                raise ValueError(
                    f"Empty question in {difficulty} item bank"
                )

            if item.question in questions:
                raise ValueError(
                    f"Duplicate item-bank question: {item.question}"
                )

            questions.add(item.question)

            answers = item.answers()

            if len(set(answers)) != 4:
                raise ValueError(
                    f"Duplicate answers for question: {item.question}"
                )

            if not item.verification_note.strip():
                raise ValueError(
                    "Missing verification note for question: "
                    f"{item.question}"
                )
