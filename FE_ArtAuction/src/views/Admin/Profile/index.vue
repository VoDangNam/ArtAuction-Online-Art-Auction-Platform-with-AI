<template>
  <div class="container-fluid py-4 bg-light min-vh-100 animate-fade-in">
    <div
      v-if="isLoading"
      class="d-flex justify-content-center align-items-center"
      style="height: 50vh"
    >
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h4 class="fw-bold text-primary mb-1">My Profile</h4>
          <p class="text-muted mb-0">Manage your account settings and preferences</p>
        </div>
        <button
          class="btn btn-primary rounded-pill px-4 shadow-sm"
          @click="toggleEditMode"
          v-if="!isEditing"
        >
          <i class="bi bi-pencil-square me-2"></i>Edit Profile
        </button>
      </div>

      <div class="row g-4">
        <div class="col-lg-4 col-xl-3">
          <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
            <div
              class="bg-primary h-100px"
              style="height: 100px; background: linear-gradient(45deg, #0d6efd, #0dcaf0)"
            ></div>

            <div class="card-body text-center px-4 pb-4" style="margin-top: -60px">
              <div class="position-relative d-inline-block mb-3">
                <img
                  :src="admin.avatar"
                  class="rounded-circle border border-4 border-white shadow-sm bg-white"
                  alt="Admin Avatar"
                  width="120"
                  height="120"
                  style="object-fit: cover"
                />
                <button
                  v-if="isEditing"
                  class="btn btn-sm btn-secondary rounded-circle position-absolute bottom-0 end-0 border border-2 border-white"
                  title="Change Avatar"
                  @click="triggerFileInput"
                >
                  <i class="bi bi-camera-fill"></i>
                </button>
                <input type="file" ref="fileInput" class="d-none" @change="handleFileUpload" />
              </div>

              <h4 class="fw-bold mb-1">{{ admin.fullName }}</h4>
              <span class="badge bg-secondary-subtle text-primary rounded-pill px-3 py-2 mb-3">
                {{ mapRole(admin.role) }}
              </span>

              <div class="d-flex justify-content-center gap-2 mt-2">
                <button
                  class="btn btn-outline-danger btn-sm px-4 rounded-pill w-100"
                  @click="performLogout"
                >
                  <i class="bi bi-box-arrow-right me-1"></i> Logout
                </button>
              </div>
            </div>

            <div class="card-footer bg-white border-top p-4">
              <ul class="list-group list-group-flush small">
                <li class="list-group-item px-0 border-0 d-flex justify-content-between">
                  <span class="text-muted"><i class="bi bi-envelope me-2"></i>Email:</span>
                  <span class="fw-medium text-dark text-truncate" style="max-width: 150px">{{
                    admin.email
                  }}</span>
                </li>
                <li class="list-group-item px-0 border-0 d-flex justify-content-between">
                  <span class="text-muted"><i class="bi bi-phone me-2"></i>Phone:</span>
                  <span class="fw-medium text-dark">{{ admin.phoneNumber }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body">
              <h6 class="fw-bold text-uppercase text-muted small mb-3">Performance</h6>
              <div class="row text-center">
                <div class="col-6 border-end">
                  <h5 class="fw-bold text-primary mb-0">1,250</h5>
                  <small class="text-muted" style="font-size: 0.75rem">Users</small>
                </div>
                <div class="col-6">
                  <h5 class="fw-bold text-warning mb-0">340</h5>
                  <small class="text-muted" style="font-size: 0.75rem">Auctions</small>
                </div>
              </div>
            </div>
          </div> -->
        </div>

        <div class="col-lg-8 col-xl-9">
          <div class="card border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4">
              <h5 class="fw-bold text-primary mb-0">Profile Details</h5>
            </div>

            <div class="card-body p-4">
              <form @submit.prevent="saveChanges">
                <div class="row g-4">
                  <div class="col-md-6">
                    <label class="form-label fw-medium text-secondary small text-uppercase"
                      >Full Name</label
                    >
                    <p v-if="!isEditing" class="fs-6 fw-bold text-dark border-bottom pb-2 mb-0">
                      {{ admin.fullName }}
                    </p>
                    <input
                      v-else
                      type="text"
                      class="form-control bg-light"
                      v-model="form.fullName"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label fw-medium text-secondary small text-uppercase"
                      >Email Address</label
                    >
                    <p v-if="!isEditing" class="fs-6 fw-bold text-dark border-bottom pb-2 mb-0">
                      {{ admin.email }}
                    </p>
                    <input
                      v-else
                      type="email"
                      class="form-control bg-light"
                      :class="{ 'is-invalid': errors.email }"
                      v-model="form.email"
                    />
                    <div class="invalid-feedback d-block" v-if="errors.email">
                      {{ errors.email }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label fw-medium text-secondary small text-uppercase"
                      >Phone Number</label
                    >
                    <p v-if="!isEditing" class="fs-6 fw-bold text-dark border-bottom pb-2 mb-0">
                      {{ admin.phoneNumber }}
                    </p>
                    <input
                      v-else
                      type="tel"
                      class="form-control bg-light"
                      :class="{ 'is-invalid': errors.phoneNumber }"
                      v-model="form.phoneNumber"
                    />
                    <div class="invalid-feedback d-block" v-if="errors.phoneNumber">
                      {{ errors.phoneNumber }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label fw-medium text-secondary small text-uppercase"
                      >Join Date</label
                    >
                    <p class="fs-6 fw-bold text-dark border-bottom pb-2 mb-0">
                      {{ formatDate(admin.createdAt) }}
                    </p>
                  </div>

                  <div class="col-12">
                    <label class="form-label fw-medium text-secondary small text-uppercase"
                      >Address</label
                    >
                    <p v-if="!isEditing" class="fs-6 text-muted border-bottom pb-2 mb-0 fst-italic">
                      {{ admin.address || "No information provided." }}
                    </p>
                    <textarea
                      v-else
                      class="form-control bg-light"
                      rows="3"
                      v-model="form.address"
                      placeholder="Enter your address..."
                    ></textarea>
                  </div>
                </div>

                <div v-if="isEditing" class="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
                  <button type="button" class="btn btn-light rounded-pill px-4" @click="cancelEdit">
                    Cancel
                  </button>
                  <button
                    type="submit"
                    class="btn btn-primary rounded-pill px-4"
                    :disabled="isSaving"
                  >
                    <span
                      v-if="isSaving"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    Save Changes
                  </button>
                </div>
              </form>
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
  name: "AdminProfile",
  data() {
    return {
      isEditing: false,
      isLoading: false,
      isSaving: false,

      admins: {},

      // Dữ liệu Admin hiển thị
      admin: {
        id: "",
        fullName: "",
        email: "",
        phoneNumber: "",
        address: "",
        avatar: "",
        role: 3,
        createdAt: "",
        updatedAt: "",
        status: 1,
      },

      // Dữ liệu Form (dùng khi chỉnh sửa)
      form: {},
      errors: {
        email: "",
        phoneNumber: "",
      },
    };
  },
  mounted() {
    this.fetchAdminProfile();
  },
  methods: {
    fetchAdminProfile() {
      this.isLoading = true;
      const token = localStorage.getItem("token");

      if (!token) {
        // alert("Bạn chưa đăng nhập!");
        this.$router.push("/admin/login");
        return;
      }

      // Gọi API check token
      axios
        .get("http://localhost:8081/api/admin/auth/profile", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          if (res.data && res.data.data) {
            this.admin = res.data.data;
          }
        })
        .catch((err) => {
          console.error("Lỗi lấy thông tin Admin:", err);
          // Nếu token hết hạn hoặc lỗi 401
          if (err.response && err.response.status === 401) {
            this.$router.push("/admin/login");
          }
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    toggleEditMode() {
      // Clone dữ liệu sang form để chỉnh sửa không ảnh hưởng trực tiếp giao diện
      this.form = { ...this.admin };
      this.isEditing = true;
    },

    cancelEdit() {
      this.isEditing = false;
      this.form = {}; // Reset form
    },

    saveChanges() {
      if (!this.validateData()) {
        return;
      }
      this.isSaving = true;
      const token = localStorage.getItem("token");

      // 1. CHỈ GỬI NHỮNG GÌ CHO PHÉP SỬA
      // Bỏ 'role', 'status', 'email' nếu backend không cho sửa hoặc backend tự lấy từ token
      const updatePayload = {
        fullName: this.form.fullName,
        phoneNumber: this.form.phoneNumber,
        address: this.form.address,
        avatar: this.form.avatar,
        email: this.form.email,
      };

      axios
        .put(`http://localhost:8081/api/admin/admins/cap-nhat/${this.admin.id}`, updatePayload, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          // ... (Giữ nguyên logic xử lý thành công)
          // Cập nhật lại UI chuẩn xác
          this.admin = { ...this.admin, ...updatePayload };
          this.isEditing = false;
          alert("Update successful!");
        })
        .catch((error) => {
          console.error("Lỗi cập nhật:", error);
          // Log chi tiết lỗi 400 từ backend để debug
          if (error.response && error.response.data) {
            console.log("Chi tiết lỗi từ Server:", error.response.data);
            alert("Lỗi: " + (error.response.data.message || "Dữ liệu không hợp lệ"));
          }
        })
        .finally(() => {
          this.isSaving = false;
        });
    },
    // --- 3. UPLOAD ẢNH ---
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Upload ảnh ngay khi chọn file
      const formData = new FormData();
      formData.append("imageFile", file); // Key này phải khớp với Backend quy định (imageFile/file/avatar...)

      const token = localStorage.getItem("token");

      axios
        .post("http://localhost:8081/api/admin/uploads/upload-image", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          const newAvatarUrl =
            response.data.data && response.data.data.imageUrl
              ? response.data.data.imageUrl
              : response.data;
          if (newAvatarUrl) {
            // Cập nhật vào form để chuẩn bị Save
            this.form.avatar = newAvatarUrl;
            // Cập nhật tạm thời vào admin để hiện preview
            this.admin.avatar = newAvatarUrl;
          }
        })
        .catch((error) => {
          console.error("Lỗi upload ảnh:", error);
          alert("Không thể tải ảnh lên.");
        });
    },

    // --- HELPER FUNCTIONS ---
    mapRole(roleId) {
      switch (roleId) {
        case 4:
          return "Super Admin";
        case 3:
          return "Admin";
        default:
          return "User";
      }
    },

    // [THÊM] Hàm kiểm tra định dạng
    validateData() {
      this.errors = { email: "", phoneNumber: "" }; // Reset lỗi cũ
      let isValid = true;

      // 1. Kiểm tra định dạng Email
      // Regex này yêu cầu: chữ + @ + chữ + . + chữ
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.form.email || !emailRegex.test(this.form.email)) {
        this.errors.email =
          "The email address is not in the correct format (e.g., abc@domain.com).";
        isValid = false;
      }

      // 2. Kiểm tra số lượng SĐT (Bắt buộc 10 số)

      const phoneRegex = /^\d{10}$/;
      if (!this.form.phoneNumber || !phoneRegex.test(this.form.phoneNumber)) {
        this.errors.phoneNumber = "The phone number must consist of exactly 10 digits.";
        isValid = false;
      }

      return isValid;
    },

    // [THÊM] Hàm xóa lỗi khi người dùng nhập lại (cho đẹp giao diện)
    clearError(field) {
      this.errors[field] = "";
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const options = { year: "numeric", month: "short", day: "numeric" };
      return new Date(dateString).toLocaleDateString("en-US", options);
    },
    performLogout() {
      const token = localStorage.getItem("token");
      const finish = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("name_admin");
        localStorage.removeItem("email_admin");
        localStorage.removeItem("check_admin");
        this.user = null;
        this.$router.push("/admin/login");
        this.$toast.success("Log out successfully");
      };

      if (!token) {
        finish();
        return;
      }

      axios
        .post(
          "http://localhost:8081/api/auth/logout",
          {},
          { headers: { Authorization: "Bearer " + token } }
        )
        .then(() => {
          finish();
        })
        .catch(() => {
          finish();
        });
    },
  },
};
</script>

<style scoped>
.form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}
</style>
