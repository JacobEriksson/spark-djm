# 4. Streaming Spark Jobs 

This lab consists of 4 files:
- order_generator.py - Python script that generate json files that represents orders
- real_time_order_processing.py - The actual application that the spark cluster will run
- products.csv - A record of products available
- spark-job.yaml - The yaml file that you will use to deploy the application


## Get started

In this lab we will explore a more advanced scenario where have a script (order_generator.py) generating orders that will be picked up and analysed by Apache Spark. This requires the app to constantly check for new order files, in addition to that we will also write the output to a new file instead of using the logs or console. This would enable another pipeline, message queue or application to pick up the output for further processing. 

This lab will require you to create a few folders and change the access rights so spark can write data to them.

Navigate to the correct folder
```
cd /path/to/spark-djm/4. Streaming Jobs/
```

Lets copy the files in the directory to your newly created folder
```
minikube cp order_generator.py /mnt/data/order_generator.py
minikube cp products.csv /mnt/data/products.csv
minikube cp real_time_order_processing.py /mnt/data/real_time_order_processing.py
```

SSH in to your minikube cluster and verify that the files have been copied:
```
minikube ssh
cd /mnt/data
ls
```

While still being logged in, create new folders that will be used for order generation, output data and checkpoint (used by spark).

Start from /mnt/data:
```
sudo mkdir orders
sudo mkdir processed_results
sudo mkdir checkpoint
sudo chmod -R 777 /mnt/data/orders
sudo chmod -R 777 /mnt/data/processed_results
sudo chmod -R 777 /mnt/data/checkpoint
```

Now we should be ready to start generating orders and our spark jobs.

## Let's get sparking!

First, we will have to start our order generation script, while connected to your minikube cluster run the order_generation.py script:
```
minikube ssh
cd /mnt/data
python3 order_generator.py
```

Let this terminal continue to run, open up a new tab in your terminal or a new window and navigate to the /mnt/data/orders to verify that json files are being created.

Let's try to run the spark-job, deploy it using the spark-job.yaml

```
kubectl apply -f /path/to/spark-job.yaml
```

Using the same window/tab that you used for checking new orders, navigate to the processed_results folder and check for new files. This might take a few minutes before new files are being generated.
