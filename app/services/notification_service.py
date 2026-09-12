from sqlalchemy.orm import Session

from app.models.notification import Notification


def get_notifications(db: Session):
    return (
        db.query(Notification)
        .order_by(Notification.id.desc())
        .all()
    )


def mark_notification_read(db: Session, notification_id: int):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return None

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return notification