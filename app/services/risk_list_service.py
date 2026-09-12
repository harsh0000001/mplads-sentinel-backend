from sqlalchemy.orm import Session

from app.models.risk import RiskAnalysis


def get_risk_list(
    db: Session,
    sabha: str | None = None,
    risk_level: str | None = None,
    is_anomaly: bool | None = None,
    page: int = 1,
    limit: int = 20
):
    query = db.query(RiskAnalysis)

    if sabha:
        query = query.filter(
            RiskAnalysis.sabha == sabha
        )

    if risk_level:
        query = query.filter(
            RiskAnalysis.risk_level == risk_level
        )

    if is_anomaly is not None:
        query = query.filter(
            RiskAnalysis.is_anomaly == is_anomaly
        )

    total = query.count()

    results = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": [
            {
                "work_id": r.work_id,
                "sabha": r.sabha,
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "is_anomaly": r.is_anomaly,
                "risk_indicators": r.risk_indicators
            }
            for r in results
        ]
    }