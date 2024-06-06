<template>
    <div>
        <v-hover v-slot:default="{ hover }">
            <v-card class="my-6 pa-0" color="white" :elevation="hover ? 24 : 6">
                <v-card-title>
                    <v-sheet color="primary" elevation="24"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                        <h3>Data Generator</h3>
                    </v-sheet>
                </v-card-title>
                <v-card-subtitle>
                    Implementing the new zero-shot generator flink architecture
                </v-card-subtitle>
                <v-card-text class="mt-6">
                    <v-container>
                        <v-card flat>
                            <v-card-text class="text-align ma-2">
                                <v-form>
                                    <v-row>
                                        <v-col>
                                            <v-select v-model="deployMode" label="Deployment Mode"
                                                :items="['Local', 'Distributed']" outlined>

                                            </v-select>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-select v-model="mode" label="Mode"
                                                :items="['train', 'test', 'randomspikedetection', 'filespikedetection', 'alternativespikedetection', 'smartgrid', 'advertisement', 'searchheuristic']"
                                                outlined></v-select>
                                        </v-col>
                                        <v-col v-if="mode == 'train'">
                                            <v-select v-model="templatesTrain" label="templates" :items="trainTemplates"
                                                item-text="name" item-value="id" outlined multiple></v-select>
                                        </v-col>
                                        <v-col v-if="mode == 'test'">

                                            <v-select v-model="templatesTest" label="templates" :items="testTemplates"
                                                item-text="name" item-value="id" outlined></v-select>
                                        </v-col>
                                    </v-row>

                                    <v-row>
                                        <v-col>
                                            <v-text-field outlined label="Number of topologies" v-model="numTop"
                                                type="number" min="0">

                                            </v-text-field>
                                        </v-col>
                                        <v-col>
                                            <v-text-field outlined label="execution time for a query in seconds"
                                                v-model="execTime" type="number" min="0">

                                            </v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-select v-model="enumStrategy" label="Enumeration Strategy"
                                                :items="['RANDOM', 'EXHAUSTIV', 'RULEBASED', 'MINAVGMAX', 'INCREASING', 'PARAMETERBASED', 'SHPREDICTIVECOMPARISON']"
                                                outlined></v-select>
                                        </v-col>
                                        <v-col v-if="enumStrategy == 'PARAMETERBASED'">
                                            <v-text-field outlined label="Parallelism" v-model="parallelism" type="number"
                                                min="0"></v-text-field>
                                        </v-col>
                                        <v-col v-if="enumStrategy == 'EXHAUSTIV'">
                                            <v-text-field outlined label="Exhaustive Parallelism Step Size"
                                                v-model="exhaustiveParallelismStepSize" type="number" min="0"></v-text-field>
                                        </v-col>
                                        <v-col v-if="enumStrategy == 'INCREASING'">
                                            <v-text-field outlined label="Increasing Parallelism Step Size"
                                                v-model="increasingStepSize" type="number" min="0"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-switch v-if="mode == 'train' && enumStrategy != ''" v-model="isDetermin"
                                        label="Deterministic" color="success" value="true" hide-details></v-switch>
                                    <v-switch v-if="mode == 'train' && enumStrategy != ''" v-model="useAllOper"
                                        label="Use all operators" color="success" value="true" hide-details></v-switch>

                                </v-form>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn class="primary pa-2" small @click="runPlanGeneratorFlink()">Deploy</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-container>
                </v-card-text>
                <v-card class="my-6 pa-0" color="white" v-if="showResults == true">
                    <v-card-title>
                        <v-sheet color="primary" elevation="24"
                            class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                            <h3>Results</h3>
                        </v-sheet>
                    </v-card-title>
                    <v-card-text class="mt-6"  style="font-size: 20px;">
                        Please click on the download button below to get the results.
                    </v-card-text>
                        <v-card-actions>
                            <v-btn variant="text" color="success" @click="downloadFile()">
                                Download
                            </v-btn>
                            <v-btn variant="text" color="success" @click="showLogs()">
                                Show logs
                            </v-btn>
                        </v-card-actions>

                        



                    
                </v-card>

            </v-card>

        </v-hover>
        <v-dialog width="50%" v-model="showProgress">
            <v-card color="primary">
                <v-card-title class="white--text">Please wait <v-progress-linear color="deep-purple green" indeterminate
                        rounded height="6"></v-progress-linear></v-card-title>
                <v-card-text color="primary">
                    <v-list dense color="primary" class="white--text">
                        <v-list-item class="white--text">
                            Running plan Generator with each topology and template
                        </v-list-item>
                        <v-list-item class="white--text">
                            This might take some time.
                        </v-list-item>
                        <v-list-item class="white--text">
                            You can download the results below after the execution is finished.
                        </v-list-item>

                    </v-list>
                </v-card-text>

            </v-card>
        </v-dialog>
        <v-dialog width="50%" v-model="showLogsDialogue">
            <v-card color="primary">
                <v-card-title class="white--text">logs</v-card-title>
                <v-card-text color="primary" class="white--text">
                    {{ this.output }}
                </v-card-text>

            </v-card>
        </v-dialog>
        <!-- mdi-download -->
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'DataGenerator',
    data() {
        return {
            increasingStepSize:'',
            showLogsDialogue: false,
            output: null,
            showResults: false,
            showProgress: false,
            url: process.env.VUE_APP_URL,
            deployMode: '',
            mode: '',
            templatesTrain: [],
            templatesTest: '',
            numTop: '',
            execTime: '',
            enumStrategy: '',
            parallelism: '',
            exhaustiveParallelismStepSize: '',
            isDetermin: false, //think about the v-model
            useAllOper: false, //think about the v-model
            headers: [
                { text: 'Node\'s host name', value: 'hostname' },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            nodes: [],
            addNodeDialog: false,
            nodeHostName: '',
            trainTemplates: [{
                id: 'template1',
                name: 'template1 - linear query',
            }, {
                id: 'template2',
                name: 'template2- two way join',
            }, {
                id: 'template3',
                name: 'template3 - three way join',
            }],
            testTemplates: [{
                id: 'testA',
                name: 'Tuple width extrapolation',
            }, {
                id: 'testB',
                name: 'Event rate extrapolation',
            }, {
                id: 'testC',
                name: 'Time-based window extrapolation',
            }, {
                id: 'testD',
                name: 'Count-based window extrapolation',
            }, {
                id: 'testE',
                name: 'Synthetic Queries extrapolation',
            }],




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
        }
    },
    methods: {
        async runPlanGeneratorFlink() {
            this.showProgress = true;
            var data = {
                "deployMode": this.deployMode,
                "mode": this.mode,
                "numberOfTopol": this.numTop,
                "executionTime": this.execTime,
                "enumerationStrategy": this.enumStrategy,
            }

            if (this.mode == 'train') {

                data["traintempl"] = this.templatesTrain

                if (this.isDetermin == 'true') {
                    data["deterministic"] = this.isDetermin
                }
                if (this.useAllOper == 'true') {
                    data["useAllOperators"] = this.useAllOper
                }

            } else if (this.mode == 'test') {
                data["testtempl"] = this.templatesTest
            }
            if (this.exhaustiveParallelismStepSize != '') {
                data["exhaustiveParallelismStepSize"] = this.exhaustiveParallelismStepSize
            }
            if (this.parallelism != '') {
                data["parallelism"] = this.parallelism
            }
            if (this.increasingStepSize != '') {
                data["increasingStepSize"] = this.increasingStepSize
            }

            console.log(data);
            await axios
                .post(this.url + ":8000/datagen/runplangenerator", data)
                .then((resp) => {
                    this.showProgress = false;
                    var respData = resp.data
                    console.log(respData)
                    this.snackbar = {
                        view: true,
                        timeout: 8000,
                        text: resp.data.status,
                        color: 'success'
                    };
                    this.showResults = true;
                    this.output = resp.data.output

                })
                .catch((err) => {
                    console.log(err)
                })


        },
        async addNodefn() {
            this.nodes.push({ 'hostname': this.nodeHostName, 'actions': '' })
        },
        deleteItem(node) {
            this.indexOfItem = this.nodes.indexOf(node)
            this.nodes.splice(this.indexOfItem, 1)
        },
        downloadFile() {

            if (this.deployMode == 'Local') {
                window.open(this.url + ":8000/datagen/download/local", '_blank')
            } else if (this.deployMode == 'Distributed') {
                window.open(this.url + ":8000/datagen/download/distributed", '_blank')
            }
        },
        showLogs() {
            if (this.output != null) {
                this.showLogsDialogue = true
            }

        }

    }
}
</script>
<style></style>