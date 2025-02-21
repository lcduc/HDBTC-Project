<template>
  <div class="page-content">
    <div class="mt-3 mb-3 ml-10 mr-10">
      <!-- Title, logout button -->
      <div>
        <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
          <div class="p-2">
            <h1>
              <img src="../assets/img/leaf-icon.png" alt="leaf_icon" />
              Monitor Center
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

      <!-- Back button -->
      <div class="mb-6">
        <button class="btn btn-light" onclick="window.history.back()" style="color: #8A8A8A;">
          <img src="../assets/img/arrow-left.png" alt="arrow_left_icon">&nbsp; Back
        </button>
      </div>

      <!-- Thresholds display -->
      <div class="d-flex align-items-center">
        <div class="p-2">
          <p style="font-weight: bold;">Thresholds:</p>
        </div>
        <div class="p-2">
          <p style="font-weight: bold; color: #7E00AC">Temperature: {{ currentThresholds.temperature.threshold }} &degC
            ±
            {{ currentThresholds.temperature.uncertainty }}&degC</p>
        </div>
        <div class="p-2">
          <p style="font-weight: bold; color: #4785E8">Humidity: {{ currentThresholds.humidity.threshold }} % ± {{
            currentThresholds.humidity.uncertainty }} %</p>
        </div>
        <div class="p-2">
          <p style="font-weight: bold; color: #B2995A">Light intensity: {{ currentThresholds.lightIntensity.threshold }}
            μmol/m²s ± {{ currentThresholds.lightIntensity.uncertainty }} μmol/m²s</p>
        </div>
        <div class="p-2">
          <p style="font-weight: bold; color: #8A8A8A">CO2 level: {{ currentThresholds.co2.threshold }} ppm ± {{
            currentThresholds.co2.uncertainty }} ppm</p>
        </div>
        <div class="p-2">
          <router-link to="/thresholds" class="btn btn-light" style="color: #8A8A8A;">Edit
            thresholds</router-link>
        </div>
      </div>

      <!-- Main dashboard container -->
      <div class="row mt-5">
        <div class="col-lg-8 col-sm-12">
          <!-- Current, predicted data -->
          <div class="row">
            <!-- Current data section -->
            <div class="col-lg-6 col-sm-12 mb-4 shadow-sm rounded">
              <header class="d-flex justify-content-between align-items-center">
                <h3 class="mt-2" style="font-weight: bold">Current statistics</h3>
                <router-link to="/managedevices" class="btn btn-primary" @click="fetchPredictedData"> Manage Devices
                </router-link>
              </header>
              <div class="row-col-12">
                <!-- Temperature Card -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #F2E5F7">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/temperature-icon.png" alt="temperature_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #7E00AC; font-weight: bold;">Temperature</h5>
                        <p class="mt-0 mb-0" style="color: #9476A0; font-style: italic; font-size: 68%">Threshold:
                          {{ currentThresholds.temperature.threshold }} &deg;C ± {{
                            currentThresholds.temperature.uncertainty }} &deg;C</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #7E00AC; font-size: 200%; font-weight: bold;">
                        {{ current_data[0]?.temperature || 'N/A' }}<sup style="font-size: 50%; top: -1rem">&deg;C</sup>
                      </p>
                    </div>
                  </div>
                </div>
                <!-- Humidity -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #EDF3FD">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/humidity-icon.png" alt="humidity_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #4785E8; font-weight: bold;">Humidity</h5>
                        <p class="mt-0 mb-0" style="color: #98A5BB; font-style: italic; font-size: 68%">
                          Threshold: {{ currentThresholds.humidity.threshold }} % ± {{
                            currentThresholds.humidity.uncertainty }} %</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #4785E8; font-size: 200%; font-weight: bold;">
                        {{ current_data[0]?.humidity || 'N/A' }}<sup style="font-size: 50%; top: -1rem">%</sup>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Light intensity -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #FDFAF1">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/light-icon.png" alt="light_intensity_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #B2995A; font-weight: bold;">Light intensity
                        </h5>
                        <p class="mt-0 mb-0" style="color: #C8C1AD; font-style: italic; font-size: 68%">
                          Threshold: {{ currentThresholds.lightIntensity.threshold }} μmol/m²s ± {{
                            currentThresholds.lightIntensity.uncertainty }} μmol/m²s</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #B2995A; font-size: 200%; font-weight: bold;">
                        {{ current_data[0]?.lightIntensity || 'N/A' }}<sup style="font-size: 50%; top: -1rem">
                          μmol/m²s</sup>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- CO2 level -->
                <div class="ml-1 mr-1 mb-4 p-3 shadow-sm rounded" style="background-color: #F2F2F2">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/co2-icon.png" alt="co2_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #8A8A8A; font-weight: bold;">CO2 level</h5>
                        <p class="mt-0 mb-0" style="color: #B5B5B5; font-style: italic; font-size: 68%">
                          Threshold: {{ currentThresholds.co2.threshold }} ppm ± {{ currentThresholds.co2.uncertainty }}
                          ppm</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #8A8A8A; font-size: 200%; font-weight: bold;">
                        {{ current_data[0]?.co2 || 'N/A' }}<sup style="font-size: 50%; top: -1rem">ppm</sup>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>



            <!-- Predicted data section -->
            <div class="col-lg-6 col-sm-12 mb-4 shadow-sm rounded">
              <header class="d-flex justify-content-between align-items-center">
                <h3 class="mt-2" style="font-weight: bold">Predicted statistics</h3>
              </header>
              <div class="row-col-12">
                <!-- Temperature Card -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #F2E5F7">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/temperature-icon.png" alt="temperature_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #7E00AC; font-weight: bold;">Temperature
                        </h5>
                        <p class="mt-0 mb-0" style="color: #9476A0; font-style: italic; font-size: 68%">
                          Threshold: 29&deg;C ± 3&deg;C</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #7E00AC; font-size: 200%; font-weight: bold;">
                        {{ predicted_data.temperature || 'N/A' }}<sup style="font-size: 50%; top: -1rem">&deg;C</sup>
                      </p>
                    </div>
                  </div>
                </div>
                <!-- Humidity -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #EDF3FD">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/humidity-icon.png" alt="humidity_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #4785E8; font-weight: bold;">Humidity
                        </h5>
                        <p class="mt-0 mb-0" style="color: #98A5BB; font-style: italic; font-size: 68%">
                          Threshold:
                          8.5 g/m<sup>3</sup> ± 0.3 g/m<sup>3</sup></p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #4785E8; font-size: 200%; font-weight: bold;">
                        {{ predicted_data.humidity || 'N/A' }}<sup
                          style="font-size: 50%; top: -1rem">g/m<sup>3</sup></sup>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Light intensity -->
                <div class="ml-1 mr-1 mb-3 p-3 shadow-sm rounded" style="background-color: #FDFAF1">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/light-icon.png" alt="light_intensity_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #B2995A; font-weight: bold;">Light
                          intensity</h5>
                        <p class="mt-0 mb-0" style="color: #C8C1AD; font-style: italic; font-size: 68%">
                          Threshold:
                          98% ± 2%</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #B2995A; font-size: 200%; font-weight: bold;">
                        {{ predicted_data.lightIntensity || 'N/A' }}<sup style="font-size: 50%; top: -1rem">%</sup>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- CO2 level -->
                <div class="ml-1 mr-1 mb-4 p-3 shadow-sm rounded" style="background-color: #F2F2F2">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                      <div class="p-0.5">
                        <img style="width: 68%" src="../assets/img/co2-icon.png" alt="co2_icon" />
                      </div>
                      <div class="p-0.5">
                        <h5 class="mb-0" style="color: #8A8A8A; font-weight: bold;">CO2 level
                        </h5>
                        <p class="mt-0 mb-0" style="color: #B5B5B5; font-style: italic; font-size: 68%">
                          Threshold:
                          482ppm ± 5ppm</p>
                      </div>
                    </div>
                    <div>
                      <p class="mb-0" style="color: #8A8A8A; font-size: 200%; font-weight: bold;">
                        {{ predicted_data.co2 || 'N/A' }}<sup style="font-size: 50%; top: -1rem">ppm</sup>
                      </p>
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
              <div class="header-with-filter">
                <div class="parameter-title">
                  <h3 class="mt-2" style="color: #7E00AC;font-weight: bold">Temperature <span
                      style="color: #8A8A8A;">overtime</span></h3>
                  <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">
                    Threshold: {{ currentThresholds.temperature.threshold }} &deg;C ± {{
                      currentThresholds.temperature.uncertainty }} &deg;C</p>
                </div>
                <div class="select-wrapper">
                  <select class="form-select form-select-sm" id="filter-option-temp" v-model="filterOption">
                    <option value="monthly-temp">Monthly</option>
                    <option value="weekly-temp">Weekly</option>
                  </select>
                </div>
              </div>

              <div class="chart-container mb-2">
                <div class="chart-position">
                  <svg id="temperature-chart"></svg>
                </div>
                <div id="tooltip-temp"></div>
              </div>
            </div>
            <!-- Humidity -->
            <div class="col-12 mb-4 shadow-sm rounded">
              <div class="header-with-filter">
                <div class="parameter-title">
                  <h3 class="mt-2" style="color: #4785E8;font-weight: bold">Humidity <span
                      style="color: #8A8A8A;">overtime</span></h3>
                  <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">
                    Threshold: {{ currentThresholds.humidity.threshold }} % ± {{
                      currentThresholds.humidity.uncertainty
                    }}
                    %
                  </p>
                </div>
                <div class="select-wrapper">
                  <select class="form-select form-select-sm" id="filter-option-humid" v-model="filterOption">
                    <option value="monthly-humid" selected>Monthly</option>
                    <option value="weekly-humid">Weekly</option>
                  </select>
                </div>
              </div>

              <div class="chart-container mb-2">
                <div class="chart-position">
                  <svg id="humidity-chart"></svg>
                </div>
                <div id="tooltip-humid"></div>
              </div>
            </div>
            <!-- Light intensity -->
            <div class="col-12 mb-4 shadow-sm rounded">
              <div class="header-with-filter">
                <div class="parameter-title">
                  <h3 class="mt-2 mb-0" style="color: #B2995A;font-weight: bold">Light intensity <span
                      style="color: #8A8A8A;">overtime</span></h3>
                  <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">
                    Threshold: {{ currentThresholds.lightIntensity.threshold }} μmol/m²s ± {{
                      currentThresholds.lightIntensity.uncertainty }} μmol/m²s</p>
                </div>
                <div class="select-wrapper">
                  <select class="form-select form-select-sm" id="filter-option-light" v-model="filterOption">
                    <option value="monthly-light">Monthly</option>
                    <option value="weekly-light">Weekly</option>
                  </select>
                </div>
              </div>

              <div class="chart-container mb-2">
                <div class="chart-position">
                  <svg id="light-chart"></svg>
                </div>
                <div id="tooltip-light"></div>
              </div>
            </div>
            <!-- CO2 level -->
            <div class="col-12 mb-4 shadow-sm rounded">
              <div class="header-with-filter">
                <div class="parameter-title">
                  <h3 class="mt-2" style="color: #8A8A8A;font-weight: bold">CO2 level <span
                      style="color: #8A8A8A;">overtime</span></h3>
                  <p class="mt-0 mb-0" style="color: #8A8A8A; font-style: italic; font-size: 80%">
                    Threshold: {{ currentThresholds.co2.threshold }} ppm ± {{ currentThresholds.co2.uncertainty }}
                    ppm
                  </p>

                </div>
                <div class="select-wrapper">
                  <select class="form-select form-select-sm" id="filter-option-co2" v-model="filterOption">
                    <option value="monthly-co2">Monthly</option>
                    <option value="weekly-co2">Weekly</option>
                  </select>
                </div>
              </div>

              <div class="chart-container mb-2">
                <div class="chart-position">
                  <svg id="co2-chart"></svg>
                </div>
                <div id="tooltip-co2"></div>
              </div>
            </div>
          </div>
        </div>


        <!-- Alert -->
        <div class="col-lg-4 shadow-sm rounded">
          <div class="card">
            <h3 class="mt-2" style="font-weight: bold">Alerts & Notifications</h3>
            <div class="card-body">
              <div class="row alert-filter">
                <div class="col-md-4 d-flex align-items-center">
                  <label for="from" class="form-label me-2" style="margin-bottom: 0;">From</label>
                  <input type="date" class="form-control form-control-sm" id="from" v-model="from">
                </div>
                <div class="col-md-4 d-flex align-items-center">
                  <label for="to" class="form-label me-2" style="margin-bottom: 0;">To</label>
                  <input type="date" class="form-control form-control-sm" id="to" v-model="to">
                </div>
                <div class="col-md-2 d-flex align-items-center">
                  <button type="button" class="btn btn-sm w-100" @click="apply">Apply</button>
                </div>
                <div class="col-md-2 d-flex align-items-center">
                  <button type="button" class="btn btn-sm w-100" @click="viewAll">View all</button>
                </div>
              </div>

              <br>

              <div class="row alert-content">
                <div class="alert-container">
                  <!-- Alerts & Notifications Section -->
                  <div v-if="groupedAlerts.length" class="mb-4">
                    <div v-for="(alertGroup, index) in groupedAlerts" :key="index">
                      <!-- Display Date for Alert Group -->
                      <div class="alert-date" style="font-weight: bold; margin-bottom: 10px;">
                        {{ alertGroup.date }}
                      </div>

                      <!-- Display Alerts for the Current Group -->
                      <div v-for="alert in alertGroup.alerts" :key="alert.alertID" class="alert" :class="alert.type"
                        style="background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <div class="d-flex align-items-center">
                          <h4 class="alert-heading"
                            :style="{ fontWeight: 'bold', color: getAlertParameterDetails(alert.parameter).color }">
                            {{ getAlertParameterDetails(alert.parameter).name }} <span
                              style="color: darkred">Warning</span>
                          </h4>
                        </div>
                        <p>
                          The
                          <span style="font-weight: bold;">
                            {{ getAlertParameterDetails(alert.parameter).name }}
                          </span>
                          will soon
                          <span style="font-weight: bold;">
                            {{ alert.changeType }}
                          </span>
                          the optimal condition by
                          <span style="font-weight: bold;">
                            {{ alert.difference }}
                          </span>
                          in the next 30 minutes.
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Message if no alerts -->
                  <div v-else>
                    <p>No alerts to display.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import the renderCo2Chart function
import { renderTempChart } from './charts/temp.js';
import { renderHumidChart } from './charts/humid.js';
import { renderLightChart } from './charts/light.js';
import { renderCo2Chart } from './charts/co2.js';
export default {
  data() {
    return {
      from: '',
      to: '',
      predicted_data: {},
      current_data: [],
      currentThresholds: {
        temperature: { threshold: 0, uncertainty: 0 },
        humidity: { threshold: 0, uncertainty: 0 },
        lightIntensity: { threshold: 0, uncertainty: 0 },
        co2: { threshold: 0, uncertainty: 0 },
      },
      alerts: [],
      isLoading: true,
      msg: '',
    };
  },

  async mounted() {
    const user = localStorage.getItem('user');
    if (!user) {
      this.$router.push('/'); // Redirect to login
      return;
    }

    renderTempChart();
    renderHumidChart();
    renderLightChart();
    renderCo2Chart();

    const greenhouseID = localStorage.getItem('selectedGreenhouseID');

    if (greenhouseID) {
      try {
        // Fetch predicted data
        const predictedResponse = await fetch(`https://slmc2nab67.execute-api.us-east-1.amazonaws.com/predicteddata?greenhouseID=2`);
        const predictedData = await predictedResponse.json();
        this.predicted_data = predictedData;

        // Fetch current data
        const currentResponse = await fetch(`https://ck28id9727.execute-api.us-east-1.amazonaws.com/Allhistoricaldata?greenhouseID=1`);
        const currentData = await currentResponse.json();
        this.current_data = currentData || [];

        // Fetch threshold data
        await this.fetchThresholdData(greenhouseID);

        // Fetch alert data
        await this.fetchAlertData(greenhouseID);
      } catch (error) {
        this.msg = 'Failed to load data. Please try again later.';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    } else {
      this.msg = 'No greenhouse selected. Please select a greenhouse first.';
      this.isLoading = false;
    }

    await this.fetchAlertData(greenhouseID);
  },

  computed: {
    // Grouping and sorting the alerts by date and time
    groupedAlerts() {
      // Sort alerts by date and time (descending order)
      const sortedAlerts = this.alerts.sort((a, b) => new Date(b.date) - new Date(a.date));

      // Group by date (ignoring time for the grouping)
      const grouped = [];
      sortedAlerts.forEach(alert => {
        const existingGroup = grouped.find(group => group.date === alert.date.split('T')[0]); // Grouping by date (ignoring time)
        if (existingGroup) {
          existingGroup.alerts.push(alert);
        } else {
          grouped.push({ date: alert.date.split('T')[0], alerts: [alert] });
        }
      });
      return grouped;
    }
  },

  methods: {

    logout() {
      localStorage.removeItem('user');
      this.$router.push('/');
    },


    // Fetch threshold data and update current thresholds
    async fetchThresholdData() {
      try {
        this.isLoading = true;
        const response = await fetch(
          "https://bq79xbfalb.execute-api.us-east-1.amazonaws.com/GETthresholds?greenhouseID=1"
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Threshold data fetched successfully!");
        console.log(data);

        // Reset current thresholds before updating
        this.currentThresholds = {
          temperature: { threshold: 0, uncertainty: 0 },
          humidity: { threshold: 0, uncertainty: 0 },
          lightIntensity: { threshold: 0, uncertainty: 0 },
          co2: { threshold: 0, uncertainty: 0 },
        };

        // Map the data to our currentThresholds object
        data.forEach((item) => {
          const parameterKey = this.mapParameterKey(item.parameter);
          if (parameterKey && this.currentThresholds[parameterKey]) {
            this.currentThresholds[parameterKey].threshold = parseFloat(item.threshold);
            this.currentThresholds[parameterKey].uncertainty = parseFloat(item.uncertainty);
          }
        });
      } catch (error) {
        console.error("Error fetching threshold data:", error);
        this.errorMessage = `Error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    },

    mapParameterKey(parameter) {
      const mapping = {
        temperature: "temperature",
        humidity: "humidity",
        lightIntensity: "lightIntensity",
        co2: "co2",
      };
      return mapping[parameter] || null;
    },

    getAlertParameterDetails(parameter) {
      const parameterMap = {
        temperature: { name: 'Temperature', color: '#7E00AC' },
        humidity: { name: 'Humidity', color: '#4785E8' },
        lightIntensity: { name: 'Light Intensity', color: '#B2995A' },
        co2: { name: 'CO2 Level', color: '#8A8A8A' }
      };

      return parameterMap[parameter] || { name: parameter, color: '#000000' };  // Default to black if no match
    },

    async fetchAlertData(greenhouseID) {
      try {
        const response = await fetch(`https://g8r6riw729.execute-api.us-east-1.amazonaws.com/alertdetails?greenhouseID=1}`);
        const data = await response.json();

        if (data && Array.isArray(data)) {
          this.alerts = data; // Update the alerts array with fetched data
        } else {
          console.error("Unexpected alert data format", data);
        }
      } catch (error) {
        console.error('Failed to fetch alerts:', error);
      }
    },

    // Apply filters based on date range (from-to)
    apply() {
      if (this.from && this.to) {
        const fromDate = new Date(this.from);
        const toDate = new Date(this.to);

        // Filter alerts that fall within the date range
        this.alerts = this.alerts.filter(alert => {
          const alertDate = new Date(alert.date);
          return alertDate >= fromDate && alertDate <= toDate;
        });
      } else {
        // If no dates are selected, reset the alerts or re-fetch the data
        this.viewAll();
      }
    },

    // View all alerts without filtering
    viewAll() {
      this.fetchAlertData(1); // Example greenhouseID, replace with dynamic value if needed
    },

  },

  created() {
    this.fetchThresholdData();
  }

};
</script>

<style scoped>
.page-content {
  margin: 0 2em;
}

.card {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.alert-filter h2 {
  margin-top: 0;
  margin-bottom: 1rem;
}


.dashboard-title {
  font-size: 2rem !important;
}

.alert-filter .form-control {
  height: 10px;
  padding: 0 10px;
  font-size: .6rem;
  border-radius: 5px;
  margin: 0;
}

.alert-filter .form-label,
.btn {
  font-size: .7rem;
  margin: 0;
  font-weight: 700;
}

.alert-filter .btn {
  background-color: #C1C1C1;
  border: #C1C1C1;
  color: #808080;
}

.alert-filter .col-md-4,
.col-md-2 {
  padding: 2px !important;
}

.timestamp {
  font-size: 0.9em;
  color: #888;
  margin-top: 0.5em;
  font-style: italic;
}

.alert {
  margin-bottom: 1em;
}

.alert-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.alert-container::-webkit-scrollbar {
  width: 8px;
}

.alert-container::-webkit-scrollbar-track {
  background: transparent;
}

.alert-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}
</style>