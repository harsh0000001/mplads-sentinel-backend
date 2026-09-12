from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.notification_service import (
    get_notifications,
    mark_notification_read
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def notifications(db: Session = Depends(get_db)):
    return get_notifications(db)


@router.patch("/{notification_id}/read")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    result = mark_notification_read(
        db=db,
        notification_id=notification_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification marked as read"
    }