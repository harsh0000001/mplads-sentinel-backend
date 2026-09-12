from app.database import engine, Base
from app.models import LokSabhaWork, RajyaSabhaWork


print("Creating separate dataset tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")