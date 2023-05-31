from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scrape import scrape_sports, scrape_startups, scrape_politics

default_args = {
    'start_date': datetime(2023, 5, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# DAG for scraping sports data
with DAG('scrape_sports_dag', default_args=default_args, schedule_interval='@daily') as sports_dag:
    scrape_sports_task = PythonOperator(
        task_id='scrape_sports_task',
        python_callable=scrape_sports
    )

# DAG for scraping startup data
with DAG('scrape_startups_dag', default_args=default_args, schedule_interval='@daily') as startups_dag:
    scrape_startups_task = PythonOperator(
        task_id='scrape_startups_task',
        python_callable=scrape_startups
    )

# DAG for scraping politics data
with DAG('scrape_politics_dag', default_args=default_args, schedule_interval='@daily') as politics_dag:
    scrape_politics_task = PythonOperator(
        task_id='scrape_politics_task',
        python_callable=scrape_politics
    )
