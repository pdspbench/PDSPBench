<template>
  <v-app>
    <div id="app" >
      <router-view />
    </div>
    <!--Snackbar global variable is used here-->
    <v-snackbar
      v-model="snackbar.view"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
    >
      {{ snackbar.text }}

      <template #action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.view = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  
    
   
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
  computed:{
    snackbar: {
			get() {
				return this.$store.state.snackbar;
			},
			set(value) {
				this.$store.commit('setSnackbar', value);
			},
		},
    loader: {
			get() {
        
				return this.$store.state.loader;
			},
			set(value) {
				this.$store.commit('setLoader', value);
			},
		},
  }
};
</script>
<style>
/* vietnamese */
@font-face {
  font-family: 'Quicksand';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(assets/quicksand_vt.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Quicksand';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(assets/quicksand_ltext.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Quicksand';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(assets/quicksand_lt.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}

div {
  font-family: "Quicksand", sans-serif;
}
