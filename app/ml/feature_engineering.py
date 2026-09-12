import numpy as np
import pandas as pd


def safe_divide(
    numerator: pd.Series,
    denominator: pd.Series
) -> pd.Series:
    """
    Safely calculate numerator / denominator.

    Division by zero or invalid denominators produces NaN.
    """

    numerator = pd.to_numeric(numerator, errors="coerce")
    denominator = pd.to_numeric(denominator, errors="coerce")

    result = numerator.div(
        denominator.replace(0, np.nan)
    )

    result = result.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return result


def add_common_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived features using only fields
    available in the selected dataset.
    """

    result = df.copy()

    # Recommendation → Sanction amount deviation
    if {
        "recommended_amount_rs",
        "sanctioned_amount_rs",
    }.issubset(result.columns):

        result["recommendation_sanction_amount_deviation_rs"] = (
            result["recommended_amount_rs"]
            - result["sanctioned_amount_rs"]
        )

        result["sanctioned_to_recommended_ratio"] = safe_divide(
            result["sanctioned_amount_rs"],
            result["recommended_amount_rs"]
        )

    # Disbursement ratio
    if {
        "amount_disbursed_rs",
        "sanctioned_amount_rs",
    }.issubset(result.columns):

        result["disbursement_ratio"] = safe_divide(
            result["amount_disbursed_rs"],
            result["sanctioned_amount_rs"]
        )

    # Remaining sanctioned amount
    if {
        "sanctioned_amount_rs",
        "amount_disbursed_rs",
    }.issubset(result.columns):

        result["remaining_amount_rs"] = (
            result["sanctioned_amount_rs"]
            - result["amount_disbursed_rs"]
        )

    # Recommendation → Sanction duration
    if {
        "recommended_date",
        "sanctioned_date",
    }.issubset(result.columns):

        calculated_days = (
            result["sanctioned_date"]
            - result["recommended_date"]
        ).dt.days

        if "recommendation_to_sanction_days" in result.columns:
            result["recommendation_to_sanction_days"] = (
                result["recommendation_to_sanction_days"]
                .fillna(calculated_days)
            )
        else:
            result["recommendation_to_sanction_days"] = calculated_days

    # Sanction → Completion duration
    if {
        "sanctioned_date",
        "completion_date",
    }.issubset(result.columns):

        calculated_days = (
            result["completion_date"]
            - result["sanctioned_date"]
        ).dt.days

        if "sanction_to_completion_days" in result.columns:
            result["sanction_to_completion_days"] = (
                result["sanction_to_completion_days"]
                .fillna(calculated_days)
            )
        else:
            result["sanction_to_completion_days"] = calculated_days

    # Completed flag
    if "completed" in result.columns:
        result["completed"] = pd.to_numeric(
            result["completed"],
            errors="coerce"
        )

    return result


def get_ml_features(
    df: pd.DataFrame,
    sabha: str
) -> pd.DataFrame:
    """
    Select numerical features appropriate
    for the selected Sabha.
    """

    sabha = sabha.strip().lower()

    if sabha == "lok_sabha":

        feature_columns = [
            "recommended_amount_rs",
            "sanctioned_amount_rs",
            "amount_disbursed_rs",
            "completed",
            "recommendation_sanction_amount_deviation_rs",
            "sanctioned_to_recommended_ratio",
            "disbursement_ratio",
            "remaining_amount_rs",
            "recommendation_to_sanction_days",
            "sanction_to_completion_days",
        ]

    elif sabha == "rajya_sabha":

        feature_columns = [
            "recommended_amount_rs",
            "sanctioned_amount_rs",
            "expenditure_total_rs",
            "expenditure_transaction_count",
            "expenditure_vendor_count",
            "expenditure_payment_status_count",
            "amount_disbursed_rs",
            "expenditure_to_sanction_ratio",
            "completed",
            "recommendation_sanction_amount_deviation_rs",
            "sanctioned_to_recommended_ratio",
            "disbursement_ratio",
            "remaining_amount_rs",
            "recommendation_to_sanction_days",
            "sanction_to_completion_days",
        ]

    else:
        raise ValueError(
            "sabha must be 'lok_sabha' or 'rajya_sabha'"
        )

    available = [
        column
        for column in feature_columns
        if column in df.columns
    ]

    if not available:
        raise ValueError(
            f"No valid ML features found for {sabha}."
        )

    return df[available].copy()