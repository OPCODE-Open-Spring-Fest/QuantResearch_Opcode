"""
Example usage of the CSV validator for price and signals files.

This script demonstrates how to use the validate_input_csv function
to validate user-provided CSV files before backtesting.
"""

import pandas as pd

from quant_research_starter.data import validate_input_csv, validate_price_csv


def example_validate_price_file():
    """Example: Validate a price CSV file."""
    print("=" * 60)
    print("Example 1: Validating Price CSV File")
    print("=" * 60)

    # Simulate a price file path
    price_file = "data/sample_prices.csv"

    # Validate using the general function
    result = validate_input_csv(price_file, csv_type="price")

    # Check results
    if result["valid"]:
        print("✓ File is valid!")
        print(f"  Rows: {result['row_count']}")
        print(f"  Columns: {result['column_count']}")
    else:
        print(f"✗ File has {len(result['errors'])} error(s):")
        for error in result["errors"]:
            print(f"  - [{error['type']}] {error['message']}")

    # Check warnings
    if result["warnings"]:
        print(f"\n⚠ {len(result['warnings'])} warning(s):")
        for warning in result["warnings"]:
            print(f"  - {warning['message']}")

    print()


def example_validate_with_required_columns():
    """Example: Validate with specific required columns."""
    print("=" * 60)
    print("Example 2: Validating with Required Columns")
    print("=" * 60)

    # Validate price file requiring specific symbols
    price_file = "data/sample_prices.csv"
    required_symbols = ["AAPL", "GOOGL", "MSFT"]

    is_valid, errors = validate_price_csv(price_file, required_symbols=required_symbols)

    if is_valid:
        print(f"✓ All required symbols present: {', '.join(required_symbols)}")
    else:
        print("✗ Validation failed:")
        for err in errors:
            print(f"  {err}")

    print()


def example_error_handling():
    """Example: Proper error handling in production code."""
    print("=" * 60)
    print("Example 3: Error Handling in Production")
    print("=" * 60)

    def load_and_validate_prices(file_path: str):
        """Load price data with validation."""
        # First validate
        result = validate_input_csv(file_path, csv_type="price")

        if not result["valid"]:
            # Handle errors
            error_messages = [err["message"] for err in result["errors"]]
            raise ValueError("Invalid price file:\n" + "\n".join(error_messages))

        # If valid, proceed with loading
        prices = pd.read_csv(file_path, index_col=0, parse_dates=True)
        print(f"✓ Loaded {len(prices)} rows of price data")
        return prices

    # Try with a file (we only demonstrate loading; don't keep the returned value)
    try:
        load_and_validate_prices("data/sample_prices.csv")
    except ValueError as e:
        print(f"✗ Error: {e}")
    except FileNotFoundError:
        print("✗ File not found (expected for this example)")

    print()


def example_detailed_error_info():
    """Example: Accessing detailed error information."""
    print("=" * 60)
    print("Example 4: Detailed Error Information")
    print("=" * 60)

    result = validate_input_csv("invalid_file.csv", csv_type="price")

    print("Validation Summary:")
    print(f"  Valid: {result['valid']}")
    print(f"  Errors: {len(result['errors'])}")
    print(f"  Warnings: {len(result['warnings'])}")
    print(f"  File: {result['file_path']}")

    # Access structured error data
    for error in result["errors"]:
        print(f"\nError Type: {error['type']}")
        print(f"Message: {error['message']}")
        if error.get("column"):
            print(f"Column: {error['column']}")
        if error.get("sample"):
            print(f"Sample data: {error['sample']}")

    print()


def main():
    """Run all examples."""
    print("\n")
    print("=" * 60)
    print("CSV VALIDATOR USAGE EXAMPLES")
    print("=" * 60)
    print()

    example_validate_price_file()
    example_validate_with_required_columns()
    example_error_handling()
    example_detailed_error_info()

    print("=" * 60)
    print("For more information, see the documentation:")
    print("src/quant_research_starter/data/validator.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
