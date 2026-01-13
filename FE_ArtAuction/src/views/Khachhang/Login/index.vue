<template>
  <!-- Background chính với gradient và triangles -->
  <div class="login-background">
    <!-- Triangle shapes positioned like in the image -->
    <div class="triangle-1"></div>
    <div class="triangle-2"></div>
    <div class="triangle-3"></div>
    <div class="triangle-5"></div>
    <div class="triangle-6"></div>
    <div class="triangle-7"></div>
    <div class="triangle-8"></div>
    <div class="triangle-9"></div>


    <!-- Nội dung chính -->
    <div class="container container-acc">
      <div class="row d-flex justify-content-around  align-items-center w-100">
        <div class="col-lg-5 col-md-4  col-sm-12 d-flex flex-column d-none d-md-inline" data-aos="fade-right"
          data-aos-duration="800">
          <div class="d-flex gap-3 align-items-center mb-auto">
            <img src="../../../assets/img/Logo_AA.png" class="logoLogin" alt="">
            <h3 class="fw-bold m-0"><span class="text-success fw-bold ">Art</span>Auction</h3>
          </div>
          <div class="py-lg-5 my-5">
            <h1 class="text-acc pb-2">Welcome back!</h1>
            <div class="border border-3 w-75 border-success rounded mb-5"></div>
            <p class="left mb-5 py-3">Logging in lets you continue your journey of discovery and bidding,
              opening the
              door to inspiring pieces, unique experiences, and meaningful connections.</p>
          </div>
        </div>
        <div class="col-lg-5 col-md-8 col-sm-12">
          <div class="card card-acc" data-aos="fade-left" data-aos-duration="800">
            <div class="card-body p-5 ">
              <!-- form -->
              <div class=" d-flex flex-column gap-2">
                <h3 class="text-center text-success fw-bold mb-4">Log In</h3>
                <div class="d-flex flex-column gap-3">
                  <!-- Username -->
                  <!-- <div class="group-input col-lg-12 col-md-12">
										<input type="text" class="form-control" id="username" required>
										<label for="username">Username</label>
										<i class="bi bi-person fa-xl text-success"></i>
									</div> -->
                  <!-- Email -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="user.email" type="email" class="form-control" id="email" required
                      @keydown.enter.prevent="DangNhap">
                    <label for="email">Email</label>
                    <i class="bi bi-envelope fa-xl text-success"></i>
                  </div>
                  <!-- Password -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="user.password" :type="showPassword ? 'text' : 'password'" class="form-control"
                      id="password" required @keydown.enter.prevent="DangNhap">
                    <label for="password">Password</label>
                    <i class="bi fa-xl" :class="showPassword ? 'bi-eye' : 'bi-eye-slash'" @click="togglePassword"
                      style="cursor: pointer;"></i>
                  </div>
                </div>

                <!-- Remember me & Forgot password -->
                <div class="d-flex justify-content-between align-items-center">
                  <div class="form-check">
                    <input class="form-check-input border border-success" type="checkbox" id="rememberMe"
                      v-model="rememberMe">
                    <label class="form-check-label text-muted" for="rememberMe">
                      Remember me
                    </label>
                  </div>
                  <router-link to="/client/forgot-password" class="text-center text-success fs-6 text-decoration-none">
                    Forgot password
                  </router-link>
                </div>

                <div class="d-flex flex-column align-items-center gap-3 mt-3">
                  <button v-on:click="DangNhap()" class="btn btn-success fw-bold w-100" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"
                      aria-hidden="true"></span>
                    {{ loading ? 'Logging in...' : 'Login' }}
                  </button>

                  <!-- Divider -->
                  <!-- <div class="d-flex align-items-center w-100">
                    <hr class="flex-grow-1 border border-success">
                    <span class="px-3 text-muted">or</span>
                    <hr class="flex-grow-1 border border-success">
                  </div> -->

                  <!-- Google Login Button -->
                  <!-- <button
                    class="btn btn-google border-2 border-success w-100 d-flex align-items-center justify-content-center gap-2"
                    @click="loginWithGoogle">
                    <i class="fab fa-google"></i>
                    <span>Continue with Google</span>
                  </button> -->

                  <p class="m-0">Don't have an account?
                    <router-link to="/register" href="#" class="text-success fw-bold text-decoration-none">Sign
                      Up</router-link>
                  </p>
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
import axios from "axios";
export default {
  data() {
    return {
      showPassword: false,
      showRePassword: false,
      rememberMe: false,
      loading: false,

      user: {
        email: "",
        password: "",
      },

    }
  },
  mounted() {
    // Add global Enter key listener
    document.addEventListener('keydown', this.handleGlobalEnter);
  },
  beforeUnmount() {
    // Remove event listener when component is destroyed
    document.removeEventListener('keydown', this.handleGlobalEnter);
  },
  methods: {
    handleGlobalEnter(event) {
      // Trigger login when Enter is pressed anywhere (except when typing in inputs)
      if (event.key === 'Enter' && !this.loading) {
        const target = event.target;
        // Only trigger if not already in an input field (inputs have their own handlers)
        if (target.tagName !== 'INPUT' && target.tagName !== 'TEXTAREA') {
          this.DangNhap();
        }
      }
    },
    DangNhap() {
      // Prevent double click
      if (this.loading) {
        return;
      }

      this.loading = true;

      axios
        .post("http://localhost:8081/api/auth/login", this.user)
        .then((res) => {
          if (res.data.status == 1) {
            this.$toast.success(res.data.message);
            console.log(res.data);

            localStorage.setItem("token", res.data.token);
            this.user = {
              email: "",
              password: "",
            };
            this.$router.push('/client/home');

          } else {
            this.$toast.error(res.data.message);
            console.log(res.data);
          }

        })
        .catch((err) => {
          if (err.response && err.response.data) {
            if (err.response.data.errors) {
              const list = Object.values(err.response.data.errors);
              list.forEach((v) => {
                this.$toast.error(v[0]);
              });
            } else {
              this.$toast.error(err.response.data.message || "Login failed");
            }
          } else {
            this.$toast.error("Server error");
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },

    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    toggleRePassword() {
      this.showRePassword = !this.showRePassword;
    },



    loginWithGoogle() {
      // Google Login method
      console.log('Login with Google clicked');
      // TODO: Implement Google OAuth
    },

    forgotPassword() {
      // Forgot password method
      console.log('Forgot password clicked');
      // TODO: Implement forgot password functionality
      this.$toast.info('Forgot password functionality will be implemented soon!');
    }
  }
}
</script>
<style></style>
