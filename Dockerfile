# Base image com Python e Java
FROM bitnami/spark:3.4.1

# Instala o Hadoop AWS para suporte ao S3A (MinIO)
USER root
RUN apt-get update && \
  apt-get install -y wget openjdk-11-jdk && \
  rm -rf /var/lib/apt/lists/*

# Define variáveis de ambiente para Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Diretório de trabalho
WORKDIR /opt/spark/work-dir

# Copia arquivos de configuração (como spark-defaults.conf)
COPY ./configs/spark-defaults.conf /opt/bitnami/spark/conf/

# Copia os scripts PySpark para o container
COPY ./scripts /opt/spark/scripts

# Hadoop AWS (S3A) + bibliotecas necessárias
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.5/hadoop-aws-3.3.5.jar -P /opt/bitnami/spark/jars/ && \
  wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.426/aws-java-sdk-bundle-1.12.426.jar -P /opt/bitnami/spark/jars/

# Permissões
RUN chmod -R 755 /opt/spark

# Usuário padrão
USER 1001
