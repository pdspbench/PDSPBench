<h1> PDSPBench - Parallel Query Plan Generator (Real-world) </h1>

PDSP-Bench workload generator offers to generate parallel query plans for 14 real-world applications and 9 synthetic applications. We are describing 

## Description of Applications 

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


### General Arguments for Real-world Applications

To execute this query you need the following parameters:
  - ```--parallelism```: The parallelism level
  - ```--mode```: Takes two values, either 'file' or 'kafka'. Depicts the source and input type. For 'file' the lines of the text file will be read, processed and the results will be written in a file. Otherwise, for 'kafka' the data arriving in a Kafka topic will be used as the input stream and after it has been processed, the results will be written in another Kafka topic.
  - ```--input```: Depicts the input file (in the case when 'mode'=='file') or the Kafka topic that will be used as input (in the case when 'mode'=='kafka').
  - ```--output```: Depicts the output folder (in the case when 'mode'=='file') or the Kafka topic that will be used as output (in the case when 'mode'=='kafka').
  - ```--kafka-server```: Depicts the address of the Kafka instance in the case when 'mode'=='kafka'. This parameter is not necessary if 'mode'=='file'.
  - ```--numTopos```: Defines how much queries should run per type.
  - ```--lateness```: This query uses event sliding window, the time, in seconds, that the query will wait for results coming out of order is needed. 

  A sample command to start this query is the following:
  ```
  ./bin/flink run -c WordCount.WordCount <path to the compiled Jar file of this application> --parallelism 2 --mode kafka --input inputTopic --output outputTopic --kafka-server localhost:9092 -- enumerationStrategy --random --numTopos 3000
  ```

 A sample command to start the first query of SmartGrid with a sliding window size of 5 seconds, window slide of 1 second and lateness of 10 seconds is the following:
  ```
  ./bin/flink run -c SmartGrid.SmartGrid <path to the compiled Jar file of this application> --parallelism 2 --mode kafka --input inputTopic --output outputTopic --kafka-server localhost:9092 --query 1 --size 5 --slide 1 --lateness 10 -- enumerationStrategy --random --numTopos 3000
  ```
  Another example Command
  ```
  ./bin/flink run -c com.kom.dsp.smartgrid.SmartGridJob /home/legion/Desktop/park/dsp_jobs/target/dsp_jobs-1.0-SNAPSHOT.jar -parallelism [1] -size 100 -slide 1 -mode kafka -input SmartGridIn -output SmartGridOut -query 1 -kafka-server localhost:9092 -- enumerationStrategy --random --numTopos 3000
  ```

### General Arguments Synthetic Query Applications

  The SyntheticQueryGenerator consists of 9 templates. Sample example for arguments to be passed in queries:
  
  #### First template
  The following parameters are required to run a query of the first template:
  - ```--template```: Defines the template that will be used. Takes one of the following values 'template_1', 'template_2' or 'template_3'. For the first template it must be 'template_1'.
  - ```--firstFilter```: Is a boolean defining if the first filter should be applied or not.
  - ```--groupBy```: Is a boolean defining if a groupBy operator should be applied or not.
  - ```--secondFilter```: Is a boolean defining if the second filter should be applied or not.
  - ```--windowType```: Defines the window type to be used. Takes one of the following values 'duration' or 'count'.
  - ```--windowSize```: Defines the size of the window. If 'windowType'=='duration' then the window size is given in seconds.
  - ```--windowSlide```: Defines the slide of the window. If 'windowType'=='duration' then the window slide is given in seconds.
  - ```--integerRange```: Defines the maximal number of integers in the data tuple. It randomly chooses the number of integers between 1 and 'integerRange' (inclusive).
  - ```--doubleRange```: Defines the maximal number of doubles in the data tuple. It randomly chooses the number of doubles between 1 and 'doubleRange' (inclusive).
  - ```--stringRange```: Defines the maximal number of strings in the data tuple. It randomly chooses the number of strings between 1 and 'stringRange' (inclusive).
  - ```--eventRate```: The rate (events/s) at which the data tuples are produced.
  - ```--queryDuration```: Defines the run time of the query (in seconds). After that time has passed, the job is cancelled on Flink. Provide the value '-1' if you want the query to run indefinitely.
  - ```--operatorChaining```: Is a boolean enabling (true) or disabling (false) the operator chaining during the execution in Flink.
  - ```--parallelism```: The parallelism level
  - ```enumerationStrategy```: Defines the enumeration strategy to be used. Can be `RANDOM`, `EXHAUSTIV`, `RULEBASED`, `MINAVGMAX`, `INCREASING` or `PARAMETERBASED`. 

  A sample command to start a query of the first template is the following:
  ```
  ./bin/flink run -c SyntheticQueryGenerator.SyntheticDataGenerator <path to the compiled Jar file of this application> --template template_1 --firstFilter true --groupBy true --secondFilter true --windowType count --windowSize 7 --windowSlide 3 --integerRange 2 --doubleRange 5 --stringRange 7 --eventRate 20 --queryDuration -1 --operatorChaining true --parallelism 2 -- enumerationStrategy --random
  ```

  #### Second template
  The following parameters are required to run a query of the second template:
  - ```--template```: Defines the template that will be used. Takes one of the following values 'template_1', 'template_2' or 'template_3'. For the second template it must be 'template_2'.
  - ```--firstFilterFirstStream```: Is a boolean defining if the first filter should be applied in the first stream or not.
  - ```--firstFilterSecondStream```: Is a boolean defining if the first filter should be applied in the second stream or not.
  - ```--groupBy```: Is a boolean defining if a groupBy operator should be applied or not.
  - ```--joinWindowSize```: Defines the size of the joining window.
  - ```--joinWindowSlide```: Defines the slide of the joining window.
  - ```--secondFilter```: Is a boolean defining if the second filter should be applied or not.
  - ```--integerRangeFirstStream```: Defines the maximal number of integers in the data tuple of the first stream. It randomly chooses the number of integers between 1 and 'integerRangeFirstStream' (inclusive).
  - ```--doubleRangeFirstStream```: Defines the maximal number of doubles in the data tuple of the first stream. It randomly chooses the number of doubles between 1 and 'doubleRangeFirstStream' (inclusive).
  - ```--stringRangeFirstStream```: Defines the maximal number of strings in the data tuple of the first stream. It randomly chooses the number of strings between 1 and 'stringRangeFirstStream' (inclusive).
  - ```--integerRangeSecondStream```: Defines the maximal number of integers in the data tuple of the second stream. It randomly chooses the number of integers between 1 and 'integerRangeSecondStream' (inclusive).
  - ```--doubleRangeSecondStream```: Defines the maximal number of doubles in the data tuple of the second stream. It randomly chooses the number of doubles between 1 and 'doubleRangeSecondStream' (inclusive).
  - ```--stringRangeSecondStream```: Defines the maximal number of strings in the data tuple of the second stream. It randomly chooses the number of strings between 1 and 'stringRangeSecondStream' (inclusive).
  - ```--eventRateFirstStream```: The rate (events/s) at which the data tuples of the first stream are produced.
  - ```--eventRateSecondStream```: The rate (events/s) at which the data tuples of the second stream are produced.
  - ```--queryDuration```: Defines the run time of the query (in seconds). After that time has passed, the job is cancelled on Flink. Provide the value '-1' if you want the query to run indefinitely.
  - ```--operatorChaining```: Is a boolean enabling (true) or disabling (false) the operator chaining during the execution in Flink.
  - ```--parallelism```: The parallelism level
  - ```enumerationStrategy```: Defines the enumeration strategy to be used. Can be `RANDOM`, `EXHAUSTIV`, `RULEBASED`, `MINAVGMAX`, `INCREASING` or `PARAMETERBASED`. 

  A sample command to start a query of the second template is the following:
  ```
  ./bin/flink run -c SyntheticQueryGenerator.SyntheticDataGenerator <path to the compiled Jar file of this application> --template template_2 --firstFilterFirstStream true --firstFilterSecondStream true --groupBy true --joinWindowSize 7 --joinWindowSlide 3 --secondFilter true --integerRangeFirstStream 2 --doubleRangeFirstStream 5 --stringRangeFirstStream 7 --integerRangeSecondStream 5 --doubleRangeSecondStream 6 --stringRangeSecondStream 3 --eventRateFirstStream 30 --eventRateSecondStream 200 --queryDuration 120 --operatorChaining true --parallelism 2 -- enumerationStrategy --random

  ```

#### Third template
  The following parameters are required to run a query of the third template:
  - ```--template```: Defines the template that will be used. Takes one of the following values 'template_1', 'template_2' or 'template_3'. For the third template it must be 'template_3'.
  - ```--firstFilterFirstStream```: Is a boolean defining if the first filter should be applied in the first stream or not.
  - ```--firstFilterSecondStream```: Is a boolean defining if the first filter should be applied in the second stream or not.
  - ```--firstFilterThirdStream```: Is a boolean defining if the first filter should be applied in the third stream or not.
  - ```--groupBy```: Is a boolean defining if a groupBy operator should be applied or not.
  - ```--joinWindowSize```: Defines the size of the joining window.
  - ```--joinWindowSlide```: Defines the slide of the joining window.
  - ```--secondFilter```: Is a boolean defining if the second filter should be applied or not.
  - ```--integerRangeFirstStream```: Defines the maximal number of integers in the data tuple of the first stream. It randomly chooses the number of integers between 1 and 'integerRangeFirstStream' (inclusive).
  - ```--doubleRangeFirstStream```: Defines the maximal number of doubles in the data tuple of the first stream. It randomly chooses the number of doubles between 1 and 'doubleRangeFirstStream' (inclusive).
  - ```--stringRangeFirstStream```: Defines the maximal number of strings in the data tuple of the first stream. It randomly chooses the number of strings between 1 and 'stringRangeFirstStream' (inclusive).
  - ```--integerRangeSecondStream```: Defines the maximal number of integers in the data tuple of the second stream. It randomly chooses the number of integers between 1 and 'integerRangeSecondStream' (inclusive).
  - ```--doubleRangeSecondStream```: Defines the maximal number of doubles in the data tuple of the second stream. It randomly chooses the number of doubles between 1 and 'doubleRangeSecondStream' (inclusive).
  - ```--stringRangeSecondStream```: Defines the maximal number of strings in the data tuple of the second stream. It randomly chooses the number of strings between 1 and 'stringRangeSecondStream' (inclusive).
  - ```--integerRangeThirdStream```: Defines the maximal number of integers in the data tuple of the third stream. It randomly chooses the number of integers between 1 and 'integerRangeThirdStream' (inclusive).
  - ```--doubleRangeThirdStream```: Defines the maximal number of doubles in the data tuple of the third stream. It randomly chooses the number of doubles between 1 and 'doubleRangeThirdStream' (inclusive).
  - ```--stringRangeThirdStream```: Defines the maximal number of strings in the data tuple of the third stream. It randomly chooses the number of strings between 1 and 'stringRangeThirdStream' (inclusive).
  - ```--eventRateFirstStream```: The rate (events/s) at which the data tuples of the first stream are produced.
  - ```--eventRateSecondStream```: The rate (events/s) at which the data tuples of the second stream are produced.
  - ```--eventRateThirdStream```: The rate (events/s) at which the data tuples of the third stream are produced.
  - ```--queryDuration```: Defines the run time of the query (in seconds). After that time has passed, the job is cancelled on Flink. Provide the value '-1' if you want the query to run indefinitely.
  - ```--operatorChaining```: Is a boolean enabling (true) or disabling (false) the operator chaining during the execution in Flink.
  - ```--parallelism```: The parallelism level
  - ```enumerationStrategy```: Defines the enumeration strategy to be used. Can be `RANDOM`, `EXHAUSTIV`, `RULEBASED`, `MINAVGMAX`, `INCREASING` or `PARAMETERBASED`. 

  A sample command to start a query of the third template is the following:
  ```
  ./bin/flink run -c SyntheticQueryGenerator.SyntheticDataGenerator <path to the compiled Jar file of this application> --template template_3 --firstFilterFirstStream true --firstFilterSecondStream true --firstFilterThirdStream true --groupBy true --joinWindowSize 7 --joinWindowSlide 3 --secondFilter true --integerRangeFirstStream 2 --doubleRangeFirstStream 5 --stringRangeFirstStream 7 --integerRangeSecondStream 5 --doubleRangeSecondStream 6 --stringRangeSecondStream 3 --integerRangeThirdStream 5 --doubleRangeThirdStream 6 --stringRangeThirdStream 3 --eventRateFirstStream 30 --eventRateSecondStream 200 --eventRateThirdStream 100 --queryDuration 120 --operatorChaining true --parallelism 2 -- enumerationStrategy --random
  ```

