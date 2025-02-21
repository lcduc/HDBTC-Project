<template>
  <div class="mt-3 mb-3 ml-10 mr-10">
    <div v-if="isLoading" class="text-center">
      Loading Devices Management...
    </div>
    <div v-else>
      <div class="page-content">
        <div class="d-flex justify-content-between align-items-center" style="margin-top: 20px;">
          <div class="p-2">
            <h1>
              <img src="../assets/img/leaf-icon.png" alt="leaf_icon" />
              Devices Management
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

      <div class="mb-6">
        <button class="back-btn btn btn-light" @click="$router.go(-1)" style="color: #8A8A8A;">
          <img src="../assets/img/arrow-left.png" alt="arrow_left_icon"> Back
        </button>
      </div>

      <div class="mb-10">
        <h2>Greenhouse Device Control</h2>
        <form @submit.prevent="submitDevices">
          <div v-for="device in devices" :key="device.id" class="device-item">
            <!-- Device Name (Left side) -->
            <span class="device-name">{{ device.name }}</span>

            <!-- ON/OFF Buttons (Right side, vertically aligned) -->
            <div class="button-group">
              <button :class="device.status ? 'on' : ''" @click.prevent="updateStatus(device, true)">
                ON
              </button>

              <button :class="!device.status ? 'off' : ''" @click.prevent="updateStatus(device, false)">
                OFF
              </button>
            </div>
          </div>

          <button type="submit" class="submit-button">Submit Changes</button>
        </form>
      </div>


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
      isLoading: true,
      devices: [],
      errorMessage: "",
      successMessage: "",
    };
  },

  methods: {
    async fetchDevices() {
      try {
        const response = await fetch(
          "http://14.225.205.88:8000/get_device_status/1"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch devices");
        }

        const data = await response.json();
        this.devices = data.map((device) => ({
          id: device.device_id,
          name: device.device_name,
          status: device.status === "1", // Convert to boolean (true for ON, false for OFF)
        }));
      } catch (error) {
        console.error("Error fetching devices:", error);
        this.errorMessage = "Failed to load device data. Please try again.";
      } finally {
        this.isLoading = false;
      }
    },

    updateStatus(device, status) {
      device.status = status;
    },

    async submitDevices() {
      try {
        const payload = this.devices.map((device) => ({
          greenhouseID: 1,
          deviceID: device.id,         // Use "deviceID" instead of "device_id"
          device_status: device.status ? 1 : 0, // Use "device_status" as a number
        }));

        console.log("Sending payload:", JSON.stringify(payload)); // Debugging output

        const response = await fetch("http://14.225.205.88:8000/update_device_status", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Server error response:", errorData);
          throw new Error("Failed to update devices");
        }

        this.successMessage = "Device statuses updated successfully!";
      } catch (error) {
        console.error("Error submitting devices:", error);
        this.errorMessage = "Failed to update device status. Please try again.";
      }
    },

    logout() {
      localStorage.removeItem("user");
      this.$router.push("/");
    },
  },

  mounted() {
    const user = localStorage.getItem("user");
    if (!user) {
      this.$router.push("/");
      return;
    }
    this.fetchDevices();
  },
};
</script>



<style scoped>
.page-content,
.mb-6,
.mb-10 {
  margin: 0 2em;
}

.container {
  max-width: 80em;
  margin: auto;
  padding: 20px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.device-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.device-name {
  flex: 1;
  /* Allows the device name to take available space */
  text-align: left;
  /* Align text to the left */
}

.button-group {
  display: flex;
  gap: 10px;
  /* Space between ON and OFF buttons */
}

button {
  width: 80px;
  /* Ensure all buttons have the same width */
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
}

.on {
  background-color: green;
  color: white;
}

.off {
  background-color: red;
  color: white;
}

.submit-button {
  width: 200px;
  /* Adjust width as needed */
  padding: 10px;
  background-color: blue;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  display: block;
  /* Ensures it aligns properly */
  margin: 20px auto;
  /* Centers it */
}
</style>
