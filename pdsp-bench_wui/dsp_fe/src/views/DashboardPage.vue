<template>
   <v-app>
    <v-card>
        <v-navigation-drawer v-model="drawer" dark color="primary" app :permanent="false"  :mini-variant.sync="mini">
  
              <v-img  :src="app_logo" style="max-width:30%; margin-left: 30%;"></v-img>
          
          <v-divider v-if="!mini" class="ma-0" />
  
          <v-list nav>
            <div v-for="(link,i) in links" :key="i">
              <v-list-item-group v-if="link.subLinks">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>{{ link.icon }}</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ link.text }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <div v-for="(subLink,i) in link.subLinks" :key="i">
                  <v-list-item v-if="!mini" :to="subLink.to" class="ml-16">
                    <v-list-item-icon>
                      <v-icon>{{ subLink.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ subLink.text }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </div>
              </v-list-item-group>
              <v-list-item-group v-else>
                <v-list-item :to="link.to">
                  <v-list-item-icon>
                    <v-icon>{{ link.icon }}</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ link.text }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </div>
          </v-list>
          
        </v-navigation-drawer>
        
      </v-card>
      <v-main>
        <v-app-bar color="primary" height="70%" app>
          <v-btn v-if="(drawer===false)" class="ml-3 mr-4" elevation="1" fab small @click.stop="drawer=true">
            <v-icon>
              mdi-dots-vertical
            </v-icon>
          </v-btn>
          <v-spacer />
          <v-toolbar-title >
            <b class="white--text">PDSP-Bench Benchmarking System</b>
          </v-toolbar-title>
  
          
          <v-spacer></v-spacer>
          
          <v-img class="mx-2" :src="df_logo" max-width="100" max-height="40"></v-img>
          <v-img class="mx-2" :src="tud_logo" max-width="100" max-height="40"></v-img>
          <v-img class="mx-2" :src="maki_logo" max-width="110" max-height="40"></v-img>
          
        </v-app-bar>
      
        
        <v-parallax class="" style="height:1000;" src="https://cdn.vuetifyjs.com/images/parallax/material.jpg">
          <div class="pa-8 " style="height:1000;" @click="mini=true;">
          
          <router-view default="ExploreInstances" />
         
        </div></v-parallax>
        
        
      </v-main>
   </v-app> 
</template>
<script>
import applogo from '@/assets/app_logo.png';
import dflogo from '@/assets/DFKI_Logo.png';
import tudlogo from '@/assets/tud_logo.png';
import makilogo from '@/assets/maki_editlogo.png';
export default {
    name: 'DashboardPage',
	data() {
		return {
      df_logo:dflogo,
			app_logo:applogo,
      tud_logo:tudlogo,
      maki_logo:makilogo,
			drawer:true,
			mini:false,
			links: [{
				to: '/dashboard/exploreCloudlabNodes',
				icon: 'mdi-network',
				text: 'Explore Nodes',
			},{
				to: '/dashboard/createCluster',
				icon: 'mdi-wrench',
				text: 'Create Cluster',
			},{
				to: '/dashboard/exploreClusters',
				icon: 'mdi-chart-bubble',
				text: 'Explore Cluster',
			},{
				to: '/dashboard/exploreJobs',
				icon: 'mdi-collage',
				text: 'Explore Jobs',
			},
      {
				to: '/dashboard/dataAnalysis',
				icon: 'mdi-chart-bar',
				text: 'Data Analysis',
			},
      
      {
				to: '/dashboard/dataGenNodes',
				icon: 'mdi-cloud',
				text: 'PQP Cluster',
			},
      {
				to: '/dashboard/dataGen',
				icon: 'mdi-engine',
				text: 'PQP Generator',
			},{
				to: '/dashboard/mlDataVis',
				icon: 'mdi-chart-bar',
				text: 'ML Data Viz',
			}]
      }
    },
  
  
}
</script>
<style>


</style>