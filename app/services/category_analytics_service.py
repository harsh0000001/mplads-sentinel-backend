from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.work import LokSabhaWork, RajyaSabhaWork


def get_category_analytics(db: Session):

    lok = (
        db.query(
            LokSabhaWork.work_category.label("category"),
            func.count(LokSabhaWork.id).label("total_works"),
            func.sum(LokSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(LokSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(LokSabhaWork.work_category)
        .all()
    )

    rajya = (
        db.query(
            RajyaSabhaWork.work_category.label("category"),
            func.count(RajyaSabhaWork.id).label("total_works"),
            func.sum(RajyaSabhaWork.sanctioned_amount_rs).label("sanctioned_amount"),
            func.sum(RajyaSabhaWork.amount_disbursed_rs).label("disbursed_amount")
        )
        .group_by(RajyaSabhaWork.work_category)
        .all()
    )

    categories = {}

    # Lok Sabha
    for row in lok:

        category = (
            row.category
            if row.category and str(row.category).lower() != "nan"
            else "Unknown"
        )

        categories[category] = {
            "category": category,
            "total_works": row.total_works,
            "sanctioned_amount": float(row.sanctioned_amount or 0),
            "disbursed_amount": float(row.disbursed_amount or 0)
        }

    # Rajya Sabha
    for row in rajya:

        category = (
            row.category
            if row.category and str(row.category).lower() != "nan"
            else "Unknown"
        )

        if category not in categories:
            categories[category] = {
                "category": category,
                "total_works": 0,
                "sanctioned_amount": 0,
                "disbursed_amount": 0
            }

        categories[category]["total_works"] += row.total_works

        categories[category]["sanctioned_amount"] += float(
            row.sanctioned_amount or 0
        )

        categories[category]["disbursed_amount"] += float(
            row.disbursed_amount or 0
        )

    return list(categories.values())