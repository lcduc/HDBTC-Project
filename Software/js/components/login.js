const Login = {
    data() {
        return {
            email: '',
            password: '',
            emailError: '',  
            passwordError: '', 
        };
    },

    methods: {
        validateForm() {
            let isValid = true; 
            this.emailError = ''; 
            this.passwordError = ''; 

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

        login() {
            if (this.validateForm()) {
                this.$router.push('/home'); 
            }
        },
    },

    template: `
        <div class="container d-flex justify-content-center align-items-center min-vh-100">
            <div class="row rounder-5 shadow box-area flex-column flex-md-row">
                <div class="col-md-6 left-box order-2 order-md-1">
                    <div class="row align-items-center">
                        <div class="header-text mb-4">
                            <img src="img/leaf-icon.png" alt="logo_image" class="logo_image">
                            <h1 class="text-center">WELCOME!</h1>
                            <p class="text-center">Please login with the account provided.</p>
                        </div>
                        <div class="login_form">
                            <form @submit.prevent="login" class="login-form" id="loginForm">
                                <div class="form-group">
                                    <div class="input-icon-wrapper">
                                        <i class="fas fa-envelope icon"></i>
                                        <input type="text" class="form-control" v-model="email" id="email" placeholder="Email Address">
                                    </div>
                                    <div v-if="emailError" class="text-danger">{{ emailError }}</div> <!-- Email error message -->
                                </div>
                                <div class="form-group mt-2">
                                    <div class="input-icon-wrapper">
                                        <i class="fas fa-lock icon"></i>
                                        <input type="password" class="form-control" v-model="password" id="password" placeholder="Password">
                                    </div>
                                    <div v-if="passwordError" class="text-danger">{{ passwordError }}</div> <!-- Password error message -->
                                </div>  
                                <button type="submit" class="btn login-button mt-4 mb-3">
                                    LOG IN
                                    <i class="fas fa-arrow-right arrow-icon"></i>
                                </button>                                                    
                            </form>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 rounder-4 d-flex justify-content-center align-items-center flex-column right-box order-1 order-md-2">
                    <div class="featured-image">
                        <img src="img/login_image.png" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
    `
};
