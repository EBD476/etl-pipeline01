import get_all_variables as gav
import logging.config
import logging
import pandas

# Load the Logging Configuration File
logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)


def get_curr_date(spark):
    try:
        opdf = spark.sql(""" SELECT current_date """)
        logger.info("Validate the Spark object by printing Current Date - " + str(opdf.collect()))
    except Exception as exp:
        logger.error("Error in the method - spark_curr_date(). Please check the Stack Trace. " + str(exp),
                     exc_info=True)
        raise
    else:
        logger.info("Spark object is validated. Spark Object is ready.")


def df_count(df, dfname):
    try:
        logger.info(f"The DataFrame Validation by count df_count() is started for Dataframe {dfname}...")
        df_counts = df.count()
        logger.info(f"The DataFrame count is {df_counts}.")
    except Exception as exp:
        logger.error("Error in the method - df_count(). Please check the Stack Trace. " + str(exp))
        raise
    else:
        logger.info(f"The DataFrame Validation by count df_count() is completed.")


def df_top10_rec(df, dfname):
    try:
        logger.info(f"The DataFrame Validation by top 10 records df_top10_rec() is started for Dataframe {dfname}...")
        logger.info(f"The DataFrame top 10 records are:.")
        df_pandas = df.limit(10).toPandas()
        logger.info('\n \t' + df_pandas.to_string(index=False))
    except Exception as exp:
        logger.error("Error in the method - df_top10_rec(). Please check the Stack Trace. " + str(exp))
        raise
    else:
        logger.info("The DataFrame Validation by top 10 record df_top10_rec() is completed.")


def df_print_schema(df, dfname):
    try:
        logger.info(f"The DataFrame Schema Validation for DataFrame {dfname}")
        sch = df.schema.fields
        logger.info(f"The DataFrame {dfname} schema is: ")
        for i in sch:
            logger.info(f"\t{i}")
    except Exception as exp:
        logger.info("Error in the method - df_show_schema(). Please check the Stack Trace. " + str(exp))
        raise
    else:
        logger.info("The DataFrame Schema Validation is completed.")
