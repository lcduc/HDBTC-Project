<template>
    <div class="mt-3 mb-3 ml-10 mr-10">
      <div>
        <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
          <div class="p-2">
            <h1>
              <img src="../assets/img/leaf-icon.png" alt="leaf_icon" />
              Smart Greenhouse Monitoring System based on Machine Learning
            </h1>
          </div>
          <div class="p-2">
            <button @click="logout" class="btn btn-link ms-3 pr-1" style="color: #8A8A8A; font-style: italic">
              <span class="d-none d-sm-inline">Log out </span>
              <img src="../assets/img/logout-icon.png" alt="logout_icon" />
            </button>
          </div>
        </div>
      </div>
  
      <div v-if="msg" class="alert alert-danger">{{ msg }}</div>
  
      <div class="row table mt-5 pl-5" v-if="greenhouses.length">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>NO.</th>
              <th>NAME</th>
              <th>LOCATION</th>
              <th>MONITOR PAGE</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gh, index) in greenhouses" :key="gh.greenhouseID">
              <td>{{ index + 1 }}</td>
              <td>{{ gh.name }}</td>
              <td>{{ gh.location }}</td>
              <td>
                <button @click="goToDashboard(gh.greenhouseID)" class="btn"
                  style="background-color: #88C47A; color: white;">
                  GO TO PAGE
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pl-2 pr-3">
        <img class="img-fluid" src="../assets/img/greenhouse-home-page.jpg" alt="greenhouse-home-page" />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        greenhouses: [],
        msg: ''
      };
    },
  
    async mounted() {
      const user = JSON.parse(localStorage.getItem('user'));
      const accountID = user ? user.accountID : null;
  
      if (accountID) {
        try {
          const response = await fetch(`https://7hv7iqdxcf.execute-api.us-east-1.amazonaws.com/greenhousedetails?accountID=${accountID}`);
          const data = await response.json();
          this.greenhouses = data;
        } catch (error) {
          this.msg = 'Failed to load greenhouse details. Please try again later.';
          console.error(error);
        }
      } else {
        this.msg = 'User not authenticated';
      }
    },
  
    methods: {
      logout() {
        localStorage.removeItem('user');
        this.$router.push('/');
      },
      goToDashboard(greenhouseID) {
        localStorage.setItem('selectedGreenhouseID', greenhouseID);
        this.$router.push('/dashboard');
      }
    },
  };
  </script>
  
  <style scoped>
  </style>
  