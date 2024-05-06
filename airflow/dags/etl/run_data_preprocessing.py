import logging.config
import logging
import get_all_variables as gav
from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.sql.functions import col
from pyspark.ml.functions import vector_to_array
from pyspark.ml import Pipeline, Transformer
from pyspark import keyword_only
from pyspark.ml.param.shared import HasInputCol, HasOutputCol  # Param, Params
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable

logging.config.fileConfig(fname=gav.logging_conf_path)
logger = logging.getLogger(__name__)


class OneHotColumnar(Transformer,  # Base Class
                     HasInputCol,  # Sets up an inputCol parameter
                     HasOutputCol,  # Sets up an outputCol parameter
                     DefaultParamsReadable,  # Makes parameters readable from file
                     DefaultParamsWritable  # Makes parameters writable from file
                     ):
    """
    A custom Transformer which convert each one hot encoder vector to columns.
    """

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None):
        super().__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setInputCol(self, new_inputCol):
        return self.setParams(inputCol=new_inputCol)

    def setOutputCol(self, new_outputCol):
        return self.setParams(outputCol=new_outputCol)

    def _transform(self, df):
        # Set the input and output and columns of table
        input_column = self.getInputCol()
        output_column = self.getOutputCol()
        columns = df.columns
        columns.remove(input_column)

        df = df.withColumn(output_column, vector_to_array(input_column))
        array_size = len(df.first()[output_column])
        df = df.select(columns + [col(output_column)[i] for i in range(array_size)])

        return df


def data_preprocessing(df):
    try:
        logger.info(f"data_preprocessing() is started for the dataframe...")
        df = df.dropna()
        stages = []
        # Indexing categorical features
        string_indexer = StringIndexer(inputCol="TRANSACTIONTYPE", outputCol="TRANSACTIONTYPE_indexed",
                                       stringOrderType="frequencyDesc")
        ohe = OneHotEncoder(inputCol="TRANSACTIONTYPE_indexed", outputCol="TRANSACTIONTYPE_one_hot")
        ohc = OneHotColumnar(inputCol="TRANSACTIONTYPE_one_hot", outputCol="TRANSACTIONTYPE_Final")

        stages.append(string_indexer)
        stages.append(ohe)
        stages.append(ohc)

        pipeline = Pipeline(stages=stages)
        model = pipeline.fit(df)
        df = model.transform(df)
    except Exception as exp:
        logger.error("Error in the method - data_preprocessing(). Please check the Stack Trace. " + str(exp))
        raise
    else:
        logger.info("data_preprocessing() is completed...")
    return df

