import get_all_variables as gav
import logging.config
import logging

# Load the Logging Configuration File
logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)

# Extraction function
def extract_files(df, format, filePath, split_no, headerReq, compressionType):
    try:
        logger.info(f"Extraction - extract_files() is started...")
        df.coalesce(split_no) \
          .write \
          .mode('overwrite') \
          .format(format) \
          .save(filePath, header=headerReq, compression=compressionType)
    except Exception as exp:
        logger.error("Error in the method - extract(). Please check the Stack Trace. " + str(exp), exc_info=True)
        raise
    else:
        logger.info("Extraction = extract_files() is completed...")