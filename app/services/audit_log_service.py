from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def get_audit_logs(db: Session):

    return (
        db.query(AuditLog)
        .order_by(AuditLog.id.desc())
        .all()
    )


def create_audit_log(
    db: Session,
    action: str,
    description: str,
    user: str | None = None,
    work_id: str | None = None
):

    log = AuditLog(
        action=action,
        description=description,
        user=user,
        work_id=work_id
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log