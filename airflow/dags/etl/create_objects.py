from pyspark import SparkConf
from pyspark.sql import SparkSession
import get_all_variables as gav
import logging.config
import logging

# Load the Logging Configuration File
logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)


def get_spark_object(appname, envn, master=gav.spark_master, instances=7, memory="7G", cores=6, d_memory="7G", d_cores=6, partitions=7):
    try:
        if envn == 'TEST':
            spark = SparkSession.builder.master('local')\
                .appName(appname)\
                .getOrCreate()
        else:
            logger.info(f"get_spark_object is started with {cores} Cores and {memory} Memory.")
            conf = SparkConf().setAppName(appname) \
                  .setMaster(master) \
		          .set("spark.jars", gav.jdbc_jar) \
                  .set("spark.executor.extraClassPath", gav.jdbc_jar) \
                  .set("spark.driver.extraClassPath", gav.jdbc_jar) \
                  .set("spark.executor.instances", str(instances)) \
                  .set("spark.executor.memory", memory) \
                  .set("spark.executor.memoryOverhead", 1024) \
                  .set("spark.executor.cores",cores) \
                  .set("spark.driver.memory",d_memory) \
                  .set("spark.driver.memoryOverhead", 1024) \
                  .set("spark.driver.cores",d_cores) \
                  .set("spark.sql.shuffle.partitions", str(partitions))                    
            #     .set("spark.jars", gav.spark_tfrecord_jar) 

            spark = SparkSession.builder.config(conf=conf).getOrCreate()
    except Exception as exp:
        logger.error("Error in the method - get_spark_object(). Please check the Stack Trace."+str(exp), exc_info=True)
    else:
        logger.info("Spark Object is created ...")
    return spark
