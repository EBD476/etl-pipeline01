FROM python:3.9.18-slim

# Install OpenJDK 8
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && \
    apt-get install -y openjdk-17-jdk maven && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
RUN echo $JAVA_HOME

RUN apt-get update -y && apt-get install -y libzbar-dev bash gcc git libc-dev curl wget vim nano \
    && apt-get install -y iputils-ping telnet openssh-client net-tools \
    man unzip vim-tiny bc openssh-server thrift-compiler netcat-traditional sudo \
    && apt-get install -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean

# install spark
RUN curl -o spark-3.1.1-bin-hadoop3.2.tgz https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz && \
    tar -xzvf spark-3.1.1-bin-hadoop3.2.tgz && \
    mv spark-3.1.1-bin-hadoop3.2 /opt/spark && \
    rm -rf spark-3.1.1-bin-hadoop3.2.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PATH=$PATH:$SPARK_HOME/sbin
ENV PYTHONPATH=$SPARK_HOME/python3:$SPARK_HOME/python3/lib/py4j-0.10.7-src.zip:$PYTHONPATH

RUN apt-get update && apt-get install -y libpq-dev
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY ./dags ./opt/airflow/dags
RUN chmod -R a+rwx /opt/airflow
COPY airflow.cfg /opt/airflow/airflow.cfg
COPY run.sh ./run.sh
RUN chmod +x /run.sh
WORKDIR /opt/airflow

CMD /run.sh
EXPOSE 8000