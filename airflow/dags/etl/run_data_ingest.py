import get_all_variables as gav
import logging.config
import logging

# Load the Logging Configuration File
logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)

def load_files(spark, file_dir, file_format='parquet', header=False, inferSchema=False):
    try:
        logger.info("load_fule is Started ...")
        raw_data = spark.read.format(file_format) \
            .option(header=header) \
            .option(inferSchema=inferSchema) \
            .load(file_dir)
    except Exception as exp:
        logger.error("Error in the method - load_files(). Please check the Stack Trace. " + str(exp))
    else:
        logger.info(f"The input File {file_dir} is loaded to the data frame. The load_files() Function is completed.")
    return raw_data


def oracle_read_files(spark, query, num_transaction=None, url="jdbc:oracle:thin:@172.16.65.163:1521/CARDDATA",
                      user="apps", password="appsnoor", partition=6 , split=True):

    try:
        if num_transaction:
            query = "(%s FETCH FIRST %s ROWS ONLY) emp " % (query, num_transaction)
        else:
            query = "(%s) emp " % query

        logger.info("oracle_read_files is Started ...")
        raw_data = spark.read.format("jdbc") \
            .option("numPartitions", partition) \
	        .option("partitionColumn","UNIQUEID") \
	        .option("lowerBound",9399643542) \
	        .option("upperBound",10829491847) \
            .option("url", url) \
            .option("dbtable", query) \
            .option("user", user) \
            .option("password", password) \
            .option("driver", "oracle.jdbc.driver.OracleDriver") \
            .load()

        if split:
            train_data, test_data = raw_data.randomSplit([0.8,0.2])

    except Exception as exp:
        logger.error("Error in method - load_files(). Please check the Stack Trace. " + str(exp))
        raise
    else:
        logger.info("The input File is loaded to the data frame. The load_files() Function is completed.")
    if split:
        return train_data, test_data
    else :
        return raw_data
