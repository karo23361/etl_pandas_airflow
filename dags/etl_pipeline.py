from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

default_args = {
    'owner': 'karo',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def transform(**kwargs):
    df = pd.read_csv("/opt/airflow/data/dirty_cafe_sales.csv")

    df_menu = pd.DataFrame({
        'Item': ['Coffee', 'Tea', 'Sandwich', 'Salad', 'Cake', 'Cookie', 'Smoothie', 'Juice'],
        'Price': [2.0, 1.5, 4.0, 5.0, 3.0, 1.0, 4.0 , 3.0]
    })
    df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors='coerce')
    df_menu["Price"] = pd.to_numeric(df_menu["Price"], errors="coerce")
    price_to_item = df_menu.set_index("Price")["Item"].to_dict()

    invalid_values = ["ERROR", "UNKNOWN", None, "", pd.NA, np.nan]
    df["Item"] = df["Item"].replace(invalid_values, pd.NA)
    mask = df["Item"].isna() & df["Price Per Unit"].isin(price_to_item.keys())
    df.loc[mask, "Item"] = df.loc[mask, "Price Per Unit"].map(price_to_item)

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')
    df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors='coerce')
    df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors='coerce')

    mask = df["Quantity"].isin(invalid_values) | df["Quantity"].isna()
    df.loc[mask, "Quantity"] = df.loc[mask, "Total Spent"] / df.loc[mask, "Price Per Unit"]
    df = df.dropna(subset=["Quantity", "Item"])

    item_to_price = df_menu.set_index("Item")["Price"].to_dict()
    mask = df["Price Per Unit"].isna() | df["Price Per Unit"].isin(invalid_values)
    df.loc[mask, "Price Per Unit"] = df.loc[mask, "Item"].map(item_to_price)

    mask = df["Total Spent"].isna() | df["Total Spent"].isin(invalid_values)
    df.loc[mask, "Total Spent"] = df.loc[mask, "Quantity"] * df.loc[mask, "Price Per Unit"]

    df["Payment Method"] = df["Payment Method"].replace(invalid_values, np.nan)
    df["Location"] = df["Location"].replace(invalid_values, np.nan)

    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df["Transaction Date"] = df["Transaction Date"].ffill()

    tmp_path = "/opt/airflow/data/cleaned_sales.pkl"
    df.to_pickle(tmp_path)
    kwargs['ti'].xcom_push(key='cleaned_file_path', value=tmp_path)

def load(**kwargs):
    ti = kwargs['ti']
    path = ti.xcom_pull(task_ids='transform', key='cleaned_file_path')
    df = pd.read_pickle(path)

    output_path = "/opt/airflow/data/cleaned_sales.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

with DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    t2 = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    t3 = PythonOperator(
        task_id='load',
        python_callable=load
    )

    t2 >> t3
