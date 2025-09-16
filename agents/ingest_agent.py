import os
import pandas as pd
import psycopg2


def _conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "mas_db"),
        user=os.getenv("PGUSER", "mas_user"),
        password=os.getenv("PGPASSWORD", "mas_pass"),
        port=int(os.getenv("PGPORT", "5432")),
    )


def ingest_transactions(csv_path: str = "data/transactions.csv") -> int:
    if not os.path.exists(csv_path):
        return 0
    df = pd.read_csv(csv_path)
    cols = ["amount", "category", "merchant", "employee_id", "fraud_flag", "tx_date"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    with _conn() as conn:
        with conn.cursor() as cur:
            for _, r in df.iterrows():
                cur.execute(
                    """
                    INSERT INTO transactions(amount, category, merchant, employee_id, fraud_flag, tx_date)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        float(r["amount"]) if r["amount"] is not None else None,
                        r["category"],
                        r["merchant"],
                        int(r["employee_id"]) if pd.notna(r["employee_id"]) else None,
                        int(r["fraud_flag"]) if pd.notna(r["fraud_flag"]) else None,
                        r["tx_date"],
                    ),
                )
        conn.commit()
    return len(df)
