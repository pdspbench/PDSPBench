<template>
    <div>
        <v-hover class="mt-12" v-slot:default="{ hover }">
        <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6" >
            <v-card-title>
                <v-sheet color="primary" elevation="16"
                  class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                  <h3>Explore Cloudlab Nodes</h3>
                </v-sheet>
            </v-card-title>
            <v-card-text>
                
                <v-text-field 
                    v-model="searchTerm" 
                    placeholder="Search" 
                ></v-text-field>
                <v-data-table 
                    v-model="nodetable"
                    :headers="headers" 
                    :items="nodes" 
                    :search="searchTerm"
                    class="flex-grow-1 "  
                    item-key="domain_name" 
                    >
                    
                    <template #[`item.action`]="{ item }">
                        <div class="actions">
                            
                            <v-btn  color="error" @click="deleteNode(item)" small>
                                Delete
                            </v-btn>
                        </div>
                    </template>
              
            </v-data-table>
            </v-card-text>
        </v-card>
        </v-hover>
        <v-hover class="mt-12" v-slot:default="{ hover }">
            <v-card class="my-6 pa-0" :elevation="hover ? 24 : 6" >
                <v-card-title>
                    <v-sheet color="primary" elevation="16"
                      class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
                      <h3>Add cloudlab node</h3>
                      

                    </v-sheet>
                </v-card-title>

                <v-card-text>
                    <v-row class="mt-6">
                       <v-col cols="6">
                            <v-text-field 
                                background-color="white"
                                color="black"
                                v-model="domain_name"
                                label="Node domain name"
                                outlined
                                clearable
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field 
                                background-color="white"
                                color="black"
                                v-model="user"
                                label="User name"
                                outlined
                                clearable
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    
              
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" class="ma-4" elevation="3" @click="addNode()">
                        <v-icon>mdi-plus</v-icon><b>Add node</b>
                    </v-btn>
                </v-card-actions>
            </v-card>
            </v-hover>
            
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'ExploreCloudlabNode',
    data(){
        return {
            nodetable:[],
            url: process.env.VUE_APP_URL,
            headers: [
				{ text: "Node domain", align: 'left', value: 'domain_name' },
				{ text: "User", align: 'left', value: 'user' },
				{ text: "Created time", value: 'creation_date' },
                { text: "Action", value:'action'}
			],
            nodes:[],
            searchTerm:'',
            user:'',
            be_ssh:'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3usQTaEKg6vGtapFu8aALvc6NbRfFZqTVcA0RfAQyBs1sX1D3CCEkW1fj0gk6pRvVZmE6prbYlH32PWxUYoIBL0tXKsSoJbSYyH/xcbjxQjysYradyq4ZW5w9FM+CFSFb4uCfe0554L1NDA80a1P3Cd1mvXlNXWlwwRpcD+qr9wEOD6XUWlCp4d8pk+73Dk/8zyOETyPLF1g68RyQEaprWqrDiA/HXdE5pgpTVzJ0+NhaN14yxr9nX5K6OlFNAOcw+8HhLeXwqmfKN67q1RpvQrjSTZvXXSe+iDsxIFCm8j9whpovzHpwEhhpWtMgil8DfgfgPK9twlCPpIpLhnrQcXJg9wJEwXDzMF7/A22ZJJ+IZPzD+VGI85OuvLjvNcUmz7L/R3Zfd7jAsbiKGw/5+mTXrY6gr0n3ul99fhY9dsaUwDJ6jpANz8C/kQ2LUM7GUI83nhZxgT2ObzZFmmbnQrFks4Q/69okXIZWakq0XjFUkec45fz+9OxR4T9390c= legion@legion',
            domain_name:''
        }
    },
    async mounted(){
        this.refresh();
    },
    methods:{
        async addNode(){
            var post_data = {
                "domain_name":this.domain_name,
                "user": this.user
            }
            await axios
                    .post(this.url+":8000/infra/create/node/1",post_data)
                    .then(async (response) => {
                        
                        var resp = await response.data;
                        if(resp.success){
                            this.snackbar = {
                                view: true,
                                timeout: 3000,
                                text: resp.status,
                                color: 'primary'
                            };
                        }
                        this.refresh()
                    })
                    .catch((err) => {
                        
                        this.snackbar = {
                            view: true,
                            timeout: 8000,
                            text: err.response.data.status,
                            color: 'error'
                        };
                    });

        },
        async deleteNode(node){
            console.log(node);
            await axios
                .delete(this.url+":8000/infra/node/delete/"+node['domain_name'])
                .then((resp)=> {
                    this.snackbar = {
                        view: true,
                        timeout: 3000,
                        text: resp.status,
                        color: 'primary'
                    };
                    this.refresh();

                })
                .catch((err)=>{
                    console.log(err)
                })

        },
        async refresh(){
            await axios
            .get(this.url+":8000/infra/getAll/nodes/1")
            .then((resp)=>{
                
                var respData = resp.data.list_of_nodes
                
                this.nodes = respData
                console.log(this.nodes)
                
            })
            .catch((err)=>{
                console.log(err)
            })
        }
    }
}
</script>
<style>

</style>