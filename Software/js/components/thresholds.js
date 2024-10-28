const Thresholds = {
    data() {
        return {
            successMessage: '',
        };
    },

    methods: {
        updateProfile() {
            this.successMessage = 'Set new thresholds successfully';

            setTimeout(() => {
                this.$router.push('/dashboard');
            }, 3000);
        },
    },

    template: `
        <div class="mt-3 mb-3 ml-10 mr-10">
            <!-- Title, logout button -->
            <div>
                <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
                    <div class="p-2">
                        <h1>
                            <img src="/img/leaf-icon.png" alt="leaf_icon" />
                            Thresholds settings
                        </h1>
                    </div>
                    <div class="p-2">
                        <button @click="logout" class="btn btn-link ms-3 pr-1" style="color: #8A8A8A; font-style: italic">
                            <span class="d-none d-sm-inline">Log out </span>
                            <img src="/img/logout-icon.png" alt="logout_icon" />
                        </button>
                    </div>
                </div>            
            </div>

            <!-- Back button -->
            <div class="mb-6">
                <button class="btn btn-light" onclick="window.history.back()" style="color: #8A8A8A;">
                    <img src="/Software/img/arrow-left.png" alt="arrow_left_icon">&nbsp; Back
                </button>
            </div>

            <!-- Threshold settings form -->
            <form novalidate method="post" @submit.prevent="updateProfile()" class="mb-10">
                <!-- Temperature -->
                <div class="mb-8">
                    <label for="temperature" class="form-label mb-0">
                        <h5 class="mb-0" style="color: #7E00AC; font-weight: bold">Temperature:</h5>
                    </label>
                    <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
                        Current threshold: <b>29&deg;C ± 3&deg;C</b>
                    </div>
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="temperature" placeholder="New threshold">
                        </div>
                        <div class="col-md-1 text-center">±</div>
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="temperature" placeholder="New uncertainty">
                        </div>
                    </div>
                </div>   

                <!-- Humidity -->
                <div class="mb-8">
                    <label for="humidity" class="form-label mb-0">
                        <h5 class="mb-0" style="color: #4785E8; font-weight: bold">Humidity:</h5>
                    </label>
                    <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
                        Current threshold: <b>8.5 g/m3 ± 0.3 g/m3</b>
                    </div>
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="humidity" placeholder="New threshold">
                        </div>
                        <div class="col-md-1 text-center">±</div>
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="humidity" placeholder="New uncertainty">
                        </div>
                    </div>
                </div>        

                <!-- Light Intensity -->
                <div class="mb-8">
                    <label for="lightintensity" class="form-label mb-0">
                        <h5 class="mb-0" style="color: #B2995A; font-weight: bold">Light Intensity:</h5>
                    </label>
                    <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
                        Current threshold: <b>98% ± 2%</b>
                    </div>
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="lightintensity" placeholder="New threshold">
                        </div>
                        <div class="col-md-1 text-center">±</div>
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="lightintensity" placeholder="New uncertainty">
                        </div>
                    </div>
                </div>        

                <!-- CO2 Level -->
                <div class="mb-8">
                    <label for="co2level" class="form-label mb-0">
                        <h5 class="mb-0" style="color: #7A7A7A; font-weight: bold">CO2 Level:</h5>
                    </label>
                    <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
                        Current threshold: <b>482ppm ± 5ppm</b>
                    </div>
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="co2level" placeholder="New threshold">
                        </div>
                        <div class="col-md-1 text-center">±</div>
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="co2level" placeholder="New uncertainty">
                        </div>
                    </div>
                </div>

                <!-- Submit button -->
                <button type="submit" class="btn" style="background-color: #88C47A; color: #FFFFFF; font-weight: bold;">
                    SET NEW THRESHOLDS
                </button> 

                <!-- Success message -->
                <div v-if="successMessage" style="color: green; margin-top: 10px;">
                    {{ successMessage }}
                </div>     
            </form>
        </div>
    `
};