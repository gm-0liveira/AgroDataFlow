from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='spark_etl_minio_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Executa pipeline ETL PySpark lendo dados do MinIO',
) as dag:

    spark_etl = SparkSubmitOperator(
        task_id='run_spark_etl',
        application='/opt/spark/scripts/etl_pipeline.py',  # Caminho no container Spark
        conn_id='spark_default',  # Conexão padrão do Spark no Airflow
        verbose=True,
        application_args=[
            "--input", "s3a://meu-bucket/raw/dados.csv",
            "--output", "s3a://meu-bucket/processed/dados_transformados"
        ],
        conf={
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": "minioadmin",
            "spark.hadoop.fs.s3a.secret.key": "minioadmin",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        }
    )

    spark_etl
