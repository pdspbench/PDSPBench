<h1> PDSPBench - Parallel Query Plan Generator</h1>

`pdspbench-plan-generation`is a Apache Flink client application to generate parallel query plans for performance benchmarking, training and testing data to be used by leaned components of DSP for performance prediction. These plans can be generate through both WUI and CLI as mentioned before. Here, I am describing how to CLI steps to generate workload as well.

## Getting Started with Parallel Query Generator

1. [Previous step: Setup Cluster](#setup)
1. [Description of applications](#applications)
1. [Run Arguments](#runArguments)
    - [General arguments](#generalArguments)
    - [Additional arguments](#additionalArguments)
1. [Enumeration strategy](#enumerationStrategy)
1. [Reproduce evaluations data](#reproduceEvaluationData)

## Description of Applications<a name="applications"></a> 

| **Applications**                                                                 | **Area**                                 | **Description**                                                                                                                                                                                                                                                                                                                                                 |
|----------------------------------------------------------------------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Word Count (WC)                                        | Text Processing                          | processes a text stream, tokenizes sentences into words, and counts the occurrences of each word in real-time using a key-based aggregation.                                                                                                                                                                                                                    |
| Machine Outlier (MO)                                | Network Monitoring                       | detects anomalies in machine usage data across a network by processing usage stream using _BFPRT algorithm to identify outliers based on statistical medians.                                                                                                                                                                           |
| Linear Road (LR)                                        | Traffic Management                       | processes vehicle-generated location data through four queries: _toll notification_, _accident notification_, _daily expenditure_, and _total travel time_, to calculate charges or detect incidents.                                                                                                                                                          |
| Logs Processing (LP)                         | Web Analytics                            | processes log data from HTTP Web Servers to extract insights using two main queries via the Volume Counter and Status Counter operators: one counts the number of visits within specified intervals, and the other tallies status codes.                                                                                                                         |
| Google Cloud Monitoring (GCM)                    | Cloud Infrastructure                     | analyzes cloud computing data by calculating average CPU usage over time, either grouped by job or category, with results processed through sliding windows and specific grouping operators.                                                                                                                                                                     |
| TPC-H (TPCH)                                               | E-commerce                               | processes a stream of order events to emit high-priority orders, utilizing operators to structure, filter, and calculate the occurrence sums of order priorities within specified time windows.                                                                                                                                                                 |
| Bargain Index (BI)                                           | Finance                                  | analyzes stock quote streams to identify potential bargain opportunities by calculating the price-to-volume ratio and comparing it against a specific threshold using a VWAP Calculator and Bargain Index Calculator, ultimately emitting quotes that surpass the threshold as potential bargains.                                                                 |
| Sentiment Analysis (SA)                     | Social Network                           | determines the emotional tone of tweets by assessing sentiment using the TwitterAnalyzer and SentimentClassifier operators, which apply Basic or LingPipe classifiers to score and label the tweets.                                                                                                                                                           |
| Smart Grid (SG)                                         | Sensor Network                           | analyzes smart home energy usage through two queries that calculate global and local average loads using sliding window.                                                                                                                                                                                                                                        |
| Click Analytics (CA)                                   | Web Analytics                            | analyzes user interactions with online content via two queries: first groups click events by Client ID to calculate repeat visits and total visits per URL, and the second identifies geographical origins of clicks using a Geo-IP database.                                                                                                                  |
| Spike Detection (SD)                                  | Sensor Network                           | processes sensor data streams from a production plant to detect sudden temperature spikes by calculating average temperatures over sliding windows, and identify spikes exceeding 3% of the average.                                                                                                                                                           |
| Trending Topics (TT)                      | Social Network                           | processes stream of tweets using the TwitterParser and TopicExtractor operators to identify trending topics on Twitter based on aggregated popular topics based on predefined thresholds.                                                                                                                                                                        |
| Traffic Monitoring (TM)                                         | Sensor Network                           | processes streaming vehicle data using TrafficEventParser and RoadMatcher operators to match vehicle locations to road segments then calculates the average speed per segment using the AverageSpeedCalculator.                                                                                                                                                |
| Ad Analytics (AD)                                          | Advertising                              | processes real-time data on user engagement with digital ads, using separate pipelines to parse clicks and impressions, calculate their counts within time windows, and compute the click-through rate (CTR) with a rolling CTR operator.                                                                                                                       |
| Synthetic Queries                                                                | Standard DSP Queries                     | designed to assess various workloads by managing different data streams and query structures to increase data distribution complexity. It utilizes data tuples of various types, supporting specific operations to facilitate realistic scenarios through synthetic query structures ranging from simple linear to complex multi-join configurations. Key operations include diverse filters, window aggregation and join, enhancing query complexity and data flow parallelism. |


## Setup Cluster<a name="setup"></a>

To setup a cluster and run the client follow the readme from [PDSPBench-Management Setup](https://github.com/pdspbench/PDSPBench/tree/main/pdspbench-management) for detailed setup instruction.

## Run Arguments<a name="runArguments"></a>

There are several run arguments available to e.g. define which data should be generated or which model the search heuristic should use. 
You can use them in the local setup environment as well as in the cluster environment. 
In the following, they are explained.

#### General Arguments<a name="generalArguments"></a>

- `logdir`: Specify where the graph- and label files get stored. The directory is required to exist. 
- `environment`: Defines in which environment PlanGeneratorFlink is running. Can be `kubernetes` for remote cluster execution, `localCluster` for local cluster execution (i.e. started by `setupPlanGeneratorFlink.sh` -> `5) Run local cluster`) or `localCommandLine` (i.e. having a local cluster setup and running PlanGeneratorFlink from the command line like calling `./bin/flink run`)
- `mode`: Defines what training/testing data should be generated. Enter one or multiple out of: `train`, `test`, `randomspikedetection`, `filespikedetection`, `smartgrid` or `advertisement`.
- `numTopos`: Defines how much queries should run per type. For training, a `numTopos` value of 3 would mean you get 3 query runs of template1, 3 of template2 and 3 of template3. For other modes it can be a little bit different. Look up `createAllQueries()` in `AbstractQueryBuilder.java` for insights.

#### Additional Arguments<a name="additionalArguments"></a>

- `debugMode`: In debugMode several things are firmly defined (i.e. seed for randomness or max count of generated source records). Sometimes helpful in the development process.
- `duration`: Duration per query in ms - including warm up time. Can be necessary to adapt for large cluster queries because resource creation can take some time. 
- `UseAllOps`: Only relevant for synthetic training data generation (-> mode = train). With this option it is assured, that every possible operator is used and its not random if a filter operator is placed or not. 
- `interceptor`: Defines if and what experiment interceptor should be used. Currently only `eventrate` is available. An interceptor changes query parameter during the data generation. 
- `interceptorStart`: Needs `interceptor` to be set. Defines the starting point of the intercepted query parameter. 
- `interceptorStep`: Needs `interceptor` to be set. Defines the step size of the intercepted query parameter. 
- `sourceParallelism`: With this option you can define the parallelism of the source operators manually. 
- `minParallelism`: Minimum Parallelism to be used. Default: 1
- `maxParallelism`: Maximum Parallelism to be used. Default: Determine max. parallelism automatically (only available on kubernetes cluster)
- `deterministic`: With this option activated, it is secured that no randomness in the query generation is used and instead predefined parameters will define the query. You can define them in `Constants.java`. This option is only available for synthetic training data generation (-> mode = train).
- `templates`: Determines which templates should be executed (Format: "--templates template1,template3" (no space between)). Only usable with synthetic training and testing templates (mode = train and mode = test). 

<hr>

### Enumeration Strategy<a name="enumerationStrategy"></a>
`enumerationStrategy`: Defines the enumeration strategy to be used. Can be `RANDOM`, `EXHAUSTIV`, `RULEBASED`, `MINAVGMAX`, `INCREASING` or `PARAMETERBASED`. 
The following runtime parameters are intended for specific enumeration strategies:
- `parallelism`: Parallelism to be used in combination with `PARAMETERBASED` enumeration strategy.
- `exhaustiveParallelismStepSize`: Parallelism step size to be used in combination with `EXHAUSTIV` enumeration strategy. Default: 1. A value of e.g. 5 would mean, that you would have the parallelisms 1, 5, 10, 15, 20, 25, 30 and so on as possible values.
- `increasingStepSize`: Set the step size to define how much the parallelism should be increased, only in combination with `INCREASING` enumeration strategy. 

#### Concept of Enumeration Strategies

- `RANDOM`
The random enumeration strategy randomly chooses a parallelism from the given inclusive boundaries i.e. available maximum number of cores in physical node. The random enumeration strategy is also used as the default strategy in Plan Generator Flink.

- `RULEBASED`
Unlike random enumeration strategy, the rule-based enumeration strategy uses the charactereistics of workload (query and workload) and physical resources such incoming event rate and operator selectivity, outgoing rate, number of cores to enumerate parallelism of upstream and downstream operators.

- `EXHAUSTIV`
The exhaustive enumeration strategy should apply every unique parallelism degree combination possible. No combination occur twice. But unfortunately the strategy is not applicable for all queries, as the number of possible combinations increases very fast with more operators or parallelism degrees. This results in enormous amount of queries necessary to fulfill a full coverage of all possible combinations.

- `MINAVGMAX`
The MinAvgMax enumeration strategy taskes the approach of generating alternately queries with the minimum, the average and the maximum number of parallelism degree.

- `INCREASING`
The increasing enumeration strategy is a simple strategy useful for creating evaluations of the influence on parallelism degrees. It starts with the minimum parallelism degree and increases the parallelism degree of each operator by one until the maximum is reached. Use the runtime parameter `increasingStepSize` to define the step size. 

- `PARAMETERBASED`
For fast testing or execution of evaluations with a constant parallelism degree, the parameter based enumeration strategy is suitable, which allows to configure the parallelism degree of all operators except the source and sink operators. Use the runtime parameter `parallelism` to define the parallelism.

<hr>

## Reproduce Evaluations Data<a name="reproduceEvaluationData"></a>
The steps to reproduce an evaluation end-to-end are explained in [PDSPBench-Management readme](https://github.com/anonymoussigmod24/dsps/blob/main/pdspbench-management/README.md). In PDSPBench, we have used various training and testing range for data generation and inference to evaluate model performance. Here, we mentioned some example to vary different parameters to generate data from `pdspbench-plan-generation`.

### Training Data Generation

**Random enumeration strategy, linear query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --templates template1`

**Random enumeration strategy, 2-way join query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --templates template2`

**Random enumeration strategy, 3-way join query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --templates template3`

**Rule-Based enumeration strategy, linear query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --enumerationStrategy RULEBASED --templates template1`

**Rule-Based enumeration strategy, 2-way join query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --enumerationStrategy RULEBASED --templates template2`

**Rule-Based enumeration strategy, 3-way join query structure**  
`--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000 --enumerationStrategy RULEBASED --templates template3`
  
### Testing Data Generation

 **Cluster Sizes**  
 `--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3000`

 **Event Rates**  
 `--mode test --logdir ~/pgf-results --environment kubernetes --numTopos 50 --templates testB`

 **Window Durations**  
 `--mode test --logdir ~/pgf-results --environment kubernetes --numTopos 100 --templates testC`

 **Window Lengths**  
 `--mode test --logdir ~/pgf-results --environment kubernetes --numTopos 100 --templates testD`

 **Tuple Widths**  
 `--mode test --logdir ~/pgf-results --environment kubernetes --numTopos 100 --templates testA`

 **Unseen Synthetic Test Queries**  
 `--mode test --logdir ~/pgf-results --environment kubernetes --numTopos 600 --templates testE`

 **Benchmark: Advertisement**  
 `--mode advertisement --logdir ~/pgf-results --environment kubernetes --numTopos 7000`

 **Benchmark: Random Spike Detection**  
 `--mode randomspikedetection --logdir ~/pgf-results --environment kubernetes --numTopos 7000`

 **Benchmark: File Spike Detection**  
 `--mode filespikedetection --logdir ~/pgf-results --environment kubernetes --numTopos 3200`

 **Benchmark: Smartgrid**  
 `--mode smartgrid --logdir ~/pgf-results --environment kubernetes --numTopos 3200`

 **Unseen Hardware**  
 `--mode train --logdir ~/pgf-results --environment kubernetes --numTopos 1500`

<hr>