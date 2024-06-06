import Vuex from 'vuex';
import Vue from 'vue';
Vue.use(Vuex);
const store = new Vuex.Store({
	state: {

		
		// UID
		uid: -11,
		cluster_id:1,
		main_node_ip:'',
		// Snackbar for quick display of small info. used in App.vue
		snackbar: {
			view: false,
			color: 'primary',
			text: '',
			timeout: 3000,
		},

		// Loader for quick UX
		loader: {
			view: false,
			text: ''
		}

	},
	// Mutations of above state variables
	mutations: {
    
		setUID(state, newUID) {
			state.uid = newUID;
		},

		setSnackbar(state, nSnackbar) {
			state.snackbar = nSnackbar;
		},

		setLoader(state, nLoader) {
			state.loader = nLoader;
		},
		setClusterId(state, nClusterId) {
			state.cluster_id = nClusterId;
		},
		setMainNodeIP(state, nMainNodeIP) {
			state.main_node_ip = nMainNodeIP;
		}

	},
	actions: {},
	modules: {},

	getters: {},
});

export default store;
