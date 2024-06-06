<template>
    <div>
        <v-hover v-slot:default="{ hover }">
            <v-card class="my-6 pa-0" color="white" :elevation="hover ? 24 : 6">
                <v-card-title>
                    <v-sheet color="primary" elevation="24"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                        <h3>Create Cluster</h3>
                    </v-sheet>
                </v-card-title>
                <v-card-text>
                    <v-row class="mt-6">
                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cname" label="Cluster name"
                                outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-select background-color="white" v-model="crestype" :items="resourcesTypes"
                                label="Resource Usage" outlined></v-select>
                        </v-col>
                    </v-row>
                    <v-row>

                        <v-col cols="6">
                            <v-text-field background-color="white" v-model="cnumoftmslots" label="Number of task slots"
                                type="number" outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-select background-color="white" v-model="hardwaretype" :items="hwlist"
                                label="select the hardware you chose on cloudlab" outlined></v-select>
                        </v-col>
                    </v-row>
                    <v-row>

                        <v-col cols="6">
                            <v-checkbox v-model="tmSeperateSpace" label="Run Task managers in seperate nodes"></v-checkbox>
                            <v-text-field v-model="cnumoftm" v-if="tmSeperateSpace == true" type="number"
                                label="Number of task managers" outlined></v-text-field>
                        </v-col>
                        <v-col cols="6">

                        </v-col>
                    </v-row>

                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" class="ma-4" elevation="3" @click="createCluster()">
                        <v-icon>mdi-plus</v-icon><b>Create cluster</b>
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-hover>

        <v-dialog width="50%" v-model="showProgress">
            <v-card color="primary">
                <v-card-title class="white--text">Please wait <v-progress-linear color="deep-purple green" indeterminate
                        rounded height="6"></v-progress-linear></v-card-title>
                <v-card-text color="primary">
                    <v-list dense color="primary" class="white--text">
                        <v-list-item class="white--text">
                            Updating configuration files
                        </v-list-item>
                        <v-list-item class="white--text">
                            Starting Flink cluster
                        </v-list-item>
                        <v-list-item class="white--text">
                            Starting Prometheus Server
                        </v-list-item>
                        <v-list-item class="white--text">
                            Starting Grafana Server
                        </v-list-item>
                        <v-list-item class="white--text">
                            Sending Job to the cluster
                        </v-list-item>
                    </v-list>
                </v-card-text>

            </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'CreateCluster',
    data() {
        return {
            hwlist: ['d710','m510','xl170','c6525-25g','c6525-100g'],
            resourcesTypes: ['CPU Only', 'CPU + GPU', 'GPU Only'],
            jobTypes: ['Word Count', 'Smart Grid', 'Ad Analytics'],
            tmSeperateSpace: false,
            url: process.env.VUE_APP_URL,
            hardwaretype: '',
            cname: '',
            crestype: '',
            parallelizationDegree: '',
            cnumoftmslots: '',
            cnumoftm: '',
            showProgress: false,

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
        async createCluster() {
            // the variable that contains cluster name as the user input is being checked if it is not empty.
            if (this.cname.trim().length == 0) {

                // snackbar global variable is changed that is defined in the store/index.js. used in App.vue
                this.snackbar = {
                    view: true,
                    timeout: 10000,
                    text: 'Please check the form',
                    color: 'error'
                };
                return;

            }
            // this variable is set true to show the progress v-dialog
            this.showProgress = true;

            // Collecting the create cluster input data to the data JSON
            var data = {
                "cluster_name": this.cname.trim(),
                "cluster_resource_type": this.crestype,

                "cluster_tm_slots": this.cnumoftmslots,
                "cluster_num_tm": this.cnumoftm,
                "cluster_seperate_space": this.tmSeperateSpace,
                "hardware_cloudlab": this.hardwaretype

            }

            // calling post method to the create cluster end point
            await axios
                .post(this.url + ':8000/infra/create', data)
                .then(async (response) => {
                    this.showProgress = false;
                    var resp = await response.data;
                    if (resp.success) {
                        this.snackbar = {
                            view: true,
                            timeout: 3000,
                            text: resp.status,
                            color: 'primary'
                        };

                    }
                })
                .catch((err) => {
                    this.showProgress = false;
                    this.snackbar = {
                        view: true,
                        timeout: 8000,
                        text: err.response.data.status,
                        color: 'error'
                    };

                });
        }
    }
}
</script>
<style></style>