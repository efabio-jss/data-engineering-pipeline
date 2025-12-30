import os
import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

BASE_URL = "https://e-redes.opendatasoft.com"

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DB = os.getenv("SQL_DB")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DRIVER = os.getenv("SQL_DRIVER")

CONN_STR = (
    f"mssql+pyodbc://{SQL_USER}:{SQL_PASSWORD}"
    f"@{SQL_SERVER}/{SQL_DB}"
    f"?driver={SQL_DRIVER.replace(' ', '+')}"
)

engine = create_engine(CONN_STR, fast_executemany=True)

DATASETS = [
    {
        "name": "Self Consumption Production Units",
        "path": "/api/explore/v2.1/catalog/datasets/8-unidades-de-producao-para-autoconsumo/records",
        "table": "raw_eredes_self_consumption"
    },
    {
        "name": "National Consumption",
        "path": "/api/explore/v2.1/catalog/datasets/consumo-total-nacional/records",
        "table": "raw_eredes_national_consumption"
    },
    {
        "name": "Municipal Consumption",
        "path": "/api/explore/v2.1/catalog/datasets/3-consumos-faturados-por-municipio-ultimos-10-anos/records",
        "table": "raw_eredes_municipal_consumption"
    },
    {
        "name": "Substation Load",
        "path": "/api/explore/v2.1/catalog/datasets/carga-na-subestacao/records",
        "table": "raw_eredes_substation_load"
    },
    {
        "name": "Low Voltage Supports",
        "path": "/api/explore/v2.1/catalog/datasets/apoios-baixa-tensao/records",
        "table": "raw_eredes_lv_supports"
    },
    {
        "name": "Energy Communities",
        "path": "/api/explore/v2.1/catalog/datasets/comunidades-de-energia/records",
        "table": "raw_eredes_energy_communities"
    },
    {
        "name": "Planned Outages",
        "path": "/api/explore/v2.1/catalog/datasets/network-scheduling-work/records",
        "table": "raw_eredes_planned_outages"
    }
]

def fetch_all_records(path: str, page_size: int = 1000) -> pd.DataFrame:
    rows = []
    offset = 0

    while True:
        params = {"limit": page_size, "offset": offset}
        url = BASE_URL + path
        print(f"[API] {url} offset={offset}")

        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            break

        for r in results:
            fields = r.get("fields", r)
            row = dict(fields)
            row["recordid"] = r.get("recordid")
            row["record_timestamp"] = r.get("record_timestamp")
            rows.append(row)

        if len(results) < page_size:
            break

        offset += page_size
        time.sleep(0.2)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    return df


def load_full_refresh(df: pd.DataFrame, table_name: str):
    if df.empty:
        print(f"[DB] {table_name} - empty, nothing loaded")
        return

    print(f"[DB] Refreshing {table_name} with {len(df)} rows...")
    df.to_sql(
        table_name,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi"
    )
    print(f"[DB] {table_name} updated.")


def run_ingestion():
    print("===== E-REDES INGEST START =====")
    for ds in DATASETS:
        print(f"\n>>> {ds['name']} <<<")
        try:
            df = fetch_all_records(ds["path"])
            print(f"[INFO] Retrieved rows: {len(df)}")
            load_full_refresh(df, ds["table"])
        except Exception as e:
            print(f"[ERROR] {ds['name']} failed: {e}")
    print("===== E-REDES INGEST DONE =====")


if __name__ == "__main__":
    run_ingestion()
