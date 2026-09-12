from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.risk import RiskAnalysis


def get_risk_summary(
    db: Session,
    sabha: str | None = None
):
    query = db.query(RiskAnalysis)

    if sabha:
        query = query.filter(
            RiskAnalysis.sabha == sabha
        )

    total = query.count()

    low = query.filter(
        RiskAnalysis.risk_level == "LOW"
    ).count()

    medium = query.filter(
        RiskAnalysis.risk_level == "MEDIUM"
    ).count()

    high = query.filter(
        RiskAnalysis.risk_level == "HIGH"
    ).count()

    anomalies = query.filter(
        RiskAnalysis.is_anomaly == True
    ).count()

    return {
        "total": total,
        "low": low,
        "medium": medium,
        "high": high,
        "anomalies": anomalies
    }