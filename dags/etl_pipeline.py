import datetime
from pipeline import extract, load, transform
from airflow.decorators import dag, task


@dag(
    dag_id="spotify_etl",
    schedule_interval="@daily",
    start_date=datetime.datetime(2024, 2, 15),
    catchup=True,
    dagrun_timeout=datetime.timedelta(minutes=60),
    max_active_runs=1,
)
def run_pipeline():
    date = datetime.datetime.today()

    @task()
    def get_data(date):
        return extract.query_data(date)

    @task()
    def transform_data(data):
        return transform.transform(data)

    @task()
    def load_data(transformed_data):
        load.write_data_to_tables(transformed_data)

    raw_data = get_data(date)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)


dag = run_pipeline()
