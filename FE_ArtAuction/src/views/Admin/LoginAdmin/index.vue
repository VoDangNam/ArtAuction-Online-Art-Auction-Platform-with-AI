<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-gradient-grey-blue">
    <div
      class="card border-0 shadow-lg rounded-4 overflow-hidden m-3"
      style="max-width: 900px; width: 100%"
    >
      <div class="row g-0">
        <div class="col-md-6 d-none d-md-block position-relative bg-primary">
          <img
            src="https://i.pinimg.com/736x/28/2f/a0/282fa0779bf72924451a31f4273b02d6.jpg"
            class="w-100 h-100 object-fit-cover position-absolute top-0 start-0"
            alt="Art Background"
            loading="lazy"
          />
          <div class="position-absolute top-0 start-0 w-100 h-100 bg-dark bg-opacity-25"></div>

          <div class="position-absolute bottom-0 start-0 p-5 text-white">
            <h3 class="fw-bold">Discover Unique Art</h3>
            <p class="small opacity-75 mb-0">Connect with local artists and collectors.</p>
          </div>
        </div>

        <div class="col-md-6 bg-white p-4 p-md-5">
          <div class="d-flex flex-column h-100 justify-content-center">
            <div class="text-center mb-4">
              <h2
                class="fw-bold text-primary mb-1 d-flex align-items-center justify-content-center gap-2"
              >
                <img src="/src/assets/img/LogoAdmin.png" alt="ArtAuction Logo" height="40" />
                ArtAuction
              </h2>
              <p class="text-secondary small">Welcome back! Please login to your account.</p>
            </div>

            <form @submit.prevent="DangNhap">
              <div class="form-floating mb-3">
                <input
                  v-model="ad.email"
                  type="text"
                  class="form-control border-0 bg-light rounded-3"
                  id="floatingInput"
                  placeholder="name@example.com"
                />

                <label for="floatingInput" class="text-secondary">Email</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  v-model="ad.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control border-0 bg-light rounded-3"
                  id="floatingPassword"
                  placeholder="Password"
                  @keyup.enter="DangNhap"
                />

                <label for="floatingPassword" class="text-secondary">Password</label>

                <span
                  class="position-absolute top-50 end-0 translate-middle-y me-3 text-secondary"
                  style="cursor: pointer; z-index: 10"
                  @click="showPassword = !showPassword"
                >
                  <i :class="showPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"></i>
                </span>
              </div>

              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="rememberMe" />
                  <label class="form-check-label text-secondary small" for="rememberMe">
                    Remember me
                  </label>
                </div>
                <!-- <a href="#" class="text-decoration-none text-primary small fw-bold"
                  >Forgot Password?</a
                > -->
              </div>

              <button
                v-on:click="DangNhap()"
                type="button"
                class="btn btn-primary btn-lg w-100 rounded-pill fw-bold shadow-sm mb-4"
              >
                Login
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      showPassword: false,
      ad: {
        password: "",
      },
    };
  },
  methods: {
    DangNhap() {
      axios
        .post("http://localhost:8081/api/admin/auth/login", this.ad)
        .then((res) => {
          if (res.data.status) {
            this.$toast.success(res.data.message);
            console.log("log ad", res.data);

            localStorage.setItem("token", res.data.token);
            this.user = {
              email: "",
              password: "",
            };

            this.$router.push("/admin/dashboard");
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
        });
    },
  },
};
</script>

<style scoped></style>
