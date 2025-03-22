<template>
  <div class="login-content">
    <div class="container d-flex justify-content-center align-items-center min-vh-95">
      <div class="row rounded-5 shadow box-area flex-column flex-md-row">
        <div class="col-md-6 left-box order-2 order-md-1">
          <div class="row align-items-center">
            <div class="header-text mb-4">
              <img src="../assets/img/leaf-icon.png" alt="logo_image" class="logo_image">
              <h1 class="text-center">WELCOME!</h1>
              <p class="text-center">Please login with the account provided.</p>
            </div>
            <div class="login_form">
              <form @submit.prevent="login" class="login-form" id="loginForm">
                <div class="form-group">
                  <div class="input-icon-wrapper">
                    <i class="fas fa-envelope icon"></i>
                    <input type="text" class="form-control" v-model="email" id="email" placeholder="Email Address"
                      @keydown.enter="login" />
                  </div>
                  <div v-if="emailError" class="text-danger">{{ emailError }}</div>
                </div>
                <div class="form-group mt-2">
                  <div class="input-icon-wrapper">
                    <i class="fas fa-lock icon"></i>
                    <input type="password" class="form-control" v-model="password" id="password" placeholder="Password"
                      @keydown.enter="login" />
                  </div>
                  <div v-if="passwordError" class="text-danger">{{ passwordError }}</div>
                </div>
                <button type="submit" class="btn login-button mt-4 mb-3">
                  LOG IN
                  <i class="fas fa-arrow-right arrow-icon"></i>
                </button>
                <div v-if="loginError" class="text-danger mt-2">{{ loginError }}</div>
              </form>
            </div>
          </div>
        </div>


        <div
          class="col-md-6 rounded-4 d-flex justify-content-center align-items-center flex-column right-box order-1 order-md-2">
          <div class="featured-image">
            <img src="../assets/img/login_image.png" class="img-fluid">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      emailError: '',
      passwordError: '',
      loginError: '',
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.emailError = '';
      this.passwordError = '';
      this.loginError = '';

      // Validate email
      if (!this.email) {
        this.emailError = 'Please enter your email address.';
        isValid = false;
      } else {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(this.email)) {
          this.emailError = 'Please enter a valid email address.';
          isValid = false;
        }
      }

      // Validate password
      if (!this.password) {
        this.passwordError = 'Please enter your password.';
        isValid = false;
      }

      return isValid;
    },
    async login() {
      if (this.validateForm()) {
        try {
          const response = await fetch('http://14.225.205.88:8000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password
            }),
          });

          if (!response.ok) {
            if (response.status === 401) {
              this.loginError = 'Invalid email or password.';
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();

          if (data.message === 'Login successful') {
            // Store user data including accountID
            localStorage.setItem('user', JSON.stringify(data));
            this.$router.push('/homepage');
          } else {
            this.loginError = 'Invalid email or password.';
          }
        } catch (error) {
          console.error('Login error:', error);
        }
      }
    }
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.login-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: url('../assets/img/login_background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}

.row {
  border-radius: 25px;
}

.box-area {
  width: 1000px;
}

.left-box {
  background-color: #fff;
  border-radius: 25px;
  padding: 0 2rem;
}

.left-box h1 {
  font-weight: 400;
  font-size: 2rem;
  color: #04360F;
}

.left-box p {
  font-size: 10px;
  color: #AEAEAE;
  font-style: italic;
  letter-spacing: .5px;
}

.input-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.icon {
  position: absolute;
  left: 10px;
  color: #AEAEAE;
  font-size: 1.5rem;
}

.form-control::placeholder {
  color: #AEAEAE;
  font-size: .9rem;
  margin-left: 20px;
  letter-spacing: .5px;
}

.form-control {
  height: 50px;
  padding-left: 50px;
  border-radius: 5px !important;
  box-sizing: border-box;
}

.login-button {
  background-color: #88C47A;
  width: 100%;
  height: 50px;
  border-radius: 5px !important;
  color: #fff !important;
  padding: 5px;
  font-weight: 500;
  transition: background-color 0.3s ease, opacity 0.3s ease;
}

.login-button:hover {
  background-color: #61995a;
  opacity: 0.9;
}

.arrow-icon {
  margin-left: 5px;
  font-size: 1rem;
  color: #fff;
}

.logo_image {
  display: block;
  margin: 3rem auto 1rem auto;
  width: 40px;
}

.right-box {
  padding: 0;
  margin: 0;
}

.right-box .featured-image img {
  padding: 0;
  margin: 0;
  max-width: 100%;
  height: auto;
  display: block;
  border-radius: 25px;
}
</style>