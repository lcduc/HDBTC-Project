const Dashboard = {
    data() {
        return {

        };
    },

    methods: {
        logout() {
            this.$router.push('/'); 
        },
    },

    template: `
        <div class="mt-3 mb-3 ml-10 mr-10">
            <!-- Title, logout button -->
            <div>
                <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
                    <div class="p-2">
                        <h1>
                            <img src="img/leaf-icon.png" alt="leaf_icon" />
                            Monitor Center
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

            <!-- Thresholds display -->
            <div class="d-flex align-items-center">
                <div class="p-2">
                    <p style="font-weight: bold;">Thresholds:</p>
                </div>
                <div class="p-2">
                    <p style="font-weight: bold; color: #7E00AC">Temperature: 29&deg;C ± 3&deg</p>
                </div>
                <div class="p-2">
                    <p style="font-weight: bold; color: #4785E8">Humidity: 8.5 g/m<sup>3</sup> ± 0.3 g/m<sup>3</sup></p>
                </div>
                <div class="p-2">
                    <p style="font-weight: bold; color: #B2995A">Light intensity: 98% ± 2%</p>
                </div>
                <div class="p-2">
                    <p style="font-weight: bold; color: #8A8A8A">CO2 level: 482ppm ± 5ppm</p>
                </div>           
                <div class="p-2">
                    <router-link to="/thresholds" class="btn btn-light" style="color: #8A8A8A;">Edit thresholds</router-link>
                </div>     
            </div>

            <!-- Main dashboard container -->
            <div class="row mt-5">
                <div class="col-lg-8 col-sm-12">
                    <!-- Current, predicted data -->
                    <div class="row">
                        <div class="col-lg-6 col-sm-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2" style="font-weight: bold">Current statistics</h3>
                        
                            <!-- 4 cards: Temperature, Humidity, Light intensity, CO2 level -->
                            <div class="row-col-12">
                                <!-- Temperature -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #F2E5F7">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/temperature-icon.png" alt="temperature_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #7E00AC; font-weight: bold;">Temperature</h5>
                                                <p class="mt-0 mb-0" style="color: #9476A0; font-style: italic; font-size: 68%">Threshold: 29&deg;C ± 3&deg;C</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #7E00AC; font-size: 200%; font-weight: bold;">30<sup style="font-size: 50%; top: -1rem">&deg;C</sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Humidity -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #EDF3FD">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/humidity-icon.png" alt="humidity_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #4785E8; font-weight: bold;">Humidity</h5>
                                                <p class="mt-0 mb-0" style="color: #98A5BB; font-style: italic; font-size: 68%">Threshold: 8.5 g/m<sup>3</sup> ± 0.3 g/m<sup>3</sup></p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #4785E8; font-size: 200%; font-weight: bold;">8.2<sup style="font-size: 50%; top: -1rem">g/m<sup>3</sup></sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Light intensity -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #FDFAF1">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/light-icon.png" alt="light_intensity_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #B2995A; font-weight: bold;">Light intensity</h5>
                                                <p class="mt-0 mb-0" style="color: #C8C1AD; font-style: italic; font-size: 68%">Threshold: 98% ± 2%</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #B2995A; font-size: 200%; font-weight: bold;">98<sup style="font-size: 50%; top: -1rem">%</sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- CO2 level -->
                                <div class="ml-1 mr-1 mb-4 p-3 shadow-sm rounded" style="background-color: #F2F2F2">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/co2-icon.png" alt="co2_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #8A8A8A; font-weight: bold;">CO2 level</h5>
                                                <p class="mt-0 mb-0" style="color: #B5B5B5; font-style: italic; font-size: 68%">Threshold: 482ppm ± 5ppm</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #8A8A8A; font-size: 200%; font-weight: bold;">484<sup style="font-size: 50%; top: -1rem">ppm</sup></p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-6 col-sm-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2" style="font-weight: bold">Predicted statistics</h3>

                            <!-- 4 cards: Temperature, Humidity, Light intensity, CO2 level -->
                            <div class="row-col-12">
                                <!-- Temperature -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #F2E5F7">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/temperature-icon.png" alt="temperature_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #7E00AC; font-weight: bold;">Temperature</h5>
                                                <p class="mt-0 mb-0" style="color: #9476A0; font-style: italic; font-size: 68%">Threshold: 29&deg;C ± 3&deg;C</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #7E00AC; font-size: 200%; font-weight: bold;">25<sup style="font-size: 50%; top: -1rem">&deg;C</sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Humidity -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #EDF3FD">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/humidity-icon.png" alt="humidity_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #4785E8; font-weight: bold;">Humidity</h5>
                                                <p class="mt-0 mb-0" style="color: #98A5BB; font-style: italic; font-size: 68%">Threshold: 8.5 g/m<sup>3</sup> ± 0.3 g/m<sup>3</sup></p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #4785E8; font-size: 200%; font-weight: bold;">8.3<sup style="font-size: 50%; top: -1rem">g/m<sup>3</sup></sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Light intensity -->
                                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #FDFAF1">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/light-icon.png" alt="light_intensity_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #B2995A; font-weight: bold;">Light intensity</h5>
                                                <p class="mt-0 mb-0" style="color: #C8C1AD; font-style: italic; font-size: 68%">Threshold: 98% ± 2%</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #B2995A; font-size: 200%; font-weight: bold;">99<sup style="font-size: 50%; top: -1rem">%</sup></p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- CO2 level -->
                                <div class="ml-1 mr-1 mb-4 p-3 shadow-sm rounded" style="background-color: #F2F2F2">
                                    <div class="d-flex flex-row align-items-center justify-content-between">
                                        <div class="d-flex flex-row align-items-center">
                                            <div class="p-0.5">
                                                <img style="width: 68%" src="img/co2-icon.png" alt="co2_icon" />
                                            </div>
                                            <div class="p-0.5">
                                                <h5 class="mb-0" style="color: #8A8A8A; font-weight: bold;">CO2 level</h5>
                                                <p class="mt-0 mb-0" style="color: #B5B5B5; font-style: italic; font-size: 68%">Threshold: 482ppm ± 5ppm</p>
                                            </div>
                                        </div>
                                        <div>
                                            <p class="mb-0" style="color: #8A8A8A; font-size: 200%; font-weight: bold;">482<sup style="font-size: 50%; top: -1rem">ppm</sup></p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- -------------------- HÙN HÙN -------------------- -->
                    <!-- Historical data -->
                    <div class="row">
                        <!-- Temperature -->
                        <div class="col-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2" style="color: #7E00AC;font-weight: bold">Temperature <span style="color: #8A8A8A;">overtime</span></h3>
                            <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">Threshold: 29&deg;C ± 3&deg;C</p>

                            <div class="chart-container mb-2">

                            </div>
                        </div>
                        <!-- Humidity -->
                        <div class="col-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2" style="color: #4785E8;font-weight: bold">Humidity <span style="color: #8A8A8A;">overtime</span></h3>
                            <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">Threshold: 8.5 g/m<sup>3</sup> ± 0.3 g/m<sup>3</sup></p>

                            <div class="chart-container mb-2">

                            </div>
                        </div>
                        <!-- Light intensity -->
                        <div class="col-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2 mb-0" style="color: #B2995A;font-weight: bold">Light intensity <span style="color: #8A8A8A;">overtime</span></h3>
                            <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">Threshold: 98% ± 2%</p>

                            <div class="chart-container mb-2">

                            </div>
                        </div>
                        <!-- CO2 level -->
                        <div class="col-12 mb-4 shadow-sm rounded">
                            <h3 class="mt-2" style="color: #8A8A8A;font-weight: bold">CO2 level <span style="color: #8A8A8A;">overtime</span></h3>
                            <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">Threshold: 482ppm ± 5ppm</p>

                            <div class="chart-container mb-2">

                            </div>
                        </div>
                    </div>
                </div>

                <!-- Alert -->
                <div class="col-lg-4 shadow-sm rounded">
                    <h3 class="mt-2" style="font-weight: bold">Alerts</h3>
                </div>
            </div>
        </div>
    `
};