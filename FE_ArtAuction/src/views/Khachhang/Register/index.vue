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
      <div class="row d-flex justify-content-around align-items-center  w-100">
        <div class="col-lg-5 col-md-4 col-sm-12 d-flex flex-column d-none d-md-inline" data-aos="fade-right"
          data-aos-duration="800">
          <div class="d-flex gap-3 align-items-center mb-auto">
            <img src="../../../assets/img/Logo_AA.png" class="logoLogin" alt="">
            <h3 class="fw-bold m-0"><span class="text-success fw-bold ">Art</span>Auction</h3>
          </div>
          <div class="py-lg-5 my-5">
            <h1 class="text-acc pb-2">Let’s get started !</h1>
            <div class="border border-3 w-75 border-success rounded mb-5"></div>
            <p class="left mb-lg-5 py-3">Becoming a member is the first step toward owning pieces that truly
              inspire, opening the
              door to
              new experiences and meaningful connections.</p>
          </div>
        </div>
        <div class="col-lg-5 col-md-8 col-sm-12 ">
          <div class="card card-acc" data-aos="fade-left" data-aos-duration="800">
            <div class="card-body p-5">
              <!-- form -->
              <div class="d-flex flex-column gap-2">
                <h3 class="text-center text-success fw-bold mb-4">Sign Up</h3>
                <div class="d-flex flex-column gap-3">
                  <!-- Username -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="tai_khoan.username" type="text" class="form-control" id="username" required
                      @keydown.enter.prevent="DangKy">
                    <label for="username">Username</label>
                    <i class="bi bi-person fa-xl text-success"></i>
                  </div>
                  <!-- Email -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="tai_khoan.email" type="email" class="form-control" id="email" required
                      @keydown.enter.prevent="DangKy">
                    <label for="email">Email</label>
                    <i class="bi bi-envelope fa-xl text-success"></i>
                  </div>
                  <!-- Password -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="tai_khoan.password" :type="showPassword ? 'text' : 'password'" class="form-control"
                      id="password" required @keydown.enter.prevent="DangKy">
                    <label for="password">Password</label>
                    <i class="bi fa-xl" :class="showPassword ? 'bi-eye' : 'bi-eye-slash'" @click="togglePassword"
                      style="cursor: pointer;"></i>
                  </div>
                  <!-- RePassword -->
                  <div class="group-input col-lg-12 col-md-12">
                    <input v-model="tai_khoan.confirmPassword" :type="showRePassword ? 'text' : 'password'"
                      class="form-control" id="repassword" required @keydown.enter.prevent="DangKy">
                    <label for="repassword">RePassword</label>
                    <i class="bi fa-xl" :class="showRePassword ? 'bi-eye' : 'bi-eye-slash'" @click="toggleRePassword"
                      style="cursor: pointer;"></i>
                  </div>
                </div>

                <!-- Terms & Conditions -->
                <div class="form-check">
                  <input class="form-check-input border border-success" type="checkbox" id="terms" v-model="acceptTerms"
                    required>
                  <label class="form-check-label text-muted" for="terms">
                    I agree to the <a href="#" class="text-success text-decoration-none" @click.prevent="openTermsModal">Terms &
                      Conditions</a>
                  </label>
                </div>

                <div class="d-flex flex-column align-items-center gap-3 mt-2">
                  <button class="btn btn-success fw-bold w-100 fs-6" @click="DangKy()" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"
                      aria-hidden="true"></span>
                    {{ loading ? 'Signing up...' : 'Sign Up' }}
                  </button>

                  <!-- Hidden button to trigger OTP modal -->
                  <button ref="otpModalTrigger" class="d-none" data-bs-toggle="modal"
                    data-bs-target="#exampleModal"></button>


                  <p class="m-0">Already have an account?
                    <router-link to="/login" href="#" class="text-success fw-bold text-decoration-none">Sign
                      In</router-link>
                  </p>
                </div>
              </div>
            </div>


          </div>
        </div>
      </div>
      <!-- Terms & Conditions Modal -->
      <div v-if="showTermsModal">
        <div class="modal-backdrop fade show"></div>
        <div class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true" @click.self="closeTermsModal">
          <div class="modal-dialog modal-lg modal-dialog-scrollable">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Terms &amp; Conditions</h5>
                <button type="button" class="btn-close" @click="closeTermsModal"></button>
              </div>
              <div class="modal-body p-0">
                <div class="px-3 py-3" style="height: 70vh; overflow-y: auto;" @scroll="handleTermsScroll"
                  ref="termsScroll">
                  <div v-if="termsHtml" v-html="termsHtml"></div>
                  <p v-else class="text-center text-muted my-4">
                    Loading terms &amp; conditions...
                  </p>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeTermsModal">
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- OTP Modal -->
      <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header position-relative d-flex justify-content-center align-items-center">
              <h1 class="modal-title text-success fw-bold fs-5 m-0" id="exampleModalLabel">Enter Verification Code</h1>
            </div>
            <div class="modal-body">
              <div class="text-center mb-4">
                <p class="text-muted mb-2">We've sent a 6-digit code to your email</p>
                <p class=" text-success fw-bold">{{ tai_khoan.email || 'your email' }}</p>
              </div>
              <div class="d-flex justify-content-center gap-2 mb-4">
                <input
                  v-for="(digit, index) in otp"
                  :key="index"
                  :ref="el => { if (el) otpInputs[index] = el }"
                  v-model="otp[index]"
                  type="text"
                  :class="['form-control', 'text-center', 'fw-bold', { 'border-success': digit !== '' }]"
                  style="width: 50px; height: 60px; font-size: 24px;"
                  maxlength="1"
                  @input="handleOtpInput(index, $event)"
                  @keydown="handleOtpKeydown(index, $event)"
                  @paste="handleOtpPaste($event)"
                />
              </div>
              <div class="text-center">
                <p class="text-muted small mb-0">Didn't receive the code?</p>
                <button type="button" class="btn btn-link p-0 text-success" @click="resendOtp">
                  Resend code
                </button>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success w-100 fw-bold fs-6" @click="verifyOtp()" :disabled="!isOtpComplete || verifyingOtp">
                <span v-if="verifyingOtp" class="spinner-border spinner-border-sm me-2"></span>
                {{ verifyingOtp ? 'Verifying...' : 'Verify' }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
<script>
import router from '@/router';
import axios from 'axios'
export default {
  data() {
    return {
      showPassword: false,
      showRePassword: false,
      acceptTerms: false,
      loading: false,
      tai_khoan: {},
      otp: ['', '', '', '', '', ''],
      otpInputs: [],
      verifyingOtp: false,
      showTermsModal: false,
      termsHtml: '',
    }
  },
  methods: {
    DangKy() {
      // Prevent double click
      if (this.loading) {
        return;
      }

      // Check all required fields
      if (!this.tai_khoan.username || !this.tai_khoan.username.trim()) {
        this.$toast.error("Please enter Username");
        this.tai_khoan.username = "";
        this.$nextTick(() => {
          document.getElementById('username')?.focus();
        });
        return;
      }

      // Validate Username length: ít nhất 3 ký tự và nhỏ hơn 20 ký tự
      const trimmedUsername = this.tai_khoan.username.trim();
      if (trimmedUsername.length < 3) {
        this.$toast.error("Username must be at least 3 characters");
        this.tai_khoan.username = "";
        this.$nextTick(() => {
          document.getElementById('username')?.focus();
        });
        return;
      }
      if (trimmedUsername.length >= 20) {
        this.$toast.error("Username must be less than 20 characters");
        this.tai_khoan.username = "";
        this.$nextTick(() => {
          document.getElementById('username')?.focus();
        });
        return;
      }
      // Cập nhật username đã được trim
      this.tai_khoan.username = trimmedUsername;

      if (!this.tai_khoan.email || !this.tai_khoan.email.trim()) {
        this.$toast.error("Please enter Email");
        this.tai_khoan.email = "";
        this.$nextTick(() => {
          document.getElementById('email')?.focus();
        });
        return;
      }

      // Check email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.tai_khoan.email)) {
        this.$toast.error("Invalid email format");
        this.tai_khoan.email = "";
        this.$nextTick(() => {
          document.getElementById('email')?.focus();
        });
        return;
      }

      if (!this.tai_khoan.password || !this.tai_khoan.password.trim()) {
        this.$toast.error("Please enter Password");
        this.tai_khoan.password = "";
        this.$nextTick(() => {
          document.getElementById('password')?.focus();
        });
        return;
      }

      // Validate Password length: ít nhất 6 ký tự
      const trimmedPassword = this.tai_khoan.password.trim();
      if (trimmedPassword.length < 6) {
        this.$toast.error("Password must be at least 6 characters");
        this.tai_khoan.password = "";
        this.tai_khoan.confirmPassword = "";
        this.$nextTick(() => {
          document.getElementById('password')?.focus();
        });
        return;
      }
      if (trimmedPassword.length >= 15) {
        this.$toast.error("Password must be less than 15 characters");
        this.tai_khoan.password = "";
        this.tai_khoan.confirmPassword = "";
        this.$nextTick(() => {
          document.getElementById('password')?.focus();
        });
        return;
      }
      // Cập nhật password đã được trim
      this.tai_khoan.password = trimmedPassword;

      if (!this.tai_khoan.confirmPassword || !this.tai_khoan.confirmPassword.trim()) {
        this.$toast.error("Please enter RePassword");
        this.tai_khoan.confirmPassword = "";
        this.$nextTick(() => {
          document.getElementById('repassword')?.focus();
        });
        return;
      }

      // Check if password and confirmPassword match
      const trimmedConfirmPassword = this.tai_khoan.confirmPassword.trim();
      if (this.tai_khoan.password !== trimmedConfirmPassword) {
        this.$toast.error("Password and RePassword do not match");
        this.tai_khoan.password = "";
        this.tai_khoan.confirmPassword = "";
        this.$nextTick(() => {
          document.getElementById('password')?.focus();
        });
        return;
      }
      // Cập nhật confirmPassword đã được trim
      this.tai_khoan.confirmPassword = trimmedConfirmPassword;

      // Check Terms & Conditions checkbox
      if (!this.acceptTerms) {
        this.$toast.error("Please agree to Terms & Conditions");
        return;
      }

      // If all fields are valid, call register API
      this.loading = true;

      axios.post('http://localhost:8081/register', this.tai_khoan)
        .then(response => {
          const data = response.data || {};

          if (data.status === 1) {
            // Hiển thị thông báo thành công
            this.$toast.success(data.message || "Registration successful! Please verify your email.");
            console.log("Registration response:", data);

            // Reset OTP trước khi mở modal
            this.resetOtp();

            // Mở modal OTP để nhập mã xác thực
            // Sử dụng setTimeout để đảm bảo DOM đã render và toast đã hiển thị
            setTimeout(() => {
              // Cách 1: Dùng button trigger (đơn giản nhất)
              if (this.$refs.otpModalTrigger) {
                this.$refs.otpModalTrigger.click();
                console.log("Modal opened via trigger button");
                return;
              }

              // Cách 2: Dùng Bootstrap Modal API
              this.$nextTick(() => {
                const modalElement = document.getElementById('exampleModal');
                console.log("Modal element:", modalElement);

                if (modalElement) {
                  try {
                    // Thử dùng window.bootstrap hoặc global bootstrap
                    const Bootstrap = window.bootstrap || (typeof bootstrap !== 'undefined' ? bootstrap : null);

                    if (Bootstrap && Bootstrap.Modal) {
                      let modal = Bootstrap.Modal.getInstance(modalElement);
                      if (!modal) {
                        modal = new Bootstrap.Modal(modalElement, {
                          backdrop: 'static',
                          keyboard: false
                        });
                      }
                      modal.show();
                      console.log("Modal opened successfully via Bootstrap API");
                    } else {
                      console.error("Bootstrap Modal is not available");
                    }
                  } catch (error) {
                    console.error("Error opening modal:", error);
                  }
                } else {
                  console.error("OTP Modal element not found!");
                }
              });
            }, 300);

          } else {
            this.$toast.error(data.message || "Registration failed");
            console.log("Registration failed:", data);
          }

        })
        .catch((res) => {
          if (res.response && res.response.data && res.response.data.errors) {
            const errors = res.response.data.errors;
            // Clear fields that have errors
            if (errors.username) {
              this.tai_khoan.username = "";
            }
            if (errors.email) {
              this.tai_khoan.email = "";
            }
            if (errors.password) {
              this.tai_khoan.password = "";
              this.tai_khoan.confirmPassword = "";
            }

            const list = Object.values(errors);
            list.forEach((v) => {
              this.$toast.error(v[0]);
            });
          } else {
            this.$toast.error("An error occurred during registration");
          }
        })
        .finally(() => {
          this.loading = false;
        })

    },

    registerWithGoogle() {
      console.log('Register with Google clicked');
    },

    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    toggleRePassword() {
      this.showRePassword = !this.showRePassword;
    },

    // OTP Methods
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
      // Prevent double submission
      if (this.verifyingOtp) {
        console.log("❌ Already verifying, please wait...");
        return;
      }

      const otpCode = this.otp.join('');
      if (otpCode.length !== 6) {
        this.$toast.error("Please enter the complete 6-digit code");
        return;
      }

      if (!this.tai_khoan.email) {
        this.$toast.error("Email is required");
        return;
      }

      this.verifyingOtp = true;

      // Gọi API verify OTP - gửi email và otp
      axios.post('http://localhost:8081/verify-otp', {
        email: this.tai_khoan.email,
        otp: otpCode
      })
        .then(response => {
          this.verifyingOtp = false;

          const data = response.data || {};
          console.log("✅ API Response:", data);

          // Nếu status = 1: Thành công
          if (data.status == 1) {
            this.$toast.success(data.message || "OTP verified successfully");

            // Đóng modal
            const modalEl = document.getElementById('exampleModal');
            if (modalEl) {
              // Ẩn modal
              modalEl.classList.remove('show');
              modalEl.style.display = 'none';
              modalEl.setAttribute('aria-hidden', 'true');
              modalEl.removeAttribute('aria-modal');
              modalEl.removeAttribute('role');

              // Xóa backdrop
              const backdrops = document.querySelectorAll('.modal-backdrop');
              backdrops.forEach(bd => bd.remove());

              // Reset body
              document.body.classList.remove('modal-open');
              document.body.style.overflow = '';
              document.body.style.paddingRight = '';
            }

            // Chuyển sang trang login sau khi modal đóng
            setTimeout(() => {
              this.$router.push('/login');
            }, 200);
          }
          // Nếu status = 0 hoặc khác: Thất bại
          else {
            this.$toast.error(data.message || "Invalid OTP. Please try again.");
            this.resetOtp();
          }
        })
        .catch(error => {
          this.verifyingOtp = false;
          console.error("❌ Error:", error);

          const errorMessage = error.response?.data?.message || "Verification failed. Please try again.";
          this.$toast.error(errorMessage);
          this.resetOtp();
        });
    },

    resendOtp() {
      // Kiểm tra email trước khi gửi
      if (!this.tai_khoan.email) {
        this.$toast.error("Email is required");
        return;
      }

      // Gọi API resend OTP - gửi lại OTP qua email
      axios.post('http://localhost:8081/resend-otp', {
        email: this.tai_khoan.email
      })
        .then(response => {
          const data = response.data || {};
          if (data.status === 1) {
            this.$toast.success(data.message || "OTP code has been resent to your email");
            this.resetOtp();
          } else {
            this.$toast.error(data.message || "Failed to resend OTP");
          }
        })
        .catch(error => {
          console.error("Resend OTP error:", error);
          const errorMessage = error.response?.data?.message || "Failed to resend OTP. Please try again.";
          this.$toast.error(errorMessage);
        });
    },

    resetOtp() {
      this.otp = ['', '', '', '', '', ''];
      this.$nextTick(() => {
        this.otpInputs[0]?.focus();
      });
    },

    openTermsModal() {
      this.showTermsModal = true;
      if (!this.termsHtml) {
        // Load terms content once from public HTML
        fetch('/terms-of-service.html')
          .then((res) => res.text())
          .then((html) => {
            this.termsHtml = html;
          })
          .catch((err) => {
            console.error('Failed to load terms:', err);
          });
      }
    },

    closeTermsModal() {
      this.showTermsModal = false;
    },

    handleTermsScroll(event) {
      // Optional: Add scroll tracking logic if needed
    },
  },
  computed: {
    isOtpComplete() {
      return this.otp.every(digit => digit !== '');
    }
  },
  mounted() {
    // Reset OTP when modal is shown
    this.$nextTick(() => {
      const modalElement = document.getElementById('exampleModal');
      if (modalElement) {
        modalElement.addEventListener('shown.bs.modal', () => {
          this.resetOtp();
        });
      }
    });
  },
}
</script>
<style></style>
