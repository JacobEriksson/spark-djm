from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# Initialize SparkSession
spark = SparkSession.builder.appName("CustomerSegmentation").getOrCreate()

# Load datasets
customers = spark.read.csv("/mnt/data/customers.csv", header=True, inferSchema=True)
purchases = spark.read.csv("/mnt/data/purchases.csv", header=True, inferSchema=True)

# Calculate total spending per customer
total_spending = purchases.groupBy("customerId").sum("amount").withColumnRenamed("sum(amount)", "totalSpend")

# Join datasets
customer_data = customers.join(total_spending, "customerId")

# Prepare data for clustering
assembler = VectorAssembler(inputCols=["age", "totalSpend"], outputCol="features")
final_data = assembler.transform(customer_data)

# Apply KMeans clustering
kmeans = KMeans(k=3, seed=1)
model = kmeans.fit(final_data)
transformed = model.transform(final_data)

# Display results
transformed.select("customerId", "age", "totalSpend", "prediction").show()

result = transformed.select("customerId", "age", "totalSpend", "prediction")

print (result)

# Stop SparkSession
spark.stop()