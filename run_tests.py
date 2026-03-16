import pytest


def main():
    return pytest.main(
        [
            "-p",
            "no:cacheprovider",
            "tests/test_cleaner.py",
            "tests/test_validator.py",
            "tests/test_transformer.py",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
