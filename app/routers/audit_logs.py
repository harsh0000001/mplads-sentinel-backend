from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse
from app.services.audit_log_service import (
    get_audit_logs,
    create_audit_log
)


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get(
    "/",
    response_model=list[AuditLogResponse]
)
def audit_logs(
    db: Session = Depends(get_db)
):
    return get_audit_logs(db)


@router.post("/")
def add_audit_log(
    data: AuditLogCreate,
    db: Session = Depends(get_db)
):
    return create_audit_log(
        db=db,
        action=data.action,
        description=data.description,
        user=data.user,
        work_id=data.work_id
    )