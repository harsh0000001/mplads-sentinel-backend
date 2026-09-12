import pandas as pd
import numpy as np


def calculate_percentile(
    series: pd.Series,
    value: float
) -> float:
    """
    Calculate the approximate percentile position
    of a value within a series.
    """

    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if values.empty or pd.isna(value):
        return 0.0

    return float(
        (values <= value).mean()
    )


def generate_risk_indicators(
    df: pd.DataFrame,
    risk_results: pd.DataFrame,
) -> pd.Series:
    """
    Generate human-readable risk indicators
    for every work.

    Indicators describe unusual patterns in the
    available data. They do not establish fraud
    or wrongdoing.
    """

    if df is None or df.empty:
        raise ValueError(
            "Input dataframe is empty."
        )

    if risk_results is None or risk_results.empty:
        raise ValueError(
            "Risk results are empty."
        )

    if len(df) != len(risk_results):
        raise ValueError(
            "Dataframe and risk results must "
            "have the same number of rows."
        )

    indicators = []

    # Pre-compute percentile distributions
    deviation_series = None
    if (
        "recommendation_sanction_amount_deviation_rs"
        in df.columns
    ):
        deviation_series = pd.to_numeric(
            df[
                "recommendation_sanction_amount_deviation_rs"
            ],
            errors="coerce"
        ).abs()

    recommendation_days_series = None
    if "recommendation_to_sanction_days" in df.columns:
        recommendation_days_series = pd.to_numeric(
            df[
                "recommendation_to_sanction_days"
            ],
            errors="coerce"
        )

    completion_days_series = None
    if "sanction_to_completion_days" in df.columns:
        completion_days_series = pd.to_numeric(
            df[
                "sanction_to_completion_days"
            ],
            errors="coerce"
        )

    disbursement_ratio_series = None
    if "disbursement_ratio" in df.columns:
        disbursement_ratio_series = pd.to_numeric(
            df[
                "disbursement_ratio"
            ],
            errors="coerce"
        )

    expenditure_ratio_series = None
    if "expenditure_to_sanction_ratio" in df.columns:
        expenditure_ratio_series = pd.to_numeric(
            df[
                "expenditure_to_sanction_ratio"
            ],
            errors="coerce"
        )

    for index in df.index:

        row_indicators = []

        # --------------------------------------------------
        # 1. Anomaly intensity
        # --------------------------------------------------

        if "anomaly_component" in risk_results.columns:

            anomaly_component = risk_results.loc[
                index,
                "anomaly_component"
            ]

            if (
                pd.notna(anomaly_component)
                and anomaly_component >= 0.75
            ):
                row_indicators.append(
                    "High anomaly intensity"
                )

            elif (
                pd.notna(anomaly_component)
                and anomaly_component >= 0.50
            ):
                row_indicators.append(
                    "Elevated anomaly intensity"
                )

        # --------------------------------------------------
        # 2. Financial deviation
        # --------------------------------------------------

        if deviation_series is not None:

            value = deviation_series.loc[index]

            percentile = calculate_percentile(
                deviation_series,
                value
            )

            if percentile >= 0.95:

                row_indicators.append(
                    "Very high recommendation/sanction "
                    "amount deviation"
                )

            elif percentile >= 0.90:

                row_indicators.append(
                    "High recommendation/sanction "
                    "amount deviation"
                )

        # --------------------------------------------------
        # 3. Disbursement pattern
        # --------------------------------------------------

        if disbursement_ratio_series is not None:

            value = disbursement_ratio_series.loc[index]

            if pd.notna(value):

                percentile = calculate_percentile(
                    disbursement_ratio_series,
                    value
                )

                if (
                    percentile >= 0.95
                    or percentile <= 0.05
                ):

                    row_indicators.append(
                        "Unusual disbursement ratio"
                    )

        # --------------------------------------------------
        # 4. Expenditure pattern
        # --------------------------------------------------

        if expenditure_ratio_series is not None:

            value = expenditure_ratio_series.loc[index]

            if pd.notna(value):

                percentile = calculate_percentile(
                    expenditure_ratio_series,
                    value
                )

                if (
                    percentile >= 0.95
                    or percentile <= 0.05
                ):

                    row_indicators.append(
                        "Unusual expenditure-to-sanction ratio"
                    )

        # --------------------------------------------------
        # 5. Recommendation → sanction duration
        # --------------------------------------------------

        if recommendation_days_series is not None:

            value = recommendation_days_series.loc[index]

            percentile = calculate_percentile(
                recommendation_days_series,
                value
            )

            if percentile >= 0.95:

                row_indicators.append(
                    "Extended recommendation-to-sanction duration"
                )

        # --------------------------------------------------
        # 6. Sanction → completion duration
        # --------------------------------------------------

        if completion_days_series is not None:

            value = completion_days_series.loc[index]

            percentile = calculate_percentile(
                completion_days_series,
                value
            )

            if percentile >= 0.95:

                row_indicators.append(
                    "Extended sanction-to-completion duration"
                )

        # --------------------------------------------------
        # 7. Data completeness
        # --------------------------------------------------

        if "completeness_component" in risk_results.columns:

            completeness = risk_results.loc[
                index,
                "completeness_component"
            ]

            if (
                pd.notna(completeness)
                and completeness >= 0.50
            ):

                row_indicators.append(
                    "Substantial missing information"
                )

        # --------------------------------------------------
        # 8. Fallback
        # --------------------------------------------------

        if not row_indicators:

            row_indicators.append(
                "No major individual risk indicator identified"
            )

        # Keep the output concise
        row_indicators = row_indicators[:5]

        indicators.append(
            row_indicators
        )

    return pd.Series(
        indicators,
        index=df.index,
        name="risk_indicators",
        dtype=object,
    )


def add_risk_indicators(
    df: pd.DataFrame,
    risk_results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add explainable risk indicators to risk results.
    """

    result = risk_results.copy()

    result["risk_indicators"] = (
        generate_risk_indicators(
            df,
            risk_results
        )
    )

    return result