import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "app/models/iforest.pkl"

def train_iforest(df_features: pd.DataFrame):
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(df_features)
    joblib.dump(model, MODEL_PATH)
    return model

if __name__ == "__main__":
    # ejemplo: carga features.csv creado por proceso offline
    df = pd.read_csv("features.csv")
    m = train_iforest(df)
    print("Modelo entrenado y guardado.")
