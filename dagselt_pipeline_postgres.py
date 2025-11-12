from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd

# Path to CSV inside Docker container
CSV_PATH = "/opt/airflow/data/users.csv"

def extract_data(ti, **kwargs):
    """
    Read CSV and push raw data via XCom.
    """
    df = pd.read_csv(CSV_PATH)
    ti.xcom_push(key="raw_records", value=df.to_dict(orient="records"))

def load_to_staging(ti, **kwargs):
    """
    Pull raw records from XCom and write to etl_staging.staging_users table.
    """
    raw_records = ti.xcom_pull(task_ids="extract", key="raw_records")
    df = pd.DataFrame.from_records(raw_records)

    pg_hook = PostgresHook(postgres_conn_id="post")
    engine = pg_hook.get_sqlalchemy_engine()
    df.to_sql("staging_users", engine, schema="etl_staging", if_exists="replace", index=False)

# DAG definition
with DAG(
    dag_id="postgres",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,  # Use '@daily' if needed
    catchup=False,
    tags=["elt", "postgres"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
    )

    load = PythonOperator(
        task_id="load_to_staging",
        python_callable=load_to_staging,
    )

    transform = PostgresOperator(
        task_id="transform_and_load_final",
        postgres_conn_id="post",
        sql="""
        DROP TABLE IF EXISTS etl_staging.final_users;
        CREATE TABLE etl_staging.final_users AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY id) AS final_id,
            CAST(id AS INTEGER) AS id,
            INITCAP(TRIM(name)) AS name,
            LOWER(NULLIF(TRIM(email), '')) AS email,
            age,
            signup_date::date AS signup_date,
            country,
            CURRENT_DATE AS load_date
        FROM etl_staging.staging_users
        WHERE
            id IS NOT NULL
            AND (email IS NULL OR position('@' in email) > 1);

        CREATE INDEX IF NOT EXISTS idx_final_users_email 
        ON etl_staging.final_users (email);
        """,
    )

    extract >> load >> transform
