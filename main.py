from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.works import router as works_router
from app.routers.dashboard import router as dashboard_router
from app.routers.risk import router as risk_router
from app.routers.similar import router as similar_router
from app.routers.risk_list import router as risk_list_router
from app.routers.risk_summary import router as risk_summary_router
from app.routers.state_analytics import router as state_analytics_router
from app.routers.financial_analytics import router as financial_analytics_router
from app.routers.category_analytics import router as category_analytics_router
from app.routers.mp_analytics import router as mp_analytics_router
from app.routers.notifications import router as notifications_router
from app.routers.audit_logs import router as audit_logs_router
from app.routers.system_statistics import router as system_statistics_router


app = FastAPI(
    title="MPLADS Sentinel API",
    description="AI-assisted MPLADS monitoring and decision-support backend",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(works_router)
app.include_router(dashboard_router)

app.include_router(risk_router)
app.include_router(risk_list_router)
app.include_router(risk_summary_router)
app.include_router(similar_router)

app.include_router(state_analytics_router)
app.include_router(financial_analytics_router)
app.include_router(category_analytics_router)
app.include_router(mp_analytics_router)

app.include_router(notifications_router)
app.include_router(audit_logs_router)

app.include_router(system_statistics_router)