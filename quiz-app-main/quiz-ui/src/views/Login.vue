<template>
    <div class="card"  style="margin:auto; border-radius: 2%; width: 400px; height: 200px;">
  <div class="card-body">
   <b><h5 style="color:black; text-align: center;" class="card-title">Admin</h5></b> <br>
    <div class="register">
            <input type="password" class="form-control" v-model="password" placeholder="Enter Password" /> <br>
            <button style="position" class="btn btn-primary" v-on:click="Connect">Login</button>
        </div>   
  </div>
</div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            password: "",
        }
    },
    created() {
    
    },
    methods: {
        async Connect() {
            const response = await axios.post('http://127.0.0.1:5000/login', {
                password: this.password
            });
            const status = response.status;
            if (status === 401) {
                this.showErrorMsg = true;
            }
            else {
                const token = response.data["token"];
                localStorage.setItem("token", token);
                this.$router.push('/admin');
                console.log(token);
            }
        }
    }
}
</script>
