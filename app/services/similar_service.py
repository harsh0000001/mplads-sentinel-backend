from sqlalchemy.orm import Session

from app.models.risk import RiskAnalysis


def get_similar_works(
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

    if result is None:
        return None

    return {
        "work_id": result.work_id,
        "sabha": result.sabha,
        "similar_works": result.similar_works
    }