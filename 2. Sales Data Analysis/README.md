# 2. Sales Data Analysis

This lab consists of 3 files:
- sales_analysis.csv - A record of previous orders
- sales_analysis.py - The actual application that the spark cluster will run
- spark-job.yaml - The yaml file that you will use to deploy the application


## Get started

Similar to previous lab (Word Count) we will need to upload the files to our minikube cluster. These could be hosted in an S3 Bucket or similar, but for simplicity and cost we will continue to use the minikube cluster.


Navigate to your Word Count folder
```
cd /path/to/spark-djm/2. Sales Data Analysis/
```

Lets copy the files in the directory to your newly created folder
```
minikube cp sales_analysis.py /mnt/data/sales_analysis.py
minikube cp sales_analysis.csv /mnt/data/sales_analysis.csv
```

SSH in to your minikube cluster and verify that the files have been copied:
```
minikube ssh
cd /mnt/data
ls
```

## Let's get sparking!
Let's try to run the application, deploy it using the spark-job.yaml

```
kubectl apply -f /path/to/spark-job.yaml
```

Check logs for output!


## Let us add Datadog Observability!
Check the spark-job.yaml, some lines of code are commented out.
Remove the "#" and rerun the job..

PS. you might have to delete it before applying it again.
```
kubectl delete -f spark-job.yaml
kubectl apply -f spark-job.yaml
```

## Add more data to analyse
Feel free to update the sales_analysis.csv with more data and check the output. Don't forget to reupload your new version to the minikube cluster.