export default {
	// global theme for the app
	globalTheme: 'light', // light | dark

	// side menu theme, use global theme or custom
	menuTheme: 'global', // global | light | dark

	// toolbar theme, use global theme or custom
	toolbarTheme: 'global', // global | light | dark

	// show toolbar detached from top
	isToolbarDetached: false,

	// wrap pages content with a max-width
	isContentBoxed: false,

	// application is right to left
	isRTL: false,

	// dark theme colors
	dark: {
		background: '#363636',
		surface: '#363636',
		primary: '#376196',
		secondary: '#829099',
		accent: '#82B1FF',
		error: '#E53935',
		info: '#2196F3',
		success: '#4CAF50',
		warning: '#FFC107',
	},

	// light theme colors
	light: {
		background: '#ffffff',
		surface: '#f2f5f8',
		primary: '#263238',
		secondary: '#455A64',
		accent: '#048ba8',
		error: '#E53935',
		info: '#2196F3',
		success: '#4CAF50',
		warning: '#ffd166',
	},
};
