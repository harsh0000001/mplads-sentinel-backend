from app.ml.risk_model import load_model


lok = load_model("Lok Sabha")
rajya = load_model("Rajya Sabha")

print("Lok Sabha model loaded!")
print("Lok keys:", lok.keys())

print("\nRajya Sabha model loaded!")
print("Rajya keys:", rajya.keys())