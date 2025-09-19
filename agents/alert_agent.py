import pandas as pd


def detect_anomalies(csv_path: str = "data/transactions_extended.csv", z_threshold: float = 3.0) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame()
    if "amount" not in df.columns:
        return pd.DataFrame()
    amounts = df["amount"].astype(float)
    mean = amounts.mean()
    std = amounts.std(ddof=0) or 1.0
    z = (amounts - mean) / std
    result = df.loc[z.abs() >= z_threshold].copy()
    result["zscore"] = z.loc[result.index]
    return result
