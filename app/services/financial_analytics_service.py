from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.work import LokSabhaWork, RajyaSabhaWork


def get_financial_analytics(db: Session):

    lok = db.query(
        func.sum(LokSabhaWork.recommended_amount_rs).label("recommended"),
        func.sum(LokSabhaWork.sanctioned_amount_rs).label("sanctioned"),
        func.sum(LokSabhaWork.amount_disbursed_rs).label("disbursed")
    ).first()

    rajya = db.query(
        func.sum(RajyaSabhaWork.recommended_amount_rs).label("recommended"),
        func.sum(RajyaSabhaWork.sanctioned_amount_rs).label("sanctioned"),
        func.sum(RajyaSabhaWork.amount_disbursed_rs).label("disbursed")
    ).first()

    return {
        "recommended_amount": float(
            (lok.recommended or 0) + (rajya.recommended or 0)
        ),
        "sanctioned_amount": float(
            (lok.sanctioned or 0) + (rajya.sanctioned or 0)
        ),
        "disbursed_amount": float(
            (lok.disbursed or 0) + (rajya.disbursed or 0)
        )
    }