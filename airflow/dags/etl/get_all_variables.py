import os

# Set Environment Variables
os.environ['envn'] = 'Production'

# Get Environment Variables
envn = os.environ['envn']

# Set Other Variables
current_path = os.getcwd()
logging_conf_path = os.path.abspath(os.path.join(os.path.abspath(__file__), '../../util/logging_to_file.conf'))
appName = "Nur_Pipeline"
#data_root = "hdfs://imen-spark-master.css.ir:9000/raw_data"
data_root = "/user/hadoop/raw_data"
hdfs_root = "hdfs://imen-spark-master.css.ir:9000/pipeline"
#spark_master = "yarn"
spark_master = "spark://imen-spark-master.css.ir:7077"

# Output directory to store artifacts generated from the pipeline
pipeline_root = os.path.join(hdfs_root, appName)
# Path to a SQLite DB file to use as an MLMD storage.
metadata_path = os.path.join("/data", appName, 'metadata.db')
# Output directory where created models from the pipeline will be exported.
serving_model_dir = os.path.join(hdfs_root, appName)
# JAR Locations
jdbc_jar = '/home/hadoop/jdbc-8.jar'
spark_tfrecord_jar = '/home/spark/sample_code/full_pipeline/jar/spark-tfrecord_2.12-0.3.3.jar'

# SQl Queries
ingest_nur_query = "SELECT UNIQUEID, DATETIMELOCALTRANSACTION, PAN, AMTTXN, TERMINALTYPE, TRANSACTIONTYPE, MCC FROM NOOR.ITXN"
