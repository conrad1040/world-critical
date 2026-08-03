from app.services.event_matching_service import titles_match


TEST_CASES = [
    (
        "Explosion near Moscow cafe kills three - AP News",
        (
            "At least three killed in explosion near cafe in Russia's Moscow "
            "- Al Jazeera"
        ),
        True,
    ),
    (
        "Explosion near Moscow cafe kills three - AP News",
        "Federal Reserve announces new interest rate decision",
        False,
    ),
    (
        "Wildfire destroys more than 600 structures",
        "More than 600 buildings destroyed by wildfire",
        True,
    ),
    (
        "California wildfire forces thousands to evacuate",
        "Thousands evacuated as California wildfire spreads",
        True,
    ),
    (
        "Actor joins Broadway production",
        "Wildfire destroys homes in California",
        False,
    ),
    (
        "Major hurricane strikes Florida in 2025",
        "Major hurricane strikes Florida in 2026",
        False,
    ),
]


def main() -> None:
    passed_count = 0

    for index, (title_a, title_b, expected) in enumerate(
        TEST_CASES,
        start=1,
    ):
        actual = titles_match(title_a, title_b)
        passed = actual == expected

        if passed:
            passed_count += 1

        print(f"Test {index}: {'PASS' if passed else 'FAIL'}")
        print(f"  A: {title_a}")
        print(f"  B: {title_b}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")
        print()

    print(f"Passed {passed_count}/{len(TEST_CASES)} tests")


if __name__ == "__main__":
    main()