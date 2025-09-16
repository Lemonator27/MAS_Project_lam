import os
import sys
import psycopg2


def get_conn():
    host = os.getenv("PGHOST", "localhost")
    db = os.getenv("PGDATABASE", "mas_db")
    user = os.getenv("PGUSER", "mas_user")
    password = os.getenv("PGPASSWORD", "mas_pass")
    port = int(os.getenv("PGPORT", "5432"))
    return psycopg2.connect(host=host, dbname=db, user=user, password=password, port=port)


SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    amount DOUBLE PRECISION,
    category VARCHAR(50),
    merchant VARCHAR(100),
    employee_id INT,
    fraud_flag INT,
    tx_date DATE
);

CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    dept VARCHAR(50),
    project_id INT,
    approved_amount DOUBLE PRECISION,
    actual_spent DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS risks (
    id SERIAL PRIMARY KEY,
    transaction_id INT,
    risk_score DOUBLE PRECISION,
    anomaly_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);
"""


def main() -> int:
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
            conn.commit()
        print("DB initialized with pgvector and base tables.")
        return 0
    except Exception as e:
        print(f"Failed to initialize DB: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
