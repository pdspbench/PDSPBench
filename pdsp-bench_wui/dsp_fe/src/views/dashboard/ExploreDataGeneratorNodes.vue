<template>
    <div>
        <v-hover class="mt-12" v-slot:default="{ hover }">
            <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6">
                <v-card-title>
                    <v-sheet color="primary" elevation="16"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                        <h3>Explore Data Generator Cluster</h3>
                    </v-sheet>
                </v-card-title>
                <v-card-text>

                    <v-text-field v-model="searchTerm" placeholder="Search"></v-text-field>
                    <v-data-table :headers="clustertableheaders" :items="clusters" :search="searchTerm"
                        class="flex-grow-1 elevation-1" item-key="cluster_name" show-expand>
                        <template v-slot:expanded-item="{ headers, item }">
                            <v-container>
                                <td :colspan="headers.length">
                                    <p v-for="(value, key) in item" :key="key">
                                        <b v-if="key != 'action'">{{ key }}: {{ value }}</b>
                                    </p>
                                </td>


                            </v-container>
                        </template>
                        <template #[`item.action`]="{ item }">
                           
                                 <div class="actions">
                                    
                                    <v-col-3 >
                                        <v-btn color="error" @click="deleteCluster(item)" small>
                                            Delete
                                        </v-btn>
                                    </v-col-3>
                                    <v-col-3>

                                        <v-btn color="primary" @click="deployCluster(item)" small>
                                            Deploy
                                        </v-btn>
                                    </v-col-3>
                                    <v-col-3>
                                        <v-btn v-if="deployLogs == true" variant="text" color="success" @click="showLogs()"
                                            small>
                                            Deployment logs
                                        </v-btn>
                                    </v-col-3>

                               

                               </div>
                            
                        </template>

                    </v-data-table>
                </v-card-text>
            </v-card>
        </v-hover>
        <v-hover class="mt-12" v-slot:default="{ hover }">
            <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6">
                <v-card-title>
                    <v-sheet color="primary" elevation="16"
                        class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                        <h3>Add Data Generator Cluster</h3>


                    </v-sheet>
                </v-card-title>

                <v-card-text class="pa-10">
                    <v-row class="mt-6">
                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cluster_name" label="Cluster name"
                                outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cluster_master_node"
                                label="Cluster's Master node" outlined clearable></v-text-field>
                        </v-col>

                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cluster_username"
                                label="Cluster's Username'" outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cluster_dockerhub_repo_name"
                                label="Cluster's dockerhub repo name" outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field background-color="white" color="black" v-model="cluster_dockerhub_username"
                                label="Cluster's dockerhub username" outlined clearable></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-textarea background-color="white" color="black"
                                v-model="cluster_dockerhub_registry_readwrite_key"
                                label="Cluster's dockerhub registry read write key" outlined clearable></v-textarea>
                        </v-col>
                        <v-col cols="6">
                            <v-textarea background-color="white" color="black"
                                v-model="cluster_dockerhub_registry_readonly_key"
                                label="Cluster's dockerhub registry read only key" outlined clearable></v-textarea>
                        </v-col>
                        <v-col cols="6">
                            <v-textarea background-color="white" color="black" v-model="cluster_private_key"
                                label="Cluster's private key" outlined clearable></v-textarea>
                        </v-col>
                    </v-row>
                    <v-container class="text-center">
                        <v-btn color="primary" dark class="mb-2" @click="addWorkerNodeDialog = true">
                            Add Worker node
                        </v-btn>
                        <v-data-table :headers="workernodetableheaders" :items="cluster_worker_nodes">
                            <template v-slot:[`item.actions`]="{ item }">
                                <v-icon small @click="deleteWorkerNode(item)">
                                    mdi-delete
                                </v-icon>
                            </template>
                        </v-data-table>
                    </v-container>

                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" class="ma-4" elevation="3" @click="createCluster()">
                        <b>Create Cluster</b>
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-hover>
        <v-dialog width="50%" v-model="addWorkerNodeDialog">
            <v-card class="pa-2" dark>
                <v-card-title>Worker Nodes</v-card-title>
                <v-card-text>
                    <v-text-field outlined label="Worker Node's Host name" v-model="nodeWorkerName" clearable />

                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn small class="success" @click="addWorkerNodeDialog = false; addWorkerNode();"> Add worker
                        node</v-btn>

                </v-card-actions>

            </v-card>
        </v-dialog>
        <v-dialog width="50%" v-model=" showProgress ">
            <v-card color="primary">
                <v-card-title class="white--text">Please wait <v-progress-linear color="deep-purple green" indeterminate
                        rounded height="6"></v-progress-linear></v-card-title>
                <v-card-text color="primary">
                    <v-list dense color="primary" class="white--text">
                        <v-list-item class="white--text">
                            Creating Remote Cluster key
                        </v-list-item>
                        <v-list-item class="white--text">
                            Writing Master Node file
                        </v-list-item>
                        <v-list-item class="white--text">
                            Writing Worker Node File
                        </v-list-item>
                        <v-list-item class="white--text">
                            Processing Dockerhub Information
                        </v-list-item>
                        <v-list-item class="white--text">
                            Setting up Kubernetes cluster
                        </v-list-item>
                        <v-list-item class="white--text">
                            Starting Flink and Plan Generator on Kubernetes cluster
                        </v-list-item>
                        <v-list-item class="white--text">
                            This might take 15-20 minutes....
                        </v-list-item>

                    </v-list>
                </v-card-text>

            </v-card>
        </v-dialog>
        <v-dialog width="50%" v-model=" showLogsDialogue ">
            <v-card color="primary">
                <v-card-title class="white--text">logs</v-card-title>
                <v-card-text color="primary" class="white--text">
                    {{ this.output }}
                </v-card-text>

            </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'ExploreCloudlabNode',
    data() {
        return {
            showLogsDialogue: false,
            output: null,
            deployLogs: false,
            showProgress: false,
            addWorkerNodeDialog: false,
            nodeWorkerName: '',
            cluster_worker_nodes: [],
            url: process.env.VUE_APP_URL,
            workernodetableheaders: [
                { text: "Worker Node domain", align: 'left', value: 'worker_node' },
                { text: "Action", value: 'actions' }
            ],

            clusters: [],
            cluster_name: '',
            cluster_master_node: '',
            cluster_username: '',
            cluster_dockerhub_username: '',
            cluster_dockerhub_repo_name: '',
            cluster_dockerhub_registry_readwrite_key: '',
            cluster_dockerhub_registry_readonly_key: '',
            cluster_private_key: '',
            searchTerm: '',
            clustertableheaders: [
                { text: "Cluster's Name", align: 'left', value: 'cluster_name' },
                { text: "Cluster's Username", align: 'left', value: 'cluster_username' },
                { text: "Cluster's Dockerhub username", align: 'left', value: 'cluster_dockerhub_username' },
                { text: "Cluster's Dockerhub repo name", align: 'left', value: 'cluster_dockerhub_repo_name' },
                { text: "Master Node", align: 'left', value: 'cluster_master_node' },
                { text: "Worker Nodes", align: 'left', value: 'cluster_worker_nodes' },
                { text: "Action", value: 'action' }
            ]

        }
    },
    async mounted() {
        this.refresh();
    },
    methods: {

        async addWorkerNode() {
            this.cluster_worker_nodes.push({ 'worker_node': this.nodeWorkerName, 'actions': '' })
        },
        deleteWorkerNode(node) {
            this.indexOfItem = this.cluster_worker_nodes.indexOf(node)
            this.cluster_worker_nodes.splice(this.indexOfItem, 1)
        },
        async createCluster() {
            var sendData = {
                'cluster_name': this.cluster_name,
                'cluster_username': this.cluster_username,
                'cluster_dockerhub_username': this.cluster_dockerhub_username,
                'cluster_dockerhub_repo_name': this.cluster_dockerhub_repo_name,
                'cluster_dockerhub_registry_readwrite_key': this.cluster_dockerhub_registry_readwrite_key,
                'cluster_dockerhub_registry_readonly_key': this.cluster_dockerhub_registry_readonly_key,
                'cluster_master_node': this.cluster_master_node,
                'cluster_worker_nodes': this.cluster_worker_nodes,
                'cluster_private_key': this.cluster_private_key,
                'action': ''
            }
            await axios
                .post(this.url + ":8000/datagen/clustercreate", sendData)
                .then((resp) => {

                    console.log(resp.data);
                    console.log(resp);
                    if (resp.data.success) {
                        this.snackbar = {
                            view: true,
                            timeout: 8000,
                            text: resp.data.status,
                            color: 'success'
                        };

                    }
                })
                .catch((err) => {
                    console.log(err)
                })
            this.refresh();
        },
        async deleteCluster(cluster) {
            var sendData = {
                'cluster_name': cluster.cluster_name
            }
            await axios
                .delete(this.url + ":8000/datagen/clustercreate", { data: sendData })
                .then((resp) => {

                    var respData = resp.data.list_of_clusters

                    this.clusters = respData


                })
                .catch((err) => {
                    console.log(err)
                })
            this.refresh();

        },
        async deployCluster(cluster) {
            this.showProgress = true;
            var sendData = {
                'cluster_name': cluster.cluster_name,
                'cluster_username': cluster.cluster_username,
                'cluster_dockerhub_username': cluster.cluster_dockerhub_username,
                'cluster_dockerhub_repo_name': cluster.cluster_dockerhub_repo_name,
                'cluster_dockerhub_registry_readwrite_key': cluster.cluster_dockerhub_registry_readwrite_key,
                'cluster_dockerhub_registry_readonly_key': cluster.cluster_dockerhub_registry_readonly_key,
                'cluster_master_node': cluster.cluster_master_node,
                'cluster_worker_nodes': cluster.cluster_worker_nodes,
                'cluster_private_key': cluster.cluster_private_key,
            }
            await axios
                .post(this.url + ":8000/datagen/clusterdeploy", sendData)
                .then((resp) => {
                    this.showProgress = false;
                    this.deployLogs = true;
                    var respData = resp.data
                    console.log(respData)
                    if (respData.success) {
                        this.snackbar = {
                            view: true,
                            timeout: 8000,
                            text: respData.status,
                            color: 'success'
                        };

                    }
                    this.output = resp.data.output
                })
                .catch((err) => {
                    console.log(err)
                })


        },
        async refresh() {
            await axios
                .get(this.url + ":8000/datagen/clustercreate")
                .then((resp) => {

                    var respData = resp.data.list_of_clusters

                    this.clusters = respData


                })
                .catch((err) => {
                    console.log(err)
                })
        },
        showLogs() {
            if (this.output != null) {
                this.showLogsDialogue = true
            }

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
}
</script>
<style></style>