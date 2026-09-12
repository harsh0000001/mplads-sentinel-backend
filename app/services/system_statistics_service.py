from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.work import LokSabhaWork, RajyaSabhaWork
from app.models.risk import RiskAnalysis


def get_system_statistics(db: Session):

    # Work statistics
    lok_total = db.query(func.count(LokSabhaWork.id)).scalar() or 0
    rajya_total = db.query(func.count(RajyaSabhaWork.id)).scalar() or 0

    lok_completed = (
        db.query(func.count(LokSabhaWork.id))
        .filter(LokSabhaWork.completed == True)
        .scalar()
        or 0
    )

    rajya_completed = (
        db.query(func.count(RajyaSabhaWork.id))
        .filter(RajyaSabhaWork.completed == True)
        .scalar()
        or 0
    )

    total_works = lok_total + rajya_total
    completed_works = lok_completed + rajya_completed
    pending_works = total_works - completed_works

    # Financial statistics
    lok_financial = db.query(
        func.sum(LokSabhaWork.sanctioned_amount_rs),
        func.sum(LokSabhaWork.amount_disbursed_rs)
    ).first()

    rajya_financial = db.query(
        func.sum(RajyaSabhaWork.sanctioned_amount_rs),
        func.sum(RajyaSabhaWork.amount_disbursed_rs)
    ).first()

    sanctioned_amount = (
        float(lok_financial[0] or 0)
        + float(rajya_financial[0] or 0)
    )

    disbursed_amount = (
        float(lok_financial[1] or 0)
        + float(rajya_financial[1] or 0)
    )

    # Risk statistics
    risk_total = db.query(func.count(RiskAnalysis.id)).scalar() or 0

    low = (
        db.query(func.count(RiskAnalysis.id))
        .filter(RiskAnalysis.risk_level == "LOW")
        .scalar()
        or 0
    )

    medium = (
        db.query(func.count(RiskAnalysis.id))
        .filter(RiskAnalysis.risk_level == "MEDIUM")
        .scalar()
        or 0
    )

    high = (
        db.query(func.count(RiskAnalysis.id))
        .filter(RiskAnalysis.risk_level == "HIGH")
        .scalar()
        or 0
    )

    anomalies = (
        db.query(func.count(RiskAnalysis.id))
        .filter(RiskAnalysis.is_anomaly == True)
        .scalar()
        or 0
    )

    return {
        "total_works": total_works,
        "lok_sabha_works": lok_total,
        "rajya_sabha_works": rajya_total,
        "completed_works": completed_works,
        "pending_works": pending_works,
        "sanctioned_amount": sanctioned_amount,
        "disbursed_amount": disbursed_amount,
        "risk_total": risk_total,
        "low_risk": low,
        "medium_risk": medium,
        "high_risk": high,
        "anomalies": anomalies
    }