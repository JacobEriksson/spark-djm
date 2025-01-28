from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("SalesAnalysis").getOrCreate()

# Load sales data
sales_df = spark.read.csv("file:///mnt/data/sales_analysis.csv", header=True, inferSchema=True)

# Calculate total revenue and items sold per product
results_df = sales_df.withColumn("revenue", sales_df["quantity"] * sales_df["price"]) \
                     .groupBy("productName") \
                     .agg({"revenue": "sum", "quantity": "sum"}) \
                     .withColumnRenamed("sum(revenue)", "total_revenue") \
                     .withColumnRenamed("sum(quantity)", "total_quantity")

# Show the results
results_df.show()

print (results_df)