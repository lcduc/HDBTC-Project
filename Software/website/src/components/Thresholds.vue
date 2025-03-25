<template>
  <div class="mt-3 mb-3 ml-10 mr-10">
    <div v-if="isLoading" class="text-center">
      Loading thresholds...
    </div>
    <div v-else>
      <!-- Title, logout button -->
      <div>
        <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
          <div class="p-2">
            <h1>
              <img src="../assets/img/leaf-icon.png" alt="leaf_icon" />
              Thresholds settings
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
        <button class="btn btn-light" @click="$router.go(-1)" style="color: #8A8A8A;">
          <img src="../assets/img/arrow-left.png" alt="arrow_left_icon">&nbsp; Back
        </button>
      </div>

      <!-- Threshold settings form -->
      <form @submit.prevent="updateThresholds" class="mb-10">
        <!-- Temperature -->
        <div class="mb-8">
          <label class="form-label mb-0">
            <h5 class="mb-0" style="color: #7E00AC; font-weight: bold">Temperature:</h5>
          </label>
          <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
            Current threshold: <b>{{ currentThresholds.temperature.threshold }}&deg;C ± {{ currentThresholds.temperature.uncertainty }}&deg;C</b>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.temperature.threshold" class="form-control" placeholder="New threshold" step="0.1" />
            </div>
            <div class="col-md-1 text-center">±</div>
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.temperature.uncertainty" class="form-control" placeholder="New uncertainty" step="0.1" />
            </div>
          </div>
        </div>
        <br>

        <!-- Humidity -->
        <div class="mb-8">
          <label class="form-label mb-0">
            <h5 class="mb-0" style="color: #4785E8; font-weight: bold">Humidity:</h5>
          </label>
          <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
            Current threshold: <b>{{ currentThresholds.humidity.threshold }} % ± {{ currentThresholds.humidity.uncertainty }} %</b>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.humidity.threshold" class="form-control" placeholder="New threshold" step="0.1" />
            </div>
            <div class="col-md-1 text-center">±</div>
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.humidity.uncertainty" class="form-control" placeholder="New uncertainty" step="0.1" />
            </div>
          </div>
        </div>
        <br>

        <!-- Light Intensity -->
        <div class="mb-8">
          <label class="form-label mb-0">
            <h5 class="mb-0" style="color: #B2995A; font-weight: bold">Light Intensity:</h5>
          </label>
          <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
            Current threshold: <b>{{ currentThresholds.lightIntensity.threshold }} μmol/m²s ± {{ currentThresholds.lightIntensity.uncertainty }} μmol/m²s</b>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.lightIntensity.threshold" class="form-control" placeholder="New threshold" step="0.1" />
            </div>
            <div class="col-md-1 text-center">±</div>
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.lightIntensity.uncertainty" class="form-control" placeholder="New uncertainty" step="0.1" />
            </div>
          </div>
        </div>
        <br>

        <!-- CO2 Level -->
        <div class="mb-8">
          <label class="form-label mb-0">
            <h5 class="mb-0" style="color: #14A44D; font-weight: bold">CO2 Levels:</h5>
          </label>
          <div class="form-text mt-0 mb-3" style="color: #8A8A8A; font-style: italic">
            Current threshold: <b>{{ currentThresholds.co2.threshold }} ppm ± {{ currentThresholds.co2.uncertainty }} ppm</b>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.co2.threshold" class="form-control" placeholder="New threshold" step="1" />
            </div>
            <div class="col-md-1 text-center">±</div>
            <div class="col-md-3">
              <input type="number" v-model.number="updatedThresholds.co2.uncertainty" class="form-control" placeholder="New uncertainty" step="1" />
            </div>
          </div>
        </div>
        <br>

        <!-- Submit Button -->
        <div class="d-flex justify-content-start mt-3">
          <button type="submit" class="pt-3 pb-3 pl-6 pr-6 rounded" style="border: 0; color: white; font-weight: bold; background-color: #88C47A" >SET NEW THRESHOLDS</button>
        </div>
      </form>

      <br>

      <!-- Error and success messages -->
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success" role="alert">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentThresholds: {
        temperature: { threshold: 0, uncertainty: 0 },
        humidity: { threshold: 0, uncertainty: 0 },
        lightIntensity: { threshold: 0, uncertainty: 0 },
        co2: { threshold: 0, uncertainty: 0 },
      },
      updatedThresholds: {
        temperature: { threshold: null, uncertainty: null },
        humidity: { threshold: null, uncertainty: null },
        lightIntensity: { threshold: null, uncertainty: null },
        co2: { threshold: null, uncertainty: null },
      },
      errorMessage: "",
      successMessage: "",
      isLoading: true
    }
  },

  mounted() {
    const user = localStorage.getItem('user');
    if (!user) {
      this.$router.push('/'); // Redirect to login
      return;
    }
  },

  methods: {

    logout() {
      localStorage.removeItem('user');
      this.$router.push('/');
    },

    async fetchThresholdData() {
      try {
        this.isLoading = true;

        // Retrieve greenhouseID from localStorage
        const greenhouseID = localStorage.getItem('selectedGreenhouseID');

        if (!greenhouseID) {
          console.error('No greenhouse selected. Please select a greenhouse first.');
          this.errorMessage = 'No greenhouse selected. Please select a greenhouse first.';
          this.isLoading = false;
          return;
        }
          
        const response = await fetch(
          `http://14.225.205.88:8000/getthreshold?greenhouseID=${greenhouseID}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Threshold data fetched successfully!", data);
        console.log("Data type:", typeof data, "Data:", data);

        // Reset current thresholds before updating
        this.currentThresholds = {
          temperature: { threshold: 0, uncertainty: 0 },
          humidity: { threshold: 0, uncertainty: 0 },
          lightIntensity: { threshold: 0, uncertainty: 0 },
          co2: { threshold: 0, uncertainty: 0 },
        };

        // 🔹 Loop through object keys instead of using forEach
        for (const key in data) {
          if (this.currentThresholds[key]) {
            this.currentThresholds[key].threshold = parseFloat(data[key].threshold);
            this.currentThresholds[key].uncertainty = parseFloat(data[key].uncertainty);
          }
        }
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

    async updateThresholds() {
      try {
        this.errorMessage = "";
        this.successMessage = "";

        const greenhouseID = localStorage.getItem("selectedGreenhouseID");

        if (!greenhouseID) {
          this.errorMessage = "No greenhouse selected. Please select a greenhouse first.";
          return;
        }

        let hasValidInput = false;
        let invalidFields = [];

        // Create the request payload
        const thresholdsData = [];

        for (const key in this.updatedThresholds) {
          const threshold = this.updatedThresholds[key].threshold;
          const uncertainty = this.updatedThresholds[key].uncertainty;

          // Check if at least one field has been filled
          if (threshold !== null || uncertainty !== null) {
            hasValidInput = true;

            // Validate input values
            if (
              (threshold !== null && isNaN(threshold)) ||
              (uncertainty !== null && isNaN(uncertainty)) ||
              (threshold !== null && threshold < 0) ||
              (uncertainty !== null && uncertainty < 0)
            ) {
              invalidFields.push(key);
            }

            // Push valid data to the request payload
            thresholdsData.push({
              greenhouseID: greenhouseID,
              parameter: key,
              threshold: threshold !== null ? threshold : this.currentThresholds[key].threshold,
              uncertainty: uncertainty !== null ? uncertainty : this.currentThresholds[key].uncertainty
            });
          }
        }

        // If no valid input, show error
        if (!hasValidInput) {
          this.errorMessage = "Please enter at least one new threshold value before submitting.";
          return;
        }

        // Send API request
        const response = await fetch("http://14.225.205.88:8000/POSTthresholds", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(thresholdsData),
        });

        const responseText = await response.text();
        console.log("API Response:", responseText);

        if (!response.ok) {
          throw new Error(`Error: ${responseText}`);
        }

        // Update the current thresholds with new values
        thresholdsData.forEach((item) => {
          this.currentThresholds[item.parameter].threshold = item.threshold;
          this.currentThresholds[item.parameter].uncertainty = item.uncertainty;
        });

        this.successMessage = "Thresholds updated successfully!";

        // Reset input fields
        this.updatedThresholds = {
          temperature: { threshold: null, uncertainty: null },
          humidity: { threshold: null, uncertainty: null },
          lightIntensity: { threshold: null, uncertainty: null },
          co2: { threshold: null, uncertainty: null },
        };

        // Refresh the threshold data from the server
        await this.fetchThresholdData();

      } catch (error) {
        console.error("Error updating thresholds:", error);
        this.errorMessage = `Error: ${error.message}`;
      }
    },
  },

  created() {
    this.fetchThresholdData();
  },
}

</script>

<style scoped>

</style>