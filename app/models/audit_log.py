from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    user = Column(String, nullable=True)

    work_id = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )