# 1. Word Count

This lab consists of 3 files:
- sample.txt - A text file with some text
- word_count.py - The actual application that the spark cluster will run
- spark-job.yaml - The yaml file that you will use to deploy the application


## Get started

In the initial spark-pi test, all the files were included in the base image that you built and uploaded as part of setting up your cluster. We will now have to manage the apps by ourselves. Normally you could host these in a central repository accessible by the kubernetes cluster, but for simplicity we will upload these to your minikube cluster


Navigate to your Word Count folder
```
cd /path/to/spark-djm/1. Word Count/
```

Lets copy the files in the directory to your newly created folder
```
minikube cp word_count.py /mnt/data/word_count.py
minikube cp sample.txt /mnt/data/sample.txt
```

SSH in to your minikube cluster and verify that the files have been copied:
```
minikube ssh
cd /mnt/data
ls
```

## Let's get sparking!
Now when the Word Count app and sample text file is copied to the cluster. 
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
Feel free to update the ssmple.txt with more data and check the output. Don't forget to reupload your new version to the minikube cluster.