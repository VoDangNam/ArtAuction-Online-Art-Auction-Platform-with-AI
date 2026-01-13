<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-1">Admin Management</h4>
      <p class="text-body-secondary mb-0">Manage administrator accounts and permissions</p>
    </div>
    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-sm-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">General Admin</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalAdmins }}</h3>
              </div>
              <div
                class="bg-secondary bg-opacity-10 text-primary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-user-shield fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total admins</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">In Operation</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.activeAdmins }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Active now</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Locked Admins</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.lockedAdmins }}</h3>
              </div>
              <div
                class="bg-secondary bg-opacity-10 text-secondary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-ban fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Access restricted</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-body-secondary fw-bold mb-1">Super Admin</h6>
                <h3 class="fw-bold mb-0">{{ statistics.totalSuperAdmins }}</h3>
              </div>
              <div
                class="bg-secondary-subtle bg-opacity-25 rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-crown fs-5"></i>
              </div>
            </div>
            <small class="text-secondary text-opacity-75 fw-medium">Highest privilege</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <div class="row g-3 mb-4">
          <div class="col-12 col-md-6 col-lg-4">
            <div class="input-group bg-light rounded-pill px-2 border-0">
              <span class="input-group-text bg-transparent border-0 text-secondary">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control bg-transparent border-0 shadow-none"
                @input="handleSearch"
                placeholder="Searching for admin..."
              />
            </div>
          </div>
          <div
            class="col-12 col-md-6 col-lg-8 text-md-end d-flex justify-content-md-end justify-content-start align-items-center gap-2"
          >
            <button
              class="btn btn-outline-primary shadow-sm"
              type="button"
              data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasFilter"
            >
              <i class="fa-solid fa-filter me-1"></i> Filter
            </button>

            <Teleport to="body">
              <div
                class="offcanvas offcanvas-end border-0 shadow-lg"
                tabindex="-1"
                id="offcanvasFilter"
                aria-labelledby="offcanvasFilterLabel"
                style="width: 400px"
              >
                <div class="offcanvas-header border-bottom bg-light-subtle">
                  <div class="d-flex align-items-center gap-2">
                    <div
                      class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
                      style="width: 32px; height: 32px"
                    >
                      <i class="fa-solid fa-sliders"></i>
                    </div>
                    <h5 class="offcanvas-title fw-bold text-primary" id="offcanvasFilterLabel">
                      Employee filter
                    </h5>
                  </div>
                  <button
                    type="button"
                    class="btn-close shadow-none"
                    data-bs-dismiss="offcanvas"
                    aria-label="Close"
                  ></button>
                </div>

                <div class="offcanvas-body p-0">
                  <div class="p-4 custom-scrollbar">
                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-solid fa-user-tag me-1"></i> Roles and Powers
                      </label>
                      <small class="text-muted d-block mb-2 fst-italic" style="font-size: 0.75rem"
                        >Multiple positions can be selected</small
                      >

                      <div class="row g-2">
                        <div class="col-6">
                          <input
                            type="checkbox"
                            class="btn-check"
                            id="roleSuperAdmin"
                            autocomplete="off"
                            v-model="filter.roles"
                            :value="4"
                          />
                          <label
                            class="btn btn-outline-danger btn-sm w-100 text-start"
                            for="roleSuperAdmin"
                          >
                            <i class="fa-solid fa-crown me-1"></i> Super Admin
                          </label>
                        </div>
                        <div class="col-6">
                          <input
                            type="checkbox"
                            class="btn-check"
                            id="roleAdmin"
                            autocomplete="off"
                            v-model="filter.roles"
                            :value="3"
                          />
                          <label
                            class="btn btn-outline-primary btn-sm w-100 text-start"
                            for="roleAdmin"
                          >
                            <i class="fa-solid fa-user-shield me-1"></i> Admin
                          </label>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        Operating status
                      </label>
                      <div class="bg-light rounded-3 p-3 border">
                        <div class="form-check mb-2">
                          <input
                            class="form-check-input"
                            type="radio"
                            name="empStatus"
                            id="stAll"
                            :value="null"
                            v-model="filter.status"
                          />
                          <label class="form-check-label fw-medium" for="stAll"> All </label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            class="form-check-input"
                            type="radio"
                            name="empStatus"
                            id="stActive"
                            :value="1"
                            v-model="filter.status"
                          />
                          <label class="form-check-label text-success fw-medium" for="stActive">
                            <i class="fa-solid fa-circle-check me-1"></i> Active
                          </label>
                        </div>

                        <div class="form-check">
                          <input
                            class="form-check-input"
                            type="radio"
                            name="empStatus"
                            id="stSuspended"
                            :value="0"
                            v-model="filter.status"
                          />
                          <label class="form-check-label text-danger" for="stSuspended">
                            <i class="fa-solid fa-ban me-1"></i> Inactive
                          </label>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-regular fa-calendar-days me-1"></i> Time of joining
                      </label>

                      <div class="input-group input-group-sm mb-3">
                        <span class="input-group-text bg-light text-secondary">From</span>
                        <input
                          type="date"
                          class="form-control shadow-none"
                          v-model="filter.createdAtFrom"
                        />
                        <span class="input-group-text bg-light text-secondary">To</span>
                        <input
                          type="date"
                          class="form-control shadow-none"
                          v-model="filter.createdAtTo"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div class="offcanvas-footer border-top p-3 bg-white">
                  <div class="row g-2">
                    <div class="col-4">
                      <button
                        class="btn btn-light border w-100 fw-bold text-secondary"
                        @click="resetFilter"
                      >
                        <i class="fa-solid fa-rotate-right me-1"></i> Reset
                      </button>
                    </div>
                    <div class="col-8">
                      <button
                        class="btn btn-primary w-100 fw-bold shadow-sm"
                        data-bs-dismiss="offcanvas"
                        @click="handleFilter"
                      >
                        Apply
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </Teleport>

            <router-link to="/admin/add-admin" class="btn btn-primary">
              <i class="fa-solid fa-plus me-2"></i>Add New Admin
            </router-link>
          </div>
        </div>

        <div class="table-responsive overflow-y-auto custom-scrollbar" style="max-height: 500px">
          <table class="table table-hover align-middle text-nowrap mb-0">
            <thead class="bg-light sticky-top shadow-sm border-bottom border-light-subtle">
              <tr>
                <th scope="col" class="ps-4 py-3 fw-bold text-dark text-uppercase x-small border-0">
                  ID
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Full Name
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Email
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Phone
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Role
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Status
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Created At
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold text-dark text-uppercase x-small border-0 text-center"
                >
                  Action
                </th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="isLoading">
                <td colspan="8" class="text-center py-5 text-muted border-0">
                  <div
                    class="spinner-border spinner-border-sm text-primary mb-2"
                    role="status"
                  ></div>
                  <p class="mb-0 small">Loading data...</p>
                </td>
              </tr>

              <tr
                v-for="employee in sortedEmployees"
                :key="employee.id"
                class="transition-bg border-bottom border-light-subtle"
              >
                <td class="ps-4 py-3 border-0">
                  <span class="badge bg-light text-secondary border border-light-subtle"
                    >#{{ employee.id }}</span
                  >
                </td>

                <td class="py-3 border-0">
                  <div class="d-flex align-items-center gap-3">
                    <div class="position-relative">
                      <img
                        :src="employee.avatar"
                        class="rounded-circle border border-2 border-white shadow-sm object-fit-cover"
                        style="width: 40px; height: 40px"
                      />
                    </div>
                    <span class="fw-bold text-dark" style="font-size: 0.95rem">{{
                      employee.fullName
                    }}</span>
                  </div>
                </td>

                <td class="py-3 border-0 text-muted">{{ employee.email }}</td>

                <td class="py-3 border-0 text-dark">{{ employee.phoneNumber }}</td>

                <td class="py-3 border-0">
                  <span
                    class="badge bg-secondary-subtle rounded-pill fw-medium px-3 py-2"
                    :class="getRoleClass(employee.role)"
                  >
                    {{ convertRole(employee.role) }}
                  </span>
                </td>

                <td class="py-3 border-0">
                  <span
                    class="badge rounded-pill border fw-medium px-3 py-2"
                    :class="
                      employee.status === 1
                        ? 'bg-success-subtle text-success border-success-subtle'
                        : 'bg-secondary-subtle text-secondary border-secondary-subtle'
                    "
                  >
                    <i
                      class="fa-solid fa-circle fa-2xs me-1"
                      :class="employee.status === 1 ? 'text-success' : 'text-secondary'"
                    ></i>
                    {{ convertStatus(employee.status) }}
                  </span>
                </td>

                <td class="py-3 border-0 small text-secondary">
                  {{ formatDate(employee.createdAt) }}
                </td>

                <td class="text-center py-3 border-0">
                  <div class="dropdown">
                    <button
                      class="btn btn-sm btn-light btn-action rounded-circle border-0"
                      type="button"
                      data-bs-toggle="dropdown"
                      style="width: 32px; height: 32px"
                    >
                      <i class="fa-solid fa-ellipsis-vertical text-secondary"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3 mt-2">
                      <!-- <li>
                        <RouterLink class="dropdown-item py-2" to="/details">
                          <i class="fa-regular fa-eye me-2 text-primary"></i>See details
                        </RouterLink>
                      </li> -->
                      <li>
                        <button class="dropdown-item py-2" @click="openEditModal(employee)">
                          <i class="fa-regular fa-pen-to-square me-2"></i>Edit
                        </button>
                      </li>
                      <li><hr class="dropdown-divider my-1" /></li>
                      <li>
                        <button
                          class="dropdown-item py-2 text-danger"
                          @click="handleDelete(employee.id, employee.fullName)"
                        >
                          <i class="fa-regular fa-trash-can me-2"></i>Delete
                        </button>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div
      class="modal fade"
      id="editAdminModal"
      tabindex="-1"
      aria-hidden="true"
      data-bs-backdrop="static"
      ref="editAdminModal"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <div class="modal-header bg-secondary-subtle px-4 py-3 border-0">
            <div class="d-flex align-items-center gap-2">
              <div
                class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm"
                style="width: 40px; height: 40px"
              >
                <i class="fa-solid fa-user-pen"></i>
              </div>
              <div>
                <h5 class="modal-title fw-bold text-primary mb-0">Update Admin Profile</h5>
                <small class="text-body-secondary">ID: #{{ editingAdmin.id }}</small>
              </div>
            </div>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body p-0">
            <div class="row g-0 h-100">
              <div class="col-12 col-lg-4 bg-light-subtle border-end border-light-subtle">
                <div
                  class="d-flex flex-column align-items-center text-center p-4 h-100 justify-content-center"
                >
                  <div class="position-relative mb-3">
                    <img
                      :src="previewAvt || editingAdmin.avatar || 'https://via.placeholder.com/150'"
                      class="rounded-circle shadow-sm border border-4 border-white object-fit-cover"
                      style="width: 150px; height: 150px"
                      alt="Avatar"
                    />
                    <label
                      for="uploadAvtInput"
                      class="position-absolute bottom-0 end-0 bg-white text-primary border border-2 border-white rounded-circle shadow-sm d-flex align-items-center justify-content-center p-2 mb-1 me-1"
                      style="width: 38px; height: 38px; cursor: pointer"
                    >
                      <i class="fa-solid fa-camera"></i>
                    </label>
                    <input
                      type="file"
                      id="uploadAvtInput"
                      class="d-none"
                      @change="handleFileUpload"
                      accept="image/*"
                    />
                  </div>

                  <h5 class="fw-bold text-dark mb-1">{{ editingAdmin.fullName }}</h5>
                  <p class="text-secondary small mb-3">{{ editingAdmin.email }}</p>
                </div>
              </div>

              <div class="col-12 col-lg-8 bg-white">
                <div class="p-4">
                  <form @submit.prevent="handleUpdateProcess">
                    <p class="text-uppercase fw-bold text-secondary small mb-3 border-bottom pb-2">
                      <i class="fa-regular fa-id-card me-1"></i> Personal Info
                    </p>

                    <div class="row g-3 mb-4">
                      <div class="col-12">
                        <div class="form-floating">
                          <input
                            type="text"
                            class="form-control bg-light-subtle"
                            id="floatName"
                            v-model="editingAdmin.fullName"
                            placeholder="Full Name"
                            required
                          />
                          <label for="floatName">Full Name</label>
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="form-floating">
                          <input
                            type="text"
                            class="form-control bg-light-subtle"
                            id="floatPhone"
                            v-model="editingAdmin.phoneNumber"
                            placeholder="Phone"
                          />
                          <label for="floatPhone">Phone Number</label>
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="form-floating">
                          <input
                            type="email"
                            class="form-control bg-light"
                            id="floatEmail"
                            v-model="editingAdmin.email"
                            disabled
                            readonly
                          />
                          <label for="floatEmail">Email</label>
                        </div>
                      </div>
                    </div>

                    <p class="text-uppercase fw-bold text-secondary small mb-3 border-bottom pb-2">
                      <i class="fa-solid fa-layer-group me-1"></i> Permissions
                    </p>

                    <div class="row g-3">
                      <div class="col-md-6">
                        <label class="form-label small fw-bold text-secondary">Role</label>
                        <select class="form-select bg-light-subtle" v-model="editingAdmin.role">
                          <option :value="1">Admin</option>
                          <option :value="4">Super Admin</option>
                        </select>
                      </div>
                      <!-- <div class="col-md-6">
                        <label class="form-label small fw-bold text-secondary">Status</label>
                        <select class="form-select bg-light-subtle" v-model="editingAdmin.status">
                          <option :value="1" class="text-success">Active</option>
                          <option :value="0" class="text-secondary">Inactive</option>
                        </select>
                      </div> -->
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer bg-white border-top px-4 py-3">
            <button
              type="button"
              class="btn btn-light rounded-pill px-4 fw-medium text-secondary border"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-primary rounded-pill px-4 fw-bold shadow-sm"
              @click="handleUpdateProcess"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
              <span v-else><i class="fa-regular fa-floppy-disk me-2"></i>Save Changes</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import * as bootstrap from 'bootstrap'; // Bật dòng này nếu dùng Vite/Webpack

export default {
  data() {
    return {
      employees: [],
      isLoading: false,
      search: "",
      statistics: [],
      searchTimeout: null,

      editingAdmin: {},
      selectedAvatarFile: null, // Biến lưu file ảnh khi chọn
      previewAvt: null, // Biến lưu URL ảnh preview
      isSaving: false,
      modalInstance: null,
      filter: {
        roles: [],
        status: null,
        createdAtFrom: "",
        createdAtTo: "",
      },
    };
  },
  mounted() {
    this.loadAdminData();
    this.loadAdminStatistical();
  },

  computed: {
    sortedEmployees() {
      return [...this.employees].reverse();
    },
  },

  methods: {
    loadAdminData() {
      axios
        .get(`http://localhost:8081/api/admin/admins/lay-du-lieu`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.employees = res.data;
        })
        .catch((err) => console.error(err));
    },

    formatDate(dateString) {
      if (!dateString) return "";
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    },

    convertStatus(status) {
      return status === 1 ? "Active" : "Inactive";
    },

    getStatusClass(status) {
      return status === 1
        ? "bg-success-subtle border-success-subtle text-success"
        : "bg-secondary-subtle border-secondary-subtle text-secondary";
    },

    convertRole(role) {
      return role === 4 ? "Super Admin" : "Admin";
    },

    getRoleClass(role) {
      return role === 4
        ? "bg-danger-subtle border-danger-subtle text-danger"
        : "bg-secondary-subtle border-secondary-subtle text-primary";
    },

    // --- 2. Các hàm Xử lý Modal & File ---

    openEditModal(adminData) {
      // Copy dữ liệu để sửa
      this.editingAdmin = { ...adminData };
      this.selectedAvatarFile = null;
      this.previewAvt = null;

      const modalElement = document.getElementById("editAdminModal");
      if (modalElement) {
        // eslint-disable-next-line no-undef
        this.modalInstance = new bootstrap.Modal(modalElement);
        this.modalInstance.show();
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Kiểm tra dung lượng (ví dụ 3MB)
        if (file.size > 3 * 1024 * 1024) {
          alert("File too large! Please select an image under 3MB.");
          return;
        }
        // Tạo URL xem trước
        this.previewAvt = URL.createObjectURL(file);
        // Lưu file thật để lát upload
        this.selectedAvatarFile = file;
      }
    },

    handleUpdateProcess() {
      this.isSaving = true;
      let uploadPromise;

      if (this.selectedAvatarFile) {
        const formData = new FormData();

        formData.append("imageFile", this.selectedAvatarFile);

        uploadPromise = axios
          .post("http://localhost:8081/api/admin/uploads/upload-image", formData, {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            console.log("KẾT QUẢ UPLOAD:", res.data);

            // Trường hợp 1: Cấu trúc data.imageUrl
            if (res.data && res.data.data && res.data.data.imageUrl) {
              return res.data.data.imageUrl;
            }
            // Trường hợp 2: Trả về string trực tiếp (Fallback)
            if (typeof res.data.data === "string") return res.data.data;

            return null;
          });
      } else {
        // Nếu không chọn ảnh mới, trả về null để biết là giữ ảnh cũ
        uploadPromise = Promise.resolve(null);
      }

      // Thực hiện Update thông tin sau khi (có thể) đã upload
      uploadPromise
        .then((newAvatarUrl) => {
          const finalAvatar = newAvatarUrl ? newAvatarUrl : this.editingAdmin.avatar;

          console.log("Link ảnh cập nhật vào DB:", finalAvatar);

          const updatePayload = {
            fullName: this.editingAdmin.fullName,
            phoneNumber: this.editingAdmin.phoneNumber,
            role: this.editingAdmin.role,
            status: this.editingAdmin.status,
            avatar: finalAvatar, // Gán link ảnh đã xử lý
            email: this.editingAdmin.email,
          };

          return axios.put(
            `http://localhost:8081/api/admin/admins/cap-nhat/${this.editingAdmin.id}`,
            updatePayload,
            {
              headers: {
                Authorization: "Bearer " + localStorage.getItem("token"),
                "Content-Type": "application/json",
              },
            }
          );
        })
        .then((res) => {
          alert("Update successful!");

          if (this.modalInstance) {
            this.modalInstance.hide();
          }
          this.loadAdminData();
          if (this.loadAdminStatistical) this.loadAdminStatistical();
        })
        .catch((err) => {
          console.error("Lỗi quy trình:", err);
          const message = err.response?.data?.message || "Có lỗi xảy ra!";
          alert(message);
        })
        .finally(() => {
          this.isSaving = false;
        });
    },

    // --- Các hàm phụ trợ khác (Search, Delete...) ---
    handleSearch() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.performSearchApi();
      }, 500);
    },

    performSearchApi() {
      if (!this.search.trim()) {
        this.loadAdminData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/admins/tim-kiem?q=${this.search}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.employees = res.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleDelete(adminId, adminName) {
      if (!confirm(`Are you sure you want to delete Admin ${adminName}?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/admins/xoa/${adminId}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadAdminData();
        })
        .catch((err) => alert(err.response?.data?.message || "Error deleting admin"));
    },

    loadAdminStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/admins/thong-ke`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => (this.statistics = res.data));
    },

    handleFilter() {
      this.isLoading = true;

      const payload = {
        roles: this.filter.roles.length > 0 ? this.filter.roles : null, // Nếu mảng rỗng thì gửi null
        status: this.filter.status,
        createdAtFrom: this.filter.createdAtFrom ? `${this.filter.createdAtFrom}T00:00:00` : null,
        createdAtTo: this.filter.createdAtTo ? `${this.filter.createdAtTo}T23:59:59` : null,
      };

      console.log("Filter Payload:", payload);

      axios
        .post(`http://localhost:8081/api/admin/admins/loc-admin`, payload, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          // Cập nhật danh sách hiển thị
          this.employees = res.data;
        })
        .catch((err) => {
          console.error("Lỗi lọc admin:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    resetFilter() {
      this.filter = {
        roles: [],
        status: null,
        createdAtFrom: "",
        createdAtTo: "",
      };

      this.loadAdminData();
    },
  },
};
</script>
