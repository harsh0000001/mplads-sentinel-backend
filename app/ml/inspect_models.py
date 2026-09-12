import joblib


LOK_MODEL = "app/ml/models/lok_sabha_anomaly_pipeline.joblib"
RAJYA_MODEL = "app/ml/models/rajya_sabha_anomaly_pipeline.joblib"


lok_pipeline = joblib.load(LOK_MODEL)
rajya_pipeline = joblib.load(RAJYA_MODEL)


print("===== LOK SABHA =====")

print("Model type:")
print(type(lok_pipeline))

print("\nFeatures:")
print(lok_pipeline["features"])


print("\n===== RAJYA SABHA =====")

print("Model type:")
print(type(rajya_pipeline))

print("\nFeatures:")
print(rajya_pipeline["features"])