<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <div class="d-flex align-items-center gap-2 mb-1">
          <router-link
            to="/admin/management-users"
            class="btn btn-light btn-sm rounded-circle shadow-sm"
          >
            <i class="fa-solid fa-arrow-left text-secondary"></i>
          </router-link>
          <h4 class="fw-bold text-primary mb-0">Create New User</h4>
        </div>
        <p class="text-body-secondary mb-0 ms-5">Onboard a new user or seller to the platform</p>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-light text-secondary fw-bold shadow-sm px-4" @click="resetForm">
          Reset
        </button>
        <button
          class="btn btn-primary fw-bold shadow-sm px-4"
          @click="submitForm"
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
          <span v-else><i class="fa-solid fa-check me-2"></i> Create User</span>
        </button>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-lg-4 col-xl-3">
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-body text-center p-4">
            <h6 class="fw-bold text-secondary mb-3">Profile Picture</h6>

            <div
              class="position-relative d-inline-block mb-3"
              @click="$refs.fileInput.click()"
              style="cursor: pointer"
            >
              <div
                class="rounded-circle border border-3 border-light shadow-sm overflow-hidden d-flex align-items-center justify-content-center bg-light"
                style="width: 150px; height: 150px; margin: 0 auto"
              >
                <img
                  v-if="previewImage"
                  :src="previewImage"
                  class="w-100 h-100 object-fit-cover"
                  alt="Avatar Preview"
                />
                <div v-else class="text-secondary text-center">
                  <i class="fa-regular fa-image fs-1 mb-2"></i>
                  <p class="small mb-0 fw-medium">Upload</p>
                </div>
              </div>

              <div
                class="position-absolute bottom-0 end-0 bg-white rounded-circle shadow-sm p-2 border"
                style="transform: translate(10%, 10%)"
              >
                <i class="fa-solid fa-camera text-primary"></i>
              </div>
            </div>

            <p class="text-muted x-small mb-3">
              Allowed *.jpeg, *.jpg, *.png <br />
              max size of 3 MB
            </p>

            <input
              type="file"
              ref="fileInput"
              class="d-none"
              accept="image/*"
              @change="handleFileUpload"
            />
          </div>
        </div>

        <!-- <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-4">
            <h6 class="fw-bold text-secondary mb-3">Account Status</h6>
            <div
              class="form-check form-switch d-flex align-items-center justify-content-between ps-0"
            >
              <label class="form-check-label fw-medium" for="statusSwitch">
                {{ form.status === 1 ? "Active" : "Locked" }}
              </label>
              <input
                class="form-check-input ms-auto"
                type="checkbox"
                role="switch"
                id="statusSwitch"
                style="width: 3em; height: 1.5em"
                v-model="statusBoolean"
              />
            </div>
            <p class="text-muted x-small mt-2 mb-0">
              If locked, this user cannot login or bid/sell items.
            </p>
          </div>
        </div> -->
      </div>

      <div class="col-12 col-lg-8 col-xl-9">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body p-4 p-md-5">
            <div class="mb-5">
              <div class="d-flex align-items-center mb-4">
                <div
                  class="bg-secondary bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center me-3"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-solid fa-shield-halved"></i>
                </div>
                <h5 class="fw-bold mb-0">Login Credentials</h5>
              </div>

              <div class="row g-3">
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control bg-light border-0"
                      id="usernameInput"
                      placeholder="username"
                      v-model="form.username"
                    />
                    <label for="usernameInput">Username <span class="text-danger">*</span></label>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      type="email"
                      class="form-control bg-light border-0"
                      id="emailInput"
                      placeholder="name@example.com"
                      v-model="form.email"
                    />
                    <label for="emailInput">Email Address <span class="text-danger">*</span></label>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      type="password"
                      class="form-control bg-light border-0"
                      id="passInput"
                      placeholder="Password"
                      v-model="form.password"
                    />
                    <label for="passInput">Password <span class="text-danger">*</span></label>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      v-model="form.confirmPassword"
                      type="password"
                      class="form-control bg-light border-0"
                      id="confirmPassInput"
                      placeholder="Confirm Password"
                    />
                    <label for="confirmPassInput"
                      >Confirm Password <span class="text-danger">*</span></label
                    >
                  </div>
                </div>
              </div>
            </div>

            <hr class="border-secondary opacity-10 my-4" />

            <div class="mb-5">
              <div class="d-flex align-items-center mb-4">
                <div
                  class="bg-success bg-opacity-10 text-success rounded-circle d-flex align-items-center justify-content-center me-3"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-regular fa-id-card"></i>
                </div>
                <h5 class="fw-bold mb-0">Personal Information</h5>
              </div>

              <div class="row g-3">
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control bg-light border-0"
                      id="nameInput"
                      placeholder="John Doe"
                      v-model="form.fullName"
                    />
                    <label for="nameInput">Full Name</label>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <!-- <div class="form-floating">
                    <input
                      type="text"
                      class="form-control bg-light border-0"
                      id="cccdInput"
                      placeholder="0123..."
                      v-model="form.cccd"
                    />
                    <label for="cccdInput">CCCD / ID Card <span class="text-danger">*</span></label>
                  </div> -->
                  <div class="form-floating">
                    <input
                      type="tel"
                      class="form-control bg-light border-0"
                      id="phoneInput"
                      placeholder="0909..."
                      v-model="form.phoneNumber"
                    />
                    <label for="phoneInput">Phone Number</label>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <input
                      type="date"
                      class="form-control bg-light border-0"
                      id="dobInput"
                      placeholder="0909..."
                      v-model="form.dateOfBirth"
                    />
                    <label for="phoneInput">Date of Birth</label>
                  </div>
                </div>

                <div class="col-12 col-md-6">
                  <div class="form-floating">
                    <select
                      class="form-select bg-light border-0"
                      id="genderSelect"
                      v-model="form.gender"
                    >
                      <option :value="0">Male</option>
                      <option :value="1">Female</option>
                      <option :value="2">Other</option>
                    </select>
                    <label for="genderSelect">Gender</label>
                  </div>
                </div>
                <div class="col-12 col-md-6"></div>

                <div class="col-12">
                  <div class="form-floating">
                    <textarea
                      class="form-control bg-light border-0"
                      placeholder="Address"
                      id="addrInput"
                      style="height: 100px"
                      v-model="form.address"
                    ></textarea>
                    <label for="addrInput">Address</label>
                  </div>
                </div>

                <div class="col-12 mt-4">
                  <label class="form-label fw-bold text-secondary small text-uppercase mb-2"
                    >User Type</label
                  >
                  <div class="row g-3">
                    <div class="col-6 col-md-4" v-for="role in roles" :key="role.value">
                      <input
                        type="radio"
                        class="btn-check"
                        name="roleOptions"
                        :id="'role' + role.value"
                        :value="role.value"
                        v-model="form.role"
                      />
                      <label
                        class="btn btn-outline-light text-dark border w-100 d-flex flex-column align-items-center justify-content-center py-3 gap-2 h-100"
                        :for="'role' + role.value"
                        :class="{
                          'border-secondary bg-secondary-subtle text-primary fw-bold':
                            form.role === role.value,
                        }"
                      >
                        <i :class="role.icon + ' fs-4'"></i>
                        <span>{{ role.label }}</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="d-md-none mt-4">
              <button class="btn btn-primary w-100 fw-bold py-3 shadow-sm" @click="submitForm">
                Create User
              </button>
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
  name: "AddUser",
  data() {
    return {
      previewImage: null,
      selectedFile: null,
      isSubmitting: false,

      form: {
        username: "",
        fullName: "",
        email: "",
        password: "",
        confirmPassword: "",
        phoneNumber: "",
        // cccd: "",
        address: "",
        dateOfBirth: "",
        gender: 0, // 0: Male, 1: Female, 2: Other
        role: 0, // 0: User, 1: Buyer, 2: Seller
        status: 1, // 1: Active, 0: Locked
        avatar: "",
      },

      roles: [
        { label: "Standard User", value: 0, icon: "fa-regular fa-user" },
        { label: "Verified Buyer", value: 1, icon: "fa-solid fa-cart-shopping text-success" },
        { label: "Seller", value: 2, icon: "fa-solid fa-store text-warning" },
      ],
    };
  },

  computed: {
    statusBoolean: {
      get() {
        return this.form.status === 1;
      },
      set(val) {
        this.form.status = val ? 1 : 0;
      },
    },
  },

  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.previewImage = URL.createObjectURL(file);
      }
    },

    resetForm() {
      this.previewImage = null;
      this.selectedFile = null;
      this.form = {
        username: "",
        fullName: "",
        email: "",
        password: "",
        confirmPassword: "",
        phoneNumber: "",
        // cccd: "",
        address: "",
        dateOfBirth: "",
        gender: 0,
        role: 0,
        status: 1,
        avatar: "",
      };
    },

    submitForm() {
      // 1. Validate cơ bản
      if (!this.form.username || !this.form.email || !this.form.password) {
        alert("Please fill in required fields (*)");
        return;
      }
      if (this.form.password !== this.form.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      this.isSubmitting = true;

      // 2. Tạo Promise xử lý upload ảnh trước
      let uploadPromise;

      if (this.selectedFile) {
        const formData = new FormData();
        formData.append("imageFile", this.selectedFile);

        // Gọi API upload
        uploadPromise = axios
          .post("http://localhost:8081/api/admin/uploads/upload-image", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          })
          .then((res) => {
            return res.data.data.imageUrl;
          });
      } else {
        // Nếu không có ảnh, trả về Promise resolve rỗng
        uploadPromise = Promise.resolve("");
      }

      // 3. Chuỗi xử lý chính (Chain)
      uploadPromise
        .then((avatarUrl) => {
          console.log("Uploaded Image URL:", avatarUrl);

          // Chuẩn bị dữ liệu để tạo User
          const payload = {
            username: this.form.username,
            password: this.form.password,
            email: this.form.email,
            phoneNumber: this.form.phoneNumber,
            address: this.form.address,
            dateOfBirth: this.form.dateOfBirth,
            gender: this.form.gender,
            role: this.form.role,
            status: this.form.status,
            fullname: this.form.fullName,
            avt: avatarUrl,
          };

          console.log("Payload sending:", payload);

          return axios.post("http://localhost:8081/api/admin/them-user", payload, {
            headers: { Authorization: "Bearer " + localStorage.getItem("token") },
          });
        })
        .then(() => {
          alert("User created successfully!");
          this.$router.push("/admin/management-users");
        })
        .catch((err) => {
          console.error("Error process:", err);
          const msg = err.response?.data?.message || "Failed to create user. Please try again.";
          alert(msg);
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
  },
};
</script>

<style scoped></style>
