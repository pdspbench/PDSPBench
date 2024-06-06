<template>
    <v-card class="ma-0 pa-0" max-width="100%" height="100vh">
  
      <v-card-text class="ma-0 pa-0" style="height:100%">
        <v-row style="height:100%" class="ma-0 pa-0">
          <v-col cols="12" class="ma-0 pa-0">
            <v-card width="100%" height="100%" class="pa-16 rounded-lg" :img="bgImg">
  
              <v-card style="position: absolute; top: 50%;left: 50%;transform: translate(-50%, -50%);" width="20%" class="pa-2">
  
                <div class="pa-16 rounded-lg primary">
                  
                    <v-img contain :aspect-ratio="16/9" color="white" :src="dsplogo" ></v-img>
  
                </div>
  
  
                <v-card-text class="mt-4 justify-center">
                <div style="text-align: center;" class="mb-5 text-h5 primary--text"><b>PDSP-Bench Benchmarking System</b></div>
                    <v-text-field
                        v-model="username"
                        label="Username"
                        :rules="nameRules"
                        clearable
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="password"
                        type="password"
                        label="Password"
                        :rules="[rules.required, rules.min]"
                        clearable
                        outlined
                    ></v-text-field>
                    <v-col  v-if="problem" >
                    <v-alert 
                      dense
                      outlined
                      :type=alerttype
                    >
                    {{problemmsg}}
                    </v-alert>
                  </v-col>
                    <v-btn color="warning" small rounded text @click="$router.push('/')">
                        Forgot Password
                    </v-btn>

                  <v-btn color="primary"  class="mt-6" block rounded small @click="loginUser()">
                    
                    <b> Login </b>
                  </v-btn>
                </v-card-text>
  
                <v-divider class="mx-4"></v-divider>
  
  
  
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" small rounded text @click="$router.push('/registration')" >
                        Register
                    </v-btn>
                </v-card-actions>
              </v-card>
  
            </v-card>
          </v-col>
  
        </v-row>
  
      </v-card-text>
    </v-card>
</template> 
<script>
import logo from '@/assets/app_logo.png';
import bg from "@/assets/bg.jpg";
import axios from 'axios';
export default {
    name: 'LandingPage',
    components:{},
    data() {
        return {
            url: process.env.VUE_APP_URL,
            dsplogo:logo,
            bgImg:bg,
            username:'',
            password:'',
            nameRules: [
              v => !!v || 'Name is required',
              v => v.length <= 10 || 'Name must be less than 10 characters',
           ],
    
            rules: {
              required: value => !!value || 'Required.',
              min: v => v.length >= 8 || 'Min 8 characters'
            },
            problem:false,
            problemmsg:'',
            alerttype:''
        };
    },
    methods:{
      async loginUser(){
        this.problem = false
        /* Aggregating the form elements into 'data' variable */
        var data = {
          username: this.username,
          password: this.password
        }
        /* Send Request to backend */
        await axios
        .post(this.url+':8000/auth/login', data)
        .then(async (response) => {
          var resp = await response.data;
          if(resp.success){
            this.$router.push('dashboard/createCluster')
          }
        })
        .catch(async(error) => {
          var err = await error.response.data;
          this.problem = !this.problem
          this.problemmsg = err.status
          this.alerttype = 'error'
          this.snackbar = {
            view: true,
            timeout: 4000,
            text: 'Invalid username/password',
            color: 'error'
          };
        }); 
      }
    }
};
</script>
  