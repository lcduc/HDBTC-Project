const Home = {
    data() {
        return {
            greenhouses: [
                {
                    name: 'GREENHOUSE 1',
                    location: '80 DUY TAN, CAU GIAY, HA NOI',
                    monitorPage: '/dashboard' 
                },
                {
                    name: 'GREENHOUSE 2',
                    location: '100 HOANG QUOC VIET, HA NOI',
                    monitorPage: '/dashboard2' 
                }
            ],
        }
    },
    
    mounted() {

    },

    methods: {
        logout() {
            this.$router.push('/'); 
        },
    },

    computed: {

    },

    template: `
        <div class="mt-3 mb-3 ml-10 mr-10">
            <div>
                <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
                    <div class="p-2">
                        <h1>
                            <img src="img/leaf-icon.png" alt="leaf_icon" />
                            Smart Greenhouse Monitoring System based on Machine Learning
                        </h1>
                    </div>
                    <div class="p-2">
                        <button @click="logout" class="btn btn-link ms-3 pr-1" style="color: #8A8A8A; font-style: italic">
                            <span class="d-none d-sm-inline">Log out </span>
                            <img src="img/logout-icon.png" alt="logout_icon" />
                        </button>
                    </div>
                </div>            
            </div>

            <div class="row table mt-5 pl-5">
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
                        <tr v-for="(greenhouse, index) in greenhouses" :key="index">
                            <td>{{ index + 1 }}</td>
                            <td>{{ greenhouse.name }}</td>
                            <td>{{ greenhouse.location }}</td>
                            <td>
                                <router-link :to="greenhouse.monitorPage" class="btn" style="background-color: #88C47A; color: white;">
                                    GO TO PAGE
                                </router-link>
                            </td>                            
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="pl-2 pr-3">
                <img class="img-fluid" src="img/greenhouse-home-page.jpg" alt="greenhouse-home-page" />
            </div>
        </div>
    `
};