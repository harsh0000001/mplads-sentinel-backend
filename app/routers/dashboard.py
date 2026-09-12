from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.work import LokSabhaWork, RajyaSabhaWork


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):

    # -------------------------
    # Total works
    # -------------------------

    lok_sabha_works = db.query(
        func.count(LokSabhaWork.id)
    ).scalar()

    rajya_sabha_works = db.query(
        func.count(RajyaSabhaWork.id)
    ).scalar()

    total_works = (
        lok_sabha_works +
        rajya_sabha_works
    )


    # -------------------------
    # Completed works
    # -------------------------

    lok_completed = db.query(
        func.count(LokSabhaWork.id)
    ).filter(
        LokSabhaWork.completed == True
    ).scalar()

    rajya_completed = db.query(
        func.count(RajyaSabhaWork.id)
    ).filter(
        RajyaSabhaWork.completed == True
    ).scalar()

    completed_works = (
        lok_completed +
        rajya_completed
    )


    # -------------------------
    # Pending works
    # -------------------------

    lok_pending = db.query(
        func.count(LokSabhaWork.id)
    ).filter(
        LokSabhaWork.completed != True
    ).scalar()

    rajya_pending = db.query(
        func.count(RajyaSabhaWork.id)
    ).filter(
        RajyaSabhaWork.completed != True
    ).scalar()

    pending_works = (
        lok_pending +
        rajya_pending
    )


    # -------------------------
    # Sanctioned amount
    # -------------------------

    lok_sanctioned = db.query(
        func.sum(LokSabhaWork.sanctioned_amount_rs)
    ).scalar() or 0

    rajya_sanctioned = db.query(
        func.sum(RajyaSabhaWork.sanctioned_amount_rs)
    ).scalar() or 0

    total_sanctioned_amount = (
        lok_sanctioned +
        rajya_sanctioned
    )


    # -------------------------
    # Disbursed amount
    # -------------------------

    lok_disbursed = db.query(
        func.sum(LokSabhaWork.amount_disbursed_rs)
    ).scalar() or 0

    rajya_disbursed = db.query(
        func.sum(RajyaSabhaWork.amount_disbursed_rs)
    ).scalar() or 0

    total_disbursed_amount = (
        lok_disbursed +
        rajya_disbursed
    )


    # -------------------------
    # Response
    # -------------------------

    return {
        "total_works": total_works,

        "lok_sabha_works": lok_sabha_works,
        "rajya_sabha_works": rajya_sabha_works,

        "completed_works": completed_works,
        "pending_works": pending_works,

        "total_sanctioned_amount": total_sanctioned_amount,
        "total_disbursed_amount": total_disbursed_amount
    }