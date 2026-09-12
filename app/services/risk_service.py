
from sqlalchemy.orm import Session

from app.models.risk import RiskAnalysis


def get_work_risk(
    db: Session,
    sabha: str,
    work_id: str
):
    result = (
        db.query(RiskAnalysis)
        .filter(
            RiskAnalysis.sabha == sabha,
            RiskAnalysis.work_id == work_id
        )
        .first()
    )

    if not result:
        return None

    return {
        "work_id": result.work_id,
        "sabha": result.sabha,
        "anomaly_score": result.anomaly_score,
        "is_anomaly": result.is_anomaly,
        "anomaly_component": result.anomaly_component,
        "financial_component": result.financial_component,
        "execution_component": result.execution_component,
        "completeness_component": result.completeness_component,
        "risk_score": result.risk_score,
        "risk_level": result.risk_level,
        "risk_indicators": result.risk_indicators,
        "similar_works": result.similar_works,
    }

