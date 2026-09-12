from pydantic import BaseModel
from datetime import date


class WorkResponse(BaseModel):
    id: int
    work_id: str | None = None
    sabha: str

    work_category: str | None = None
    work: str | None = None
    state: str | None = None
    mp_name: str | None = None
    work_description: str | None = None

    recommended_date: date | None = None
    recommended_amount_rs: float | None = None

    sanctioned_date: date | None = None
    sanctioned_amount_rs: float | None = None

    work_status: str | None = None
    completed: bool | None = None
    completion_date: date | None = None

    amount_disbursed_rs: float | None = None
    allocated_amount_rs: float | None = None

    image: str | None = None

    model_config = {
        "from_attributes": True
    }