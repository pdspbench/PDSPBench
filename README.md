<h1 align="center">
  <img src="reference_images/pdspbench_logo-1.png" alt="PDSP-Bench Logo" width="300"/>
  <br>Welcome to PDSP-Bench - Code and Documentation
</h1>

PDSP-Bench, a novel benchmarking system specifically designed for benchmarking parallel and distributed stream processing on heterogeneous hardware configurations.

<h3>Dedicated Repository for Paper Submission:</h3>

This repository is created to support our paper submission titled **PDSP-Bench: A Benchmarking System for Parallel and Distributed Stream Processing**, showcasing the capabilities of PDSP-Bench.

<h3> Exploring PDSP-Bench's Key Components:</h3>

- [pdsp-bench_Cloud_setup:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_Cloud_setup#readme) The main instructions to setup CloudLab environment for benchmarking using PDSP-Bench. It provides scripts to install dependecies and setup CloudLab resources for performance benchmarking.

- [pdsp-bench_controller:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_controller#readme) Controller is the backend of PDSP-Bench benchmarking system. It offers API endpoints to communicate with *pdsp-bench_wui* and automate various tasks like creating the cluster, providing jobs to Flink, saving the cluster and user information on sqlite DB.


- [pdsp-bench_workload_generator:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_workload_generator#readme) Apache flink client application which functions as an essential tool for generating workload and parallel query plans related to synthetic and real-world benchmark applicaitons. These plans are vital for the benchmarking performance and performance forecasting using training and testing of learned cost models.


- [pdsp-bench_wui:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme) Web user interface of PDSP-Bench system to enable communication with *controller* take user input for resource provisioning on CloudLab, workload generation and performance analysis and visualization.


- [pdsp-bench_ml_models:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_ml_models#readme) Main component of ML manager consisting of various learned component of DSP such as cost models to provide accurate inference cost predictions for various workload and resource configurations in parallel and distributed processing environment. 


- [pdsp-bench_experiment_data](https://github.com/pdspbench/pdsp-bench_experiment_data) Selected set of sample data of real-world and synthetic application collected for parallel query plans during performance benchmarking. 


## PDSP-Bench Description
PDSP-Bench allows to benchmarkk Distributed Stream Processing (DSP) systems. It offers to deploy choice of DSP systems such as SUT e.g., Apache Flink which can be benchmarked using 14 real-world and 9 synthetic applications.  By interacting to the `web user interface` ([pdsp-bench_wui:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme)), you can execute different paralle query plans (PQP) related to these real-world and synthetic applications under varying workload such as data stream and query parameters and resource configurations. After query execution, you can visualize the performance of each query in real-time such as end to end latency, throughput, resource utilization  or visualize historical performance data of different query execution to compare performances. In addition, PDSP-Bench offers to collect these data to be used by for training learned component of DSP systems. [pdsp-bench_ml_models:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_ml_models#readme) offers performance or cost prediction using different learned cost models which were training on data collected from PDSP-Bench.

## Overview of Step-wise Operations in PDSP-Bench
1. Create `CloudLab` account and setup cluster in `CloudLab` using [pdsp-bench_Cloud_setup](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_Cloud_setup#readme).
1. Make sure clone `PDSPBench` in your home folder or Create a folder `PDSPBench` in your home folder directory unzip downloaded files and copy subfoloder in `PDSPBench` e.g., `~\PDSPBench\dsp_be`
1. Setup and Start [pdsp-bench_controller](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_controller#readme)
1. Setup and Start [pdsp-bench_wui](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme)
1. In frontend, go to `Explore Node` tab put `hostname` from all `CloudLab` nodes in the frontend.
1. Go to `Create Cluster` tab and Create distributed environment by creating and deploying Apache Flink on cluster nodes. You can decided how many node you need for Flink while creating clusters.
1. After successful deployment of Flink and running cluster, you can select cluster and execute query specific real-world or synthetic applications by defing query specific parameters like, event rate, parallelism, execution time, number of iteration, as well as enumeration strategy.
1. During the execution, you can visualize the real-time performance or
1. Wait for the job to run for the specified duration then anaylze and visualize the historical performance metrics of different query from same or different applications. 
1. Query execution specific configurations and metrics is collected automatically and dowloaded as JSON files and graph representation after the job has run for the specified time. These details are also stored in MongoDB and SQLite database.
1. These benchmark data can be collected to be used to train performance cost mode. We provide different trained learned cost models in [pdsp-bench_ml_models:](https://github.com/pdspbench/PDSPBench/tree/master/infer) for performance prediction.
1. [pdsp-bench_ml_models:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_ml_models#readme) can be used to predict performance and compare the performance accuracy of different learned cost models in `Learned Model` tab.

> Note: Detailed steps about each component of PDSP-Bench is provided in their respective README.md files.