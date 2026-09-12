import joblib
from pathlib import Path
from functools import lru_cache


MODEL_DIR = Path(__file__).resolve().parent / "models"


@lru_cache
def load_model(sabha: str):
    if sabha == "Lok Sabha":
        model_path = MODEL_DIR / "lok_sabha_anomaly_pipeline.joblib"

    elif sabha == "Rajya Sabha":
        model_path = MODEL_DIR / "rajya_sabha_anomaly_pipeline.joblib"

    else:
        raise ValueError("Invalid sabha. Use 'Lok Sabha' or 'Rajya Sabha'.")

    return joblib.load(model_path)