from pydantic import BaseModel


class RiskResponse(BaseModel):
    work_id: str
    sabha: str

    anomaly_score: float | None = None
    is_anomaly: bool | None = None

    anomaly_component: float | None = None
    financial_component: float | None = None
    execution_component: float | None = None
    completeness_component: float | None = None

    risk_score: float | None = None
    risk_level: str | None = None

    risk_indicators: str | None = None
    similar_works: str | None = None

    model_config = {
        "from_attributes": True
    }