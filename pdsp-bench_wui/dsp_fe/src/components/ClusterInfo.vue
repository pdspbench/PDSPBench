<template>
  <div>
    <v-card>
      <v-toolbar flat color="primary" dark>
        <v-toolbar-title>Cluster Info: {{ cluster_name }}</v-toolbar-title>
      </v-toolbar>
      <v-tabs>
        <v-tab>
          <v-icon left>
            mdi-account
          </v-icon>
          Cluster Admin
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-lock
          </v-icon>
          Cluster Logs
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-access-point
          </v-icon>
          Provide Jobs
        </v-tab>


        <v-tab-item>
          <v-card flat class="mx-16 mb-6">
            <v-card-subtitle>Cluster Configuration:</v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="3">
                  <v-list dense>
                    <v-list-item>
                      <v-list-item-title></v-list-item-title>
                      <v-list-item-subtitle></v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>


            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn v-if="cluster_status == 'Stopped'" @click="startCluster()" color="primary">Start Cluster</v-btn>
              <v-btn v-if="cluster_status == 'Running'" @click="stopCluster()" color="error">Stop Cluster</v-btn>
            </v-card-actions>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-subtitle>Flink Logs</v-card-subtitle>
            <v-card-text>
              <v-card dark max-height="100%">
                {{ joblogs }}

              </v-card>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-select v-model="f_job_class_name" :items="job_class" label="Please select a job class" outlined>
                  </v-select>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="f_num_of_times_job_run" label="Number of times job has to run" outlined type="number">
                  </v-text-field>
                </v-col>
                <v-col cols="12" v-if="f_job_class_name != ''">
                  <v-select v-model="f_job_query_name" :items="getSelectedQueryList" item-text="name"
                    item-value="id" label="Please select a query" outlined>
                  </v-select>
                </v-col>
                
               <!--  <v-col>
                  <h1>Flowchart</h1>
                  <flow-chart></flow-chart>
                </v-col> -->

                <v-col cols="12" v-if="f_job_query_name != ''">
                  <v-select v-model="f_job_class_input_type" :items="job_input" label="Please select the input for query"
                    outlined>
                  </v-select>
                </v-col>
                <v-col cols="12" v-if="f_job_class_input_type == 'File'">
                  <v-file-input v-model="f_job_class_input" label="File input" outlined dense>
                  </v-file-input>
                </v-col>
                <v-col cols="12" v-if="f_job_class_input_type == 'Kafka'">
                  <v-text-field v-model="f_job_class_input" label="Kafka event rate" outlined type="number">

                  </v-text-field>
                </v-col>
                <v-col cols="12" v-if="f_job_class_input != ''">
                  <v-text-field
                    v-for="(operator, index) in job_queries[f_job_class_name].query_list[f_job_query_name - 1].operators"
                    :key="operator" v-model="f_parallelization_degree[index]" :label="operator + ' parallelization degree'"
                    outlined type="number">

                  </v-text-field>
                </v-col>

                <v-col cols="12" v-if="f_job_query_name != ''">
                  <code-editor :query-plan="getSelectedQueryPlan"></code-editor>
                </v-col>

                <v-col cols="12"
                  v-if="f_job_class_input != '' && job_queries[f_job_class_name].query_list[f_job_query_name - 1].hasThreshold">
                  <v-text-field v-model="f_job_threshold" label="threshold" outlined type="number">

                  </v-text-field>
                </v-col>

                <v-col cols="12"
                  v-if="f_job_class_input != '' && job_queries[f_job_class_name].query_list[f_job_query_name - 1].hasWindows">
                  <v-text-field v-model="f_job_window_size" label="Window Size" outlined type="number">

                  </v-text-field>
                </v-col>
                <v-col cols="12"
                  v-if="f_job_class_input != '' && job_queries[f_job_class_name].query_list[f_job_query_name - 1].hasWindows">
                  <v-text-field v-model="f_job_window_slide_size" label="Window Slide Size" outlined type="number">

                  </v-text-field>
                </v-col>
                <v-col cols="12"
                  v-if="f_job_class_input != '' && job_queries[f_job_class_name].query_list[f_job_query_name - 1].hasLateness">
                  <v-text-field v-model="f_job_google_lateness" label="Watermark Lateness" outlined type="number">

                  </v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-if="f_job_class_input != ''" v-model="f_job_run_time"
                    label="How long the job should run in minutes" outlined type="number">
                  </v-text-field>
                </v-col>
                
              </v-row>
              <v-row>

                <v-col cols="4">
                  <v-btn dark color="primary" @click="createJob()">
                    Submit Job
                  </v-btn>
                </v-col>
                <v-col cols="4"></v-col>
              </v-row>
            </v-card-text>

          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card>
    <v-dialog width="50%" v-model="showProgress">
      <v-card dark>
        <v-card-title>Please wait <v-progress-linear color="deep-purple green" indeterminate rounded
            height="6"></v-progress-linear></v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-item>
              Starting Zookeeper
            </v-list-item>
            <v-list-item>
              Starting Kafka
            </v-list-item>
            <v-list-item>
              Creating topics
            </v-list-item>
            <v-list-item>
              Sending Job
            </v-list-item>
            <v-list-item>
              Starting producer
            </v-list-item>






          </v-list>
        </v-card-text>

      </v-card>
    </v-dialog>
  </div>
</template>
<script lang="js">
import axios from 'axios';
import CodeEditor from './CodeEditor.vue';


export default {

  name: 'ClusterInfo',
  components: {
    CodeEditor
  },
  props: {
    id: String
  },
  data() {
    return {
      showProgress: false,
      joblogs: 'Job logs ',
      url: process.env.VUE_APP_URL,
      cluster_name: '',
      cluster_id: '',
      cluster_status: '',
      job_class: ['Word Count', 'Smart Grid', 'Ad Analytics', 'Google cloud Monitoring', 'Sentiment Analysis', 'Spike Detection', 'Log Processing', 'Trending Topics', 'Bargain Index', 'Click Analytics', 'Machine Outlier', 'Linear Road', 'TPCH', 'Traffic Monitoring' ],

      job_queries: {
        'Word Count': {
          query_list: [{
            id: 1,
            name: '1. Counting the number of words',
            operators: ['tokenizer', 'Counter'],
            query_plan: 'SELECT count(*) FROM words'
          }],

        },
        'Smart Grid': {
          query_list: [{
            id: 1,
            name: '1. Calculate the global average load of each house',
            operators: ['house-event-parser','global average load','output'],
            hasWindows: true,
            query_plan: `SELECT
    HouseEvent.house,
    AVG(HouseEvent.load) AS average_load,
    TUMBLE_START(event_time, INTERVAL slidingWindowSize SECOND) AS window_start,
    TUMBLE_END(event_time, INTERVAL slidingWindowSize SECOND) AS window_end
FROM
    HouseEvent
GROUP BY  
    HouseEvent.house,
    TUMBLE(event_time, INTERVAL slidingWindowSize SECOND) //PARALLELIZATION -- *

`
          }, {
            id: 2,
            name: '2. Calculate the local average load of plugs in each household',
            operators: ['house-event-parser','local average load','output'],
            hasWindows: true,
            query_plan: `SELECT
    HouseEvent.house,
    HouseEvent.households,
    HouseEvent.plugs,
    AVG(HouseEvent.load) AS average_load,
    TUMBLE_START(event_time, INTERVAL slidingWindowSize SECOND) AS window_start,
    TUMBLE_END(event_time, INTERVAL slidingWindowSize SECOND) AS window_end
FROM
    HouseEvent
GROUP BY
    HouseEvent.house,
    HouseEvent.households,
    HouseEvent.plugs,
    TUMBLE(event_time, INTERVAL slidingWindowSize SECOND) //PARALLELIZATION -- *
`
          },
          ]

        },
        'Ad Analytics': {
          query_list: [{
            id: 1,
            name: '1. Calculate the Ad_analytics query',
            operators: ["click-parser", "impression-parser", "clicks-counter", "impressions-counter", "rollingCTR"],
            hasWindows: true,
            query_plan: `-- Step 1: Parse clicks and impressions
WITH parsed_clicks AS (
  SELECT query_id, ad_id, COUNT(*) AS click_count
  FROM clicks
  GROUP BY query_id, ad_id 
),  //PARALLELIZATION -- *
parsed_impressions AS (
  SELECT query_id, ad_id, COUNT(*) AS impression_count
  FROM impressions
  GROUP BY query_id, ad_id 
),//PARALLELIZATION -- **

-- Step 2: Calculate CTR
rolling_ctr AS (
  SELECT
    pc.query_id,
    pc.ad_id,
    pc.click_count,
    pi.impression_count,
    pc.click_count / pi.impression_count AS ctr
  FROM parsed_clicks pc
  JOIN parsed_impressions pi ON pc.query_id = pi.query_id AND pc.ad_id = pi.ad_id
  WHERE pc.click_count <= pi.impression_count
) //PARALLELIZATION -- ***

-- Step 3: Output the result //PARALLELIZATION -- ****
SELECT *
FROM rolling_ctr; //PARALLELIZATION -- *****`
          }
          ]
        },
        'Google cloud Monitoring': {
          query_list: [{
            id: 1,
            name: '1. Calculate average-cpu-per-category',
            operators: ["parser", "avg-cpu-per-category"],
            hasWindows: true,
            hasLateness: true,
            query_plan: `SELECT  //PARALLELIZATION -- *
    category,
    AVG(cpu_usage) AS avg_cpu_usage
FROM
    Google_Cloud_Monitoring_stream
WHERE
    event_type = 1
GROUP BY  //PARALLELIZATION -- **
    category  
`
          }, {
            id: 2,
            name: '2. Calculate average-cpu-per-job',
            operators: ["parser", "avg-cpu-per-job"],
            hasWindows: true,
            hasLateness: true,
            query_plan: `SELECT //PARALLELIZATION -- *
    job_id,
    AVG(cpu_usage) AS avg_cpu_usage
FROM
Google_Cloud_Monitoring_stream
WHERE
    event_type = 1
GROUP BY  //PARALLELIZATION -- **
    job_id  `
          },
          ]

        },
        'Sentiment Analysis': {
          query_list: [{
            id: 1,
            name: '1. Calculate sentiment analysis',
            operators: ["twitter parser", "twitter analyser"],
            hasWindows: false,
            query_plan: `SELECT //PARALLELIZATION -- *
  id,
  timestamp,
  text,
  sentimentResult.sentiment AS sentiment,
  sentimentResult.score AS sentimentScore
FROM (
  SELECT //PARALLELIZATION -- **
    id,
    timestamp,
    text,
    SentimentClassifierFactory.create(SentimentClassifierFactory.BASIC).classify(text) AS sentimentResult
  FROM <parsed_tweets_table>
) AS intermediate
`
          }
          ]

        },
        'Spike Detection': {
          query_list: [{
            id: 1,
            name: '1. Calculate Spike Detection',
            operators: ["parser", "average calculator", "spike detector"],
            hasWindows: true,
            hasLateness: true,
            query_plan: `-- Step 1: Parse the input data
CREATE TABLE SensorMeasurement (
  sensorId INT,
  timestamp TIMESTAMP,
  value DOUBLE
);

INSERT INTO SensorMeasurement
SELECT
  PARSE_JSON(data).sensorId AS sensorId,
  PARSE_JSON(data).timestamp AS timestamp,
  PARSE_JSON(data).value AS value
FROM inputDataStream; //PARALLELIZATION -- *

-- Step 2: Assign timestamps and watermarks
CREATE TABLE SensorMeasurementWithWatermarks (
  sensorId INT,
  timestamp TIMESTAMP,
  value DOUBLE,
  watermark TIMESTAMP
) WITH (
  WATERMARK FOR timestamp AS timestamp - INTERVAL 'X' SECOND -- Specify the watermark strategy
);

INSERT INTO SensorMeasurementWithWatermarks
SELECT
  sensorId,
  timestamp,
  value,
  timestamp - INTERVAL 'X' SECOND AS watermark
FROM SensorMeasurement; //PARALLELIZATION -- **

-- Step 3: Key the stream by sensorId
CREATE TABLE KeyedSensorMeasurement (
  sensorId INT,
  timestamp TIMESTAMP,
  value DOUBLE,
  watermark TIMESTAMP
) WITH (
  WATERMARK FOR watermark AS watermark
);

INSERT INTO KeyedSensorMeasurement
SELECT
  sensorId,
  timestamp,
  value,
  watermark
FROM SensorMeasurementWithWatermarks;

-- Step 4: Apply sliding processing time window
CREATE TABLE WindowedSensorMeasurement AS (
  SELECT
    sensorId,
    TUMBLE_START(timestamp, INTERVAL 'X' SECOND) AS windowStart,
    TUMBLE_END(timestamp, INTERVAL 'X' SECOND) AS windowEnd,
    AVG(value) AS averageValue
  FROM KeyedSensorMeasurement
  GROUP BY
    sensorId,
    TUMBLE(timestamp, INTERVAL 'X' SECOND)
);

-- Step 5: Filter spikes
CREATE TABLE DetectedSpikes AS (
  SELECT
    sensorId,
    windowStart,
    windowEnd,
    averageValue
  FROM WindowedSensorMeasurement
  WHERE ABS(value - averageValue) > 0.03 * averageValue
); //PARALLELIZATION -- ***

-- Step 6: Sink detected spikes
INSERT INTO outputSink
SELECT *
FROM DetectedSpikes;
`
          }
          ]


        },
        'Log Processing': {
          query_list: [{
            id: 1,
            name: '1. Volume Counter',
            operators: ['log-parser', 'volume counter'],
            hasWindows: true,
            query_plan: `SELECT
    logTime,
    COUNT(*) AS visitCount //PARALLELIZATION -- **
FROM
    (SELECT
        logTime
    FROM
        LogEventTable
    WHERE
        logParserOutput = 'log-parser' //PARALLELIZATION -- *
    ) AS filteredLogs
GROUP BY
    logTime;

`
          }, {
            id: 2,
            name: '2. Status Counter',
            operators: ['log-parser', 'status counter'],
            hasWindows: true,
            query_plan: `SELECT
    statusCode,
    COUNT(*) AS statusCodeCount //PARALLELIZATION -- **
FROM
    (SELECT
        statusCode
    FROM
        LogEventTable
    WHERE
        logParserOutput = 'log-parser' //PARALLELIZATION -- *
    ) AS filteredLogs
GROUP BY
    statusCode;

`
          },
          ]

        },
        'Trending Topics': {
          query_list: [{
            id: 1,
            name: '1. Twitter trending topics',
            operators: ['twitter-parser', 'topic-extractor', 'topic-popularity-detector'],
            hasWindows: true,
            hasThreshold: true,
            query_plan: `INSERT INTO Topics (Topic, Count)
SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(word, ' ', 1), '#', -1) AS topic, COUNT(*) AS count //PARALLELIZATION -- ***
FROM (
    SELECT
        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(t.TweetText, ' ', n.n), ' ', -1), '[^a-zA-Z0-9#]', '') AS word //PARALLELIZATION -- **
    FROM
        Tweets t
    CROSS JOIN
        (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) n -- Adjust the number of cross joins based on the maximum number of words per tweet
    WHERE
        t.TweetText LIKE '%#%' -- Filter tweets containing hashtags
) subquery
GROUP BY topic; //PARALLELIZATION -- *

`
          }
          ]

        },
        'Bargain Index': {
          query_list: [{
            id: 1,
            name: '1. Bargain-Index Calculator',
            operators: ["quote-parser", "VWAP-operator", "bargain-index-calculator"],
            hasWindows: true,
            query_plan: `CREATE VIEW VWAP AS
SELECT
    symbol,
    SUM(close * volume) / SUM(volume) AS vwap,  //PARALLELIZATION -- **
    SUM(volume) AS totalVolume
FROM
    StockQuotes
GROUP BY
    symbol;

-- Calculate bargain index and filter quotes
SET @threshold = 0; -- Set your desired threshold value here  //PARALLELIZATION -- ***
SELECT
    q.symbol,
    q.close,
    q.volume
FROM
    StockQuotes q  //PARALLELIZATION -- *
JOIN
    VWAP v ON q.symbol = v.symbol
WHERE
    q.close / q.volume > @threshold;
`
          }
          ]

        },
        'Click Analytics': {
          query_list: [{
            id: 1,
            name: '1. Unique and total visits',
            operators: ["click-log-parser", "repeat-visit", "reduce-operation"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT url, COUNT(*) AS total_visits, 
            COUNT(DISTINCT user_id) AS unique_visits  //PARALLELIZATION -- **
FROM ClickLogs //PARALLELIZATION -- *
GROUP BY url; //PARALLELIZATION -- ***
`
          },{
            id: 2,
            name: '2. visits based on location',
            operators: ["click-log-parser", "geography-visit"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT 
  location.country,
  COUNT(*) AS visits,
  location.city,
  COUNT(*) AS city_visits
FROM ClickLogs //PARALLELIZATION -- *
JOIN (
  SELECT   //PARALLELIZATION -- **
    ip_address,
    MAX(city) AS city,
    MAX(country) AS country
  FROM GeoIPDatabase
  GROUP BY ip_address
) AS location ON ClickLogs.ip_address = location.ip_address
GROUP BY location.country, location.city;
`
          },
          ]

        },
        'Linear Road': {
          query_list: [{
            id: 1,
            name: '1. Toll Notification',
            operators: ["Vehicle-event-parser", "toll-notification", "formatter-toll-notification"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT
    v.vehicleId,
    COALESCE(SUM(t.tollAmount), 0) AS totalToll
FROM
    Vehicles v //PARALLELIZATION -- *
LEFT JOIN
    (
        SELECT  //PARALLELIZATION -- **
            vehicleId,
            segmentId,
            calculateToll(averageSpeed, numVehicles) AS tollAmount
        FROM
            (
                SELECT //PARALLELIZATION -- ***
                    segmentId,
                    vehicleId,
                    AVG(speed) AS averageSpeed,
                    COUNT(*) AS numVehicles
                FROM
                    VehicleSpeedData
                GROUP BY
                    segmentId, vehicleId
            ) subquery
    ) t
ON
    v.vehicleId = t.vehicleId
GROUP BY
    v.vehicleId

`
          },{
            id: 2,
            name: '2. Accident Notification',
            operators: ["Vehicle-event-parser", "accident-notification", "formatter-accident-notification"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT //PARALLELIZATION -- ***
    eventTime,
    CASE
        WHEN COUNT(*) >= 3 THEN 'Accident Detected' //PARALLELIZATION -- **
        ELSE 'No Accident'
    END AS accidentStatus
FROM
    VehicleEvents //PARALLELIZATION -- *
GROUP BY
    SlidingWindow(eventTime, 5 minutes, 30 seconds)

`
          },{
            id: 3,
            name: '3. Daily Expenditure',
            operators: ["Vehicle-event-parser", "daily-expenditure"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT  //PARALLELIZATION -- **
    vehicleId,
    DATE(eventTime) AS expenditureDate,
    SUM(expenditureAmount) AS dailyExpenditure
FROM
    VehicleEvents  //PARALLELIZATION -- *
GROUP BY
    vehicleId, DATE(eventTime)

`
          },{
            id: 4,
            name: '4. visits based on location',
            operators: ["Vehicle-event-parser", "vehicle-report-mapper"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `SELECT  //PARALLELIZATION -- **
    vehicleId,
    COUNT(*) AS totalReports
FROM
    VehicleEvents   //PARALLELIZATION -- *
GROUP BY
    vehicleId

`
          },
          ]

        },
        'TPCH': {
          query_list: [{
            id: 1,
            name: '1. Priority Order Counter',
            operators: ["tpch-event-parser", "tpch-data-filter", "tpch-flat-mapper", "priority-counter", "formatter"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `-- Filter and count orders with priorities between "1-URGENT" and "5-LOW"
SELECT
    o_orderpriority,
    COUNT(*) AS orderCount  //PARALLELIZATION -- ***
FROM
    TPCHEvents //PARALLELIZATION -- *
WHERE
    o_orderpriority >= '1-URGENT' AND o_orderpriority <= '5-LOW' //PARALLELIZATION -- **
GROUP BY
    o_orderpriority

`
          }
          ]

        },
        'Machine Outlier': {
          query_list: [{
            id: 1,
            name: '1. Machine Outlier Detection',
            operators: ["machine-usage-parser", "machine-usage-grouper", "outlier-detector"],
            hasWindows: true,
            hasThreshold: true,
            query_plan: `
SELECT
    MachineId,
    Timestamp,
    UsageValue
FROM
    MachineUsageData  //PARALLELIZATION -- *
WHERE  
    Timestamp >= (CurrentTimestamp - SlidingWindowSize) //PARALLELIZATION -- **
    AND Timestamp <= CurrentTimestamp 
GROUP BY
    MachineId, Timestamp
HAVING    
    COUNT(*) = 1    //PARALLELIZATION -- ***

`
          }
          ]

        },
        'Traffic Monitoring': {
          query_list: [{
            id: 1,
            name: '1. Traffic Monitor',
            operators: ["traffic-event-parser", "road-matcher", "avg-speed","formatter"],
            hasWindows: true,
            hasThreshold: false,
            query_plan: `

-- Step 1: Parse Traffic Events
SELECT        //PARALLELIZATION -- *
    TrafficEventId,
    Timestamp,
    VehicleId,
    RoadId,
    Speed
FROM
    TrafficEvents;

-- Step 2: Road Matching
WITH RoadMatch AS (         //PARALLELIZATION -- **
    SELECT
        TrafficEventId,
        Timestamp,
        VehicleId,
        RoadId
    FROM
        ParsedTrafficEvents
    WHERE
        RoadId IS NOT NULL
),

-- Step 3: Calculate Average Speed
AvgSpeed AS (           //PARALLELIZATION -- ***
    SELECT
        RoadId,
        AVG(Speed) AS AverageSpeed
    FROM
        RoadMatch
    GROUP BY
        RoadId
),

-- Step 4: Format Results
FormattedResults AS (         //PARALLELIZATION -- ****
    SELECT
        RoadId,
        AverageSpeed
    FROM
        AvgSpeed
    WHERE
        AverageSpeed > 0
)

-- Step 5: Output Results (Sink)
INSERT INTO
    TrafficResults
SELECT
    RoadId,
    AverageSpeed
FROM
    FormattedResults;

`
          }
          ]

        },
      },
      job_input: ['File', 'Kafka'],
      f_job_class_name: '',
      f_job_query_name: '',
      f_job_class_input_type: '',
      f_job_class_input: '',
      f_parallelization_degree: [],
      f_job_window_size: 100,
      f_job_window_slide_size: 10,
      f_job_google_lateness: 0,
      f_job_run_time: 100,
      f_job_threshold: 5,
      f_num_of_times_job_run: 1,
      show_progress: false,


    }
  },
  // 
  // 
  methods: {
    async createJob() {
      this.showProgress = true;
      var data = {
        "job_class": this.f_job_class_name,//'Ad Analytics'
        "job_class_input_type": this.f_job_class_input_type, //'Kafka'
        "job_class_input": this.f_job_class_input, //kafka event rate
        "job_query_name": this.f_job_query_name, //'1'
        "job_pds": this.f_parallelization_degree,//[1,3,5,1,3]
        "job_window_size": this.f_job_window_size,
        "job_window_slide_size": this.f_job_window_slide_size,
        "job_run_time": this.f_job_run_time,
        "job_google_lateness": this.f_job_google_lateness,
        "job_threshold": this.f_job_threshold,
        "num_of_times_job_run": this.f_num_of_times_job_run
      }
      console.log('providing job with these parameters')
      console.log(data)
      axios
        .post(this.url + ":8000/infra/jobcreate/" + this.cluster_id, data)
        .then((resp) => {
          this.showProgress = false
          console.log(resp.data)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    async startCluster() {
      await axios
        .get(this.url + ":8000/infra/start/" + this.id)
        .then((resp) => {
          this.snackbar = {
            view: true,
            timeout: 3000,
            text: 'Started the cluster successfully',
            color: 'primary'
          };
          console.log(resp)
          this.refresh(this.id)
          this.$emit('refresh', 'refreshed')
        })
    },
    async stopCluster() {
      await axios
        .get(this.url + ":8000/infra/stop/" + this.id)
        .then((resp) => {

          console.log(resp)
          this.refresh(this.id)
          this.snackbar = {
            view: true,
            timeout: 3000,
            text: 'Stopped the cluster successfully',
            color: 'primary'
          };
          this.$emit('refresh', 'refreshed')
        })
    },
    async refresh(cluster_identifier) {
      await axios
        .get(this.url + ":8000/infra/getCluster/" + cluster_identifier)
        .then((resp) => {
          this.cluster_id = resp.data.id;
          this.cluster_name = resp.data.name;
          this.cluster_status = resp.data.status;
          console.log(resp)
        })
    },

  },
  computed: {
    snackbar: {
      get() {
        return this.$store.state.snackbar;
      },
      set(value) {
        this.$store.commit('setSnackbar', value);
      },
    },
    getSelectedQueryPlan() {

      const queryIndex = this.f_job_query_name - 1;
      let queryPlan = this.job_queries[this.f_job_class_name].query_list[queryIndex].query_plan;
      console.log('reached main')
      if(this.f_job_class_name == 'Smart Grid' && (this.f_job_query_name == 1 || this.f_job_query_name == 2)){
        console.log('reacheed inside smart grid')

        let newQuery = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
        queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery)
        console.log(queryPlan);

      }else if(this.f_job_class_name == 'Ad Analytics' && this.f_job_query_name == 1){


        let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
        let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
        let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]
        let newQuery4 = '//PARALLELIZATION --'+ this.f_parallelization_degree[3]
        let newQuery5 = '//PARALLELIZATION --'+ this.f_parallelization_degree[4]

        queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
        queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
        queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)
        queryPlan = queryPlan.replace('//PARALLELIZATION -- ****', newQuery4)
        queryPlan = queryPlan.replace('//PARALLELIZATION -- *****', newQuery5)

      }else if(this.f_job_class_name == 'Google cloud Monitoring' && (this.f_job_query_name == 1 || this.f_job_query_name == 2)){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]


queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)


}else if(this.f_job_class_name == 'Sentiment Analysis' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]


queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)


}else if(this.f_job_class_name == 'Spike Detection' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Log Processing' && (this.f_job_query_name == 1 || this.f_job_query_name == 2)){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]


queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)



}else if(this.f_job_class_name == 'Trending Topics' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Bargain Index' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Click Analytics' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)

}else if(this.f_job_class_name == 'Click Analytics' && this.f_job_query_name == 2){

let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
}else if(this.f_job_class_name == 'Linear Road' && this.f_job_query_name == 1 ){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Linear Road' && this.f_job_query_name == 2 ){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Linear Road' && (this.f_job_query_name == 3 || this.f_job_query_name == 4)){

let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)

}else if(this.f_job_class_name == 'TPCH' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Machine Outlier' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}else if(this.f_job_class_name == 'Traffic Monitoring' && this.f_job_query_name == 1){


let newQuery1 = '//PARALLELIZATION --'+ this.f_parallelization_degree[0]
let newQuery2 = '//PARALLELIZATION --'+ this.f_parallelization_degree[1]
let newQuery3 = '//PARALLELIZATION --'+ this.f_parallelization_degree[2]

queryPlan = queryPlan.replace('//PARALLELIZATION -- *', newQuery1)
queryPlan = queryPlan.replace('//PARALLELIZATION -- **', newQuery2)
queryPlan = queryPlan.replace('//PARALLELIZATION -- ***', newQuery3)


}
      return queryPlan
    },
    getSelectedQueryList() {


return this.job_queries[this.f_job_class_name].query_list
}
  },
  async mounted() {

    this.refresh(this.id)


  },
  watch: {
    id(new_val, old_val) {
      if (new_val != old_val)
        this.refresh(this.id)
    }
  }
}
</script>
