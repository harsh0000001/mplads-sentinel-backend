from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.risk_list_service import get_risk_list


router = APIRouter(
    prefix="/risk-analysis",
    tags=["Risk Analysis"]
)


@router.get("/")
def risk_list(
    sabha: str | None = None,
    risk_level: str | None = None,
    is_anomaly: bool | None = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return get_risk_list(
        db=db,
        sabha=sabha,
        risk_level=risk_level,
        is_anomaly=is_anomaly,
        page=page,
        limit=limit
    )