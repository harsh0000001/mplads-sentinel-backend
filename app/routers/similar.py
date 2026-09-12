from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.similar_service import get_similar_works


router = APIRouter(
    prefix="/similar-works",
    tags=["Similar Works"]
)


@router.get("/{sabha}/{work_id:path}")
def similar_works(
    sabha: str,
    work_id: str,
    db: Session = Depends(get_db)
):
    result = get_similar_works(
        db=db,
        sabha=sabha,
        work_id=work_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Work not found"
        )

    return result