from scrape import scrape_sports, scrape_politics, scrape_startups
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    "start_date":datetime(2023,5,28),
    "owner":"test_user"
}

dag = DAG(
    dag_id = "my_dag",
    default_args = default_args,
    schedule_interval = "*/5 * * * *"
)

scrape_sports_task = PythonOperator(
    task_id = 'scrape_sports',
    python_callable = scrape_sports,
    dag = dag,
)

scrape_startups_task = PythonOperator(
    task_id = "scrape_startups",
    python_callable = scrape_startups,
    dag = dag,
)

scrape_politics_task = PythonOperator(
    task_id = "scrape_politics",
    python_callable = scrape_politics,
    dag = dag,
)

update_task = BashOperator(
    task_id = 'update',
    bash_command = "./update.py",
    dag = dag,
)

scrape_sports_task >> update_task
scrape_startups_task >> update_task
scrape_politics_task >> update_task