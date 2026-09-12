from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    work_id = Column(String, index=True, nullable=True)

    sabha = Column(String, nullable=True)

    notification_type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False)
