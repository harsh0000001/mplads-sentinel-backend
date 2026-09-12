from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.financial_analytics_service import get_financial_analytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/financial")
def financial_analytics(
    db: Session = Depends(get_db)
):
    return get_financial_analytics(db)