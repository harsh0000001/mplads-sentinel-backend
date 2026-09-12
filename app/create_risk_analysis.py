import pandas as pd

from app.database import SessionLocal, Base, engine
from app.models.risk import RiskAnalysis


def import_risk_data(file_path, sabha):
    df = pd.read_csv(file_path)

    db = SessionLocal()

    try:
        for _, row in df.iterrows():
            risk = RiskAnalysis(
                work_id=row["work_id"],
                sabha=sabha,
                anomaly_score=row["anomaly_score"],
                is_anomaly=row["is_anomaly"],
                anomaly_component=row["anomaly_component"],
                financial_component=row["financial_component"],
                execution_component=row["execution_component"],
                completeness_component=row["completeness_component"],
                risk_score=row["risk_score"],
                risk_level=row["risk_level"],
                risk_indicators=str(row["risk_indicators"]),
                similar_works=str(row["similar_works"]),
            )

            db.add(risk)

        db.commit()
        print(f"{sabha} risk data imported successfully.")

    finally:
        db.close()


Base.metadata.create_all(bind=engine)

import_risk_data(
    "data/lok_sabha_ml_output.csv",
    "Lok Sabha"
)

import_risk_data(
    "data/rajya_sabha_ml_output.csv",
    "Rajya Sabha"
)