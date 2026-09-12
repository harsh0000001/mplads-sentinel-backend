from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.state_analytics_service import get_state_analytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/states")
def state_analytics(
    db: Session = Depends(get_db)
):
    return get_state_analytics(db)