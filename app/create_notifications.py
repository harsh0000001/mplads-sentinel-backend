from app.database import Base, engine

from app.models.notification import Notification


Base.metadata.create_all(bind=engine)

print("Notifications table created successfully.")