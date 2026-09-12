import joblib


LOK_MODEL = "app/ml/models/lok_sabha_anomaly_pipeline.joblib"
RAJYA_MODEL = "app/ml/models/rajya_sabha_anomaly_pipeline.joblib"


print("Loading Lok Sabha model...")

lok_pipeline = joblib.load(LOK_MODEL)

print("Lok Sabha model loaded successfully!")


print("Loading Rajya Sabha model...")

rajya_pipeline = joblib.load(RAJYA_MODEL)

print("Rajya Sabha model loaded successfully!")


print("\nBoth ML models loaded successfully!")