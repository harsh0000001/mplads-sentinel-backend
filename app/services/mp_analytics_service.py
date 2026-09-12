from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.work import LokSabhaWork, RajyaSabhaWork


def get_mp_analytics(db: Session):

    lok = (
        db.query(
            LokSabhaWork.mp_name.label("mp_name"),
            func.count(LokSabhaWork.id).label("total_works"),
            func.sum(LokSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(LokSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(LokSabhaWork.mp_name)
        .all()
    )

    rajya = (
        db.query(
            RajyaSabhaWork.mp_name.label("mp_name"),
            func.count(RajyaSabhaWork.id).label("total_works"),
            func.sum(RajyaSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(RajyaSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(RajyaSabhaWork.mp_name)
        .all()
    )

    mps = {}

    # Lok Sabha
    for row in lok:

        mp_name = (
            row.mp_name
            if row.mp_name and str(row.mp_name).lower() != "nan"
            else "Unknown"
        )

        mps[mp_name] = {
            "mp_name": mp_name,
            "total_works": row.total_works,
            "sanctioned_amount": float(row.sanctioned_amount or 0),
            "disbursed_amount": float(row.disbursed_amount or 0)
        }

    # Rajya Sabha
    for row in rajya:

        mp_name = (
            row.mp_name
            if row.mp_name and str(row.mp_name).lower() != "nan"
            else "Unknown"
        )

        if mp_name not in mps:
            mps[mp_name] = {
                "mp_name": mp_name,
                "total_works": 0,
                "sanctioned_amount": 0,
                "disbursed_amount": 0
            }

        mps[mp_name]["total_works"] += row.total_works

        mps[mp_name]["sanctioned_amount"] += float(
            row.sanctioned_amount or 0
        )

        mps[mp_name]["disbursed_amount"] += float(
            row.disbursed_amount or 0
        )

    return list(mps.values())