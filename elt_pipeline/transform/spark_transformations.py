from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

def transform_data():
    spark = SparkSession.builder.appName("Transform").getOrCreate()
    
    df_ibge = spark.read.csv("data/raw/ibge_producao.csv", header=True, inferSchema=True)
    df_inmet = spark.read.csv("data/raw/inmet/BRASIL.csv", header=True, inferSchema=True)
    
    df_ibge_clean = df_ibge.select("Municipio", "Ano", "Produto", "Quantidade Produzida")\
        .withColumnRenamed("Quantidade Produzida", "qtd_produzida")
    
    df_inmet_clean = df_inmet.select("Data", "UF", "TempMedia", "Precipitacao")\
        .withColumn("Data", to_date("Data", "yyyy-MM-dd"))
    
    df_joined = df_ibge_clean.join(
        df_inmet_clean,
        (df_ibge_clean["Ano"] == df_inmet_clean["Data"].substr(0,4)) &
        (df_ibge_clean["Municipio"] == df_inmet_clean["UF"]),
        how="left"
    )
    
    df_joined.write.mode("overwrite").parquet("data/curated/ibge_inmet_joined/")
    print("Dados transformados e salvos.")

if __name__ == "__main__":
    transform_data()
