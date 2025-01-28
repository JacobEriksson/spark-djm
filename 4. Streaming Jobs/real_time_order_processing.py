from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, sum, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Initialize SparkSession
spark = SparkSession.builder.appName("RealTimeOrderProcessing").getOrCreate()

# Define schema for JSON orders
data_schema = StructType([
    StructField("orderId", StringType(), True),
    StructField("customerId", StringType(), True),
    StructField("amount", IntegerType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Read real-time data from JSON file
orders_df = spark.readStream.format("json") \
    .schema(data_schema) \
    .load("/mnt/data/orders")

# Load product catalog
products = spark.read.csv("/mnt/data/products.csv", header=True, inferSchema=True)

# Transformation logic: Calculate total sales per category
orders_with_products = orders_df.join(products, orders_df.orderId == products.productId, "left")
total_sales = orders_with_products.withWatermark("timestamp", "30 seconds") \
    .groupBy(window(col("timestamp"), "30 seconds"), col("category"), col("price")) \
    .agg(sum("amount").alias("totalSales"),
        expr("sum(amount * price)").alias("totalValue"))

# Define the output file path
output_path = "/mnt/data/processed_results"

# Output the results to the console
#query = total_sales.writeStream.outputMode("update").format("console").start()

# Write the results to a text file
query = total_sales.writeStream.outputMode("append") \
    .format("json") \
    .option("path", output_path) \
    .option("checkpointLocation", "/mnt/data/checkpoint") \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()