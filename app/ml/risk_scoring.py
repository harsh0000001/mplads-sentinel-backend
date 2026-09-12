import numpy as np
import pandas as pd


def min_max_normalize(series: pd.Series) -> pd.Series:
    """
    Normalize a numerical series to the range 0-1.

    If all values are identical, return zeros.
    """

    values = pd.to_numeric(series, errors="coerce")

    minimum = values.min()
    maximum = values.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(
            0.0,
            index=series.index
        )

    if maximum == minimum:
        return pd.Series(
            0.0,
            index=series.index
        )

    normalized = (
        (values - minimum)
        / (maximum - minimum)
    )

    return normalized.clip(0, 1).fillna(0)


def percentile_normalize(
    series: pd.Series,
    lower_percentile: float = 5,
    upper_percentile: float = 95,
) -> pd.Series:
    """
    Normalize values using percentile bounds.

    This reduces the effect of extreme outliers.
    """

    values = pd.to_numeric(
        series,
        errors="coerce"
    )

    valid_values = values.dropna()

    if valid_values.empty:
        return pd.Series(
            0.0,
            index=series.index
        )

    lower = np.percentile(
        valid_values,
        lower_percentile
    )

    upper = np.percentile(
        valid_values,
        upper_percentile
    )

    if upper <= lower:
        return pd.Series(
            0.0,
            index=series.index
        )

    normalized = (
        (values - lower)
        / (upper - lower)
    )

    return normalized.clip(0, 1).fillna(0)


def normalize_anomaly_scores(
    anomaly_scores: pd.Series
) -> pd.Series:
    """
    Convert Isolation Forest anomaly scores into
    a relative 0-1 anomaly intensity.

    Higher value = more anomalous.

    The normalization is performed independently
    for each Sabha dataset.
    """

    return percentile_normalize(
        anomaly_scores,
        lower_percentile=5,
        upper_percentile=95,
    )


def calculate_financial_risk(
    df: pd.DataFrame
) -> pd.Series:
    """
    Calculate a financial-pattern risk component
    from available engineered financial features.

    This does NOT represent fraud probability.
    """

    components = []

    # Recommendation vs sanction deviation
    if (
        "recommendation_sanction_amount_deviation_rs"
        in df.columns
    ):

        deviation = df[
            "recommendation_sanction_amount_deviation_rs"
        ].abs()

        components.append(
            percentile_normalize(deviation)
        )

    # Disbursement ratio
    if "disbursement_ratio" in df.columns:

        ratio = pd.to_numeric(
            df["disbursement_ratio"],
            errors="coerce"
        )

        # Distance from the expected 0-1 range
        ratio_risk = (
            ratio.sub(1).abs()
        )

        components.append(
            percentile_normalize(ratio_risk)
        )

    # Remaining amount
    if "remaining_amount_rs" in df.columns:

        remaining = pd.to_numeric(
            df["remaining_amount_rs"],
            errors="coerce"
        )

        # Large absolute financial difference
        components.append(
            percentile_normalize(
                remaining.abs()
            )
        )

    if not components:

        return pd.Series(
            0.0,
            index=df.index
        )

    financial_risk = pd.concat(
        components,
        axis=1
    ).mean(axis=1)

    return financial_risk.fillna(0).clip(0, 1)


def calculate_execution_risk(
    df: pd.DataFrame
) -> pd.Series:
    """
    Calculate an execution/timing risk component.

    Uses actual duration fields present in the
    datasets.

    This is an execution risk signal, not a
    prediction of fraud.
    """

    components = []

    if "recommendation_to_sanction_days" in df.columns:

        recommendation_days = pd.to_numeric(
            df["recommendation_to_sanction_days"],
            errors="coerce"
        )

        components.append(
            percentile_normalize(
                recommendation_days
            )
        )

    if "sanction_to_completion_days" in df.columns:

        completion_days = pd.to_numeric(
            df["sanction_to_completion_days"],
            errors="coerce"
        )

        components.append(
            percentile_normalize(
                completion_days
            )
        )

    if not components:

        return pd.Series(
            0.0,
            index=df.index
        )

    execution_risk = pd.concat(
        components,
        axis=1
    ).mean(axis=1)

    return execution_risk.fillna(0).clip(0, 1)


def calculate_completeness_risk(
    df: pd.DataFrame
) -> pd.Series:
    """
    Calculate a data-completeness risk component.

    A missing value itself is NOT evidence of fraud.
    It is only an indicator that the available
    information is incomplete.
    """

    relevant_columns = [
        "sanctioned_amount_rs",
        "amount_disbursed_rs",
        "recommendation_to_sanction_days",
        "sanction_to_completion_days",
    ]

    available_columns = [
        column
        for column in relevant_columns
        if column in df.columns
    ]

    if not available_columns:

        return pd.Series(
            0.0,
            index=df.index
        )

    missing_fraction = (
        df[available_columns]
        .isna()
        .mean(axis=1)
    )

    return missing_fraction.clip(
        0,
        1
    )


def calculate_risk_score(
    df: pd.DataFrame,
    anomaly_scores: pd.Series,
) -> pd.DataFrame:
    """
    Calculate the final transparent 0-100 risk score.

    Components:

        50% anomaly intensity
        30% financial-pattern signal
        15% execution/timing signal
         5% data-completeness signal

    The resulting score is a screening/priority score.
    It is NOT a probability of fraud.
    """

    if df is None or df.empty:
        raise ValueError(
            "Input dataframe is empty."
        )

    if anomaly_scores is None:
        raise ValueError(
            "Anomaly scores are required."
        )

    if len(df) != len(anomaly_scores):
        raise ValueError(
            "Dataframe and anomaly scores "
            "must have the same number of rows."
        )

    anomaly_component = normalize_anomaly_scores(
        anomaly_scores
    )

    financial_component = calculate_financial_risk(
        df
    )

    execution_component = calculate_execution_risk(
        df
    )

    completeness_component = calculate_completeness_risk(
        df
    )

    risk_score = (
        0.50 * anomaly_component
        + 0.30 * financial_component
        + 0.15 * execution_component
        + 0.05 * completeness_component
    ) * 100

    risk_score = risk_score.clip(
        0,
        100
    )

    result = pd.DataFrame(
        {
            "anomaly_component": anomaly_component,
            "financial_component": financial_component,
            "execution_component": execution_component,
            "completeness_component": completeness_component,
            "risk_score": risk_score,
        },
        index=df.index,
    )

    result["risk_score"] = result[
        "risk_score"
    ].round(2)

    return result


def assign_risk_level(
    risk_score: pd.Series
) -> pd.Series:
    """
    Convert numerical risk scores into
    transparent risk levels.
    """

    return pd.cut(
        risk_score,
        bins=[
            -np.inf,
            33.33,
            66.66,
            np.inf,
        ],
        labels=[
            "LOW",
            "MEDIUM",
            "HIGH",
        ],
        include_lowest=True,
    )


def add_risk_levels(
    risk_results: pd.DataFrame
) -> pd.DataFrame:
    """
    Add risk level to risk-score output.
    """

    if "risk_score" not in risk_results.columns:
        raise ValueError(
            "risk_score column not found."
        )

    result = risk_results.copy()

    result["risk_level"] = assign_risk_level(
        result["risk_score"]
    )

    return result