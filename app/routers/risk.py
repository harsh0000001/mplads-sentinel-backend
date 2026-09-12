from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.risk_service import get_work_risk

router = APIRouter(
    prefix="/risk-analysis",
    tags=["Risk Analysis"]
)

@router.get("/{sabha}/{work_id:path}")
def risk_analysis(
    sabha: str,
    work_id: str,
    db: Session = Depends(get_db)
):
    try:
        result = get_work_risk(db, sabha, work_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Work not found"
            )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )