from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.work import LokSabhaWork, RajyaSabhaWork


router = APIRouter(
    prefix="/works",
    tags=["Works"]
)


@router.get("/")
def get_works(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),

    state: str | None = None,
    sabha: str | None = None,
    work_status: str | None = None,
    search: str | None = None,

    db: Session = Depends(get_db)
):

    results = []

    # -----------------------------
    # Choose which table to query
    # -----------------------------

    if sabha == "Lok Sabha":

        query = db.query(LokSabhaWork)

        if state:
            query = query.filter(
                LokSabhaWork.state == state
            )

        if work_status:
            query = query.filter(
                LokSabhaWork.work_status == work_status
            )

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                (LokSabhaWork.work.ilike(search_pattern)) |
                (LokSabhaWork.work_description.ilike(search_pattern)) |
                (LokSabhaWork.mp_name.ilike(search_pattern)) |
                (LokSabhaWork.state.ilike(search_pattern))
            )

        total = query.count()

        offset = (page - 1) * limit

        results = query.offset(offset).limit(limit).all()

    elif sabha == "Rajya Sabha":

        query = db.query(RajyaSabhaWork)

        if state:
            query = query.filter(
                RajyaSabhaWork.state == state
            )

        if work_status:
            query = query.filter(
                RajyaSabhaWork.work_status == work_status
            )

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                (RajyaSabhaWork.work.ilike(search_pattern)) |
                (RajyaSabhaWork.work_description.ilike(search_pattern)) |
                (RajyaSabhaWork.mp_name.ilike(search_pattern)) |
                (RajyaSabhaWork.state.ilike(search_pattern))
            )

        total = query.count()

        offset = (page - 1) * limit

        results = query.offset(offset).limit(limit).all()

    else:

        # No sabha filter → get from both tables

        lok_query = db.query(LokSabhaWork)
        rajya_query = db.query(RajyaSabhaWork)

        if state:

            lok_query = lok_query.filter(
                LokSabhaWork.state == state
            )

            rajya_query = rajya_query.filter(
                RajyaSabhaWork.state == state
            )

        if work_status:

            lok_query = lok_query.filter(
                LokSabhaWork.work_status == work_status
            )

            rajya_query = rajya_query.filter(
                RajyaSabhaWork.work_status == work_status
            )

        if search:

            search_pattern = f"%{search}%"

            lok_query = lok_query.filter(
                (LokSabhaWork.work.ilike(search_pattern)) |
                (LokSabhaWork.work_description.ilike(search_pattern)) |
                (LokSabhaWork.mp_name.ilike(search_pattern)) |
                (LokSabhaWork.state.ilike(search_pattern))
            )

            rajya_query = rajya_query.filter(
                (RajyaSabhaWork.work.ilike(search_pattern)) |
                (RajyaSabhaWork.work_description.ilike(search_pattern)) |
                (RajyaSabhaWork.mp_name.ilike(search_pattern)) |
                (RajyaSabhaWork.state.ilike(search_pattern))
            )

        lok_results = lok_query.all()
        rajya_results = rajya_query.all()

        results = lok_results + rajya_results

        total = len(results)

        offset = (page - 1) * limit

        results = results[offset:offset + limit]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": results
    }


@router.get("/{sabha}/{work_id}")
def get_work(
    sabha: str,
    work_id: int,
    db: Session = Depends(get_db)
):

    if sabha == "Lok Sabha":

        work = (
            db.query(LokSabhaWork)
            .filter(LokSabhaWork.id == work_id)
            .first()
        )

    elif sabha == "Rajya Sabha":

        work = (
            db.query(RajyaSabhaWork)
            .filter(RajyaSabhaWork.id == work_id)
            .first()
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid Sabha. Use Lok Sabha or Rajya Sabha."
        )

    if not work:

        raise HTTPException(
            status_code=404,
            detail="Work not found"
        )

    return work