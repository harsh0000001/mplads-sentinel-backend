from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.category_analytics_service import get_category_analytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/categories")
def category_analytics(db: Session = Depends(get_db)):
    return get_category_analytics(db)