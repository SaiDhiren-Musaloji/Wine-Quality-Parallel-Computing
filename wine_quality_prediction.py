import argparse
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import col
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Wine Quality Prediction Model Evaluation')
parser.add_argument('input_file', type=str, help='Path to the input CSV dataset file')
args = parser.parse_args()



# Initialize the Spark session
spark_session = SparkSession.builder \
    .appName("WineQualityModelEvaluation") \
    .config("spark.hadoop.fs.s3a.access.key", "ASIAWFYUHIX5NRETFDVT") \
    .config("spark.hadoop.fs.s3a.secret.key", "ykYm64huUZrIXbSsPft/VPPQSaRA9e50lYzTT/zI") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.maximum", "100") \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .getOrCreate()

# Load the dataset from S3
dataframe = (spark_session.read
    .option("header", "true")
    .csv("s3a://wine-quality-dhiren/ValidationDataset.csv"))

# Show a sample of the data
dataframe.show()


spark_ctx = spark_session.sparkContext
spark_ctx.setLogLevel('ERROR')

# Configure Hadoop to use S3A for accessing S3
spark_ctx._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# Read input file path from command line argument
input_file = args.input_file

# Define the model directory path in S3
model_directory = "s3a://wine-quality-dhiren/model"

# Load the dataset
dataframe = (spark_session.read
                .format("csv")
                .option('header', 'true')
                .option("sep", ";")
                .option("inferschema", 'true')
                .load(input_file))

# Debugging print to check columns in the dataframe
print(f"Columns in the input data: {dataframe.columns}")

# Cast all columns to double (remove any unwanted quotes or characters)
dataframe = dataframe.select(*(col(c).cast("double").alias(c.strip("\"")) for c in dataframe.columns))

# Load the trained model from S3
trained_model = PipelineModel.load(model_directory)

# Make predictions on the input data
prediction_results = trained_model.transform(dataframe)

# Select 'prediction' and 'label' columns for evaluation
prediction_data = prediction_results.select(['prediction', 'label'])

# Evaluate model accuracy
accuracy_calculator = MulticlassClassificationEvaluator(labelCol='label', predictionCol='prediction', metricName='accuracy')
accuracy_value = accuracy_calculator.evaluate(prediction_results)
print(f'Accuracy on Test Data: {round(accuracy_value, 2)}')

# Evaluate F1 score
evaluation_metrics = MulticlassMetrics(prediction_data.rdd.map(tuple))
f1_score = evaluation_metrics.weightedFMeasure()
print(f'F1 Score of Wine Quality Prediction: {f1_score}')

# Stop the Spark session
spark_session.stop()
