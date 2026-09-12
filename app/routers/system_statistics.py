from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.system_statistics_service import get_system_statistics


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/statistics")
def system_statistics(db: Session = Depends(get_db)):
    return get_system_statistics(db)