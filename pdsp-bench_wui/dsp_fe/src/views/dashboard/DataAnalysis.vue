<template>
    <div>
        
            <v-card class="my-6 pa-0" color="white" elevation="24px">
                <v-card-title>
                    <v-sheet color="primary" elevation="24"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                        <h3>Data Analysis</h3>
                    </v-sheet>
                </v-card-title>
                <v-card-subtitle class="text-right">
                    <v-btn v-if="array_of_individual_user_selections.length>=2" color="primary" class="ma-4" elevation="3"
                        @click="showComparisonOptions()">
                        <v-icon>mdi-plus</v-icon><b>Compare</b>
                    </v-btn>
                </v-card-subtitle>
                <v-card-text>
                    <v-form ref="formingMetrics">
                        <v-row class="mt-6">
                            <v-col cols="3">
                                <v-select background-color="white" color="black" v-model="cname"
                                    :items="list_of_all_clusters" item-text="name" item-value="id" label="Select Cluster"
                                    outlined @change="onSelectCluster"></v-select>
                            </v-col>
                            <v-col cols="3">
                                <v-select background-color="white" v-model="job" :items="jobs" item-text="full_name"
                                    item-value="jid" label="Select Job" outlined @change="getJobOperators"></v-select>
                            </v-col>
                            <v-col cols="3">
                                <v-select background-color="white" v-model="analysis_of" :items="list_of_analysis_options"
                                    label="Analysis of ?" outlined @input="onSelectAnalysisOption"></v-select>
                            </v-col>
                            <v-col cols="3" v-if="showQueryMetrics">
                                <v-select background-color="white" v-model="chosen_query_metrics"
                                    :items="list_of_query_metrics" label="Metrics list" outlined></v-select>
                            </v-col>
                            <v-row class="mt-6" v-else-if="showOperatorMetrics">
                                <v-col cols="3">
                                    <v-select background-color="white" v-model="chosen_operator" :items="list_of_operators"
                                        item-text="name" item-value="id" label="Operator list" outlined @change="saveOpName" ></v-select>
                                </v-col>
                                <v-col cols="3">
                                    <v-select background-color="white" v-model="chosen_operator_metrics"
                                        :items="list_of_operator_metrics" label="Metrics list" outlined></v-select>
                                </v-col>
                            </v-row>
                        </v-row>
                    </v-form>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :disabled="isBtnDisabled" color="primary" class="ma-4" elevation="3"
                        @click="plotIndividualGraph()">
                        <v-icon>mdi-plus</v-icon><b>Plot Graph</b>
                    </v-btn>
                </v-card-actions>


            </v-card>
            
        <v-card class="my-12 pa-0" color="white" elevation="24">
            <v-card-title>
                <v-sheet color="primary" elevation="24"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                    <h3>Individual charts</h3>
                </v-sheet>
            </v-card-title>
            <v-card-text>
                <v-row>
                    <v-col v-for="chart,index in array_of_individual_user_selections" :key="index">
                        <div class="pa-3" :id="'chartContainer'+index"></div>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card> 
        
        <v-card class="my-12 pa-0" color="white" elevation="24">
            <v-card-title>
                <v-sheet color="primary" elevation="24"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                    <h3>Compare charts</h3>
                </v-sheet>
            </v-card-title>
            <v-card-text>
                <v-row>
                    <v-col v-for="chart,index in array_of_compare_user_selection" :key="index">
                        <div class ="pa-3" :id="'comparechartContainer'+index"></div>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <v-dialog 
            
            v-model="showCompareDialog"
            persistent
            max-width="500"
            
            class="primary">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Compare Metrics</span>
                </v-card-title>
                <v-card-text> 
                    <div v-for="selectInput,index in array_of_individual_user_selections" :key="index">
                        <v-checkbox
                            v-model="selected"
                            
                            
                            :value="selectInput"
                        >
                            <template v-slot:label>
                                <v-card class="w-full" dark>
                                    <v-card-text>
                                        ClusterId:{{ selectInput.selected_clusterId }}<br/>
                                        JobId: {{ selectInput.selected_jobId }}<br/>
                                        Anaylsis_type: {{ selectInput.selected_analysis_type }}<br/>
                                        <div v-if="selectInput.selected_analysis_type==='Entire Query'">
                                        Query_Metrics: {{ selectInput.selected_query_metrics }}<br/>
                                        </div>
                                        <div v-else>
                                        Selected_Operator_id: {{ selectInput.selected_operator }}
                                        Selected_Operator_metrics: {{ selectInput.selected_operator_metrics }}    
                                        </div>
                                    </v-card-text>
                                </v-card>
                            </template>
                        </v-checkbox>
                        
                    </div>  
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn class="error mr-2" small @click="showCompareDialog=false"> Close </v-btn>
                    <v-btn class="success mr-2" small @click="finishCompareInputs() "> Finish </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios';
import * as d3 from 'd3';

export default {
    name: 'DataAnalysis',
    data() {
        return {
            jobGivenName:'',
            selected: [],
            showCompareDialog: false,
            name_of_clusters: [],
            url: process.env.VUE_APP_URL,
            list_of_all_clusters: [],
            list_of_jobs: [],
            list_of_analysis_options: ['Entire Query', 'Operator'],
            list_of_query_metrics: ['Latency', 'Throughput', 'N/W Utilization', 'CPU Utilization', 'Memory Utilization'],
            list_of_operators: [],
            list_of_operator_metrics: ['Processing Latency 98th percentile', 'Processing Latency 95th percentile', 'Selectivity', 'Processing Latency median'],
            cname: null,
            job: '',
            jid: '',
            cluster_main_node_ip: '',
            jobInfo: {},
            jobs: [],
            jobsAndOperators: [
                {
                    name: 'Flink word count job',
                    operators: [
                        { name: "tokenizer" },
                        { name: "counter" },
                    ]
                },
                {
                    name: 'Flink smart grid job',
                    operators: [
                        { name: "global average load" },
                        { name: "local average load" },
                    ]
                },
                {
                    name: 'Ads Analytics',
                    operators: [
                        { name: "click-parser" },
                        { name: "impression-parser" },
                        { name: "clicks-counter" },
                        { name: "impressions-counter" },
                        { name: "rollingCTR" },
                    ]
                },
                {
                    name: 'Google Cloud Monitoring',
                    operators: [
                        { name: "parser" },
                        { name: "average-cpu-per-category" },
                        { name: "average-cpu-per-job" },

                    ]
                },
                {
                    name: "Sentiment Analysis",
                    operators: [
                        { name: "twitter-parser" },
                        { name: "twitter-analyser" },

                    ]
                },
                {
                    name: "Spike Detection",
                    operators: [
                        { name: "parser" },
                        { name: "average-calculator" },
                        { name: "spike-detector" },

                    ]
                },
                {
                    name: "Logs Processing",
                    operators: [
                        { name: "Log-parser" },
                        { name: "volume-counter" },
                        { name: "status-counter" },
                        

                    ]
                },
                {
                    name: "Trending Topics",
                    operators: [
                        { name: "twitter-parser" },
                        { name: "topic-extractor" },
                        { name: "popularity-detector" },
                        

                    ]
                },
                {
                    name: "Bargain Index",
                    operators: [
                        { name: "quote-parser" },
                        { name: "VWAP-operator" },
                        { name: "bargain-index-calculator" },

                    ]
                },
                {
                    name: "Click Analytics",
                    operators: [
                        { name: "click-log-parser" },
                        { name: "repeat-visit" },
                        { name: "reduce-operation" },
                        { name: "geography-visit" },
                        
                    ]
                },
                {
                    name: "Linear Road", 
                    operators: [
                        { name: "Vehicle-event-parser" },
                        { name: "toll-notification" },
                        { name: "formatter-toll-notification" },
                        { name: "accident-notification"},
                        { name: "formatter-accident-notification" },
                        { name: "daily-expenditure" },
                        { name: "vehicle-report-mapper" }, 
                         
                    ]
                },
                {
                    name: "TPCH",
                    operators: [
                        { name: "tpch-event-parser" },
                        { name: "tpch-data-filter"},
                        { name: "tpch-flat-mapper"},
                        { name: "priority-counter" },
                        { name: "formatter" },
                    ]
                },
                {
                    name: "Machine Outlier",
                    operators: [
                        { name: "machine-usage-parser"},
                        { name: "machine-usage-grouper"},
                        { name: "outlier-detector"},
                        
                    ]
                },
                {
                    name: "Traffic Monitoring",
                    operators: [
                        { name: "traffic-event-parser"},
                        { name: "road-matcher"},
                        { name: "avg-speed"},
                        { name: "formatter"},
                        
                    ]
                },
            ],
            analysis_of: '',
            chosen_query_metrics: null,
            chosen_operator: '',
            chosen_operator_metrics: null,
            showQueryMetrics: false,
            showOperatorMetrics: false,
            array_of_individual_user_selections: [],
            array_of_compare_user_selection:[],
            graphs: [],
            opName:'',
            parallOp:'',
            givenOpName:''


        }
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
        isBtnDisabled() {
            return this.chosen_query_metrics === null && this.chosen_operator_metrics === null;
        }
    },
    methods: {
        async showComparisonOptions(){
            this.showCompareDialog = true;
        },
        async finishCompareInputs() {
            this.array_of_compare_user_selection.push(this.selected)
            this.showCompareDialog=false;
            console.log(this.selected)
            await axios

                .post(this.url + ':8000/report/getCompareGraphData', this.selected)
                .then(async (resp) => {
                    await resp.data;
                    console.log("data from backend for comparison plot");
                    console.log(resp.data);
                    var container2DisplayOn = "#comparechartContainer" + (this.array_of_compare_user_selection.length-1)
                if(this.selected[0]["selected_analysis_type"]=="Operator"){
                    if (this.selected[0]["selected_operator_metrics"]=="Selectivity") {
                        var barData = {}
                        for(var bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            var intermediateData = resp.data[bardatacount]
                            
                            
                            barData = Object.assign({}, barData, intermediateData)
                            
                        }
                        this.plotHistogram(container2DisplayOn, 'Selectivity', barData, 'Operators', 'Selectivity')
                        return
                    }else if(this.selected[0]["selected_operator_metrics"]=="Processing Latency 98th percentile") {
                        console.log('in 98th percentile');
                        barData = {}
                        for(bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            barData = Object.assign({}, barData, intermediateData)   
                        }
                        this.plotHistogram(container2DisplayOn, 'lat-98', barData, 'Operators', 'milliseconds')
                        return
                        
                    }else if(this.selected[0]["selected_operator_metrics"]=="Processing Latency 95th percentile") {
                        console.log('in 95th percentile');
                        barData = {}
                        for(bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            barData = Object.assign({}, barData, intermediateData)   
                        }
                        this.plotHistogram(container2DisplayOn, 'lat-95', barData, 'Operators', 'milliseconds')
                        return
                    }else if(this.selected[0]["selected_operator_metrics"]=="Processing Latency median") {
                        console.log('median');
                        barData = {}
                        for(bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            barData = Object.assign({}, barData, intermediateData)   
                        }
                        this.plotHistogram(container2DisplayOn, 'lat-median', barData, 'Operators', 'milliseconds')
                        return
                    }
                }else if(this.selected[0]["selected_analysis_type"]=="Entire Query"){
                    console.log(resp.data)
                    if(this.selected[0]["selected_query_metrics"]=="Throughput"){
                        barData = {}
                        for( bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            
                            
                            barData = Object.assign({}, barData, intermediateData)
                            
                        }
                        this.plotHistogram(container2DisplayOn, 'Throughput', barData, 'jobs', 'Records/Sec')
                        return
                    }else if(this.selected[0]["selected_query_metrics"]=="N/W Utilization"){
                         barData = {}
                        for( bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            
                            
                            barData = Object.assign({}, barData, intermediateData)
                            console.log(barData);
                            
                        }
                        this.plotHistogram(container2DisplayOn, 'N/W Usage', barData, 'jobs', 'Bytes/Sec')
                        return

                    }else if (this.selected[0]["selected_query_metrics"]=='CPU Utilization'){
                        barData = {}
                        for( bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            
                            
                            barData = Object.assign({}, barData, intermediateData)
                            
                        }
                        this.plotHistogram(container2DisplayOn, 'CPU Usage', barData, 'jobs', 'CPU %')
                        return

                    }else if (this.selected[0]["selected_query_metrics"]=='Memory Utilization'){
                        barData = {}
                        for( bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            
                            
                            barData = Object.assign({}, barData, intermediateData)
                            
                        }
                        this.plotHistogram(container2DisplayOn, 'Memory Usage', barData, 'jobs', 'Bytes')
                        return

                    }else if(this.selected[0]["selected_query_metrics"]=="Latency"){
                        console.log('E2E Latency');
                        barData = {}
                        for(bardatacount=0; bardatacount < resp.data.length; bardatacount++){
                            intermediateData = resp.data[bardatacount]
                            barData = Object.assign({}, barData, intermediateData)   
                        }
                        console.log(barData);
                        this.plotHistogram(container2DisplayOn, 'E2E Latency', barData, 'jobs', 'milliseconds')
                        return
                    }
                }
                    
                })
        },
        async refresh() {

            await axios
                .get(this.url + ":8000/infra/getAll/1")
                .then((resp) => {
                    this.list_of_all_clusters = resp.data.list_of_cluster;

                })
        },
        async onSelectCluster() {
            this.chosen_operator_metrics = null
            this.chosen_query_metrics = null
            await axios
                .get(this.url + ":8000/report/getThisClusterJobs/" + this.cname)
                .then((resp) => {

                    var respData = resp.data
                    console.log(respData)
                    this.jobs = respData['jobs']
                    console.log('printing all jobs to one cluster');
                    console.log(this.jobs);
                    
                })
                .catch((err) => {
                    console.log(err)
                })

        },
        async getJobOperators() {
            this.chosen_operator_metrics = null
            this.chosen_query_metrics = null
            let each_cluster

            for (each_cluster in this.list_of_all_clusters) {

                if (this.list_of_all_clusters[each_cluster].id == this.cname) {
                    this.cluster_main_node_ip = this.list_of_all_clusters[each_cluster].main_node_ip

                    break;

                }

            }

            let selectedJob = this.jobs.find(job => job.jid === this.job)

            // access the name property of the selected job
            let jobName = selectedJob ? selectedJob.name : ''
            
            const fullJobId = this.job
            const cutJobId = fullJobId.substring(0,4);
            
            const fulljobName = jobName
            const cutjobName = fulljobName.substring(0,3);
            console.log(cutJobId)
            console.log(cutjobName)
            this.jobGivenName =  cutjobName + '-' + cutJobId 

            await axios
                .get(this.url + ':8000/report/getOperatorInfo/' + this.cluster_main_node_ip + '/' + this.job)
                .then((resp) => {


                    this.jobInfo = JSON.parse(resp.data);
                    let vert = this.jobInfo["vertices"]

                    let operators_list = []

                    if (jobName == this.jobsAndOperators[0].name) {
                        let index

                        for (index in vert) {
                            if (vert[index].name.trim() === this.jobsAndOperators[0].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[0].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }
                        }

                        this.list_of_operators = operators_list
                        
                    }
                    if (jobName == this.jobsAndOperators[1].name) {
                        let index

                        for (index in vert) {

                            if (vert[index].name.trim() === this.jobsAndOperators[1].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[1].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list
                    }
                    if (jobName == this.jobsAndOperators[2].name) {
                        let index

                        for (index in vert) {

                            if (vert[index].name.trim() === this.jobsAndOperators[2].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[2].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[2].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[2].operators[3].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[2].operators[4].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[3].name) {
                        let index

                        for (index in vert) {

                            if (vert[index].name.trim() === this.jobsAndOperators[3].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[3].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[3].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }
                        
                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[4].name) {


                        let index

                        for (index in vert) {

                            if (vert[index].name.trim() === this.jobsAndOperators[4].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[4].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list


                    }
                    if (jobName == this.jobsAndOperators[5].name) {

                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[5].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[5].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[5].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[6].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[6].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[6].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[6].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[7].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[7].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[7].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[7].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[8].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[8].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[8].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[8].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[9].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[9].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[9].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[9].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[9].operators[3].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[10].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[10].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[10].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[10].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } 

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[11].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[11].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[11].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[11].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[11].operators[3].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }else if (vert[index].name == this.jobsAndOperators[11].operators[4].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[12].name) {
                        let index


                        for (index in vert) {


                            if (vert[index].name.trim() === this.jobsAndOperators[12].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[12].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[12].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    if (jobName == this.jobsAndOperators[13].name) {
                        let index


                        for (index in vert) {
                            if (vert[index].name.trim() === this.jobsAndOperators[13].operators[0].name.trim()) {

                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[13].operators[1].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[13].operators[2].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            } else if (vert[index].name == this.jobsAndOperators[13].operators[3].name) {
                                operators_list.push({
                                    "name": vert[index].name,
                                    "id": vert[index].id
                                })

                            }

                        }

                        this.list_of_operators = operators_list

                    }
                    console.log('list of operrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr');
                    console.log(this.list_of_operators);
                });

        },
        saveOpName() {
            console.log("save op name called");
            for (const item of this.list_of_operators) {
              if (item.id === this.chosen_operator) {
                this.opName = item.name // Found a matching id, return the corresponding name
                console.log(this.opName);
              }
            }
            return null; // Return null if no match is found
        },
        onSelectAnalysisOption(option) {
            this.chosen_operator_metrics = null
            this.chosen_query_metrics = null

            if (option == 'Entire Query') {
                this.showQueryMetrics = true
                this.showOperatorMetrics = false

            } else if (option == 'Operator') {

                this.showOperatorMetrics = true
                this.showQueryMetrics = false


            }
        },
        async plotIndividualGraph() {
            let form_data = {}
            form_data['selected_clusterId'] = this.cname
            form_data['cluster_main_node_ip'] = this.cluster_main_node_ip
            form_data['selected_jobId'] = this.job
            form_data['selected_analysis_type'] = this.analysis_of

            if (this.analysis_of == 'Entire Query') {
                form_data['selected_query_metrics'] = this.chosen_query_metrics

            } if (this.analysis_of == 'Operator') {

                form_data['selected_operator'] = this.chosen_operator
                form_data['selected_operator_metrics'] = this.chosen_operator_metrics

            }

            this.array_of_individual_user_selections.push(form_data)

            await axios
                .get("http://"+this.cluster_main_node_ip+":8086/v1/jobs/"+this.job)
                .then((resp) => {
                    console.log(resp.data.vertices)
                    const operatorList = resp.data.vertices
                    console.log("operator parallelism found");
                    for (const item of operatorList) {
                      if (item.id === this.chosen_operator) {
                        this.parallOp = item.parallelism // Found a matching id, return the corresponding name
                        console.log(this.parallOp);
                      }
                    }
                })

                 this.givenOpName = this.opName + "-p-" + this.parallOp

            await axios

                .post(this.url + ':8000/report/getIndividualGraphData', form_data)
                .then(async (resp) => {
                    console.log(resp.data)
                    await resp.data;
                    // const responseData = resp.data
                    
                    var incoming_data;
                    var data;
                    var container2DisplayOn;
                    var container2Display;
                    
            if (this.analysis_of == 'Entire Query') {
                    if(this.chosen_query_metrics == "Throughput"){
                       
                        incoming_data = JSON.parse(resp.data)
                        data = JSON.parse(JSON.stringify(incoming_data["data"]["result"])) 
                        const incoming_data_2 = JSON.parse(resp.data)

                    let maxValue = Number.NEGATIVE_INFINITY;

                    incoming_data_2["data"]["result"].forEach(subtask => {
                        subtask["values"].forEach(dataPoint => {
                            const value = parseFloat(dataPoint[1]);
                            maxValue = Math.max(maxValue, value);
                        });
                    });

                    console.log("The largest value among all subtasks is:", maxValue);
                        container2DisplayOn = "#chartContainer" + (this.array_of_individual_user_selections.length-1)
                     
                    this.drawLineGraph(container2DisplayOn, 'Throughput',data,"Time",'Records/Sec',maxValue)
                }else if(this.chosen_query_metrics == 'N/W Utilization'){
                        
                        incoming_data = JSON.parse(resp.data)

                        data = JSON.parse(JSON.stringify(incoming_data["data"]["result"]))
                        const incoming_data_4 = JSON.parse(resp.data)

                    let maxValue4 = Number.NEGATIVE_INFINITY;

                    incoming_data_4["data"]["result"].forEach(host => {
                        host["values"].forEach(dataPoint4 => {
                            const value4 = parseFloat(dataPoint4[1]);
                            maxValue4 = Math.max(maxValue4, value4);
                        });
                    });

                    console.log("The largest value among all hosts is:", maxValue4);
                       
                        
                       container2DisplayOn = "#chartContainer" + (this.array_of_individual_user_selections.length-1)
                      
                    this.drawLineGraph(container2DisplayOn, 'N/W Utilization',data,"Time","Bytes/Sec",maxValue4)
                } else if(this.chosen_query_metrics == 'CPU Utilization'){
                       
                        incoming_data = JSON.parse(resp.data)

                        data = JSON.parse(JSON.stringify(incoming_data["data"]["result"]))
                        const incoming_data_7 = JSON.parse(resp.data)

                    let maxValue7 = Number.NEGATIVE_INFINITY;

                    incoming_data_7["data"]["result"].forEach(host => {
                        host["values"].forEach(dataPoint7 => {
                            const value7 = parseFloat(dataPoint7[1]);
                            maxValue7 = Math.max(maxValue7, value7);
                        });
                    });

                    console.log("The largest value among all hosts is:", maxValue7);
                        
                       container2DisplayOn = "#chartContainer" + (this.array_of_individual_user_selections.length-1)
                     
                    this.drawLineGraph(container2DisplayOn, 'CPU Utilization',data,"Time","CPU %",maxValue7)
                }else if(this.chosen_query_metrics == 'Memory Utilization'){
                        
                        incoming_data = JSON.parse(resp.data)

                        data = JSON.parse(JSON.stringify(incoming_data["data"]["result"]))
                        const incoming_data_3 = JSON.parse(resp.data)

                    let maxValue3 = Number.NEGATIVE_INFINITY;

                    incoming_data_3["data"]["result"].forEach(host => {
                        host["values"].forEach(dataPoint3 => {
                            const value3 = parseFloat(dataPoint3[1]);
                            maxValue3 = Math.max(maxValue3, value3);
                        });
                    });

                    console.log("The largest value among all hosts is:", maxValue3);
                        
                        
                       container2DisplayOn = "#chartContainer" + (this.array_of_individual_user_selections.length-1)
                     
                    this.drawLineGraph(container2DisplayOn, 'Memory Utilization',data,"Time",'Bytes', maxValue3)
                }else if(this.chosen_query_metrics == 'Latency'){
                        
                    let ne_per = resp.data //ninty eight percentile end to end latency
                    console.log('latency resp');
                    console.log(ne_per.data.result[0].value[1]);
                    let ne_per_etoe = ne_per.data.result[0].value[1]
                    
                    const data = { [this.jobGivenName]:ne_per_etoe};

                        container2Display = "#chartContainer" + (this.array_of_individual_user_selections.length-1)

                        this.plotHistogram(container2Display, 'E2E Latency 98th percentile', data, '',"milliseconds");
                }
            }
            else if (this.analysis_of == 'Operator') {
                    
                if(this.chosen_operator_metrics=="Processing Latency 98th percentile"){
                    let ne_per = resp.data
                    console.log(ne_per);
                    
                    const data = { [this.givenOpName]:ne_per };

                        container2Display = "#chartContainer" + (this.array_of_individual_user_selections.length-1)

                        this.plotHistogram(container2Display, 'Processing Latency 98th percentile', data, 'operators',"milliseconds");
                    

                }else if(this.chosen_operator_metrics=='Processing Latency 95th percentile'){
                    let nf_per = resp.data
                    const data = { [this.givenOpName]:nf_per};

                        container2Display = "#chartContainer" + (this.array_of_individual_user_selections.length-1)

                        this.plotHistogram(container2Display, 'Processing Latency 95th percentile', data, 'operators',"milliseconds");
                    

                }else if(this.chosen_operator_metrics=='Processing Latency median'){
                    let nf_per = resp.data
                    const data = { [this.givenOpName]:nf_per};

                        container2Display = "#chartContainer" + (this.array_of_individual_user_selections.length-1)

                        this.plotHistogram(container2Display, 'Processing Latency median', data, 'operators',"milliseconds");
                    

                }
                else if(this.chosen_operator_metrics=='Selectivity'){
                    let selectivity = resp.data
                    let targetValue = null;

for (let key in selectivity) {
    // eslint-disable-next-line
    if (selectivity.hasOwnProperty(key)) {
        targetValue = selectivity[key];
        break; // Exit the loop after finding the first value
    }
}

console.log(targetValue);
                    
                    const data = { [this.givenOpName]: targetValue};
                    console.log(data);
                    container2Display = "#chartContainer" + (this.array_of_individual_user_selections.length-1)
                       
                    this.plotHistogram(container2Display, 'Selectivity', data, 'operators',"Selectivity");
                
                }
                }
            })
               
        },
        plotHistogram(container, title, data, x_axis_name, y_axis_name) {

            

            let maxValue = Number.NEGATIVE_INFINITY;

            for (const key in data) {
            const value = parseFloat(data[key]);
            maxValue = Math.max(maxValue, value);
            }

            maxValue = Math.ceil(maxValue);
            console.log('The maximum value is:', maxValue);


            const margin = { top: 50, right: 50, bottom: 100, left: 50 };
            const width = 480 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;

            let svg = d3.select(container).select('svg');

            // Create a new SVG element if not already present
            svg = d3
              .select(container)
              .append('svg')
              .attr('width', width + margin.right + margin.right + margin.right + margin.right)
              .attr('height', height + margin.bottom + margin.bottom + margin.bottom)
              .append('g')
              .attr('transform', `translate(${2 * margin.left}, ${margin.top})`);

            svg.append("text")
              .attr("x", width / 2)
              .attr("y", 0 - (margin.top / 2))
              .attr("text-anchor", "middle")
              .style("font-size", "16px")
              .style("fill", "white")
              .attr("dy", 10)
              .text(title);

            const xScale = d3
              .scaleBand()
              .range([0, width])
              .padding(0.1)
              .domain(Object.keys(data));
            //d3.max(Object.values(data))
            const yScale = d3
              .scaleLinear()
              .range([height, 0])
              .domain([0, 1.5 * maxValue])
              .nice();

            svg.append("g")
              .attr("transform", `translate(0, ${height})`)
              .call(d3.axisBottom(xScale)
                .tickSizeOuter(0))
              .selectAll("text")
              .style("fill", "white")
              .attr("transform", "rotate(-45)") // Rotate the x-axis labels by -45 degrees
              .style("text-anchor", "end");

            // Add Y Axis
            svg.append("g")
              .call(d3.axisLeft(yScale)
                .tickSizeOuter(0))
              .selectAll("text")
              .style("fill", "white");

            // Adding x and y gridlines
            svg.append("g")
              .attr("class", "grid")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(xScale)
              .tickSize(-height)
              .tickFormat("")
            );

            svg.append("g")
              .attr("class", "grid")
              .call(d3.axisLeft(yScale)
              .tickSize(-width)
              .tickFormat("")
            );

            // Add the x axis label
            svg.append("text")
              .attr("class", "x-axis-label")
              .attr("x", width / 2)
              .attr("y", height + margin.bottom + 40)
              .attr("text-anchor", "middle")
              .style("fill", "#FFFDD0")
              .attr("dy", "0.5em")
              .text(x_axis_name);

            // Add the y axis label
            svg.append("text")
              .attr("class", "y-axis-label")
              .attr("x", 0 - (height / 2))
              .attr("y", 0 - margin.left - (margin.left / 2))
              .attr("text-anchor", "middle")
              .attr("transform", "rotate(-90)")
              .attr("dy", "0.5em")
              .style("fill", "#FFFDD0")
              .text(y_axis_name);

            const colorScale = d3.scaleOrdinal()
             .domain(Object.keys(data))
             .range(["#ffb3ba", "#baffc9", "#ffffba", "#bae1ff", "#9467bd", "#8c564b", "#e377c2"]);


            svg.selectAll(".bar")
              .data(Object.entries(data))
              .enter().append("rect")
              .attr("class", "bar") // Added class "bar" to the rect elements for easier selection
              .attr("x", d => xScale(d[0])) // Changed x position to use the xScale with the key of the data object
              .attr("y", d => yScale(d[1])) // Changed y position to use the yScale with the value of the data object
              .attr("width", xScale.bandwidth()) // Changed width to use the bandwidth of the xScale
              .attr("height", d => height - yScale(d[1])) // Changed height to be the difference between the height and the yScale value
              .style("fill", (i) => colorScale(i));
            svg.selectAll(".label")
              .data(Object.entries(data))
              .enter().append("text")
              .attr("class", "label")
              .attr("id", d => `label-${d[0]}`) // Set unique ID for each label
              .attr("x", d => xScale(d[0]) + xScale.bandwidth() / 2)
              .attr("y", d => yScale(d[1]) - 25)
              .attr("text-anchor", "middle")
              .style("fill", "white")
              .text(d => parseFloat(d[1]).toFixed(2))
              .style("visibility", "visible");
            },

        drawLineGraph(container_id, title, data, x_axis_name, y_axis_name, max_value) {
            var margin = {top: 50, right: 50, bottom: 50, left: 50},
            width = 480 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;

            // Create the SVG container
            var svg = d3.select(container_id)
              .append("svg")
              .style("background-color", "black")
              .attr("width", width + margin.left + margin.right + margin.right + margin.right)
              .attr("height", height + margin.bottom + margin.bottom + margin.bottom)
              .append("g")
              .attr("transform", "translate(" + (2 * margin.left) + "," + margin.top + ")");

            // Set up the x and y scales
            var xScale = d3.scaleTime()
              .range([0, width]);
            var yScale = d3.scaleLinear()
              .range([height, 0]);

            // Set up the x and y axes
            var xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
            var yAxis = d3.axisLeft(yScale).tickSizeOuter(0);

            // Update the x and y domains based on the data
            var allData = [];
            data.forEach(function(lineData) {
              allData = allData.concat(lineData.values);
            });
            
            xScale.domain(d3.extent(allData, function(d) { return new Date(d[0] * 1000); }));
            yScale.domain([0, 2 * (max_value)]);
            //yScale.domain([0, d3.max(allData, function(d) { return d[1]; })]);
            // Add the x and y axes to the SVG container
            svg.append("g")
              .attr("class", "x-axis")
              .attr("transform", "translate(0," + height + ")")
              .style("fill", "#FFFDD0")

              .call(xAxis);
            svg.append("g")
              .attr("class", "y-axis")
              .style("fill", "#FFFDD0")

              .call(yAxis);
        
            //Add the x and y gridlines
            svg.append("g")
              .attr("class", "grid")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(xScale)
                .tickSize(-height)
                .tickFormat("")
              );

            svg.append("g")
              .attr("class", "grid")
              .call(d3.axisLeft(yScale)
                .tickSize(-width)
                .tickFormat("")
              );

              // Add the title to the graph
              svg.append("text")
                .attr("class", "title")
                .attr("x", (width / 2))
                .attr("y", 0 - (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("fill", "#FFFDD0") 
                .text(title);

              // Add the x axis label
              svg.append("text")
                .attr("class", "x-axis-label")
                .attr("x", width / 2)
                .attr("y", height + margin.bottom - 10)
                .attr("text-anchor", "middle")
                .style("fill", "#FFFDD0") 
                .text(x_axis_name);

              // Add the y axis label
              svg.append("text")
                .attr("class", "y-axis-label")
                .attr("x", 0 - (height / 2))
                .attr("y", 0 - margin.left - (margin.left / 2)- 10)
                .attr("text-anchor", "middle")
                .attr("transform", "rotate(-90)")
                .attr("dy", "0.5em")
                .style("fill", "#FFFDD0") 
                .text(y_axis_name);
              svg.selectAll(".x-axis text")      
                .style("fill", "#FFFDD0");
              svg.selectAll(".y-axis text")
                .attr("dx", "0.5em")
                .style("fill", "#FFFDD0");
          
                // Define a color scale for lines
                var contrastColors = ["#FF5733", "#2ECC71", "#3498DB", "#E74C3C", "#1ABC9C", "#F39C12", "#9B59B6", "#27AE60"];

                var colorSelected = []
                // Loop through the data and draw the line for each line in the graph
                data.forEach(function(lineData, i) {
                  var line = d3.line()
                    .x(function(d) { return xScale(new Date(d[0] * 1000)); })
                  .y(function(d) { return yScale(d[1]); });
                var color_line = contrastColors[i];
                colorSelected.push(color_line)
                svg.append("path")
                  .datum(lineData.values)
                  .attr("class", "line")
                  .attr("d", line)
                  .style("stroke", color_line) // Set the stroke color based on index
                  .style("fill", "none");

                  
              });
             

                var legendContainer = svg.append("g") // This creates a container for the legend
    .attr("class", "legend-container")
    .attr("transform", "translate(" + (width + margin.right - 40) + "," + (margin.top - 60) + ")")
    .style("overflow-y", "auto") // Enable vertical scrolling
    .attr("height", height - margin.top - margin.bottom)
    .attr("height", height);

var legend = legendContainer.selectAll(".legend")
    .data(data.slice(0, 21))
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 15 + ")"; })
    .style("fill", "#FFFDD0");

legend.append("rect")
    .attr("x", 0)
    .attr("width", 5)
    .attr("height", 5)
    .style("fill", function(d, i) { return colorSelected[i]; });

legend.append("text")
    .attr("x", 15)
    .attr("y", 5)
    .attr("dy", ".35em")
    .style("text-anchor", "start")
    .style("fill", "#FFFDD0")
    .style("font-size", "10px")
    .text(function(d) { return (d.metric["host"]).slice(0 , 5); });

        },

        clusterBarGraph(extractData, container){
            
            const margin = { top: 20, right: 30, bottom: 40, left: 50 };
            const width = 600 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;
                    
            const svg = d3.select(container)
              .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("transform", `translate(${margin.left},${margin.top})`);
                    
            const x0 = d3.scaleBand()
              .domain(extractData[0].map(d => d.host))
              .rangeRound([0, width])
              .paddingInner(0.1);
                    
            const x1 = d3.scaleBand()
              .domain([0, 1])
              .rangeRound([0, x0.bandwidth()])
              .padding(0.05);
                    
            const y = d3.scaleLinear()
              .domain([0, d3.max(extractData.flat(), d => d.value)])
              .rangeRound([height, 0]);
                    
            const color = d3.scaleOrdinal()
              .range(["#fcba03", "#8a89a6"]);
                    
            const xAxis = d3.axisBottom(x0);
            const yAxis = d3.axisLeft(y);
                    
            svg.append("g")
              .attr("transform", `translate(0, ${height})`)
              .call(xAxis);
                    
            svg.append("g")
              .call(yAxis);
                    
            const barGroups = svg.selectAll(".barGroup")
              .data(extractData)
              .enter().append("g")
              .attr("class", "barGroup")
              .attr("transform", (d, i) => `translate(${x1(i)},0)`);
                    
            barGroups.selectAll(".bar")
              .data(d => d)
              .enter().append("rect")
              .attr("class", "bar")
              .attr("x", d => x0(d.host))
              .attr("y", d => y(d.value))
              .attr("width", x0.bandwidth() * 0.2)
              .attr("height", d => height - y(d.value))
              .attr("fill", (d, i) => color(i));

        }



   
    },  
    async mounted() {
        this.refresh();
    }
}
</script>
<style>
.legend{
  padding: 2%;
  max-height: 150px;
  overflow-x: scroll;
  border: 1px solid blue;
}

</style>