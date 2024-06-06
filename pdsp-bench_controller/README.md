
<h1> PDSP-Bench Controller </h1>

PDSP-Bench Controller acts a central management hub, orchestrating the benchmarking process and performance prediction across diverse workload and resource configurations.

-  It offers API endpoints for the frontend [PDSP-Bench WUI](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme) to take user input for resource provisioning on CloudLab clusters, deploying DSP system, e.g., Apache Flink on cluster, executing job on DSP systems and collecting parallel queries configuration and their performance in databases like MongoDB and SQLite DB.

## Getting Started with Web User Interface (WUI) 

1. [Prerequisite](#prerequisite)
1. [General Steps](#general)
    - [local and remote cluster environment](#local)
1. [Setup CloudLab Cluster](#setupCluster)
1. [Next steps: Setup and Start WUI](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme)

## Prerequisite<a name="prerequisite"></a>
- `Ubuntu 20.04` - we used Ubuntu 20.04 for setting up our local and remote clusters for PDSP-Bench.
- `Windows 10 or 11` - we used Windows Subsystem for Linux (wsl) for the same purpose.
- `Docker` - We support using Docker as well to install and manage dependencies.
- Controller is implemented using [Django](https://www.djangoproject.com/) framework written in Python that allows for modular and scalable development of controller.
- Python3 and pip3 installed.

## General Steps for Setting up WUI
PDSP-Bench can be run on local machine or it can be delopyed on remote machine as well.

### First time setup local or remote cluster environment<a name="local"></a>

- Go to the root folder containing manage.python

```bash
cd ~/PDSPBench/dsp_be

```
- To install dependencies such as `django`, `ansible`, `requests, `channels`, `click`, `pandas`, `paramiko`, execute requirements.txt using pip.

```bash
pip install -r requirements.txt

```

- After successful installation, you can run the controller

```bash
python manage.py runserver

```
- If you are setting up a vm or remote machine

```bash

python3 manage.py runserver 0.0.0.0:8000

```

## PDSP-Bench Controller Project Structure

PDSP-controller has the following main components

| Folder             | Functionality                                                                |
| ----------------- | ------------------------------------------------------------------ |
| dsp_be | It is the main django app with base urls in its urls.py |
| auth | Authenticates users and save their info in DB. |
| infra | Contains logic to create the clusters, providing jobs etc. |
| report | Logic to call endpoints from Flink API and send the cluster/job specific information to the Frontend |
| utils | Contains Ansible playbooks |

### Performance Monitoring using Prometheus to Collect Metrics 

We are using [Prometheus](https://prometheus.io/) for monitoring performance while query are executing on Flink. You can extend controller to monitor more performance based on your requirement. These steps are only for explanation purpose. For current performance metrics, it is already being done using CloudLab profile.

In general, the performance monitoring profile via Prometheus connection flow is as follows:

- Flink exposes metrics to Prometheus -----> Prometheus stores this data in a time-series database -----> Grafana queries this metric data from Prometheus's time-series database using PromQL.

- To connect Prometheus to Flink: you need to include these jar files in ```flink-1.16.2/lib``` : ```jna-platform-5.10.0.jar```, ```jna-5.10.0.jar```, ```oshi-core-6.1.5.jar```

- The ```flink-conf.yaml``` file, that resides at /flink-1.16.2/conf(in CloudLab node) must contain these lines
```metrics.reporter.prom.factory.class: org.apache.flink.metrics.prometheus.PrometheusReporterFactory```
```metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter```
```metrics.reporter.prom.port: 9250```

- The ```prometheus.yml``` that resides at ```/prometheus-2.42.0.linux-amd64``` in CloudLab node should have the following details about job and task managers. The jobmanager and taskmanager targets change with changing cluster nodes.


### Performance Visualization using Grafana Graphs

We are using [Grafana](https://grafana.com/) for visualizing performance in real-time. These steps are only for explanation purpose. These steps are only for explanation purpose. For current performance metrics, it is already being done using CloudLab profile. 

- To add Grafana graphs, you can plot all the metrics Flink exposes to Prometheus. Flink exposes several default metrics that can be checked at [Flink's official documentation](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/metrics/). However, to create the Grafana graphs, you would need the exact ```PromQL query``` which can be checked in the Prometheus dashboard running at locally or remote machine e.g., `http://localhost:9090` or `REMOTE_MACHINE_IP:9090`. 

- Currently in our application, Grafana is plotting graphs for four PromQL queries. They are ```flink_taskmanager_Status_JVM_CPU_Load , flink_jobmanager_Status_JVM_CPU_Load , flink_taskmanager_Status_JVM_Memory_Heap_Used , flink_taskmanager_System_Network_eno33np0_SendRate```. For other metrics such as for data analysis, learned cost models' accuracy, metrics which are not supported by Flink, we are also using `D3.js` as well.

- The connection flow is as follows: Flink exposes metrics to Prometheus -----> Prometheus stores this data in a time-series database -----> Grafana queries this metric data from Prometheus's time-series database using PromQL for eg: ```flink_taskmanager_Status_JVM_CPU_Load``` -----> Then this plotted graph from the Grafana dashboard is used as an ``iframe``to embed on our vue.js frontend.

- Let us assume, you decide to add another graph for the example metrics query ```flink_taskmanager_Status_JVM_CPU_Load_example_query_metrics``` in Grafana. You can use following steps to add metrics to Grafana for real-time visualization:
    - Navigate to the folder ```~/PDSPBench/dsp_be/infra/grafana_files/``` and open the file cluster.json. It is a JSON object and you can see there is a key called ```"panels"``` that contains a list of objects. When you expand one of the objects ```{}```, you will see the data specific to one metric graph in the front end. 
    -   To create one of your own, copy and paste the entire single ```{}``` and then change the values for the following keys ```"id"```, ```"expr"```, ```"title"```. for example: ```"id"``` can be ```5```, ```"expr"``` can be ```flink_taskmanager_Status_JVM_CPU_Load_example_query_metrics``` and ```"title"``` can be ```Test metric number 5```. 
    - At this stage, you can re-create the CloudLab experiment. 
    - You can provide a job and then look into Grafana dashboard at the URL `http://localhost:3000` or `REMOTE_MACHINE_IP:3000`, depending upon whether Grafana is running locally or remotely. 
    - Now you can navigate to each of the panels(graph windows) to select and copy the ``iframe`` which you can embed in the vue.js frontend. 
    - To embed the ``iframe`` in the vue.js app, navigate to ```~/PDSPBench/dsp_fe/src/views/dashboard/IndividualJob.vue```. 
    - Line numbers 166 to 177 already contain existing embedded iframes. just paste your copied iframe below them and then you can see the new graph in the frontend if you refresh the browser page.