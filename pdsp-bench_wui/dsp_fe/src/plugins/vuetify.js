import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import '@mdi/font/css/materialdesignicons.css';
import theme from '../config/theme';
Vue.use(Vuetify);

export default new Vuetify({
	
	theme: {
		dark: theme.globalTheme === 'dark',
		options: {
			customProperties: true,
		},
		themes: {
			dark: theme.dark,
			light: theme.light,
		},
	},
	icons: {
		iconfont: 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg',
	},
});
