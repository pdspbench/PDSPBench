<template>
    <div>
        

        <v-hover v-slot:default="{ hover }"> 
        <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6" >
            <v-card-title>
                <v-sheet color="primary" elevation="16"
                  class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                  <h3>Explore All Clusters</h3>
                </v-sheet>
            </v-card-title>
            <v-card-text>
                <v-row>
                   <v-col v-if="showidle">
                    <v-sheet 
                    color="secondary" 
                    elevation="16"
                    height="150"
                    class="justify-center  pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                    <h3>No running clusters at the moment !</h3>
                </v-sheet>
                   </v-col>
                   
                
                    <v-col v-for="cluster in list_of_all_clusters" :key="cluster.id" cols="4">

 <v-hover v-slot:default="{ hover }">                     
  <v-card :elevation="hover ? 24 : 6"
    :loading="loading"
    class="mx-auto my-12"
    max-width="374"
  >
    <template slot="progress">
      <v-progress-linear
        color="deep-purple"
        height="10"
        indeterminate
      ></v-progress-linear>
    </template>

    <v-img
      height="250"
      src="../../assets/Apache.png"
    ></v-img>

    <v-card-title>Cluster name: 
    
        <span>{{cluster.name }} </span>
    </v-card-title>                           
    
    <v-card-text>
      

     
      <div><b>Creation date: {{ clusterDate(cluster.creation_date) }}</b></div>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>

    <v-card-title>Cluster Status</v-card-title>

    <v-card-text>
      <v-chip-group
        column
      >
        <v-chip v-if="cluster.status == 'Running'"  color="success">Running</v-chip>

        <v-chip v-if="cluster.status == 'Stopped'">Stopped</v-chip>

       
      </v-chip-group>
    </v-card-text>

    <v-card-actions>
      <v-btn
        color="primary"
        text
        @click="deleteCluster(cluster)"
      >
        Delete
      </v-btn>
      <v-btn
        color="primary"
        text
        @click="viewMore(cluster)"
      >
        View more
      </v-btn>

     
    </v-card-actions>
  </v-card>
 </v-hover>

                        <!-- old one -->
                        
                    </v-col>
                    
                </v-row>
                
            </v-card-text>
            
        </v-card>
        </v-hover>
        
        <cluster-info @refresh="refresh()" v-if="showClusterInfo == true" :id="selectedClusterId" ></cluster-info>
        
    </div>
</template>
<script>
import ClusterInfo from "@/components/ClusterInfo.vue";
import axios from 'axios';
export default {
    name: 'ExploreClusters',
    components: {
        ClusterInfo
    },
    data(){
        return {
            url: process.env.VUE_APP_URL,
            loading: false,
            showidle:true,
            list_of_all_clusters: [],
            showClusterInfo: false,
            selectedClusterId: ''
        }   
    },
    
    computed:{
        snackbar: {
          get() {
            return this.$store.state.snackbar;
          },
          set(value) {
            this.$store.commit('setSnackbar', value);
          },
        },
        cluster_id: {
          get() {
            return this.$store.state.cluster_id;
          },
          set(value) {
            this.$store.commit('setClusterId', value);
          }
        }
    },
    methods:{
        
        async viewMore(cluster){
            
            this.showClusterInfo = true;
            this.selectedClusterId = cluster.id;
        },
        async deleteCluster(cluster){
            await axios
            .delete(this.url+":8000/infra/delete/"+cluster.id)
            .then(async (resp)=>{
                console.log(resp)
                this.loading = true
                setTimeout(() => (this.loading = false), 2000)
                this.snackbar = {
					view: true,
					timeout: 3000,
					text: 'Deleted the cluster successfully',
					color: 'primary'
				};
                this.refresh()
            })
            .catch((err)=>{
                console.log(err)
                this.snackbar = {
					view: true,
					timeout: 3000,
					text: 'Could not delete the cluster ',
					color: 'error'
				};
            })  
        },
        async refresh() {
            
            await axios
            .get(this.url+":8000/infra/getAll/1")
            .then((resp)=>{
                
                console.log(resp)  
                this.list_of_all_clusters = resp.data.list_of_cluster;
                if(this.list_of_all_clusters.length == 0){
                    this.showidle = true
                }else{
                    this.showidle = !this.showidle
                }
            })
        },
        clusterDate(clusterdate){
            let date = new Date(clusterdate)
            return date.toLocaleString()
        } 
    },
    //whenever this component (explorecluster.vue) is loaded the mounted method is executed at the first.
    async mounted(){
        
        this.refresh();
        
    }
}
</script>
<style>

</style>