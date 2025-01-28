from pyspark import SparkContext

# Initialize Spark context
sc = SparkContext(appName="WordCount")

# Read the text file into an RDD
text_file = sc.textFile("file:///mnt/data/sample.txt")

# Split the lines into words and count occurrences
counts = text_file.flatMap(lambda line: line.split(" ")) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a + b)

# Collect and print the result
results = counts.collect()
for word, count in results:
    print(f"{word}: {count}")
