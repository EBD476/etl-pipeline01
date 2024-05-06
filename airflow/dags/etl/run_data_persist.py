import get_all_variables as gav
import logging.config
import logging 
import datetime as date

# Load the Logging Configuration File
logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)

def data_persist(spark, df, dfName,dbName='noor', partitionBy='delivery_date', mode='append'):
    try:
        logger.info(f"Data Persist Script - data_persist() us started for saving dataframe "+ dfName + "into Hive Table...")
        # Add a Static column with Current Date
        df= df.withColumn("delivery_date", lit(date.datetime.now().strftime("%Y-%m-%d")))
        spark.sql(f""" CREATE DATABASE IF NOT EXISTS {dbName} LOCATION 'hdfs://imen-spark-master.css.ir:9000/user/hive/warehouse/{dbName}.db'  """)
        spark.sql(f""" USE {dbName} """)
        df.write.saveAsTable(dfName, partitionBy=partitionBy, mode=mode)
    except Exception as exp:
        logger.error("Error in the method - data_persist(). Please check the Stack Trace. " + str(exp), exc_info=True)
        raise
    else:
        logger.info("Data Persist - data_persist() is completed for saving datafram "+ dfName +" into Hive Table... ")