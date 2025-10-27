"""CSV validator for user-provided historical price and signals files."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class ValidationError:
    """Container for validation error information."""

    def __init__(
        self,
        error_type: str,
        message: str,
        sample_rows: Optional[pd.DataFrame] = None,
        column: Optional[str] = None,
    ):
        self.error_type = error_type
        self.message = message
        self.sample_rows = sample_rows
        self.column = column

    def __repr__(self) -> str:
        """String representation of error."""
        lines = [f"[{self.error_type}] {self.message}"]
        if self.sample_rows is not None and not self.sample_rows.empty:
            lines.append("\nSample of offending rows (first 5):")
            lines.append(self.sample_rows.head(5).to_string())
        return "\n".join(lines)


class CSVValidator:
    """
    Validator for user-provided CSV files containing price or signal data.

    Validates:
    - File existence and readability
    - Required columns presence
    - Date parsing and format
    - Timezone handling
    - Data types
    - Missing values
    - Duplicate dates
    """

    def __init__(
        self,
        required_columns: Optional[List[str]] = None,
        date_column: str = "date",
        allow_timezone: bool = True,
        min_rows: int = 10,
    ):
        """
        Initialize validator.

        Args:
            required_columns: List of required column names (besides date)
            date_column: Name of the date/datetime column
            allow_timezone: Whether to allow timezone-aware datetimes
            min_rows: Minimum number of data rows required
        """
        self.required_columns = required_columns or []
        self.date_column = date_column
        self.allow_timezone = allow_timezone
        self.min_rows = min_rows
        self.errors: List[ValidationError] = []

    def validate(self, file_path: str) -> Tuple[bool, List[ValidationError]]:
        """
        Validate a CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        self.errors = []
        path = Path(file_path)

        # Check file existence
        if not self._check_file_exists(path):
            return False, self.errors

        # Try to read the CSV
        df = self._read_csv(path)
        if df is None:
            return False, self.errors

        # Validate structure
        self._validate_columns(df)
        self._validate_date_index(df)
        self._validate_data_types(df)
        self._validate_missing_values(df)
        self._validate_duplicates(df)
        self._validate_row_count(df)

        is_valid = len(self.errors) == 0
        return is_valid, self.errors

    def _check_file_exists(self, path: Path) -> bool:
        """Check if file exists and is readable."""
        if not path.exists():
            self.errors.append(
                ValidationError("FILE_NOT_FOUND", f"File not found: {path.absolute()}")
            )
            return False

        if not path.is_file():
            self.errors.append(
                ValidationError(
                    "INVALID_FILE", f"Path is not a file: {path.absolute()}"
                )
            )
            return False

        return True

    def _read_csv(self, path: Path) -> Optional[pd.DataFrame]:
        """Attempt to read CSV file."""
        try:
            # Try reading with date parsing
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            return df
        except pd.errors.EmptyDataError:
            self.errors.append(
                ValidationError("EMPTY_FILE", f"File is empty: {path.name}")
            )
            return None
        except pd.errors.ParserError as e:
            self.errors.append(
                ValidationError(
                    "PARSE_ERROR", f"Failed to parse CSV: {str(e)}", column=path.name
                )
            )
            return None
        except Exception as e:
            self.errors.append(
                ValidationError(
                    "READ_ERROR", f"Failed to read file: {str(e)}", column=path.name
                )
            )
            return None

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Validate that required columns are present."""
        if not self.required_columns:
            return

        actual_columns = set(df.columns)
        required_set = set(self.required_columns)
        missing = required_set - actual_columns

        if missing:
            for col in sorted(missing):
                self.errors.append(
                    ValidationError(
                        "MISSING_COLUMN",
                        f"Missing required column: '{col}' - required for price/signal series",
                        column=col,
                    )
                )

    def _validate_date_index(self, df: pd.DataFrame) -> None:
        """Validate date index format and properties."""
        # Check if index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            sample_df = pd.DataFrame({"index": df.index[:5]})
            self.errors.append(
                ValidationError(
                    "INVALID_DATE_FORMAT",
                    f"Index is not a valid datetime. Expected datetime index, got {type(df.index).__name__}",
                    sample_rows=sample_df,
                )
            )
            return

        # Check timezone
        if df.index.tz is not None and not self.allow_timezone:
            self.errors.append(
                ValidationError(
                    "TIMEZONE_NOT_ALLOWED",
                    f"Timezone-aware datetime not allowed. Index has timezone: {df.index.tz}",
                )
            )

        # Check for NaT (Not a Time) values
        nat_mask = df.index.isna()
        if nat_mask.any():
            nat_indices = df[nat_mask].index[:5]
            sample_df = pd.DataFrame(
                {"row_number": range(len(nat_indices)), "invalid_date": nat_indices}
            )
            self.errors.append(
                ValidationError(
                    "INVALID_DATES",
                    f"Found {nat_mask.sum()} invalid date(s) (NaT) in index",
                    sample_rows=sample_df,
                )
            )

    def _validate_data_types(self, df: pd.DataFrame) -> None:
        """Validate data types of columns."""
        for col in df.columns:
            # Check if column is numeric
            if not pd.api.types.is_numeric_dtype(df[col]):
                # Try to show sample of non-numeric values
                try:
                    non_numeric_mask = pd.to_numeric(df[col], errors="coerce").isna()
                    non_numeric_rows = df[non_numeric_mask].head(5)
                    self.errors.append(
                        ValidationError(
                            "INVALID_DTYPE",
                            f"Column '{col}' contains non-numeric values. "
                            f"Expected float/int, got {df[col].dtype}",
                            sample_rows=non_numeric_rows[[col]],
                            column=col,
                        )
                    )
                except Exception:
                    self.errors.append(
                        ValidationError(
                            "INVALID_DTYPE",
                            f"Column '{col}' has invalid data type: {df[col].dtype}",
                            column=col,
                        )
                    )

    def _validate_missing_values(self, df: pd.DataFrame) -> None:
        """Validate and report missing values."""
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                missing_pct = (missing_count / len(df)) * 100
                # Show sample rows with missing values
                missing_rows = df[df[col].isna()].head(5)
                self.errors.append(
                    ValidationError(
                        "MISSING_VALUES",
                        f"Column '{col}' has {missing_count} missing values ({missing_pct:.1f}% of data)",
                        sample_rows=missing_rows[[col]],
                        column=col,
                    )
                )

    def _validate_duplicates(self, df: pd.DataFrame) -> None:
        """Check for duplicate date indices."""
        duplicates = df.index.duplicated()
        if duplicates.any():
            dup_count = duplicates.sum()
            dup_dates = df[duplicates].index[:5]
            sample_df = pd.DataFrame(
                {"duplicate_date": dup_dates, "occurrence": "duplicate"}
            )
            self.errors.append(
                ValidationError(
                    "DUPLICATE_DATES",
                    f"Found {dup_count} duplicate date(s) in index. Each date should appear only once.",
                    sample_rows=sample_df,
                )
            )

    def _validate_row_count(self, df: pd.DataFrame) -> None:
        """Validate minimum number of rows."""
        if len(df) < self.min_rows:
            self.errors.append(
                ValidationError(
                    "INSUFFICIENT_DATA",
                    f"File has only {len(df)} rows. Minimum required: {self.min_rows}",
                )
            )


def validate_price_csv(
    file_path: str, required_symbols: Optional[List[str]] = None
) -> Tuple[bool, List[ValidationError]]:
    """
    Validate a price CSV file.

    Expected format:
    - First column (index): date
    - Other columns: symbol names with price data
    - All values numeric (float/int)
    - No missing dates

    Args:
        file_path: Path to the CSV file
        required_symbols: Optional list of required symbol columns

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validator = CSVValidator(
        required_columns=required_symbols, date_column="date", min_rows=20
    )
    return validator.validate(file_path)


def validate_signals_csv(
    file_path: str, required_columns: Optional[List[str]] = None
) -> Tuple[bool, List[ValidationError]]:
    """
    Validate a signals CSV file.

    Expected format:
    - First column (index): date
    - Other columns: signal names or symbol signals
    - All values numeric (float/int)

    Args:
        file_path: Path to the CSV file
        required_columns: Optional list of required column names

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validator = CSVValidator(
        required_columns=required_columns, date_column="date", min_rows=20
    )
    return validator.validate(file_path)


def validate_input_csv(
    file_path: str, csv_type: str = "price", **kwargs
) -> Dict[str, Any]:
    """
    General-purpose CSV validator with structured error reporting.

    Args:
        file_path: Path to CSV file
        csv_type: Type of CSV - 'price' or 'signals'
        **kwargs: Additional arguments passed to specific validators

    Returns:
        Dictionary with validation results:
        {
            'valid': bool,
            'errors': List[Dict],  # Structured error information
            'warnings': List[Dict],
            'file_path': str,
            'row_count': int (if file readable),
            'column_count': int (if file readable)
        }
    """
    path = Path(file_path)

    # Choose appropriate validator
    if csv_type == "price":
        is_valid, errors = validate_price_csv(file_path, **kwargs)
    elif csv_type == "signals":
        is_valid, errors = validate_signals_csv(file_path, **kwargs)
    else:
        validator = CSVValidator(**kwargs)
        is_valid, errors = validator.validate(file_path)

    # Try to get basic file info
    row_count = None
    column_count = None
    try:
        if path.exists():
            df = pd.read_csv(file_path, index_col=0)
            row_count = len(df)
            column_count = len(df.columns)
    except Exception:
        pass

    # Structure errors for output
    error_dicts = []
    warnings = []

    for err in errors:
        err_dict = {
            "type": err.error_type,
            "message": err.message,
            "column": err.column,
        }

        # Include sample data if available
        if err.sample_rows is not None:
            err_dict["sample"] = err.sample_rows.to_dict()

        # Categorize some errors as warnings
        if err.error_type == "MISSING_VALUES":
            warnings.append(err_dict)
        else:
            error_dicts.append(err_dict)

    return {
        "valid": is_valid and len(error_dicts) == 0,
        "errors": error_dicts,
        "warnings": warnings,
        "file_path": str(path.absolute()),
        "row_count": row_count,
        "column_count": column_count,
    }
