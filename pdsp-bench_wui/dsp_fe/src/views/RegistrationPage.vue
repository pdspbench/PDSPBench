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
                <div style="text-align: center;" class="mb-5 text-h5 primary--text"><b>Register for PDSP-Bench</b></div>
                <v-row>
                  <v-col cols="6">
                    <v-text-field
                      v-model="username"
                      :rules="nameRules"
                      label="Username"
                      clearable
                      outlined
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      v-model="email"
                      label="Email"
                      :rules="emailRules"
                      clearable
                      outlined
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      type="password"
                      v-model="password"
                      label="Password"
                      :rules="[rules.required, rules.min]"
                      clearable
                      outlined
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      type="password"
                      v-model="retypePassword"
                      label="Retype password"
                      :rules="[rules.required, rules.min]"
                      clearable
                      outlined
                    ></v-text-field>
                  </v-col>
                  <v-col  v-if="problem" >
                    <v-alert 
                      dense
                      outlined
                      :type=alerttype
                     
                      
                    >
                    {{problemmsg}}
                    </v-alert>
                  </v-col>
                </v-row>    
                    
                <!-- $router.push('dashboard/createCluster') -->
                  <v-btn  color="primary"  class="mt-6" block rounded small  @click="registerUser()">
                    
                    <b> Register </b>
                  </v-btn>
                </v-card-text>
  
                <v-divider class="mx-4"></v-divider>
  
  
  
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" small rounded text @click="$router.push('/')">
                        Go to login
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
import logo from '@/assets/logo.webp';
import bg from "@/assets/bg.jpg";
import axios from 'axios';
export default {
    name: 'RegistrationPage',
    components:{},
    data() {
        return {
            url: process.env.VUE_APP_URL,
            dsplogo:logo,
            bgImg:bg,
            email:'',
            username: '',
            password:'',
            retypePassword:'',
            problem:false,
            problemmsg:'',
            alerttype:'',
            nameRules: [
              v => !!v || 'Name is required',
              v => v.length <= 10 || 'Name must be less than 10 characters',
           ],
            emailRules: [
              v => !!v || 'E-mail is required',
              v => /.+@.+/.test(v) || 'E-mail must be valid',
            ],
            rules: {
              required: value => !!value || 'Required.',
              min: v => v.length >= 8 || 'Min 8 characters'
            }
            
        };
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
      
    },
    methods:{
      async registerUser(){
        
        
        /* check if the fields are filled */
      
        /* Check is password fields are matching */
        this.problem = false
        if(this.password != this.retypePassword){
          this.problem = !this.problem
          this.problemmsg = 'passwords dont match'
          this.alerttype = 'error'
          return
        } else if(this.username.length == 0 || this.email.length == 0){
          this.problem = !this.problem 
          this.problemmsg = 'please provide username and email address'
          this.alerttype = 'error'
          return
        }
        /* Aggregating the form elements into 'data' variable */
        var data = {
          username: this.username,
          password: this.password,
          email: this.email
        }
        /* Send Request to backend */
        await axios
        .post(this.url+':8000/auth/register', data)
        .then(async (response) => {
          var resp = await response.data;
          if(resp.success){
            this.problem = !this.problem
            this.problemmsg = resp.status
            this.alerttype = 'success'
            this.snackbar = {
              view: true,
              timeout: 3000,
              text: 'Please accept email sent to your email address',
              color: 'primary'
            };
          }
        })
        .catch(async (error) => {
          var err = await error.response.data;
          console.log(err.success);
          this.problem = !this.problem
          this.problemmsg = err.status
          console.log(err.status);
          this.alerttype = 'error'
          this.snackbar = {
            view: true,
            timeout: 8000,
            text: 'Please fill the form correctly',
            color: 'error'
          };
        }); 


      }
    }
};
</script>
  