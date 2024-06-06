import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router';
import store from './store/index';

import LandingPage from '@/views/LandingPage.vue';
import DashboardPage from '@/views/DashboardPage.vue';
import ExploreClusters from '@/views/dashboard/ExploreClusters.vue';
import ExploreJobs from '@/views/dashboard/ExploreJobs.vue';
import ExploreCloudlabNodes from '@/views/dashboard/ExploreCloudlabNode.vue';
import CreateCluster from '@/views/dashboard/CreateCluster.vue';
import RegistrationPage from '@/views/RegistrationPage.vue';
import IndividualJob from '@/views/dashboard/IndividualJob.vue';
import DataAnalysis from '@/views/dashboard/DataAnalysis.vue';
import DataGenerator from '@/views/dashboard/DataGenerator.vue';
import ExploreDataGeneratorNodes from '@/views/dashboard/ExploreDataGeneratorNodes.vue';
import MlDataVis from '@/views/dashboard/MlDataVis.vue';
Vue.config.productionTip = false
Vue.use(VueRouter);

const routes = [
	{ path: '/', component: LandingPage },
	{ path: '/registration', component: RegistrationPage },
	{
		path: '/dashboard',
		component: DashboardPage,
		children: [
			{
				path: '/dashboard/exploreClusters',
				component: ExploreClusters,
			},
			{
				path: '/dashboard/createCluster',
				component: CreateCluster,
			},
			{	
				path: '/dashboard/exploreJobs',
				component: ExploreJobs,
			},
			{
				path: '/dashboard/job/:id',
				component: IndividualJob,
			},
			{
				path: '/dashboard/exploreCloudlabNodes',
				component: ExploreCloudlabNodes 
			},
			{
				path: '/dashboard/dataAnalysis',
				component: DataAnalysis 
			},
			{
				path: '/dashboard/dataGen',
				component: DataGenerator 
			},
			{
				path: '/dashboard/dataGenNodes',
				component: ExploreDataGeneratorNodes 
			},
			{
				path: '/dashboard/mlDataVis',
				component: MlDataVis
			}
		],
	},
];

const router = new VueRouter({
	routes
});

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
