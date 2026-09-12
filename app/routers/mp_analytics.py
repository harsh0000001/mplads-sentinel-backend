from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.mp_analytics_service import get_mp_analytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/mps")
def mp_analytics(db: Session = Depends(get_db)):
    return get_mp_analytics(db)