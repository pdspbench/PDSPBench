<template>
    <div>
        <v-hover v-slot:default="{ hover }">
        <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6" >
            <v-card-title>
                <v-sheet color="primary" elevation="16"
                  class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                  <h3>Explore Jobs</h3>
                </v-sheet>
            </v-card-title>
            <v-card-text>
                
                <v-text-field 
                    v-model="searchTerm" 
                    placeholder="Search" 
                ></v-text-field>
                <v-data-table 
                    v-model="jobtable"
                    :headers="headers" 
                    :items="jobs" 
                    :search="searchTerm"
                    class="flex-grow-1 "  
                    item-key="name" 
                    >
                    
                    <template #[`item.last-modification`]="{ item }">
                        <div class="actions">
                            <v-btn class="ma-2" color="primary" @click="viewMore(item)" small>
                                View more
                            </v-btn>
                            
                        </div>
                    </template>
              
            </v-data-table>
            </v-card-text>
        </v-card>
    </v-hover>
    </div>
</template>
<script>
import axios from 'axios';
import { saveAs } from 'file-saver';
export default {
    name: 'ExploreJobs',
    data(){
        return {
            jobtable:[],
            url: process.env.VUE_APP_URL,
            headers: [
				{ text: "Job name", align: 'left', value: 'name' },
                { text: "Cluster's main node", align:'left', value:'main_node_ip'},
                { text: "Cluster's ID", align:'left', value:'cluster'},
                { text: "Job ID", align:'left', value:'jid'},
				{ text: "State", value: 'state' },
				{ text: "Submitted time", value: 'start-time' },
                { text: "Tasks", value: 'tasks.total' },
				{ text: "Actions", sortable: false, align: 'right', value: 'last-modification' }
			],
            jobs:[],
            searchTerm:''

        }
    },
    async mounted(){
        await axios
            .get(this.url+":8000/report/getAll/1")
            .then((resp)=>{
                console.log(resp)
                var respData = resp.data
                this.jobs = respData['jobs']
                console.log(this.jobs);
            })
            .catch((err)=>{
                console.log(err)
            })
    },
    methods:{
        viewMore(job){
            console.log(job);
            this.cluster_id = job.cluster;
            this.main_node_ip = job.main_node_ip;
            this.$router.push('job/'+job['jid']);
        },
        async downloadFile(job){
            console.log("ghh")
            await axios
                .get(this.url+':8000/report/getSinkTopicResults/'+job['cluster'] + 
                    '/'+job['jid']+'/full')
            .then((resp)=>{
                console.log(resp.data.messages)
                const jsonString = JSON.stringify(resp.data.messages);
                const blob = new Blob([jsonString], { type: 'text/plain;charset=utf-8'})
                saveAs(blob,'result.txt')
            });
      }
    },
    computed:{
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

</style>