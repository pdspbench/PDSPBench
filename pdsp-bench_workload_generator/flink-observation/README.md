<!---Flink-Observation: added explanations of this custom build-->
# Custom Apache Flink with Observations Logging for Workload Generator Flink

This is a modified fork of Apache Flink that is used for research projects in Distributed Stream
Processing.

The changes are mainly regarding custom logging of observations of operators regarding properties
such as tupleWidthIn, tupleWidthOut, selectivity, inputRate, outputRate and others. Logging can be
done to local files or to a centralized MongoDB database.

## Prerequisites and Configuration

Both methods require certain parameters to be used. These parameters are set via global job
parameters in PlanGeneratorFlink.

- For cluster execution:
    - A MongoDB service running to save logs in a centralized way.
    - The parameters `distributedLogging`, `mongoAddress`, `mongoPort`, `mongoDatabase`
      , `mongoUsername` and `mongoPassword` are required.
    - The MongoDB service needs to have a user authentication for the database set up.
    - For a local set up you can use `docker-compose` and start a `mongoDB` service in the
      folder `mongoDBLocal` in `plangeneratorflink-management`. Note that you maybe need to adapt
      the `.env` and `mongo-init.js` files with your credentials.
    - For a kubernetes setup the address and port of mongoDB gets automatically determined by
      extracting the IP of the service `mongodb`.
- For local execution:
    - Logs are stored to disk (see `observationLogDir` parameter in PlanGeneratorFlink)
    - Local execution has only been tested with a linux machine and won`t probably run on Windows.
      But you can use windows subsystem for linux (wsl) without problems.
## Modifications
- `flink-dist/src/main/flink-bin/conf/log4j.properties` Added observation logger
- `flink-streaming-java/pom.xml` Added `org.mongodb`, `com.googlecode.json-simple` dependencies
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/datastream/AllWindowedStream.java`
  Changed `aggregate()` method to be able to include an operator description
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/datastream/DataStream.java`
  Changed `filter()` method to be able to include an operator description
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/datastream/JoinedStreams.java`
  Changed `apply()` method to be able to include an operator description. Changed
  also `JoinCoGroupFunction` class to create a StreamMonitor and log observations of joins
  when `coGroup()` gets called.
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/datastream/WindowedStream.java`
  Changed `aggregate()` method to be able to include an operator description.
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/operators/StreamFilter.java`
  Changed `StreamFilter` class to create a StreamMonitor and log observations of filters
  when `processElement()` gets called.
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/runtime/operators/windowing/WindowOperator.java`
  Changed `WindowOperator` class to create a StreamMonitor and log observations of windows
  when `processElement()` gets called.
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/runtime/operators/windowing/WindowOperatorBuilder.java`
  Changed to support operator description.
- `flink-streaming-java/src/main/java/org/apache/flink/streaming/api/operators/StreamMonitor.java`
  New class to handle observation logging to local file or centralized mongoDB database.
- `web-dashboard/src/app/app.component.html` To visualize that you are running a custom flink build,
  a reference on the top right in the web frontend is embedded

## Build & Execution

### Build

- The recommended way to build this custom flink from source is to use
  the `plangeneratorflink-management` scripts (`setupPlanGeneratorFlink.sh` or directly `build.sh`)
- alternatively you can build the source from ground up using maven by
  calling `mvn clean install -DskipTests`
- By running `mvn clean install -DskipTests -P docs-and-source -pl flink-streaming-java,flink-dist`
  only the relevant `flink-streaming-java` modul will be build again. That reduces the time to
  build.
- The generated build can be found in the folder `build-target`.

### Execution
- In case of `distributedLogging` be sure, that mongoDB has been started.
- Run `./bin/start-cluster.sh` in the build folder to start a local cluster.


---