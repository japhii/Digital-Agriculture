import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=10000):
    np.random.seed(42)
    data = {
        "TS": np.random.uniform(273.15 - 5, 273.15 + 45, num_samples),
        "T2M_MAX": np.random.uniform(5, 50, num_samples),
        "T2M": np.random.uniform(0, 45, num_samples),
        "QV2M": np.random.uniform(2, 22, num_samples),
        "WS10M": np.random.uniform(0, 12, num_samples),
        "T2M_MIN": np.random.uniform(-5, 35, num_samples),
        "RH2M": np.random.uniform(20, 95, num_samples),
        "T2MDEW": np.random.uniform(-10, 25, num_samples),
        "WS2M": np.random.uniform(0, 8, num_samples),
        "ALLSKY_SFC_PAR_TOT": np.random.uniform(10, 80, num_samples),
        "PS": np.random.uniform(90, 105, num_samples),
        "ALLSKY_SFC_SW_DWN": np.random.uniform(5, 35, num_samples),
        "PRECTOTCORR": np.random.uniform(0, 200, num_samples),
    }
    df = pd.DataFrame(data)
    def calculate_index(row):
        ts_c = row["TS"] - 273.15
        t2m = row["T2M"]
        precip = row["PRECTOTCORR"]
        rh = row["RH2M"]
        sw_dwn = row["ALLSKY_SFC_SW_DWN"]
        ps = row["PS"]
        ws = row["WS2M"]
        qv = row["QV2M"]
        def temp_score(t):
            if t < 10 or t > 40: return 0
            if t <= 25: return (t - 10) / (25 - 10)
            return (40 - t) / (40 - 25)

        t_score = 0.5 * temp_score(t2m) + 0.5 * temp_score(ts_c)
        if precip < 20: p_score = precip / 20 * 0.5
        elif precip < 50: p_score = 0.5 + (precip - 20) / 30 * 0.5
        elif precip < 150: p_score = 1.0
        else: p_score = max(0.4, 1.0 - (precip - 150) / 150)
        rh_score = rh / 100
        m_score = 0.6 * p_score + 0.4 * rh_score
        s_score = min(1.0, sw_dwn / 25)
        ps_score = 1.0 - abs(ps - 101.3) / 20
        ps_score = max(0, ps_score)
        ws_score = max(0, 1.0 - ws / 15)
        env_score = 0.7 * ps_score + 0.3 * ws_score
        index = (
            0.35 * t_score +
            0.30 * m_score +
            0.20 * s_score +
            0.15 * env_score
        )
        index += np.random.normal(0, 0.03)
        return max(0, min(1, index))

    df["soil_health_index"] = df.apply(calculate_index, axis=1)
    return df

if __name__ == "__main__":
    out_dir = "/Users/yaphetesayas/Desktop/DigitalAgricultureUpdate/Soil_Suitability_Prediction/dataset"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print("Generating synthetic data...")
    df = generate_synthetic_data(15000)
    csv_path = os.path.join(out_dir, "advanced_soil_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}. Samples: {len(df)}")