from __future__ import annotations

from source_items import Item


def build_math_validation_items() -> dict[str, list[Item]]:
    easy = [
        Item(
            "Which integer is 4 less than -2?",
            "-6",
            "2",
            "-4",
            "6",
            "Subtracting 4 from -2 gives -6.",
        ),
        Item(
            "What is the value of the digit 8 in 3,842?",
            "800",
            "80",
            "8",
            "8,000",
            "The digit 8 is in the hundreds place.",
        ),
        Item(
            "Which fraction is closest to 1?",
            "9/10",
            "1/10",
            "3/8",
            "2/5",
            "Nine tenths is only one tenth below 1.",
        ),
        Item(
            "How many minutes are in one and a quarter hours?",
            "75 minutes",
            "61 minutes",
            "90 minutes",
            "45 minutes",
            "One hour is 60 minutes and one quarter hour is 15.",
        ),
        Item(
            "Which number is a common factor of 18 and 42?",
            "6",
            "9",
            "7",
            "12",
            "Both 18 and 42 are divisible by 6.",
        ),
        Item(
            "What is the perimeter of a regular pentagon with side length 4?",
            "20 units",
            "16 units",
            "10 units",
            "25 units",
            "A pentagon has five sides, so its perimeter is 5 × 4.",
        ),
        Item(
            "What is 0.09 written as a percentage?",
            "9%",
            "0.9%",
            "90%",
            "0.09%",
            "Multiplying 0.09 by 100 gives 9%.",
        ),
        Item(
            "Which point lies on the y-axis?",
            "(0, 5)",
            "(5, 0)",
            "(5, 5)",
            "(-5, 5)",
            "Every point on the y-axis has x-coordinate zero.",
        ),
    ]

    medium = [
        Item(
            "A number is divided by 5 and then increased by 7, giving 15. What is the number?",
            "40",
            "8",
            "22",
            "110",
            "If n/5 + 7 = 15, then n/5 = 8 and n = 40.",
        ),
        Item(
            "A circular path has circumference 30 pi meters. What is its diameter?",
            "30 meters",
            "15 meters",
            "60 meters",
            "900 meters",
            "Circumference equals pi times diameter, so the diameter is 30.",
        ),
        Item(
            "A box contains 5 green, 4 yellow, and 3 purple tokens. What is the probability of selecting a token that is not purple?",
            "3/4",
            "1/4",
            "5/12",
            "2/3",
            "Nine of the 12 tokens are not purple, giving 9/12 = 3/4.",
        ),
        Item(
            "The first term of a geometric sequence is 160 and its ratio is 1/2. What is the fourth term?",
            "20",
            "10",
            "40",
            "80",
            "The fourth term is 160 × (1/2)³ = 20.",
        ),
        Item(
            "A square's area is 196 square centimeters. What is its perimeter?",
            "56 centimeters",
            "49 centimeters",
            "28 centimeters",
            "784 centimeters",
            "The side is the square root of 196, or 14, so the perimeter is 56.",
        ),
        Item(
            "What is the equation of a horizontal line passing through (3, -4)?",
            "y = -4",
            "x = -4",
            "y = 3",
            "x = 3",
            "A horizontal line has constant y-coordinate, here -4.",
        ),
        Item(
            "The values 6, 10, 14, and x have mean 12. What is x?",
            "18",
            "12",
            "16",
            "20",
            "The required total is 48; the known values total 30, so x = 18.",
        ),
        Item(
            "A 30-liter mixture is 20% salt solution. How many liters of salt does it contain?",
            "6 liters",
            "24 liters",
            "10 liters",
            "1.5 liters",
            "Twenty percent of 30 liters is 0.20 × 30 = 6 liters.",
        ),
        Item(
            "A right rectangular pyramid has base area 45 and height 8. What is its volume?",
            "120 cubic units",
            "360 cubic units",
            "53 cubic units",
            "180 cubic units",
            "Pyramid volume is one third of base area times height: 45×8/3 = 120.",
        ),
        Item(
            "If x is negative, which expression must be positive?",
            "x squared",
            "x cubed",
            "2x",
            "x - 1",
            "The square of any nonzero real number is positive.",
        ),
    ]

    hard = [
        Item(
            "A boat travels 24 kilometers downstream in 2 hours and the same distance upstream in 3 hours. What is the speed of the current?",
            "2 km/h",
            "4 km/h",
            "10 km/h",
            "12 km/h",
            "Downstream speed is 12 and upstream speed is 8; half their difference is 2.",
        ),
        Item(
            "A rectangle is inscribed under the line y = 12 - 2x in the first quadrant with sides on the axes. If its x-coordinate is 3, what is its area?",
            "18 square units",
            "30 square units",
            "9 square units",
            "36 square units",
            "At x = 3, y = 6, so the rectangle's area is 3 × 6 = 18.",
        ),
    ]

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }
