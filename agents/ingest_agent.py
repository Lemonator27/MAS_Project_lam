import os
import pandas as pd


def ingest_transactions(csv_path: str = "data/transactions.csv") -> pd.DataFrame:
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    # Chuẩn hoá các cột tối thiểu
    expected = ["transaction_id", "amount", "date", "category", "merchant", "employee_id", "fraud_flag"]
    for c in expected:
        if c not in df.columns:
            df[c] = None
    return df
