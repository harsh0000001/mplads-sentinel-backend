from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.work import LokSabhaWork, RajyaSabhaWork


def get_state_analytics(db: Session):

    lok = (
        db.query(
            LokSabhaWork.state.label("state"),
            func.count(LokSabhaWork.id).label("total_works"),
            func.sum(LokSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(LokSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(LokSabhaWork.state)
        .all()
    )

    rajya = (
        db.query(
            RajyaSabhaWork.state.label("state"),
            func.count(RajyaSabhaWork.id).label("total_works"),
            func.sum(RajyaSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(RajyaSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(RajyaSabhaWork.state)
        .all()
    )

    states = {}

    # Lok Sabha
    for row in lok:

        state = (
            row.state
            if row.state and str(row.state).lower() != "nan"
            else "Unknown"
        )

        states[state] = {
            "state": state,
            "total_works": row.total_works,
            "sanctioned_amount": float(row.sanctioned_amount or 0),
            "disbursed_amount": float(row.disbursed_amount or 0)
        }

    # Rajya Sabha
    for row in rajya:

        state = (
            row.state
            if row.state and str(row.state).lower() != "nan"
            else "Unknown"
        )

        if state not in states:
            states[state] = {
                "state": state,
                "total_works": 0,
                "sanctioned_amount": 0,
                "disbursed_amount": 0
            }

        states[state]["total_works"] += row.total_works

        states[state]["sanctioned_amount"] += float(
            row.sanctioned_amount or 0
        )

        states[state]["disbursed_amount"] += float(
            row.disbursed_amount or 0
        )

    return list(states.values())