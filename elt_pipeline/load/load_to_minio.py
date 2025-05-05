from pyspark.sql import SparkSession

def load_to_lake():
    spark = SparkSession.builder \
        .appName("LoadMinIO") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .getOrCreate()

    df = spark.read.parquet("data/curated/ibge_inmet_joined/")
    df.write.mode("overwrite").parquet("s3a://agronegocio/curated/")
    print("Dados enviados para o Data Lake (MinIO).")

if __name__ == "__main__":
    load_to_lake()
