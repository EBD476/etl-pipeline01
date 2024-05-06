from create_objects import get_spark_object
from run_data_ingest import oracle_read_files
from run_data_extraction import extract_files
import get_all_variables as gav
import logging.config
import logging
import sys

logging.config.fileConfig(fname=gav.logging_conf_path)

def main():
    try:
        logging.info("main() is Started...")
        # Get the Spark Object
        spark = get_spark_object(appname="Data Ingest to HDFS", envn=gav.envn)

        # Read the data from Oracle 
        nur_data =  oracle_read_files(spark=spark, query="SELECT * FROM NOOR.ITXN",
                                      num_transaction=None, partition=14, split=False)

        # Write data to the HDFS
        extract_files(df=nur_data, format="parquet", filePath=gav.data_root, split_no=3 , headerReq=True, compressionType="snappy")

        # End of Writing to HDFS
        logging.info("Oracle to HDFS is Completed.")

    except Exception as exp:
        logging.error("Error Occured in the main() method. Please check the Stack Trace to go to the respective module "
        "and fix it." + str(exp), exc_info=True)
        sys.exit(1)

if __name__=="__main__":
    logging.info("Oracle To HDFS is Started ...")
    main()

