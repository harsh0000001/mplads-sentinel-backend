from app.database import Base, engine
from app.models.audit_log import AuditLog


Base.metadata.create_all(bind=engine)

print("Audit logs table created successfully.")