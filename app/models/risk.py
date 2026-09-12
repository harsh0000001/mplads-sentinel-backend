from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base


class RiskAnalysis(Base):
    __tablename__ = "risk_analysis"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String, index=True, nullable=False)
    sabha = Column(String, index=True, nullable=False)

    anomaly_score = Column(Float)
    is_anomaly = Column(Boolean)

    anomaly_component = Column(Float)
    financial_component = Column(Float)
    execution_component = Column(Float)
    completeness_component = Column(Float)

    risk_score = Column(Float)
    risk_level = Column(String)

    risk_indicators = Column(Text)
    similar_works = Column(Text)