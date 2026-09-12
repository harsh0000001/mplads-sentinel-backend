from sqlalchemy import Column, Integer, String, Float, Boolean, Date, JSON
from app.database import Base


class LokSabhaWork(Base):
    __tablename__ = "lok_sabha_works"

    id = Column(Integer, primary_key=True, index=True)

    work_id = Column(String, index=True)
    sabha = Column(String, nullable=False)

    work_category = Column(String)
    work = Column(String)
    state = Column(String, index=True)
    mp_name = Column(String)
    work_description = Column(String)

    recommended_date = Column(Date)
    recommended_amount_rs = Column(Float)

    sanctioned_date = Column(Date)
    sanctioned_amount_rs = Column(Float)

    work_status = Column(String)
    completed = Column(Boolean)
    completion_date = Column(Date)

    amount_disbursed_rs = Column(Float)
    allocated_amount_rs = Column(Float)

    image = Column(String)

    # Dataset-specific fields
    extra_data = Column(JSON)


class RajyaSabhaWork(Base):
    __tablename__ = "rajya_sabha_works"

    id = Column(Integer, primary_key=True, index=True)

    work_id = Column(String, index=True)
    sabha = Column(String, nullable=False)

    work_category = Column(String)
    work = Column(String)
    state = Column(String, index=True)
    mp_name = Column(String)
    work_description = Column(String)

    recommended_date = Column(Date)
    recommended_amount_rs = Column(Float)

    sanctioned_date = Column(Date)
    sanctioned_amount_rs = Column(Float)

    work_status = Column(String)
    completed = Column(Boolean)
    completion_date = Column(Date)

    amount_disbursed_rs = Column(Float)
    allocated_amount_rs = Column(Float)

    image = Column(String)

    # Dataset-specific fields
    extra_data = Column(JSON)