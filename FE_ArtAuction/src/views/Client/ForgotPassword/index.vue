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
      <div class="row d-flex justify-content-around align-items-center w-100">
        <div class="col-lg-5 col-md-8 col-sm-12">
          <div class="card card-acc" data-aos="zoom-in" data-aos-duration="500">
            <div class="card-body p-5 ">
              <!-- Step 1: Enter Email -->
              <div v-if="step === 1" class="d-flex flex-column gap-3">
                <div class="d-flex justify-content-center align-items-center gap-3">
                  <div class="d-flex gap-3 align-items-center mb-auto">
                    <img src="../../../assets/img/Logo_AA.png" class="logoLogin" alt="">
                  </div>
                </div>
                <div class="d-flex flex-column gap-2 mb-2">
                  <h3 class="text-center text-success fw-bold m-0">Change Password</h3>
                  <p class="text-center text-muted">Enter your email. We’ll send a verification code.</p>
                </div>
                <div class="group-input col-lg-12 col-md-12">
                  <input v-model="email" type="email" class="form-control" id="forgotEmail" required
                    @keydown.enter.prevent="sendOtp" :disabled="sendingOtp">
                  <label for="forgotEmail">Email</label>
                  <i class="bi bi-envelope fa-xl text-success"></i>
                </div>

                <button class="btn btn-success fw-bold w-100 fs-6" @click="sendOtp" :disabled="sendingOtp || !email">
                  <span v-if="sendingOtp" class="spinner-border spinner-border-sm me-2" role="status"
                    aria-hidden="true"></span>
                  {{ sendingOtp ? 'Sending...' : 'Send Verification Code' }}
                </button>

                <router-link to="/login" class="text-center text-success fs-6 text-decoration-none">
                  <i class="fa-solid fa-arrow-left me-2"></i>Back
                </router-link>
              </div>

              <!-- Step 2: Enter OTP -->
              <div v-if="step === 2" class="d-flex flex-column gap-3">
                <h3 class="text-center text-success fw-bold mb-4">Enter Verification Code</h3>
                <p class="text-center text-muted mb-2">We've sent a 6-digit code to</p>
                <p class="text-center text-success fw-bold mb-4">{{ email }}</p>

                <div class="d-flex justify-content-center gap-2 mb-3">
                  <input v-for="(digit, index) in otp" :key="index" :ref="el => { if (el) otpInputs[index] = el }"
                    v-model="otp[index]" type="text"
                    :class="['form-control', 'text-center', 'fw-bold', { 'border-success': digit !== '' }]"
                    style="width: 50px; height: 60px; font-size: 24px;" maxlength="1"
                    @input="handleOtpInput(index, $event)" @keydown="handleOtpKeydown(index, $event)"
                    @paste="handleOtpPaste($event)" :disabled="verifyingOtp" />
                </div>

                <div class="text-center mb-3">
                  <p class="text-muted small mb-0">Didn't receive the code?</p>
                  <button type="button" class="btn btn-link p-0 text-success" @click="resendOtp" :disabled="sendingOtp">
                    {{ sendingOtp ? 'Sending...' : 'Resend code' }}
                  </button>
                </div>

                <button class="btn btn-success fw-bold w-100 fs-6" @click="verifyOtp"
                  :disabled="!isOtpComplete || verifyingOtp">
                  <span v-if="verifyingOtp" class="spinner-border spinner-border-sm me-2"></span>
                  {{ verifyingOtp ? 'Verifying...' : 'Verify Code' }}
                </button>

                <button type="button" class="btn btn-link text-center text-muted text-decoration-none"
                  @click="step = 1">
                  <i class="fa-solid fa-arrow-left me-2"></i>Change email
                </button>
              </div>

              <!-- Step 3: Reset Password -->
              <div v-if="step === 3" class="d-flex flex-column gap-3">
                <h3 class="text-center text-success fw-bold mb-4">Reset Password</h3>
                <p class="text-center text-muted">Enter your new password</p>

                <div class="group-input col-lg-12 col-md-12">
                  <input v-model="newPassword" :type="showPassword ? 'text' : 'password'" class="form-control"
                    id="newPassword" required @keydown.enter.prevent="resetPassword">
                  <label for="newPassword">New Password</label>
                  <i class="bi fa-xl" :class="showPassword ? 'bi-eye' : 'bi-eye-slash'" @click="togglePassword"
                    style="cursor: pointer;"></i>
                </div>

                <div class="group-input col-lg-12 col-md-12">
                  <input v-model="confirmPassword" :type="showRePassword ? 'text' : 'password'" class="form-control"
                    id="confirmPassword" required @keydown.enter.prevent="resetPassword">
                  <label for="confirmPassword">Confirm Password</label>
                  <i class="bi fa-xl" :class="showRePassword ? 'bi-eye' : 'bi-eye-slash'" @click="toggleRePassword"
                    style="cursor: pointer;"></i>
                </div>

                <button class="btn btn-success fw-bold w-100 fs-6" @click="resetPassword"
                  :disabled="resettingPassword || !newPassword || !confirmPassword">
                  <span v-if="resettingPassword" class="spinner-border spinner-border-sm me-2"></span>
                  {{ resettingPassword ? 'Resetting...' : 'Reset Password' }}
                </button>

                <button type="button" class="btn btn-link text-center text-muted text-decoration-none"
                  @click="step = 2">
                  <i class="fa-solid fa-arrow-left me-2"></i>Back to verification
                </button>
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
  name: "ForgotPassword",
  data() {
    return {
      step: 1, // 1: Email, 2: OTP, 3: New Password
      email: "",
      otp: ['', '', '', '', '', ''],
      otpInputs: [],
      newPassword: "",
      confirmPassword: "",
      showPassword: false,
      showRePassword: false,
      sendingOtp: false,
      verifyingOtp: false,
      resettingPassword: false,
    };
  },
  computed: {
    isOtpComplete() {
      return this.otp.every(digit => digit !== '');
    }
  },
  mounted() {
    // Focus first OTP input when step changes to 2
    this.$watch('step', (newStep) => {
      if (newStep === 2) {
        this.$nextTick(() => {
          this.resetOtp();
        });
      }
    });
  },
  methods: {
    // Step 1: Send OTP
    sendOtp() {
      if (!this.email || !this.email.trim()) {
        this.$toast.error("Please enter your email");
        return;
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.$toast.error("Invalid email format");
        return;
      }

      this.sendingOtp = true;

      axios
        .post("http://localhost:8081/api/auth/forgot-password", { email: this.email })
        .then((res) => {
          if (res.data.status === 1) {
            this.$toast.success(res.data.message || "Verification code has been sent to your email");
            this.step = 2;
          } else {
            this.$toast.error(res.data.message || "Failed to send verification code");
          }
        })
        .catch((err) => {
          const errorMessage = err.response?.data?.message || "Failed to send verification code. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.sendingOtp = false;
        });
    },

    // Step 2: Verify OTP
    handleOtpInput(index, event) {
      const value = event.target.value.replace(/[^0-9]/g, '');
      this.otp[index] = value;

      // Auto focus next input
      if (value && index < 5) {
        this.$nextTick(() => {
          this.otpInputs[index + 1]?.focus();
        });
      }
    },

    handleOtpKeydown(index, event) {
      // Handle backspace
      if (event.key === 'Backspace' && !this.otp[index] && index > 0) {
        this.$nextTick(() => {
          this.otpInputs[index - 1]?.focus();
        });
      }
      // Handle arrow keys
      if (event.key === 'ArrowLeft' && index > 0) {
        this.otpInputs[index - 1]?.focus();
      }
      if (event.key === 'ArrowRight' && index < 5) {
        this.otpInputs[index + 1]?.focus();
      }
    },

    handleOtpPaste(event) {
      event.preventDefault();
      const pastedData = event.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, 6);

      for (let i = 0; i < 6; i++) {
        this.otp[i] = pastedData[i] || '';
      }

      // Focus the last filled input or the first empty one
      const lastFilledIndex = Math.min(pastedData.length - 1, 5);
      this.$nextTick(() => {
        this.otpInputs[lastFilledIndex]?.focus();
      });
    },

    verifyOtp() {
      const otpCode = this.otp.join('');
      if (otpCode.length !== 6) {
        this.$toast.error("Please enter the complete 6-digit code");
        return;
      }

      this.verifyingOtp = true;

      axios
        .post("http://localhost:8081/api/auth/verify-otp", {
          email: this.email,
          otp: otpCode
        })
        .then((res) => {
          if (res.data.status === 1) {
            this.$toast.success(res.data.message || "OTP verified successfully");
            this.step = 3;
          } else {
            this.$toast.error(res.data.message || "Invalid OTP");
            this.resetOtp();
          }
        })
        .catch((err) => {
          const errorMessage = err.response?.data?.message || "Verification failed. Please try again.";
          this.$toast.error(errorMessage);
          this.resetOtp();
        })
        .finally(() => {
          this.verifyingOtp = false;
        });
    },

    resendOtp() {
      this.sendingOtp = true;
      axios
        .post("http://localhost:8081/api/auth/forgot-password", { email: this.email })
        .then((res) => {
          if (res.data.status === 1) {
            this.$toast.success(res.data.message || "Verification code has been resent");
            this.resetOtp();
          } else {
            this.$toast.error(res.data.message || "Failed to resend verification code");
          }
        })
        .catch((err) => {
          const errorMessage = err.response?.data?.message || "Failed to resend OTP. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.sendingOtp = false;
        });
    },

    resetOtp() {
      this.otp = ['', '', '', '', '', ''];
      this.$nextTick(() => {
        this.otpInputs[0]?.focus();
      });
    },

    // Step 3: Reset Password
    resetPassword() {
      if (!this.newPassword || !this.newPassword.trim()) {
        this.$toast.error("Please enter new password");
        return;
      }

      // Validate Password length
      const trimmedPassword = this.newPassword.trim();
      if (trimmedPassword.length < 6) {
        this.$toast.error("Password must be at least 6 characters");
        return;
      }
      if (trimmedPassword.length >= 15) {
        this.$toast.error("Password must be less than 15 characters");
        return;
      }

      if (!this.confirmPassword || !this.confirmPassword.trim()) {
        this.$toast.error("Please confirm your password");
        return;
      }

      // Check if password and confirmPassword match
      if (trimmedPassword !== this.confirmPassword.trim()) {
        this.$toast.error("Password and Confirm Password do not match");
        this.newPassword = "";
        this.confirmPassword = "";
        return;
      }

      this.resettingPassword = true;

      const otpCode = this.otp.join('');

      axios
        .post("http://localhost:8081/api/auth/reset-password", {
          email: this.email,
          otp: otpCode,
          newPassword: trimmedPassword
        })
        .then((res) => {
          if (res.data.status === 1) {
            this.$toast.success(res.data.message || "Password reset successfully");
            // Redirect to login after 2 seconds
            setTimeout(() => {
              this.$router.push('/login');
            }, 2000);
          } else {
            this.$toast.error(res.data.message || "Failed to reset password");
          }
        })
        .catch((err) => {
          const errorMessage = err.response?.data?.message || "Failed to reset password. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.resettingPassword = false;
        });
    },

    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    toggleRePassword() {
      this.showRePassword = !this.showRePassword;
    },
  }
};
</script>

<style></style>
