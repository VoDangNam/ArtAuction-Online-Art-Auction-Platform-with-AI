<template>
  <div class="container mb-5">
    <div class="row">
      <div class="col-8">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-4 d-flex align-items-center flex-column gap-3">
                <img v-bind:src="thong_tin.avt || '/src/assets/img/avt.png'"
                  class="rounded-circle border border-3 border-success" alt="avt"
                  style="width: 150px; aspect-ratio: 1/1;" />
                <p class="m-0">{{ thong_tin.email }}</p>

                <!-- nút đổi avt -->
                <button class="btn btn-outline-success w-100 d-flex align-items-center justify-content-center gap-2 "
                  @click="triggerFileInput" :disabled="uploadingAvatar">
                  <div v-if="uploadingAvatar" class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <i v-else class="fa-solid fa-rotate"></i>
                  <p class="m-0 p-0">{{ uploadingAvatar ? 'Processing image...' : 'Change Avatar' }}</p>
                </button>

                <!-- input file ẩn -->
                <input type="file" ref="file" style="display: none" accept="image/*" @change="handleFileChange" />


                <router-link to="/client/forgot-password" class="text-center text-success fs-6 text-decoration-none w-100">
                  <button type="button" class="btn btn-success w-100">Change Password</button>
                </router-link>
              </div>
              <div class="col-8 ps-3">
                <div class="row">
                  <div class="mb-4 col-lg-12">
                    <label class="mb-2 text-success">Full name</label>
                    <input type="text" class="form-control" id="fullname" v-model="thong_tin.username" />
                  </div>

                  <div class="mb-4 col-lg-6">
                    <label class="mb-2 text-success">Gender</label>
                    <select v-model="thong_tin.gender" class="form-select" id="gender">
                      <option disabled value="">-- Choose Gender --</option>
                      <option v-for="option in genderOptions" :key="option.value" :value="option.value">
                        {{ option.label }}
                      </option>
                    </select>
                  </div>
                  <div class="mb-4 col-lg-6">
                    <label class="mb-2 text-success">Date of Birth</label>
                    <input type="date" class="form-control" v-model="thong_tin.dateOfBirth" :max="maxDate" />
                  </div>

                  <div class="mb-4 col-lg-12">
                    <label class="mb-2 text-success">Contact Number</label>
                    <input type="tel" class="form-control" id="phonenumber" v-model="thong_tin.phonenumber"
                      @input="formatPhoneNumber" maxlength="10" />
                    <small class="text-muted">Must be exactly 10 digits (numbers only)</small>
                  </div>

                  <div class="mb-4 col-lg-12">
                    <div class="d-flex align-items-center justify-content-between">
                      <label class="mb-2 text-success">Identification</label>
                      <small v-if="isKycVerified" class="text-success text-muted">ID card number has been
                        verified.</small>
                    </div>
                    <input type="text" class="form-control" v-model="thong_tin.cccd" :disabled="isKycVerified">
                  </div>



                  <div class="mb-4 col-lg-12">
                    <label class="mb-2 text-success">Address</label>
                    <input type="text" class="form-control" v-model="thong_tin.address" />
                  </div>

                  <div class="col-lg-12 d-flex justify-content-end gap-3">
                    <button type="button" class="btn btn-success w-md-100 w-md-auto px-5" @click="updateProfile()"
                      :disabled="loading">
                      <span v-if="loading">Saving...</span>
                      <span class="fs-6" v-else>Save changes</span>
                    </button>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>

      <div class="col-4">
        <div class="card">
          <div class="card-body d-flex flex-column gap-3">
            <div class="d-flex flex-column gap-2">
              <div class="d-flex align-items-center justify-content-between gap-2">
                <h5 class="m-0 fw-bold text-success">Identity Verification</h5>
                <span class="badge px-3 py-2" :class="kycStatusBadge.class">
                  {{ kycStatusBadge.label }}
                </span>
              </div>
              <small class="text-muted">Upload ID cards and a selfie to verify your identity</small>
            </div>

            <div class="kyc-upload" :class="{ 'disabled-upload': isKycVerified }" v-for="section in kycSections"
              :key="section.key">
              <label class="form-label fw-semibold d-flex align-items-center gap-2">
                <i :class="section.icon"></i> {{ section.label }}
                <span class="text-danger">*</span>
              </label>
              <div class="upload-dropzone" :class="{ 'has-file': kycFiles[section.key].preview }">
                <input type="file" accept="image/*" class="form-control" :id="`kyc-${section.key}`"
                  @change="handleKycFileChange(section.key, $event)" :disabled="isKycVerified" />
                <div v-if="!kycFiles[section.key].preview" class="text-center text-muted small">
                  <p class="m-0">Drag or click to choose an image (JPG/PNG, &lt; 5MB)</p>
                </div>
                <div v-else class="preview-wrapper">
                  <img :src="kycFiles[section.key].preview" alt="preview" class="img-fluid rounded">
                  <button class="btn btn-link text-danger p-0" @click="removeKycFile(section.key)"
                    :disabled="isKycVerified">
                    <i class="fa-solid fa-trash me-2"></i>Remove image
                  </button>
                </div>
              </div>
            </div>

            <button class="btn btn-success w-100 mt-auto" :disabled="isKycVerified || !canSubmitKyc || isSubmittingKyc"
              @click="submitKycVerification">
              <span v-if="isSubmittingKyc">
                <span class="spinner-border spinner-border-sm me-2"></span>Submitting...
              </span>
              <span v-else>Submit KYC Verification</span>
            </button>
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
      thong_tin: {
        username: "",
        email: "",
        phonenumber: "",
        cccd: "",
        address: "",
        avt: "",
        dateOfBirth: "",

      },
      gender: "",
      accountOwner: "",
      bankAccount: "",
      banks: [],
      bankName: "",
      loading: false,
      uploadingAvatar: false,
      error: null,
      avtPreview: "",
      kycStatus: 0,
      kycMessage: '',
      isSubmittingKyc: false,
      userRole: 0,
      kycSections: [
        { key: 'cccdFront', label: 'ID card - front side', icon: 'fa-regular fa-id-card' },
        { key: 'cccdBack', label: 'ID card - back side', icon: 'fa-regular fa-id-card' },
        { key: 'selfie', label: 'Selfie with ID card', icon: 'fa-solid fa-user-check' }
      ],
      kycFiles: {
        cccdFront: { file: null, preview: '' },
        cccdBack: { file: null, preview: '' },
        selfie: { file: null, preview: '' }
      },
      genderOptions: [
        { value: 0, label: "Male" },
        { value: 1, label: "Female" },
        { value: 2, label: "Other" },
      ],
    };
  },

  computed: {
    kycStatusBadge() {
      const status = Number(this.kycStatus);
      if (status === 1) {
        return { label: 'Verified', class: 'bg-success text-white' };
      }
      return { label: 'Not verified', class: 'bg-secondary text-white' };
    },
    isKycVerified() {
      return Number(this.kycStatus) === 1;
    },
    canSubmitKyc() {
      return Object.values(this.kycFiles).every(item => !!item.file);
    },
    maxDate() {
      // Trả về ngày hiện tại dưới dạng YYYY-MM-DD
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  },

  mounted() {
    // this.loadEmail();
    // this.loadAvt();
    this.fetchBankName();
    this.loadUserData();
  },

  methods: {
    loadUserData() {
      axios
        .get('http://localhost:8081/api/user/info', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          this.thong_tin = res.data;
          this.kycStatus = res.data?.kycStatus ?? 0;
          this.kycMessage = res.data?.kycNote || '';

          // Luôn sync role từ API vào localStorage
          if (res.data?.role !== undefined && res.data?.role !== null) {
            this.userRole = res.data.role;
            localStorage.setItem("role_kh", res.data.role.toString());
          }
        })
        .catch((err) => {
          console.error(err);
          this.$toast.error("Unable to load user information!");
        });
    },

    // loadEmail() {
    //   this.email = localStorage.getItem("email_kh") || "";
    // },

    loadAvt() {
      this.avt = localStorage.getItem("userAvt") || "";
    },

    // mở input file
    triggerFileInput() {
      this.$refs.file.click();
    },

    // chọn file
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        // Kiểm tra xem có phải là ảnh không
        if (!file.type.startsWith('image/')) {
          this.$toast.error('Please select an image file!');
          return;
        }

        this.uploadingAvatar = true;
        this.avtPreview = URL.createObjectURL(file);

        try {
          const compressedFile = await this.compressImage(file);
          await this.uploadAvatar(compressedFile);
        } catch (error) {
          console.error('Image compression error:', error);
          this.$toast.error('Failed to process image!');
        } finally {
          this.uploadingAvatar = false;
        }
      }
    },

    // Hàm compress ảnh với độ nén cao
    compressImage(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = (event) => {
          const img = new Image();
          img.src = event.target.result;

          img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            // Giảm kích thước tối đa xuống 500x500 (cho avatar không cần quá lớn)
            const maxWidth = 500;
            const maxHeight = 500;
            let width = img.width;
            let height = img.height;

            // Tính toán tỷ lệ resize
            if (width > height) {
              if (width > maxWidth) {
                height *= maxWidth / width;
                width = maxWidth;
              }
            } else {
              if (height > maxHeight) {
                width *= maxHeight / height;
                height = maxHeight;
              }
            }

            canvas.width = width;
            canvas.height = height;

            // Enable image smoothing để ảnh mượt hơn khi resize
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';

            // Vẽ ảnh lên canvas với kích thước mới
            ctx.drawImage(img, 0, 0, width, height);

            // Convert canvas sang blob với chất lượng 0.65 (65%) - giảm mạnh hơn
            canvas.toBlob(
              (blob) => {
                if (blob) {
                  // Kiểm tra nếu ảnh vẫn còn quá lớn, compress thêm lần nữa
                  if (blob.size > 200 * 1024) { // Nếu > 200KB
                    // Compress thêm lần nữa với chất lượng thấp hơn
                    canvas.toBlob(
                      (secondBlob) => {
                        if (secondBlob) {
                          const compressedFile = new File([secondBlob], file.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                          });

                          this.logCompressionResult(file.size, compressedFile.size);
                          resolve(compressedFile);
                        } else {
                          reject(new Error('Second compression failed'));
                        }
                      },
                      'image/jpeg',
                      0.5 // Chất lượng 50% cho file lớn
                    );
                  } else {
                    // Tạo file mới từ blob
                    const compressedFile = new File([blob], file.name, {
                      type: 'image/jpeg',
                      lastModified: Date.now()
                    });

                    this.logCompressionResult(file.size, compressedFile.size);
                    resolve(compressedFile);
                  }
                } else {
                  reject(new Error('Canvas to blob failed'));
                }
              },
              'image/jpeg',
              0.65 // Chất lượng 65%
            );
          };

          img.onerror = () => {
            reject(new Error('Image load failed'));
          };
        };

        reader.onerror = () => {
          reject(new Error('File read failed'));
        };
      });
    },

    // Helper function để log kết quả compression
    logCompressionResult(originalSize, compressedSize) {
      const originalKB = (originalSize / 1024).toFixed(2);
      const compressedKB = (compressedSize / 1024).toFixed(2);
      const reducedPercent = (((originalSize - compressedSize) / originalSize) * 100).toFixed(2);

      console.log('%c📊 Image Compression Results:', 'color: #044a42; font-weight: bold; font-size: 14px');
      console.log(`%c   Original:    ${originalKB} KB`, 'color: #ff6b6b');
      console.log(`%c   Compressed:  ${compressedKB} KB`, 'color: #51cf66');
      console.log(`%c   Reduced by:  ${reducedPercent}%`, 'color: #339af0; font-weight: bold');
      console.log(`%c   Final size:  ${compressedKB} KB ${compressedSize < 100 * 1024 ? '✅' : compressedSize < 200 * 1024 ? '⚠️' : '❌'}`, 'color: #868e96');
    },

    // upload avatar dùng async/await
    async uploadAvatar(file) {
      const formData = new FormData();
      formData.append("avatarFile", file);

      try {
        const res = await axios.put("http://localhost:8081/api/user/profile/avatar", formData, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            // "Content-Type": "multipart/form-data",
          },
        });

        console.log("Avatar upload success:", res.data);

        // Cập nhật avatar mới vào thong_tin
        this.thong_tin.avt = res.data.avt || res.data;

        //lưu vào localStorage để giữ lại sau reload
        localStorage.setItem("userAvt", this.thong_tin.avt);
        localStorage.setItem("avatar_kh", this.thong_tin.avt);

        // Xóa preview vì đã có link thật
        this.avtPreview = "";

        // Emit event để thông báo cho các component khác (như MenuClient) cập nhật avatar
        window.dispatchEvent(new CustomEvent('avatar-updated', {
          detail: { avatar: this.thong_tin.avt }
        }));

        this.$toast.success("Avatar updated successfully!");
      } catch (err) {
        console.error("Upload avatar error:", err);
        this.$toast.error("Failed to upload avatar!");
        throw err;
      }
    },

    //  update thông tin
    updateProfile() {
      // Lưu giá trị username ban đầu để restore nếu validation fail
      const originalUsername = this.thong_tin.username;

      // Validate Full name không được để trống
      if (!this.thong_tin.username || !this.thong_tin.username.trim()) {
        this.$toast.error("Full name cannot be empty");
        // Restore lại giá trị ban đầu
        this.thong_tin.username = originalUsername;
        this.$nextTick(() => {
          document.getElementById('fullname')?.focus();
        });
        return;
      }

      // Validate Full name length: ít nhất 3 ký tự và nhỏ hơn 20 ký tự
      const trimmedUsername = this.thong_tin.username.trim();
      if (trimmedUsername.length < 3) {
        this.$toast.error("Full name must be at least 3 characters");
        // Restore lại giá trị ban đầu
        this.thong_tin.username = originalUsername;
        this.$nextTick(() => {
          document.getElementById('fullname')?.focus();
        });
        return;
      }
      if (trimmedUsername.length >= 20) {
        this.$toast.error("Full name must be less than 20 characters");
        // Restore lại giá trị ban đầu
        this.thong_tin.username = originalUsername;
        this.$nextTick(() => {
          document.getElementById('fullname')?.focus();
        });
        return;
      }
      // Cập nhật username đã được trim
      this.thong_tin.username = trimmedUsername;

      // Validate Date of Birth không được quá ngày hiện tại
      if (this.thong_tin.dateOfBirth && this.thong_tin.dateOfBirth > this.maxDate) {
        this.$toast.error("Date of Birth cannot be in the future");
        this.thong_tin.dateOfBirth = '';
        return;
      }

      // Validate Contact Number: phải là số và đúng 10 ký tự
      if (this.thong_tin.phonenumber) {
        const phoneRegex = /^[0-9]{10}$/;
        if (!phoneRegex.test(this.thong_tin.phonenumber)) {
          this.$toast.error("Contact Number must be exactly 10 digits");
          this.$nextTick(() => {
            document.getElementById('phonenumber')?.focus();
          });
          return;
        }
      }

      this.loading = true;
      this.error = null;


      axios
        .put("http://localhost:8081/api/user/profile", this.thong_tin, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          if (res.data.status) {
            this.loadUserData();
            this.$toast.success("Profile updated successfully!");
            console.log("Update response:", res.data.data);
          } else {
            this.$toast.error(res.data.message || "Update failed!");
          }

        })
        .catch((err) => {
          this.error = "Update failed!";
          this.$toast.error("Unable to update profile!");
          console.log("Update error:", err);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // tên ngân hàng
    fetchBankName() {
      axios
        .get("https://api.vietqr.io/v2/banks")
        .then((res) => {
          this.banks = res.data.data;
        })
        .catch((err) => {
          console.error("Failed to load banks:", err);
          this.$toast.error("Unable to load bank list!");
        });
    },

    handleKycFileChange(key, event) {
      if (this.isKycVerified) return;
      const file = event.target.files[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        this.$toast.error('Please choose an image file (JPG, PNG...)');
        return;
      }

      if (file.size > 5 * 1024 * 1024) {
        this.$toast.error('Each image must be under 5MB');
        return;
      }

      const preview = URL.createObjectURL(file);
      if (this.kycFiles[key].preview) {
        URL.revokeObjectURL(this.kycFiles[key].preview);
      }
      this.kycFiles[key] = { file, preview };
    },

    removeKycFile(key) {
      if (this.isKycVerified) return;
      if (this.kycFiles[key].preview) {
        URL.revokeObjectURL(this.kycFiles[key].preview);
      }
      this.kycFiles[key] = { file: null, preview: '' };
    },

    formatPhoneNumber(event) {
      // Chỉ cho phép nhập số và giới hạn 10 ký tự
      let value = event.target.value.replace(/[^0-9]/g, '');
      if (value.length > 10) {
        value = value.substring(0, 10);
      }
      // Cập nhật giá trị trực tiếp vào input để tránh conflict với v-model
      event.target.value = value;
      this.thong_tin.phonenumber = value;
    },

    submitKycVerification() {
      if (this.isKycVerified || !this.canSubmitKyc || this.isSubmittingKyc) return;
      this.isSubmittingKyc = true;

      const formData = new FormData();
      formData.append("cccdFront", this.kycFiles.cccdFront.file);
      formData.append("cccdBack", this.kycFiles.cccdBack.file);
      formData.append("selfie", this.kycFiles.selfie.file);

      axios
        .post("http://localhost:8081/api/user/kyc/verify", formData, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        })
        .then((res) => {
          this.$toast.success(res.data?.message || "KYC request submitted. Please wait for review.");

          // Update status từ API response
          this.kycStatus = res.data?.kycStatus ?? res.data?.status ?? 0;
          this.kycMessage = res.data?.note || res.data?.message || "Your documents are under review.";

          if (this.kycStatus === 0) {
            this.$toast.error(res.data?.message);
          }
          // Chỉ lưu role vào localStorage khi kycStatus === 1 (Verified)
          if (this.kycStatus === 1 && res.data?.role !== undefined && res.data?.role !== null) {
            this.userRole = res.data.role;
            localStorage.setItem("role_kh", res.data.role.toString());
          }


          // Reload user info để cập nhật toàn bộ
          this.loadUserData();
        })
        .catch((err) => {
          console.error("KYC error:", err);
          this.$toast.error("KYC submission failed. Please try again.");
        })
        .finally(() => {
          this.isSubmittingKyc = false;
        });
    }
  },


};
</script>

<style scoped>
.circle-bg {
  width: 30px;
  height: 30px;
  background: rgba(0, 123, 255, 0.1);
  box-shadow: 0 0 30px rgba(0, 123, 255, 0.2);
}

.button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: rgba(4, 74, 66, 0.05) !important;
}

.button:hover:not(:disabled) {
  background-color: rgba(4, 74, 66, 0.1) !important;
  transform: translateY(-1px);
}

.kyc-upload {
  border: 1px dashed rgba(4, 74, 66, 0.3);
  border-radius: 12px;
  padding: 0.75rem;
  background: rgba(4, 74, 66, 0.02);
  transition: border-color 0.2s ease;
}

.kyc-upload:hover {
  border-color: rgba(4, 74, 66, 0.6);
}

.preview-wrapper img {
  margin: 10px 20px 0 0;
  border-radius: 10px;
  border: 1px solid rgba(4, 74, 66, 0.1);
  max-height: 200px;
  object-fit: contain;
}

.preview-wrapper button {
  font-size: 0.85rem;
}

.kyc-upload.disabled-upload {
  opacity: 0.6;
  pointer-events: none;
}
</style>
