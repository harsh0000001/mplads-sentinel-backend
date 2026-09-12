import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """
    Convert a pandas Series to numeric values.
    Invalid values become NaN.
    """
    return pd.to_numeric(series, errors="coerce")


def prepare_base_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning before feature engineering.
    """

    if df is None or df.empty:
        raise ValueError("Input dataset is empty.")

    result = df.copy()

    # Clean column names
    result.columns = result.columns.str.strip()

    # Columns expected to be numeric
    numeric_columns = [
        "recommended_amount_rs",
        "sanctioned_amount_rs",
        "amount_disbursed_rs",
        "fund_disbursed_amount_rs",
        "allocated_amount_rs",
        "consent_amount_rs",
        "expenditure_total_rs",
        "expenditure_transaction_count",
        "expenditure_vendor_count",
        "expenditure_payment_status_count",
        "consent_total_rs",
        "consent_event_count",
        "consent_calamity_type_count",
        "consent_calamity_name_count",
        "recommendation_sanction_gap_rs",
        "expenditure_to_sanction_ratio",
        "recommendation_to_sanction_days",
        "sanction_to_completion_days",
        "completed",
    ]

    for column in numeric_columns:

        if column in result.columns:
            result[column] = clean_numeric_series(
                result[column]
            )

    # Date columns
    date_columns = [
        "recommended_date",
        "sanctioned_date",
        "completion_date",
        "expenditure_date",
        "expenditure_first_date",
        "expenditure_last_date",
    ]

    for column in date_columns:

        if column in result.columns:
            result[column] = pd.to_datetime(
                result[column],
                errors="coerce"
            )

    # Financial values cannot be negative
    financial_columns = [
        "recommended_amount_rs",
        "sanctioned_amount_rs",
        "amount_disbursed_rs",
        "fund_disbursed_amount_rs",
        "allocated_amount_rs",
        "consent_amount_rs",
        "expenditure_total_rs",
        "consent_total_rs",
    ]

    for column in financial_columns:

        if column in result.columns:

            invalid_negative = result[column] < 0

            result.loc[
                invalid_negative,
                column
            ] = np.nan

    # Duration values cannot be negative
    duration_columns = [
        "recommendation_to_sanction_days",
        "sanction_to_completion_days",
    ]

    for column in duration_columns:

        if column in result.columns:

            invalid_duration = result[column] < 0

            result.loc[
                invalid_duration,
                column
            ] = np.nan

    return result


def build_preprocessed_matrix(
    X: pd.DataFrame,
    add_missing_indicators: bool = True
):
    """
    Convert the engineered feature matrix into a clean
    numerical matrix suitable for ML models.

    Steps:
    1. Convert all features to numeric.
    2. Replace infinite values with NaN.
    3. Add missing-value indicators.
    4. Median imputation.
    5. Robust scaling.
    """

    if X is None or X.empty:
        raise ValueError("Feature matrix is empty.")

    X_work = X.copy()

    # Ensure every feature is numeric
    for column in X_work.columns:

        X_work[column] = pd.to_numeric(
            X_work[column],
            errors="coerce"
        )

    # Convert infinity to missing values
    X_work = X_work.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Add missing-value indicators
    if add_missing_indicators:

        original_columns = list(
            X_work.columns
        )

        for column in original_columns:

            if X_work[column].isna().any():

                X_work[
                    f"{column}_missing"
                ] = X_work[column].isna().astype(int)

    # Median imputation
    imputer = SimpleImputer(
        strategy="median",
        keep_empty_features=True
    )

    X_imputed_array = imputer.fit_transform(
        X_work
    )

    X_imputed = pd.DataFrame(
        X_imputed_array,
        columns=X_work.columns,
        index=X_work.index
    )

    # Robust scaling
    scaler = RobustScaler()

    X_scaled_array = scaler.fit_transform(
        X_imputed
    )

    X_processed = pd.DataFrame(
        X_scaled_array,
        columns=X_imputed.columns,
        index=X_imputed.index
    )

    # Final validation
    if X_processed.isna().any().any():

        raise ValueError(
            "Preprocessing produced NaN values."
        )

    if not np.isfinite(
        X_processed.to_numpy()
    ).all():

        raise ValueError(
            "Preprocessing produced infinite values."
        )

    return (
        X_processed,
        imputer,
        scaler
    )