from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.risk_summary_service import get_risk_summary


router = APIRouter(
    prefix="/risk-analysis",
    tags=["Risk Analysis"]
)


@router.get("/summary")
def risk_summary(
    sabha: str | None = None,
    db: Session = Depends(get_db)
):
    return get_risk_summary(
        db=db,
        sabha=sabha
    )