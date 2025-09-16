import pandas as pd


def summarize_subscriptions(csv_path: str = "data/transactions.csv") -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame()
    needed = {"merchant", "amount", "category"}
    if not needed.issubset(set(df.columns)):
        return pd.DataFrame()
    subs = df[df["category"].str.lower().eq("subscription")]
    return subs.groupby("merchant", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
