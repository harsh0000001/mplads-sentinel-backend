from app.database import engine, Base
from app.models.work import Work


print("Connecting to database...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")