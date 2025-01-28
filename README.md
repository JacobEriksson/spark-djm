# Apache Spark & DJM - Lab
Lab to demonstrate Apache Spark functionaltiy and how Datadog can add observabiltiy and provide detailed monitoring capabilities

Docs:
- [Apache Spark & DJM Slides](https://docs.google.com/presentation/d/1K4ff2QDKr0cXvO8KW0z-qk_LNa8SI-gfwAYPPjXmpV8/edit?usp=sharing)
- [Apache Spark](https://spark.apache.org/)
- [Data Jobs Monitoring](https://docs.datadoghq.com/data_jobs/)
- [Setup for Spark on Kubernetes](https://docs.datadoghq.com/data_jobs/kubernetes/?tab=datadogoperator)

## Pre-reqs
- minikube
- Code Editor
- Sparkpy
- Helm
- apache-spark
- python
- openjdk@11
- docker

Optional: [homebrew](https://docs.brew.sh/)


## Instructions using homebrew
1. Install Homebrew
2. (Optional) Add homebrew to $PATH:
   ```
   echo >> /Users/dusan.okanovic/.zprofile
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/dusan.okanovic/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```
3. Install necessary packages using Homebrew


In terminal, use brew & pip to install necessary packages and libraries.

Example (assuming only python & code editor is already in place):
```
brew install minikube helm apache-spark openjdk@11
pip3 install pyspark

```

## Set up your minikube cluster

Give your minikube cluster enough resources to run apache-spark, this will delete your old cluster (make a back-up if necessary)
```
minikube delete
minikube start --cpus=4 --memory=6144

```

Validate your config during startup:
```
🔥  Creating docker container (CPUs=4, Memory=6144MB) ...
🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
```

Check status:
```
kubectl cluster-info
```

## Prepare Cluster with necessary Operators

Install Spark Operator using Helm.

In terminal:
```
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --set webhook.enable=true
```



## Build & upload your Spark image

In your terminal, go to your homebrew directory where you installed apache-spark
```
cd /opt/homebrew/Cellar/apache-spark/3.5.4
```

Run the following config to build your spark image
```
./bin/docker-image-tool.sh -t my-apache-spark-kb8 build
```

Upload your image to your minikube cluster
```
minikube image load spark:my-apache-spark-kb8
```

# Let's test Spark!
Let's try one of the built in example apps.

There are 2 different yaml files in the base directory:
- spark-pi-python.yaml
- spark-pi.yaml

Both are running the same type of application, but one is using Python the other Scala. But both are fully working..

```
kubectl apply -f /path/to/spark-pi.yaml
```

Double check that a spark-driver starts and succesfully completes
```
kubectl get pods
```

When the container is marked "Completed" check the spark driver log files for results
```
kubectl logs spark-pi-driver
```

You should find "Pi is roughly 3.14149491828299".

## Deploy Datadog Agent

Install the Datadog Operator by running the following command:
```
helm repo add datadog https://helm.datadoghq.com
helm install my-datadog-operator datadog/datadog-operator
```

Create a K8s Secret to store your DD API Key.
Replace <DATADOG_API_KEY> with your Datadog API key.
Replace <DATADOG_APP_KEY> with your Datadog app key.

```
kubectl create secret generic datadog-secret --from-literal api-key=<DATADOG_API_KEY> --from-literal app-key=<DATADOG_APP_KEY>
```

Create a datadog-agent.yaml or reuse the file found in folder DD Agent Config.
Example DD Operator config:
```
kind: DatadogAgent
apiVersion: datadoghq.com/v2alpha1
metadata:
  name: datadog
spec:
  features:
    apm:
      enabled: true
      hostPortConfig:
        enabled: true
        hostPort: 8126
    admissionController:
      enabled: true
      mutateUnlabelled: false
  global:
    site: <DATADOG_SITE>
    credentials:
      apiSecret:
        secretName: datadog-secret
        keyName: api-key
      appSecret:
        secretName: datadog-secret
        keyName: app-key
  override:
    nodeAgent:
      image:
        tag: <DATADOG_AGENT_VERSION>
```

Deploy the config file:
```
kubectl apply -f /path/to/your/datadog-agent.yaml
```

# Let's get started!

There are 4 different Spark Jobs available, from simple to more advanced.
1. Word Count - Count and group words
2. Sales Data Analaýsis - Analyse Sales Data
3. Customer Segmentation - Leverage K-Means and MLlib to analyse customer data
4. Streaming Jobs - Automatic order creation and streaming job analysis

Recommendation is to start simple and gradually move to more advanced.

