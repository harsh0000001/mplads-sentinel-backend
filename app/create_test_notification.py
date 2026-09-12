from app.database import SessionLocal
from app.models.notification import Notification


db = SessionLocal()

notification = Notification(
    work_id="WS/MP18065/2024-2025/134737",
    sabha="Lok Sabha",
    notification_type="risk",
    title="High Risk Work Detected",
    message="This work has been identified as a potential risk indicator."
)

db.add(notification)
db.commit()

print("Test notification created successfully.")

db.close()
