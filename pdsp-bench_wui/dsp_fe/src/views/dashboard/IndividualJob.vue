<template>
  <div>

    <v-card class="my-6 pa-0">
      <v-card-title>
        <v-sheet color="primary" elevation="16" class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
          <h3>Job Information</h3>
        </v-sheet>
      </v-card-title>
      <v-card-text class="mt-5">
        <v-row>
          <v-col cols="5">
            <v-list>
              <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title>
                    <b>{{ jobInfo.jid }}</b>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Job Id
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="4">
            <v-list>
              <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title>
                    <b>{{ jobInfo.name }}</b>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Job name
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="3">
            <v-list>
              <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title>
                    <b>{{ millisToMinutesAndSeconds(jobInfo.duration) }} (mm:ss)</b>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Job running duration
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="5">
            <v-list>
              <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title>
                    <b>{{ new Date(jobInfo.now).toLocaleString('en-GB') }}</b>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Job Submitted time
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="4">
            <v-list>
              <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title>
                    <v-chip color="primary">
                      Status: <b>{{ jobInfo.state }}</b>
                    </v-chip>

                  </v-list-item-title>

                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>

        </v-row>
        <v-card class=" mt-4 justify-center ">
          <v-card-title class="justify-center"> Subtasks </v-card-title>

          <v-card-text>
            <v-expansion-panels focusable>
              <v-expansion-panel v-for="vertex in jobInfo.vertices" :key="vertex.name">
                <v-expansion-panel-header>
                  <h3>{{ vertex.name }}</h3>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="pa-3">
                  <v-row class="mb-2">
                    <v-col cols="6">
                      <v-list-item two-line>
                        <v-list-item-content>
                          <v-list-item-title>{{ vertex.parallelism }}</v-list-item-title>
                          <v-list-item-subtitle>Subtask parallelization degree</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="6">
                      <v-list-item two-line>
                        <v-list-item-content>
                          <v-list-item-title>{{ vertex.maxParallelism }}</v-list-item-title>
                          <v-list-item-subtitle>Subtask's maximum parallelization degree</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>

                  </v-row>
                  <br />
                  <p><b>Metrics of the subtasks:</b></p>
                  <v-row>
                    <v-col cols="6" v-for="(metric_key, metric_value, index) in vertex.metrics" :key="index">
                      <v-list-item two-line>
                        <v-list-item-content>
                          <v-list-item-title>{{ metric_key }}</v-list-item-title>
                          <v-list-item-subtitle>{{ metric_value }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>

          </v-card-text>
        </v-card>
        <v-card class=" mt-14 justify-center ">
          <v-card-title class="justify-center"> Output in the Sink Topic

          </v-card-title>
          <v-card-text>
            <v-expansion-panels focusable>
              <v-expansion-panel>
                <v-expansion-panel-header>
                  <h3>Results</h3><v-spacer />
                </v-expansion-panel-header>
                <v-expansion-panel-content class="pa-3">
                  <v-list-item v-for="result in resultOfJob" :key="result">
                    <v-list-item-content>
                      <v-list-item-title>{{result}}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-expansion-panel-content>
              </v-expansion-panel>

            </v-expansion-panels>

          </v-card-text>
        </v-card>
        <v-card class=" mt-14 justify-center ">
          <v-card-title class="justify-center"> Job Analysis </v-card-title>
          <v-card-text>
            <div class="my-2">
              <v-btn depressed color="primary" @click="stopUpdates = !stopUpdates">
                Pause
              </v-btn>

            </div>

            <iframe
              :src="'http://' + this.main_node_ip + ':3000/d-solo/8fUKTEF4k/flink-dashboard?orgId=1&refresh=1s&panelId=5'"
              width="50%" height="400" frameborder="2"></iframe>
            <iframe
              :src="'http://' + this.main_node_ip + ':3000/d-solo/8fUKTEF4k/flink-dashboard?orgId=1&refresh=1s&panelId=3'"
              width="50%" height="400" frameborder="2"></iframe>
            <iframe
              :src="'http://' + this.main_node_ip + ':3000/d-solo/8fUKTEF4k/flink-dashboard?orgId=1&refresh=1s&panelId=6'"
              width="50%" height="400" frameborder="2"></iframe>
            <iframe
              :src="'http://' + this.main_node_ip + ':3000/d-solo/8fUKTEF4k/flink-dashboard?orgId=1&refresh=1s&panelId=7'"
              width="50%" height="400" frameborder="2"></iframe>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer1" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">
                <div id="chartContainer" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer2" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer3" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer4" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer5" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer6" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer7" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer8" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer9" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer10" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer11" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer12" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer13" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer14" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer15" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer16" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">
 
                <div id="chartContainer17" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">
               
                <div id="chartContainer18" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer19" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer20" class="my-2"></div>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="graph-column" cols="4">
                
                <div id="chartContainer21" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer22" class="my-2"></div>
              </v-col>
              <v-col class="graph-column" cols="4">

                <div id="chartContainer23" class="my-2"></div>
              </v-col>
            </v-row>


          </v-card-text>
        </v-card>

      </v-card-text>

    </v-card>


  </div>
</template>

<script>
import axios from 'axios';
import * as d3 from "d3";
export default {
  name: "IndividualJob",
  data() {
    return {


      resultOfJob: [],
      url: process.env.VUE_APP_URL,
      first_parsed_data: null,
      stopUpdates: false,
      AllMetrics: {},
      jobInfo: {},
      timerjobInfo: null,
      timerjobMetrics: null,
      //**************************COMMON METRICS VARIABLES********************************************************* */
      chartDatasinkthroughput: [],
      chartDatasourcethroughput: [],
      chartDatasourcelatency: [],

      sinkthroughputvalue: 0,
      sourcethroughputvalue: 0,
      latency: null,

      sinkthroughput_graph_title: null,
      sourcethroughput_graph_title: null,
      //**********************************WORD COUNT*************************************************** */
      chartDataTokenPerSecondOut: [],
      chartDataTokenSelectivity: [],
      chartDataTokenBytesOfEachRecord: [],

      chartDataCountPerSecondOut: [],
      chartDatacounterSelectivity: [],
      chartDatacounterBytesOfEachRecord: [],

      //**********************************SMART GRID*************************************************** */            
      chartDataGridPerSecondOut: [],
      chartDataGridSelectivity: [],
      chartDataGridBytesOfEachRecord: [],

      //**********************************ADS ANALYTICS*************************************************** */ 

      chartDataClickParserPerSecondOut: [],
      chartDataClickParserSelectivity: [],
      chartDataClickParserBytesOfEachRecord: [],

      chartDataImpressionParserPerSecondOut: [],
      chartDataImpressionParserSelectivity: [],
      chartDataImpressionParserBytesOfEachRecord: [],

      chartDataClicksCounterPerSecondOut: [],
      chartDataClicksCounterSelectivity: [],
      chartDataClicksCounterBytesOfEachRecord: [],

      chartDataImpressionsCounterPerSecondOut: [],
      chartDataImpressionsCounterSelectivity: [],
      chartDataImpressionsCounterBytesOfEachRecord: [],

      chartDatarollingCTRPerSecondOut: [],
      chartDatarollingCTRSelectivity: [],
      chartDatarollingCTRBytesOfEachRecord: [],



      //**********************************GOOGLE CLOUD MONITORING*************************************************** */ 
      chartDataParserPerSecondOut: [],
      chartDataParserSelectivity: [],
      chartDataParserBytesOfEachRecord: [],


      chartDataAvgCpuCatPerSecondOut: [],
      chartDataAvgCpuCatSelectivity: [],
      chartDataAvgCpuCatBytesOfEachRecord: [],

      chartDataAvgCpuJobPerSecondOut: [],
      chartDataAvgCpuJobSelectivity: [],
      chartDataAvgCpuJobBytesOfEachRecord: [],

      //**********************************SENTIMENT ANALYSIS*************************************************** */ 

      chartDataTwitterParserPerSecondOut: [],
      chartDataTwitterParserSelectivity: [],
      chartDataTwitterParserBytesOfEachRecord: [],


      chartDataTwitterAnalyserPerSecondOut: [],
      chartDataTwitterAnalyserSelectivity: [],
      chartDataTwitterAnalyserBytesOfEachRecord: [],

      //**********************************SPIKE DETECTION*************************************************** */ 

      chartDataSpikeParserPerSecondOut: [],
      chartDataSpikeParserSelectivity: [],
      chartDataSpikeParserBytesOfEachRecord: [],


      chartDataAvgCalPerSecondOut: [],
      chartDataAvgCalSelectivity: [],
      chartDataAvgCalBytesOfEachRecord: [],

      chartDataSpikeDetectorPerSecondOut: [],
      chartDataSpikeDetectorSelectivity: [],
      chartDataSpikeDetectorBytesOfEachRecord: [],

      //**********************************LOG PROCESSING*************************************************** */ 

      chartDataLogAnalyzerParserPerSecondOut: [],
      chartDataLogAnalyzerParserSelectivity: [],
      chartDataLogAnalyzerParserBytesOfEachRecord: [],


      chartDataLogAnalyzerVolumePerSecondOut: [],
      chartDataLogAnalyzerVolumeSelectivity: [],
      chartDataLogAnalyzerVolumeBytesOfEachRecord: [],

      chartDataLogAnalyzerStatusPerSecondOut: [],
      chartDataLogAnalyzerStatusSelectivity: [],
      chartDataLogAnalyzerStatusBytesOfEachRecord: [],

      //**********************************Trending Topics*************************************************** */ 

      chartDataTrendingTopicsExtractorPerSecondOut: [],
      chartDataTrendingTopicsExtractorSelectivity: [],
      chartDataTrendingTopicsExtractorBytesOfEachRecord: [],


      chartDataTrendingTopicsParserPerSecondOut: [],
      chartDataTrendingTopicsParserSelectivity: [],
      chartDataTrendingTopicsParserBytesOfEachRecord: [],

      chartDataTrendingTopicsFilterPerSecondOut: [],
      chartDataTrendingTopicsFilterSelectivity: [],
      chartDataTrendingTopicsFilterBytesOfEachRecord: [],

      //**********************************Bargain Index*************************************************** */ 

      chartDataBargainIndexParserPerSecondOut: [],
      chartDataBargainIndexParserSelectivity: [],
      chartDataBargainIndexParserBytesOfEachRecord: [],


      chartDataBargainIndexVWAPPerSecondOut: [],
      chartDataBargainIndexVWAPSelectivity: [],
      chartDataBargainIndexVWAPBytesOfEachRecord: [],

      chartDataBargainIndexCalcPerSecondOut: [],
      chartDataBargainIndexCalcSelectivity: [],
      chartDataBargainIndexCalcBytesOfEachRecord: [],

      //**********************************Click Analytics*************************************************** */ 

      chartDataClickAnalyticsParserPerSecondOut: [],
      chartDataClickAnalyticsParserSelectivity: [],
      chartDataClickAnalyticsParserBytesOfEachRecord: [],


      chartDataClickAnalyticsRepeatPerSecondOut: [],
      chartDataClickAnalyticsRepeatSelectivity: [],
      chartDataClickAnalyticsRepeatBytesOfEachRecord: [],

      chartDataClickAnalyticsReducePerSecondOut: [],
      chartDataClickAnalyticsReduceSelectivity: [],
      chartDataClickAnalyticsReduceBytesOfEachRecord: [],

      chartDataClickAnalyticsGeoPerSecondOut: [],
      chartDataClickAnalyticsGeoSelectivity: [],
      chartDataClickAnalyticsGeoBytesOfEachRecord: [],

      //**********************************Linear Road*************************************************** */ 

      chartDataVehicleEventParserPerSecondOut: [],
      chartDataVehicleEventParserSelectivity: [],
      chartDataVehicleEventParserBytesOfEachRecord: [],

      chartDataTollNotificationPerSecondOut: [],
      chartDataTollNotificationSelectivity: [],
      chartDataTollNotificationBytesOfEachRecord: [],

      chartDataFormatterTollNotificationPerSecondOut: [],
      chartDataFormatterTollNotificationSelectivity: [],
      chartDataFormatterTollNotificationBytesOfEachRecord: [],

      chartDataAccidentNotificationPerSecondOut: [],
      chartDataAccidentNotificationSelectivity: [],
      chartDataAccidentNotificationBytesOfEachRecord: [],

      chartDataFormatterAccidentNotificationPerSecondOut: [],
      chartDataFormatterAccidentNotificationSelectivity: [],
      chartDataFormatterAccidentNotificationBytesOfEachRecord: [],

      chartDataDailyExpenditurePerSecondOut: [],
      chartDataDailyExpenditureSelectivity: [],
      chartDataDailyExpenditureBytesOfEachRecord: [],

      chartDataVehicleReportMapperPerSecondOut: [],
      chartDataVehicleReportMapperSelectivity: [],
      chartDataVehicleReportMapperBytesOfEachRecord: [],

      //**********************************TPCH*************************************************** */ 

      chartDataTpchEventParserPerSecondOut: [],
      chartDataTpchEventParserSelectivity: [],
      chartDataTpchEventParserBytesOfEachRecord: [],

      chartDataTpchDataFilterPerSecondOut: [],
      chartDataTpchDataFilterSelectivity: [],
      chartDataTpchDataFilterBytesOfEachRecord: [],

      chartDataTpchFlatMapperPerSecondOut: [],
      chartDataTpchFlatMapperSelectivity: [],
      chartDataTpchFlatMapperBytesOfEachRecord: [],

      chartDataPriorityCounterPerSecondOut: [],
      chartDataPriorityCounterSelectivity: [],
      chartDataPriorityCounterBytesOfEachRecord: [],

      chartDataTpchFormatterPerSecondOut: [],
      chartDataTpchFormatterSelectivity: [],
      chartDataTpchFormatterBytesOfEachRecord: [],

      //**********************************Machine Outlier*************************************************** */ 

      chartDataMachineUsageParserPerSecondOut: [],
      chartDataMachineUsageParserSelectivity: [],
      chartDataMachineUsageParserBytesOfEachRecord: [],

      chartDataMachineUsageGrouperPerSecondOut: [],
      chartDataMachineUsageGrouperSelectivity: [],
      chartDataMachineUsageGrouperBytesOfEachRecord: [],

      chartDataOutlierDetectorPerSecondOut: [],
      chartDataOutlierDetectorSelectivity: [],
      chartDataOutlierDetectorBytesOfEachRecord: [],

      //**********************************Traffic Monitoring*************************************************** */ 

      chartDataTrafficEventParserPerSecondOut: [],
      chartDataTrafficEventParserSelectivity: [],
      chartDataTrafficEventParserBytesOfEachRecord: [],

      chartDataRoadMatcherPerSecondOut: [],
      chartDataRoadMatcherSelectivity: [],
      chartDataRoadMatcherBytesOfEachRecord: [],

      chartDataAvgSpeedPerSecondOut: [],
      chartDataAvgSpeedSelectivity: [],
      chartDataAvgSpeedBytesOfEachRecord: [],

      chartDataFormatterPerSecondOut: [],
      chartDataFormatterSelectivity: [],
      chartDataFormatterBytesOfEachRecord: [],
    }
  },
  methods: {

    job() {
    },

    millisToMinutesAndSeconds(millis) {
      var minutes = Math.floor(millis / 60000);
      var seconds = ((millis % 60000) / 1000).toFixed(0);
      return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
    },
    async refresh() {
      console.log("Reached here at refresh")
      await axios
        .get(this.url + ':8000/report/getJobInfo/' + this.cluster_id + '/' + this.$route.params.id)
        .then((resp) => {
          this.jobInfo = JSON.parse(resp.data);

        });

    },
    async refresh1() {
      console.log("Reached here at refresh1")
      await axios
        .get(this.url + ':8000/report/getJobMetrics/' + this.cluster_id + '/' + this.$route.params.id)
        .then((resp) => {

          this.first_parsed_data = JSON.parse(resp.data);
        });

      this.AllMetrics = JSON.parse(this.first_parsed_data);

      //extracting common metrics
      this.extractCommonMetrics();

      // plotting the common metrics graphs
      this.plotGraph('#chartContainer', this.sinkthroughput_graph_title,'records/sec', this.chartDatasinkthroughput);
      this.plotGraph('#chartContainer1', this.sourcethroughput_graph_title, 'records/sec', this.chartDatasourcethroughput);
      this.plotGraph('#chartContainer2', "End to End latency", 'milliseconds', this.chartDatasourcelatency);
      
      if (Object.is(this.AllMetrics.job_name, "Flink word count job")) {


        let operator1 = "tokenizer"
        let operator2 = "counter"

        this.extractJobSpecificMetrics(this.chartDataTokenPerSecondOut, this.chartDataTokenSelectivity, this.chartDataTokenBytesOfEachRecord, operator1);
 
        this.plotGraph('#chartContainer3', 'Tokenizer_Throughput','records/sec', this.chartDataTokenPerSecondOut)
        this.plotGraph('#chartContainer4', 'Tokenizer_Selectivity', 'rec out/rec in',  this.chartDataTokenSelectivity)
        this.plotGraph('#chartContainer5', 'Tokenizer_BytesPerRec', 'bytes/rec', this.chartDataTokenBytesOfEachRecord)

        this.extractJobSpecificMetrics(this.chartDataCountPerSecondOut, this.chartDatacounterSelectivity, this.chartDatacounterBytesOfEachRecord, operator2);

        this.plotGraph('#chartContainer6', 'Counter_Throughput', 'records/sec', this.chartDataCountPerSecondOut)
        this.plotGraph('#chartContainer7', 'Counter_Selectivity', 'rec out/rec in',this.chartDatacounterSelectivity)
        this.plotGraph('#chartContainer8', 'Counter_BytesPerRec', 'bytes/rec', this.chartDatacounterBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Flink smart grid job")) {

        if ("global average load" in this.AllMetrics) {
          let operator = "global average load"
          this.extractJobSpecificMetrics(this.chartDataGridPerSecondOut, this.chartDataGridSelectivity, this.chartDataGridBytesOfEachRecord, operator);
          this.plotGraph('#chartContainer3', 'GlobalAvgL_Throughput', 'records/sec', this.chartDataGridPerSecondOut)
          this.plotGraph('#chartContainer4', 'GlobalAvgL_Selectivity', 'rec out/rec in', this.chartDataGridSelectivity)
          this.plotGraph('#chartContainer5', 'GlobalAvgL_BytesPerRec','bytes/rec', this.chartDataGridBytesOfEachRecord)

        } else if ("local average load" in this.AllMetrics) {
          let operator = "local average load"
          this.extractJobSpecificMetrics(this.chartDataGridPerSecondOut, this.chartDataGridSelectivity, this.chartDataGridBytesOfEachRecord, operator);
          this.plotGraph('#chartContainer3', 'LocalAvgL_Throughput', 'records/sec', this.chartDataGridPerSecondOut)
          this.plotGraph('#chartContainer4', 'LocalAvgL_Selectivity','rec out/rec in', this.chartDataGridSelectivity)
          this.plotGraph('#chartContainer5', 'LocalAvgL_BytesPerRec', 'bytes/rec',this.chartDataGridBytesOfEachRecord)
        }

      } else if (Object.is(this.AllMetrics.job_name, "Ads Analytics")) {

        let operator1 = "click-parser"
        let operator2 = "impression-parser"
        let operator3 = "clicks-counter"
        let operator4 = "impressions-counter"
        let operator5 = "rollingCTR"

        this.extractJobSpecificMetrics(this.chartDataClickParserPerSecondOut, this.chartDataClickParserSelectivity, this.chartDataClickParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'ClickParser_Throughput', 'records/sec', this.chartDataClickParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'ClickParser_Selectivity', 'rec out/rec in',this.chartDataClickParserSelectivity)
        this.plotGraph('#chartContainer5', 'ClickParser_BytesPerRec', 'bytes/rec', this.chartDataClickParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataImpressionParserPerSecondOut, this.chartDataImpressionParserSelectivity, this.chartDataImpressionParserBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'ImpressionParser_Throughput', 'records/sec', this.chartDataImpressionParserPerSecondOut)
        this.plotGraph('#chartContainer7', 'ImpressionParser_Selectivity','rec out/rec in', this.chartDataImpressionParserSelectivity)
        this.plotGraph('#chartContainer8', 'ImpressionParser_BytesPerRec', 'bytes/rec', this.chartDataImpressionParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataClicksCounterPerSecondOut, this.chartDataClicksCounterSelectivity, this.chartDataClicksCounterBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'ClicksCounter_Throughput', 'records/sec', this.chartDataClicksCounterPerSecondOut)
        this.plotGraph('#chartContainer10', 'ClicksCounter_Selectivity','rec out/rec in', this.chartDataClicksCounterSelectivity)
        this.plotGraph('#chartContainer11', 'ClicksCounter_BytesPerRec', 'bytes/rec',this.chartDataClicksCounterBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataImpressionsCounterPerSecondOut, this.chartDataImpressionsCounterSelectivity, this.chartDataImpressionsCounterBytesOfEachRecord, operator4);
        this.plotGraph('#chartContainer12', 'ImpressionsCounter_Throughput','records/sec', this.chartDataImpressionsCounterPerSecondOut)
        this.plotGraph('#chartContainer13', 'ImpressionsCounter_Selectivity','rec out/rec in', this.chartDataImpressionsCounterSelectivity)
        this.plotGraph('#chartContainer14', 'ImpressionsCounter_BytesPerRec','bytes/rec', this.chartDataImpressionsCounterBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDatarollingCTRPerSecondOut, this.chartDatarollingCTRSelectivity, this.chartDatarollingCTRBytesOfEachRecord, operator5);
        this.plotGraph('#chartContainer15', 'rollingCTR_Throughput','records/sec', this.chartDatarollingCTRPerSecondOut)
        this.plotGraph('#chartContainer16', 'rollingCTR_Selectivity','rec out/rec in', this.chartDatarollingCTRSelectivity)
        this.plotGraph('#chartContainer17', 'rollingCTR_BytesPerRec','bytes/rec', this.chartDatarollingCTRBytesOfEachRecord)
      } else if (Object.is(this.AllMetrics.job_name, "Google Cloud Monitoring")) {

        let operator1 = "parser"

        this.extractJobSpecificMetrics(this.chartDataParserPerSecondOut, this.chartDataParserSelectivity, this.chartDataParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'Parser_Throughput','records/sec', this.chartDataParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'Parser_Selectivity','rec out/rec in', this.chartDataParserSelectivity)
        this.plotGraph('#chartContainer5', 'Parser_BytesPerRec','bytes/rec', this.chartDataParserBytesOfEachRecord)

        if ("average-cpu-per-category" in this.AllMetrics) {
          let operator2 = "average-cpu-per-category"
          this.extractJobSpecificMetrics(this.chartDataAvgCpuCatPerSecondOut, this.chartDataAvgCpuCatSelectivity, this.chartDataAvgCpuCatBytesOfEachRecord, operator2);
          this.plotGraph('#chartContainer6', 'AvgCpuCat_Throughput','records/sec', this.chartDataAvgCpuCatPerSecondOut)
          this.plotGraph('#chartContainer7', 'AvgCpuCat_Selectivity','rec out/rec in', this.chartDataAvgCpuCatSelectivity)
          this.plotGraph('#chartContainer8', 'AvgCpuCat_BytesPerRec','bytes/rec', this.chartDataAvgCpuCatBytesOfEachRecord)

        } else if ("average-cpu-per-job" in this.AllMetrics) {
          let operator2 = "average-cpu-per-job"
          this.extractJobSpecificMetrics(this.chartDataAvgCpuJobPerSecondOut, this.chartDataAvgCpuJobSelectivity, this.chartDataAvgCpuJobBytesOfEachRecord, operator2);
          this.plotGraph('#chartContainer6', 'AvgCpuJob_Throughput','records/sec', this.chartDataAvgCpuJobPerSecondOut)
          this.plotGraph('#chartContainer7', 'AvgCpuJob_Selectivity','rec out/rec in', this.chartDataAvgCpuJobSelectivity)
          this.plotGraph('#chartContainer8', 'AvgCpuJob_BytesPerRec','bytes/rec', this.chartDataAvgCpuJobBytesOfEachRecord)
        }

      } else if (Object.is(this.AllMetrics.job_name, "Sentiment Analysis")) {
        let operator1 = "twitter-parser"
        let operator2 = "twitter-analyser"


        this.extractJobSpecificMetrics(this.chartDataTwitterParserPerSecondOut, this.chartDataTwitterParserSelectivity, this.chartDataTwitterParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'TwitterParser_Throughput','records/sec', this.chartDataTwitterParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'TwitterParser_Selectivity','rec out/rec in', this.chartDataTwitterParserSelectivity)
        this.plotGraph('#chartContainer5', 'TwitterParser_BytesPerRec','bytes/rec', this.chartDataTwitterParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTwitterAnalyserPerSecondOut, this.chartDataTwitterAnalyserSelectivity, this.chartDataTwitterAnalyserBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'TwitterAnalyser_Throughput','records/sec', this.chartDataTwitterAnalyserPerSecondOut)
        this.plotGraph('#chartContainer7', 'TwitterAnalyser_Selectivity','rec out/rec in', this.chartDataTwitterAnalyserSelectivity)
        this.plotGraph('#chartContainer8', 'TwitterAnalyser_BytesPerRec','bytes/rec', this.chartDataTwitterAnalyserBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Spike Detection")) {

        let operator1 = "parser"
        let operator2 = "average-calculator"
        let operator3 = "spike-detector"


        this.extractJobSpecificMetrics(this.chartDataSpikeParserPerSecondOut, this.chartDataSpikeParserSelectivity, this.chartDataSpikeParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'SpikeParser_Throughput','records/sec', this.chartDataSpikeParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'SpikeParser_Selectivity','rec out/rec in', this.chartDataSpikeParserSelectivity)
        this.plotGraph('#chartContainer5', 'SpikeParser_BytesPerRec','bytes/rec', this.chartDataSpikeParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataAvgCalPerSecondOut, this.chartDataAvgCalSelectivity, this.chartDataAvgCalBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'AvgCal_Throughput','records/sec', this.chartDataAvgCalPerSecondOut)
        this.plotGraph('#chartContainer7', 'AvgCal_Selectivity','rec out/rec in', this.chartDataAvgCalSelectivity)
        this.plotGraph('#chartContainer8', 'AvgCal_BytesPerRec','bytes/rec', this.chartDataAvgCalBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataSpikeDetectorPerSecondOut, this.chartDataSpikeDetectorSelectivity, this.chartDataSpikeDetectorBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'SpikeDetector_Throughput','records/sec', this.chartDataSpikeDetectorPerSecondOut)
        this.plotGraph('#chartContainer10', 'SpikeDetector_Selectivity','rec out/rec in', this.chartDataSpikeDetectorSelectivity)
        this.plotGraph('#chartContainer11', 'SpikeDetector_BytesPerRec','bytes/rec', this.chartDataSpikeDetectorBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Logs Processing")) {

        let operator1 = "Log-parser"
        let operator2 = "volume-counter"
        let operator3 = "status-counter"


        this.extractJobSpecificMetrics(this.chartDataLogAnalyzerParserPerSecondOut, this.chartDataLogAnalyzerParserSelectivity, this.chartDataLogAnalyzerParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'LogAnalyzerParser_Throughput','records/sec', this.chartDataLogAnalyzerParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'LogAnalyzerParser_Selectivity','rec out/rec in', this.chartDataLogAnalyzerParserSelectivity)
        this.plotGraph('#chartContainer5', 'LogAnalyzerParser_BytesPerRec','bytes/rec', this.chartDataLogAnalyzerParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataLogAnalyzerVolumePerSecondOut, this.chartDataLogAnalyzerVolumeSelectivity, this.chartDataLogAnalyzerVolumeBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'LogAnalyzerVolume_Throughput','records/sec', this.chartDataLogAnalyzerVolumePerSecondOut)
        this.plotGraph('#chartContainer7', 'LogAnalyzerVolume_Selectivity','rec out/rec in', this.chartDataLogAnalyzerVolumeSelectivity)
        this.plotGraph('#chartContainer8', 'LogAnalyzerVolume_BytesPerRec','bytes/rec', this.chartDataLogAnalyzerVolumeBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataLogAnalyzerStatusPerSecondOut, this.chartDataLogAnalyzerStatusSelectivity, this.chartDataLogAnalyzerStatusBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'LogAnalyzerStatus_Throughput','records/sec', this.chartDataLogAnalyzerStatusPerSecondOut)
        this.plotGraph('#chartContainer10', 'LogAnalyzerStatus_Selectivity','rec out/rec in', this.chartDataLogAnalyzerStatusSelectivity)
        this.plotGraph('#chartContainer11', 'LogAnalyzerStatus_BytesPerRec','bytes/rec', this.chartDataLogAnalyzerStatusBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Bargain Index")) {

        let operator1 = "quote-parser"
        let operator2 = "VWAP-operator"
        let operator3 = "bargain-index-calculator"


        this.extractJobSpecificMetrics(this.chartDataBargainIndexParserPerSecondOut, this.chartDataBargainIndexParserSelectivity, this.chartDataBargainIndexParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'BargainIndexParser_Throughput','records/sec', this.chartDataBargainIndexParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'BargainIndexParser_Selectivity','rec out/rec in', this.chartDataBargainIndexParserSelectivity)
        this.plotGraph('#chartContainer5', 'BargainIndexParser_BytesPerRec','bytes/rec', this.chartDataBargainIndexParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataBargainIndexVWAPPerSecondOut, this.chartDataBargainIndexVWAPSelectivity, this.chartDataBargainIndexVWAPBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'BargainIndexVWAP_Throughput','records/sec', this.chartDataBargainIndexVWAPPerSecondOut)
        this.plotGraph('#chartContainer7', 'BargainIndexVWAP_Selectivity','rec out/rec in', this.chartDataBargainIndexVWAPSelectivity)
        this.plotGraph('#chartContainer8', 'BargainIndexVWAP_BytesPerRec','bytes/rec', this.chartDataBargainIndexVWAPBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataBargainIndexCalcPerSecondOut, this.chartDataBargainIndexCalcSelectivity, this.chartDataBargainIndexCalcBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'BargainIndexCalc_Throughput','records/sec', this.chartDataBargainIndexCalcPerSecondOut)
        this.plotGraph('#chartContainer10', 'BargainIndexCalc_Selectivity','rec out/rec in', this.chartDataBargainIndexCalcSelectivity)
        this.plotGraph('#chartContainer11', 'BargainIndexCalc_BytesPerRec','bytes/rec', this.chartDataBargainIndexCalcBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Click Analytics")) {

        let operator1 = "click-log-parser"
        let operator2 = "repeat-visit"
        let operator3 = "reduce-operation"
        let operator4 = "geography-visit"


        this.extractJobSpecificMetrics(this.chartDataClickAnalyticsParserPerSecondOut, this.chartDataClickAnalyticsParserSelectivity, this.chartDataClickAnalyticsParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'ClickAnalyticsParser_Throughput','records/sec', this.chartDataClickAnalyticsParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'ClickAnalyticsParser_Selectivity','rec out/rec in', this.chartDataClickAnalyticsParserSelectivity)
        this.plotGraph('#chartContainer5', 'ClickAnalyticsParser_BytesPerRec','bytes/rec', this.chartDataClickAnalyticsParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataClickAnalyticsRepeatPerSecondOut, this.chartDataClickAnalyticsRepeatSelectivity, this.chartDataClickAnalyticsRepeatBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'ClickAnalyticsRepeat_Throughput','records/sec', this.chartDataClickAnalyticsRepeatPerSecondOut)
        this.plotGraph('#chartContainer7', 'ClickAnalyticsRepeat_Selectivity','rec out/rec in', this.chartDataClickAnalyticsRepeatSelectivity)
        this.plotGraph('#chartContainer8', 'ClickAnalyticsRepeat_BytesPerRec','bytes/rec', this.chartDataClickAnalyticsRepeatBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataClickAnalyticsReducePerSecondOut, this.chartDataClickAnalyticsReduceSelectivity, this.chartDataClickAnalyticsReduceBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'ClickAnalyticsReduce_Throughput','records/sec', this.chartDataClickAnalyticsReducePerSecondOut)
        this.plotGraph('#chartContainer10', 'ClickAnalyticsReduce_Selectivity','rec out/rec in', this.chartDataClickAnalyticsReduceSelectivity)
        this.plotGraph('#chartContainer11', 'ClickAnalyticsReduce_BytesPerRec','bytes/rec', this.chartDataClickAnalyticsReduceBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataClickAnalyticsGeoPerSecondOut, this.chartDataClickAnalyticsGeoSelectivity, this.chartDataClickAnalyticsGeoBytesOfEachRecord, operator4);
        this.plotGraph('#chartContainer12', 'ClickAnalyticsGeo_Throughput','records/sec', this.chartDataClickAnalyticsGeoPerSecondOut)
        this.plotGraph('#chartContainer13', 'ClickAnalyticsGeo_Selectivity','rec out/rec in', this.chartDataClickAnalyticsGeoSelectivity)
        this.plotGraph('#chartContainer14', 'ClickAnalyticsGeo_BytesPerRec','bytes/rec', this.chartDataClickAnalyticsGeoBytesOfEachRecord)

      } else if (Object.is(this.AllMetrics.job_name, "Trending Topics")) {

        let operator1 = "twitter-parser"
        let operator2 = "topic-extractor"
        let operator3 = "popularity-detector"
        

        this.extractJobSpecificMetrics(this.chartDataTrendingTopicsParserPerSecondOut, this.chartDataTrendingTopicsParserSelectivity, this.chartDataTrendingTopicsParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'TrendingTopicsParser_Throughput','records/sec', this.chartDataTrendingTopicsParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'TrendingTopicsParser_Selectivity','rec out/rec in', this.chartDataTrendingTopicsParserSelectivity)
        this.plotGraph('#chartContainer5', 'TrendingTopicsParser_BytesPerRec','bytes/rec', this.chartDataTrendingTopicsParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTrendingTopicsExtractorPerSecondOut, this.chartDataTrendingTopicsExtractorSelectivity, this.chartDataTrendingTopicsExtractorBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'TrendingTopicsExtractor_Throughput','records/sec', this.chartDataTrendingTopicsExtractorPerSecondOut)
        this.plotGraph('#chartContainer7', 'TrendingTopicsExtractor_Selectivity','rec out/rec in', this.chartDataTrendingTopicsExtractorSelectivity)
        this.plotGraph('#chartContainer8', 'TrendingTopicsExtractor_BytesPerRec','bytes/rec', this.chartDataTrendingTopicsExtractorBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTrendingTopicsFilterPerSecondOut, this.chartDataTrendingTopicsFilterSelectivity, this.chartDataTrendingTopicsFilterBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'TrendingTopicsFilter_Throughput','records/sec', this.chartDataTrendingTopicsFilterPerSecondOut)
        this.plotGraph('#chartContainer10', 'TrendingTopicsFilter_Selectivity','rec out/rec in', this.chartDataTrendingTopicsFilterSelectivity)
        this.plotGraph('#chartContainer11', 'TrendingTopicsFilter_BytesPerRec','bytes/rec', this.chartDataTrendingTopicsFilterBytesOfEachRecord)
        

      } else if (Object.is(this.AllMetrics.job_name, "Linear Road")) {

        let operator1 = "Vehicle-event-parser"
        

        this.extractJobSpecificMetrics(this.chartDataVehicleEventParserPerSecondOut, this.chartDataVehicleEventParserSelectivity, this.chartDataVehicleEventParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'VehicleEventParser_Throughput','records/sec', this.chartDataVehicleEventParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'VehicleEventParser_Selectivity','rec out/rec in', this.chartDataVehicleEventParserSelectivity)
        this.plotGraph('#chartContainer5', 'VehicleEventParser_BytesPerRec','bytes/rec', this.chartDataVehicleEventParserBytesOfEachRecord)
        if ("toll-notification" in this.AllMetrics) {
          let operator2 = "toll-notification"
        this.extractJobSpecificMetrics(this.chartDataTollNotificationPerSecondOut, this.chartDataTollNotificationSelectivity, this.chartDataTollNotificationBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'TollNotification_Throughput','records/sec', this.chartDataTollNotificationPerSecondOut)
        this.plotGraph('#chartContainer7', 'TollNotification_Selectivity','rec out/rec in', this.chartDataTollNotificationSelectivity)
        this.plotGraph('#chartContainer8', 'TollNotification_BytesPerRec','bytes/rec', this.chartDataTollNotificationBytesOfEachRecord)
        }else if ("formatter-toll-notification" in this.AllMetrics) {
          let operator3 = "formatter-toll-notification"
        this.extractJobSpecificMetrics(this.chartDataFormatterTollNotificationPerSecondOut, this.chartDataFormatterTollNotificationSelectivity, this.chartDataFormatterTollNotificationBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'FormatterTollNotification_Throughput','records/sec', this.chartDataFormatterTollNotificationPerSecondOut)
        this.plotGraph('#chartContainer10', 'FormatterTollNotification_Selectivity','rec out/rec in', this.chartDataFormatterTollNotificationSelectivity)
        this.plotGraph('#chartContainer11', 'FormatterTollNotification_BytesPerRec','bytes/rec', this.chartDataFormatterTollNotificationBytesOfEachRecord)
        }else if ("accident-notification" in this.AllMetrics) {
          let operator4 = "accident-notification"
        this.extractJobSpecificMetrics(this.chartDataAccidentNotificationPerSecondOut, this.chartDataAccidentNotificationSelectivity, this.chartDataAccidentNotificationBytesOfEachRecord, operator4);
        this.plotGraph('#chartContainer12', 'AccidentNotification_Throughput','records/sec', this.chartDataAccidentNotificationPerSecondOut)
        this.plotGraph('#chartContainer13', 'AccidentNotification_Selectivity','rec out/rec in', this.chartDataAccidentNotificationSelectivity)
        this.plotGraph('#chartContainer14', 'AccidentNotification_BytesPerRec','bytes/rec', this.chartDataAccidentNotificationBytesOfEachRecord)
        }else if ("formatter-accident-notification" in this.AllMetrics) {
          let operator5 = "formatter-accident-notification"
        this.extractJobSpecificMetrics(this.chartDataFormatterAccidentNotificationPerSecondOut, this.chartDataFormatterAccidentNotificationSelectivity, this.chartDataFormatterAccidentNotificationBytesOfEachRecord, operator5);
        this.plotGraph('#chartContainer15', 'FormatterAccidentNotification_Throughput','records/sec', this.chartDataFormatterAccidentNotificationPerSecondOut)
        this.plotGraph('#chartContainer16', 'FormatterAccidentNotification_Selectivity','rec out/rec in', this.chartDataFormatterAccidentNotificationSelectivity)
        this.plotGraph('#chartContainer17', 'FormatterAccidentNotification_BytesPerRec','bytes/rec', this.chartDataFormatterAccidentNotificationBytesOfEachRecord)
        }else if ("daily-expenditure" in this.AllMetrics) {
          let operator6 = "daily-expenditure"
        this.extractJobSpecificMetrics(this.chartDataDailyExpenditurePerSecondOut, this.chartDataDailyExpenditureSelectivity, this.chartDataDailyExpenditureBytesOfEachRecord, operator6);
        this.plotGraph('#chartContainer18', 'DailyExpenditure_Throughput','records/sec', this.chartDataDailyExpenditurePerSecondOut)
        this.plotGraph('#chartContainer19', 'DailyExpenditure_Selectivity','rec out/rec in', this.chartDataDailyExpenditureSelectivity)
        this.plotGraph('#chartContainer20', 'DailyExpenditure_BytesPerRec','bytes/rec', this.chartDataDailyExpenditureBytesOfEachRecord)
        }else if ("vehicle-report-mapper" in this.AllMetrics) {
          let operator7 = "vehicle-report-mapper"
        this.extractJobSpecificMetrics(this.chartDataVehicleReportMapperPerSecondOut, this.chartDataVehicleReportMapperSelectivity, this.chartDataVehicleReportMapperBytesOfEachRecord, operator7);
        this.plotGraph('#chartContainer21', 'VehicleReportMapper_Throughput','records/sec', this.chartDataVehicleReportMapperPerSecondOut)
        this.plotGraph('#chartContainer22', 'VehicleReportMapper_Selectivity','rec out/rec in', this.chartDataVehicleReportMapperSelectivity)
        this.plotGraph('#chartContainer23', 'VehicleReportMapper_BytesPerRec','bytes/rec', this.chartDataVehicleReportMapperBytesOfEachRecord)
        }

      } else if (Object.is(this.AllMetrics.job_name, "TPCH")) {
  
        let operator1 = "tpch-event-parser"
        let operator2 = "tpch-data-filter"
        let operator3 = "tpch-flat-mapper"
        let operator4 = "priority-counter"
        let operator5 = "formatter"

        this.extractJobSpecificMetrics(this.chartDataTpchEventParserPerSecondOut, this.chartDataTpchEventParserSelectivity, this.chartDataTpchEventParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'TpchEventParser_Throughput','records/sec', this.chartDataTpchEventParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'TpchEventParser_Selectivity','rec out/rec in', this.chartDataTpchEventParserSelectivity)
        this.plotGraph('#chartContainer5', 'TpchEventParser_BytesPerRec','bytes/rec', this.chartDataTpchEventParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTpchDataFilterPerSecondOut, this.chartDataTpchDataFilterSelectivity, this.chartDataTpchDataFilterBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'TpchDataFilter_Throughput','records/sec', this.chartDataTpchDataFilterPerSecondOut)
        this.plotGraph('#chartContainer7', 'TpchDataFilter_Selectivity','rec out/rec in', this.chartDataTpchDataFilterSelectivity)
        this.plotGraph('#chartContainer8', 'TpchDataFilter_BytesPerRec','bytes/rec', this.chartDataTpchDataFilterBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTpchFlatMapperPerSecondOut, this.chartDataTpchFlatMapperSelectivity, this.chartDataTpchFlatMapperBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'TpchFlatMapper_Throughput','records/sec', this.chartDataTpchFlatMapperPerSecondOut)
        this.plotGraph('#chartContainer10', 'TpchFlatMapper_Selectivity','rec out/rec in', this.chartDataTpchFlatMapperSelectivity)
        this.plotGraph('#chartContainer11', 'TpchFlatMapper_BytesPerRec','bytes/rec', this.chartDataTpchFlatMapperBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataPriorityCounterPerSecondOut, this.chartDataPriorityCounterSelectivity, this.chartDataPriorityCounterBytesOfEachRecord, operator4);
        this.plotGraph('#chartContainer9', 'PriorityCounter_Throughput','records/sec', this.chartDataPriorityCounterPerSecondOut)
        this.plotGraph('#chartContainer10', 'PriorityCounter_Selectivity','rec out/rec in', this.chartDataPriorityCounterSelectivity)
        this.plotGraph('#chartContainer11', 'PriorityCounter_BytesPerRec','bytes/rec', this.chartDataPriorityCounterBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataTpchFormatterPerSecondOut, this.chartDataTpchFormatterSelectivity, this.chartDataTpchFormatterBytesOfEachRecord, operator5);
        this.plotGraph('#chartContainer9', 'TpchFormatter_Throughput','records/sec', this.chartDataTpchFormatterPerSecondOut)
        this.plotGraph('#chartContainer10', 'TpchFormatter_Selectivity','rec out/rec in', this.chartDataTpchFormatterSelectivity)
        this.plotGraph('#chartContainer11', 'TpchFormatter_BytesPerRec','bytes/rec', this.chartDataTpchFormatterBytesOfEachRecord)
        

      } else if (Object.is(this.AllMetrics.job_name, "Machine Outlier")) {

        let operator1 = "machine-usage-parser"
        let operator2 = "machine-usage-grouper"
        let operator3 = "outlier-detector"
        

        this.extractJobSpecificMetrics(this.chartDataMachineUsageParserPerSecondOut, this.chartDataMachineUsageParserSelectivity, this.chartDataMachineUsageParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'MachineUsageParser_Throughput','records/sec', this.chartDataMachineUsageParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'MachineUsageParser_Selectivity','rec out/rec in', this.chartDataMachineUsageParserSelectivity)
        this.plotGraph('#chartContainer5', 'MachineUsageParser_BytesPerRec','bytes/rec', this.chartDataMachineUsageParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataMachineUsageGrouperPerSecondOut, this.chartDataMachineUsageGrouperSelectivity, this.chartDataMachineUsageGrouperBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'MachineUsageGrouper_Throughput','records/sec', this.chartDataMachineUsageGrouperPerSecondOut)
        this.plotGraph('#chartContainer7', 'MachineUsageGrouper_Selectivity','rec out/rec in', this.chartDataMachineUsageGrouperSelectivity)
        this.plotGraph('#chartContainer8', 'MachineUsageGrouper_BytesPerRec','bytes/rec', this.chartDataMachineUsageGrouperBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataOutlierDetectorPerSecondOut, this.chartDataOutlierDetectorSelectivity, this.chartDataOutlierDetectorBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'OutlierDetector_Throughput','records/sec', this.chartDataOutlierDetectorPerSecondOut)
        this.plotGraph('#chartContainer10', 'OutlierDetector_Selectivity','rec out/rec in', this.chartDataOutlierDetectorSelectivity)
        this.plotGraph('#chartContainer11', 'OutlierDetector_BytesPerRec','bytes/rec', this.chartDataOutlierDetectorBytesOfEachRecord)
        

      } else if (Object.is(this.AllMetrics.job_name, "Traffic Monitoring")) {

        let operator1 = "traffic-event-parser"
        let operator2 = "road-matcher"
        let operator3 = "avg-speed"
        let operator4 = "formatter"   
        

        this.extractJobSpecificMetrics(this.chartDataTrafficEventParserPerSecondOut, this.chartDataTrafficEventParserSelectivity, this.chartDataTrafficEventParserBytesOfEachRecord, operator1);
        this.plotGraph('#chartContainer3', 'TrafficEventParser_Throughput','records/sec', this.chartDataTrafficEventParserPerSecondOut)
        this.plotGraph('#chartContainer4', 'TrafficEventParser_Selectivity','rec out/rec in', this.chartDataTrafficEventParserSelectivity)
        this.plotGraph('#chartContainer5', 'TrafficEventParser_BytesPerRec','bytes/rec', this.chartDataTrafficEventParserBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataRoadMatcherPerSecondOut, this.chartDataRoadMatcherSelectivity, this.chartDataRoadMatcherBytesOfEachRecord, operator2);
        this.plotGraph('#chartContainer6', 'RoadMatcher_Throughput','records/sec', this.chartDataRoadMatcherPerSecondOut)
        this.plotGraph('#chartContainer7', 'RoadMatcher_Selectivity','rec out/rec in', this.chartDataRoadMatcherSelectivity)
        this.plotGraph('#chartContainer8', 'RoadMatcher_BytesPerRec','bytes/rec', this.chartDataRoadMatcherBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataAvgSpeedPerSecondOut, this.chartDataAvgSpeedSelectivity, this.chartDataAvgSpeedBytesOfEachRecord, operator3);
        this.plotGraph('#chartContainer9', 'AvgSpeed_Throughput','records/sec', this.chartDataAvgSpeedPerSecondOut)
        this.plotGraph('#chartContainer10', 'AvgSpeed_Selectivity','rec out/rec in', this.chartDataAvgSpeedSelectivity)
        this.plotGraph('#chartContainer11', 'AvgSpeed_BytesPerRec','bytes/rec', this.chartDataAvgSpeedBytesOfEachRecord)
        this.extractJobSpecificMetrics(this.chartDataFormatterPerSecondOut, this.chartDataFormatterSelectivity, this.chartDataFormatterBytesOfEachRecord, operator4);
        this.plotGraph('#chartContainer9', 'Formatter_Throughput','records/sec', this.chartDataFormatterPerSecondOut)
        this.plotGraph('#chartContainer10', 'Formatter_Selectivity','rec out/rec in', this.chartDataFormatterSelectivity)
        this.plotGraph('#chartContainer11', 'Formatter_BytesPerRec','bytes/rec', this.chartDataFormatterBytesOfEachRecord)
        
      }
    },
    async results(data_size) {
      var vm = this;
      await axios
        .get(this.url + ':8000/report/getSinkTopicResults/' + this.cluster_id + '/' + this.$route.params.id + '/' + data_size)
        .then((resp) => {
          console.log(resp.data.messages)
          vm.resultOfJob = resp.data.messages;
        });
    },


    plotGraph(div_id, graph_title,yAxisName, chartData) {
      if (this.stopUpdates) return;
      const margin = { top: 60, right: 40, bottom: 30, left: 70 };
      const width = 500 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      let svg = d3.select(div_id).select('svg');
      if (svg.empty()) {
        svg = d3
          .select(div_id)
          .append('svg')
          .attr('width', width + margin.right + margin.right + margin.right)
          .attr('height', height + margin.bottom + margin.bottom + margin.bottom)
          .append('g')
          .attr('transform', `translate(${margin.left}, ${margin.top})`);

        svg.append("text")
          .attr("x", width / 2)
          .attr("y", 0 - (margin.top / 2))
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .style("fill", "white")
          .attr("dy", 10)
          .text(graph_title);

        const xScale = d3
          .scaleTime()
          .range([0, width]);

        const yScale = d3
          .scaleLinear()
          .range([height, 0]);

        const xGrid = d3
          .axisBottom(xScale)
          .tickSize(-height)
          .tickFormat('');

        const yGrid = d3
          .axisLeft(yScale)
          .tickSize(-width)
          .tickFormat('');

        svg
          .append('g')
          .attr('class', 'grid')
          .call(xGrid)
          .attr('transform', `translate(0, ${height})`);

        svg
          .append('g')
          .attr('class', 'grid')
          .call(yGrid);

        svg
          .append('g')
          .attr('class', 'x axis')
          .attr('transform', `translate(0, ${height})`)
          .call(d3.axisBottom(xScale))


        svg
          .append('g')
          .attr('class', 'y axis')
          .call(d3.axisLeft(yScale))

      }

      const xScale = d3
        .scaleTime()
        .range([0, width]);

      const yScale = d3
        .scaleLinear()
        .range([height, 0]);


      const line = d3
        .line()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value));

      xScale.domain(d3.extent(chartData, d => d.time));
      yScale.domain([0, 2 * d3.max(chartData, d => d.value)]);

      svg
        .select('.x.axis')
        .transition()
        .call(d3.axisBottom(xScale));

      svg
        .select('.y.axis')
        .transition()
        .call(d3.axisLeft(yScale))
        .select('text')
        .text(yAxisName)
        .attr("font-size", "1.3em")
        .attr("font-weight","2.5em")
        .attr("transform", "rotate(-90)")
        .attr("x", 0 + 70)
        .attr("y", 0 - margin.left)
        .attr("dy", "1.7em")
        .style("text-anchor", "middle");

      svg
        .selectAll('.line')
        .data([chartData])
        .join('path')
        .attr('class', 'line')
        .transition()
        .attr('d', line)
        .style('stroke', '#73BF69')
        .style('fill', 'none');

    },

    extractCommonMetrics() {
      //operation to extract latency
      this.latency = this.AllMetrics.latency

      let parts = this.latency.split(":");

      let millisecs = +(parts[2].split(".")[1]);


      let seconds = +(parts[2].split(".")[0]) + 60 * +parts[1] + 60 * 60 * +parts[0];
      let addedmilisecs = seconds * 1000 + millisecs;


      // now you have the latency in microseconds, you can use it as the value in chartDatasourcelatency:
      this.chartDatasourcelatency.push({ time: new Date(), value: addedmilisecs });


      // operation to extract sink throughput value

      this.sinkthroughput_graph_title = "Throughput: Sink";
      this.sinkthroughputvalue = parseFloat(this.AllMetrics.persecondoutsink.value);

      let time = new Date();
      this.chartDatasinkthroughput.push({ time, value: this.sinkthroughputvalue });


      //operation to extract source throughput value

      this.sourcethroughput_graph_title = "Records_Out/Sec Source";
      this.sourcethroughputvalue = parseFloat(this.AllMetrics.persecondoutsource.value);

      time = new Date();
      this.chartDatasourcethroughput.push({ time, value: this.sourcethroughputvalue });

    },
    extractJobSpecificMetrics(chartDataOperatorPerSecondOut, chartDataOperatorSelectivity, chartDataOperatorBytesOfEachRecord, operator_name) {
      let operatorRecOutPerSec = 0;
      let operatorSelectivity = 0;
      let operatorBytesOfEachRecord = 0;
      let operatorAvgRecOut = 0;
      let operatorAvgSelectivity = 0;
      let operatorAvgBytesOfEachRecord = 0;

      let time = new Date();
      for (let i = 0; i < this.AllMetrics[operator_name].length; i++) {
        operatorRecOutPerSec += parseFloat(Object.values(this.AllMetrics[operator_name][i])[0].value);
        operatorSelectivity += parseFloat(Object.values(this.AllMetrics[operator_name][i])[1]);
        operatorBytesOfEachRecord += parseFloat(Object.values(this.AllMetrics[operator_name][i])[2]);
      }

      operatorAvgRecOut = operatorRecOutPerSec / this.AllMetrics[operator_name].length
      chartDataOperatorPerSecondOut.push({ time, value: operatorAvgRecOut })
      operatorAvgSelectivity = operatorSelectivity / this.AllMetrics[operator_name].length
      chartDataOperatorSelectivity.push({ time, value: operatorAvgSelectivity })
      operatorAvgBytesOfEachRecord = operatorBytesOfEachRecord / this.AllMetrics[operator_name].length
      chartDataOperatorBytesOfEachRecord.push({ time, value: operatorAvgBytesOfEachRecord })

    },
  
  },



  created: async function () {
    console.log("Here")
    await this.refresh()
    
    this.timerjobInfo = setInterval(async () => {
      console.log("Inside set interval")
      await this.refresh()


    }, 60000)
    this.timerjobMetrics = setInterval(async () => {

      await this.refresh1()

    }, 2000)
    await this.results('partial')
  },

  destroyed: function () {
    clearInterval(this.timerjobInfo)
    clearInterval(this.timerjobMetrics)
  },
  computed: {
    cluster_id: {
      get() {
        return this.$store.state.cluster_id;
      },
      set(value) {
        this.$store.commit('setClusterId', value);
      },
    },
    main_node_ip: {
      get() {
        return this.$store.state.main_node_ip;
      },
      set(value) {
        this.$store.commit('setMainNodeIP', value);
      },
    }
  },

}
</script>

<style>
.graph-column {
  padding: 10px;
}

.grid line {
  stroke: rgb(37, 35, 35);
  stroke-opacity: 0.7;
  shape-rendering: crispEdges;
}

svg {
  background-color: black;
}

.y text {
  fill: white;
}

.x text {
  fill: white;
}
</style>