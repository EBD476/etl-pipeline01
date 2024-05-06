import logging
import logging.config
import get_all_variables as gav
from validations import get_curr_date, df_count
from create_objects import get_spark_object
from run_data_ingest import oracle_read_files
from run_data_preprocessing import data_preprocessing

# Load the Logging Configuration File

logging.config.fileConfig(fname=gav.logging_conf_path)
print(gav.logging_conf_path)

def main():
    logging.info("main() is started ...")
    # Get Spark Object
    spark = get_spark_object(appname=gav.appName, envn=gav.envn)
    # Validate Spark Object
    get_curr_date(spark)

    # Data Ingestion
    df_train, df_test = oracle_read_files(spark=spark, query=gav.ingest_nur_query, num_transaction=None, partition=6)

    # Validate the Data Ingestion
    df_count(df_train, 'Train Data')
    df_count(df_test, 'Test Data')

    # Data Preprocessing
    df_train = data_preprocessing(df_train)
    df_train.show()

    # Statistics Gen (


if __name__ == "__main__":
    logging.info("run_pipeline is Started ...")
    main()
