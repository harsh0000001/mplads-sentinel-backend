from app.database import SessionLocal
from app.services.audit_log_service import create_audit_log


db = SessionLocal()

create_audit_log(
    db=db,
    action="VIEW_RISK",
    description="User viewed a high-risk work.",
    user="test_user",
    work_id="WS/MP18065/2024-2025/134737"
)

print("Test audit log created successfully.")

db.close()