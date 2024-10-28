const Dashboard = {
    data() {
        return {
            greenhouses: [
                {
                    name: 'GREENHOUSE 1',
                    location: '80 DUY TÂN, CAU GIAY, HA NOI',
                    monitorPage: '/greenhouse1' 
                },
                {
                    name: 'GREENHOUSE 2',
                    location: '100 HOANG QUOC VIET, HA NOI',
                    monitorPage: '/greenhouse2' 
                }
            ],
        };
    },

    methods: {
        logout() {
            // console.log("Logged out");
            this.$router.push('/'); 
        },
    },

    template: `
        <div class="container dashboard-page mt-3 mb-3">
            <div class="row header">
                <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
                    <div class="p-2">
                        <h1 class="dashboard-title">
                            <img src="/Software/img/leaf-icon.png" alt="leaf_icon" />
                            Smart Greenhouse Monitoring System based on Machine Learning
                        </h1>
                    </div>
                    <div class="p-2">
                        <button @click="logout" class="btn btn-link ms-3 pr-1" style="color: #8A8A8A; font-style: italic">
                            <span class="d-none d-sm-inline">Log out </span>
                            <img src="/Software/img/logout-icon.png" alt="logout_icon" />
                        </button>
                    </div>
                </div>
            </div>
            <div class="row table mt-5">
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
        </div>
    `
};
