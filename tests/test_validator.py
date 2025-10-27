"""Tests for CSV validator."""

import numpy as np
import pandas as pd
import pytest

from quant_research_starter.data.validator import (
    CSVValidator,
    ValidationError,
    validate_input_csv,
    validate_price_csv,
    validate_signals_csv,
)


@pytest.fixture
def valid_price_csv(tmp_path):
    """Create a valid price CSV file."""
    dates = pd.date_range("2020-01-01", periods=50, freq="D")
    data = {
        "AAPL": np.random.uniform(100, 200, 50),
        "GOOGL": np.random.uniform(1000, 2000, 50),
        "MSFT": np.random.uniform(200, 300, 50),
    }
    df = pd.DataFrame(data, index=dates)
    df.index.name = "date"

    file_path = tmp_path / "valid_prices.csv"
    df.to_csv(file_path)
    return file_path


@pytest.fixture
def valid_signals_csv(tmp_path):
    """Create a valid signals CSV file."""
    dates = pd.date_range("2020-01-01", periods=50, freq="D")
    data = {
        "momentum": np.random.normal(0, 1, 50),
        "value": np.random.normal(0, 1, 50),
        "composite": np.random.normal(0, 1, 50),
    }
    df = pd.DataFrame(data, index=dates)
    df.index.name = "date"

    file_path = tmp_path / "valid_signals.csv"
    df.to_csv(file_path)
    return file_path


class TestValidationError:
    """Test ValidationError class."""

    def test_error_creation(self):
        """Test creating a validation error."""
        err = ValidationError("TEST_ERROR", "This is a test error")
        assert err.error_type == "TEST_ERROR"
        assert err.message == "This is a test error"
        assert err.sample_rows is None
        assert err.column is None

    def test_error_with_sample(self):
        """Test error with sample rows."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        err = ValidationError(
            "TEST_ERROR", "Error with sample", sample_rows=df, column="col1"
        )
        assert err.sample_rows is not None
        assert err.column == "col1"

    def test_error_repr(self):
        """Test error string representation."""
        err = ValidationError("TEST_ERROR", "Test message")
        repr_str = repr(err)
        assert "TEST_ERROR" in repr_str
        assert "Test message" in repr_str


class TestCSVValidator:
    """Test CSV validator class."""

    def test_file_not_found(self):
        """Test validation of non-existent file."""
        validator = CSVValidator()
        is_valid, errors = validator.validate("nonexistent_file.csv")

        assert not is_valid
        assert len(errors) > 0
        assert errors[0].error_type == "FILE_NOT_FOUND"

    def test_valid_price_file(self, valid_price_csv):
        """Test validation of valid price CSV."""
        validator = CSVValidator(min_rows=10)
        is_valid, errors = validator.validate(str(valid_price_csv))

        assert is_valid
        assert len(errors) == 0

    def test_missing_required_columns(self, tmp_path):
        """Test detection of missing required columns."""
        dates = pd.date_range("2020-01-01", periods=20, freq="D")
        df = pd.DataFrame({"AAPL": np.random.uniform(100, 200, 20)}, index=dates)
        df.index.name = "date"

        file_path = tmp_path / "missing_cols.csv"
        df.to_csv(file_path)

        validator = CSVValidator(required_columns=["AAPL", "GOOGL", "MSFT"])
        is_valid, errors = validator.validate(str(file_path))

        assert not is_valid
        assert any(e.error_type == "MISSING_COLUMN" for e in errors)
        # Should find 2 missing columns: GOOGL and MSFT
        missing_errors = [e for e in errors if e.error_type == "MISSING_COLUMN"]
        assert len(missing_errors) == 2

    def test_non_numeric_data(self, tmp_path):
        """Test detection of non-numeric data."""
        dates = pd.date_range("2020-01-01", periods=20, freq="D")
        df = pd.DataFrame(
            {
                "AAPL": ["100.5", "invalid", "102.3"] + list(range(17)),
                "GOOGL": np.random.uniform(1000, 2000, 20),
            },
            index=dates,
        )
        df.index.name = "date"

        file_path = tmp_path / "non_numeric.csv"
        df.to_csv(file_path)

        validator = CSVValidator()
        is_valid, errors = validator.validate(str(file_path))

        assert not is_valid
        assert any(e.error_type == "INVALID_DTYPE" for e in errors)

    def test_missing_values_detection(self, tmp_path):
        """Test detection of missing values."""
        dates = pd.date_range("2020-01-01", periods=30, freq="D")
        data = np.random.uniform(100, 200, 30)
        data[5:10] = np.nan  # Add some NaN values

        df = pd.DataFrame({"AAPL": data}, index=dates)
        df.index.name = "date"

        file_path = tmp_path / "missing_values.csv"
        df.to_csv(file_path)

        validator = CSVValidator()
        is_valid, errors = validator.validate(str(file_path))

        # Missing values generate errors
        assert any(e.error_type == "MISSING_VALUES" for e in errors)

    def test_duplicate_dates(self, tmp_path):
        """Test detection of duplicate dates."""
        dates = pd.date_range("2020-01-01", periods=20, freq="D")
        # Create duplicates by repeating some dates
        dates_with_dups = dates.tolist() + [dates[5], dates[10]]

        df = pd.DataFrame(
            {"AAPL": np.random.uniform(100, 200, 22)}, index=dates_with_dups
        )
        df.index.name = "date"

        file_path = tmp_path / "duplicate_dates.csv"
        df.to_csv(file_path)

        validator = CSVValidator()
        is_valid, errors = validator.validate(str(file_path))

        assert not is_valid
        assert any(e.error_type == "DUPLICATE_DATES" for e in errors)

    def test_insufficient_data(self, tmp_path):
        """Test detection of insufficient data rows."""
        dates = pd.date_range("2020-01-01", periods=5, freq="D")
        df = pd.DataFrame({"AAPL": np.random.uniform(100, 200, 5)}, index=dates)
        df.index.name = "date"

        file_path = tmp_path / "insufficient.csv"
        df.to_csv(file_path)

        validator = CSVValidator(min_rows=10)
        is_valid, errors = validator.validate(str(file_path))

        assert not is_valid
        assert any(e.error_type == "INSUFFICIENT_DATA" for e in errors)

    def test_invalid_date_format(self, tmp_path):
        """Test detection of invalid date format."""
        # Create CSV with non-date index
        df = pd.DataFrame(
            {
                "date": ["not-a-date", "2020-01-02", "2020-01-03"],
                "AAPL": [100, 101, 102],
            }
        )

        file_path = tmp_path / "invalid_dates.csv"
        df.to_csv(file_path, index=False)

        validator = CSVValidator()
        is_valid, errors = validator.validate(str(file_path))

        # Should have date format issues
        assert not is_valid

    def test_empty_file(self, tmp_path):
        """Test validation of empty CSV file."""
        file_path = tmp_path / "empty.csv"
        file_path.write_text("")

        validator = CSVValidator()
        is_valid, errors = validator.validate(str(file_path))

        assert not is_valid
        assert any(e.error_type == "EMPTY_FILE" for e in errors)


class TestValidatePriceCSV:
    """Test price CSV validation function."""

    def test_valid_price_csv(self, valid_price_csv):
        """Test validation of valid price CSV."""
        is_valid, errors = validate_price_csv(str(valid_price_csv))

        assert is_valid
        assert len(errors) == 0

    def test_price_csv_with_required_symbols(self, valid_price_csv):
        """Test price CSV validation with required symbols."""
        # Valid - has AAPL
        is_valid, errors = validate_price_csv(
            str(valid_price_csv), required_symbols=["AAPL"]
        )
        assert is_valid

        # Invalid - missing TSLA
        is_valid, errors = validate_price_csv(
            str(valid_price_csv), required_symbols=["AAPL", "TSLA"]
        )
        assert not is_valid
        assert any(e.error_type == "MISSING_COLUMN" for e in errors)


class TestValidateSignalsCSV:
    """Test signals CSV validation function."""

    def test_valid_signals_csv(self, valid_signals_csv):
        """Test validation of valid signals CSV."""
        is_valid, errors = validate_signals_csv(str(valid_signals_csv))

        assert is_valid
        assert len(errors) == 0

    def test_signals_csv_with_required_columns(self, valid_signals_csv):
        """Test signals CSV validation with required columns."""
        # Valid - has momentum
        is_valid, errors = validate_signals_csv(
            str(valid_signals_csv), required_columns=["momentum"]
        )
        assert is_valid

        # Invalid - missing size
        is_valid, errors = validate_signals_csv(
            str(valid_signals_csv), required_columns=["momentum", "size"]
        )
        assert not is_valid


class TestValidateInputCSV:
    """Test general-purpose validate_input_csv function."""

    def test_validate_price_type(self, valid_price_csv):
        """Test validation with price type."""
        result = validate_input_csv(str(valid_price_csv), csv_type="price")

        assert result["valid"]
        assert len(result["errors"]) == 0
        assert result["row_count"] == 50
        assert result["column_count"] == 3
        assert "file_path" in result

    def test_validate_signals_type(self, valid_signals_csv):
        """Test validation with signals type."""
        result = validate_input_csv(str(valid_signals_csv), csv_type="signals")

        assert result["valid"]
        assert len(result["errors"]) == 0
        assert result["row_count"] == 50
        assert result["column_count"] == 3

    def test_validate_with_errors(self, tmp_path):
        """Test validation that returns errors."""
        # Create invalid CSV (too few rows)
        dates = pd.date_range("2020-01-01", periods=5, freq="D")
        df = pd.DataFrame({"AAPL": [100, 101, 102, 103, 104]}, index=dates)
        df.index.name = "date"

        file_path = tmp_path / "invalid.csv"
        df.to_csv(file_path)

        result = validate_input_csv(str(file_path), csv_type="price")

        assert not result["valid"]
        assert len(result["errors"]) > 0
        assert result["row_count"] == 5

    def test_validate_with_warnings(self, tmp_path):
        """Test validation with warnings (missing values)."""
        dates = pd.date_range("2020-01-01", periods=25, freq="D")
        data = np.random.uniform(100, 200, 25)
        data[10] = np.nan  # Add one missing value

        df = pd.DataFrame({"AAPL": data}, index=dates)
        df.index.name = "date"

        file_path = tmp_path / "with_warnings.csv"
        df.to_csv(file_path)

        result = validate_input_csv(str(file_path), csv_type="price")

        # Should have warnings but still be valid (warnings are separated)
        assert len(result["warnings"]) > 0

    def test_nonexistent_file(self):
        """Test validation of non-existent file."""
        result = validate_input_csv("nonexistent.csv", csv_type="price")

        assert not result["valid"]
        assert len(result["errors"]) > 0
        assert result["row_count"] is None
        assert result["column_count"] is None

    def test_structured_error_output(self, tmp_path):
        """Test that errors are properly structured."""
        # Create file with multiple error types
        dates = ["2020-01-01", "invalid-date", "2020-01-03"]
        df = pd.DataFrame({"date": dates, "AAPL": [100, "invalid", 102]})

        file_path = tmp_path / "multi_error.csv"
        df.to_csv(file_path, index=False)

        result = validate_input_csv(str(file_path), csv_type="price")

        assert not result["valid"]
        # Check error structure
        for error in result["errors"]:
            assert "type" in error
            assert "message" in error
            assert "column" in error
