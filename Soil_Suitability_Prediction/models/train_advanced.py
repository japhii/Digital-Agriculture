import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def train_advanced_model():
    csv_path = "/Users/yaphetesayas/Desktop/DigitalAgricultureUpdate/Soil_Suitability_Prediction/dataset/advanced_soil_data.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
    df = pd.read_csv(csv_path)
    features = [
        "TS", "T2M_MAX", "T2M", "QV2M", "WS10M", "T2M_MIN", "RH2M",
        "T2MDEW", "WS2M", "ALLSKY_SFC_PAR_TOT", "PS", "ALLSKY_SFC_SW_DWN", "PRECTOTCORR"
    ]
    X = df[features]
    y = df["soil_health_index"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R2 Score: {r2:.4f}")
    model_dir = "/Users/yaphetesayas/Desktop/DigitalAgricultureUpdate/Models/Soil Suitability"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_path = os.path.join(model_dir, "prediction_model_v2.pkl")
    scaler_path = os.path.join(model_dir, "scaler_v2.pkl")
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == "__main__":
    train_advanced_model()