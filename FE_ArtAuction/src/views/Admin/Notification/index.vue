<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4">
      <div class="mb-3 mb-md-0">
        <h4 class="fw-bold text-primary mb-1">Notification Management</h4>
        <p class="text-body-secondary mb-0">Manage all auction rooms notifications</p>
      </div>
      <router-link to="/admin/sent-notification" class="btn btn-primary shadow-sm px-4">
        <i class="fa-solid fa-paper-plane"></i> Create Notification
      </router-link>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-md-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Total Notifications</h6>
                <h3 class="fw-bold mb-0">
                  {{ (statistical && statistical.totalNotifications) || 0 }}
                </h3>
              </div>
              <div
                class="bg-secondary-subtle text-primary rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-bell fs-5"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Sent</h6>
                <h3 class="fw-bold mb-0">
                  {{ statistical && statistical.statusCounts && statistical.statusCounts["1"] }}
                </h3>
              </div>
              <div
                class="bg-success-subtle text-success rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Failed</h6>
                <h3 class="fw-bold mb-0">
                  {{ statistical && statistical.statusCounts && statistical.statusCounts["0"] }}
                </h3>
              </div>
              <div
                class="bg-danger-subtle text-danger rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-ban fs-5"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Read Rate</h6>
                <h3 class="fw-bold mb-0">
                  {{
                    (statistical && statistical.readRate ? statistical.readRate * 100 : 0).toFixed(
                      0
                    )
                  }}%
                </h3>
              </div>
              <div
                class="bg-info-subtle text-info rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-eye fs-5"></i>
              </div>
            </div>
          </div>
        </div>
      </div> -->
    </div>

    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-12 col-md-8">
            <div class="input-group bg-light rounded-pill px-2 border-0">
              <span class="input-group-text bg-transparent border-0 text-secondary">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control bg-transparent border-0 shadow-none"
                placeholder="Search by notification content..."
                @input="handleSearch"
              />
            </div>
          </div>
          <div class="col-12 col-md-4">
            <select
              v-model="selectedStatus"
              @change="handleFilter"
              class="form-select rounded-pill border-0 bg-light shadow-none"
              aria-label="Filter select"
            >
              <option value="">All Status</option>
              <option value="1">Sent</option>
              <option value="0">Failed</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex no-scrollbar flex-column gap-3 overflow-y-auto" style="max-height: 500px">
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div v-else-if="notifications.length === 0" class="text-center py-5 text-muted">
        <p>No announcements</p>
      </div>

      <div v-else class="d-flex flex-column gap-3">
        <div
          v-for="notification in sortedNotifications"
          :key="notification.id"
          class="card border-0 shadow-sm position-relative"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div class="d-flex align-items-center gap-2">
                <h5 class="fw-bold mb-0">{{ notification.title }}</h5>
                <span
                  class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1"
                  :class="getStatusClass(notification.notificationStatus)"
                >
                  {{ convertStatus(notification.notificationStatus) }}
                </span>
              </div>

              <div class="d-flex align-items-center text-body-secondary small">
                <i class="fa-solid fa-user-group me-2"></i>
                <span
                  >Receiver: <strong>{{ notification.userId }}</strong></span
                >
              </div>
            </div>

            <div class="d-flex justify-content-between align-items-start mb-3">
              <p class="text-dark mb-0" style="max-width: 80%">
                {{ notification.notificationContent }}
              </p>

              <div class="dropdown">
                <button
                  class="btn btn-sm btn-light rounded-circle shadow-sm"
                  type="button"
                  data-bs-toggle="dropdown"
                  style="width: 34px; height: 34px"
                >
                  <i class="fa-solid fa-ellipsis-vertical text-secondary"></i>
                </button>

                <ul
                  class="dropdown-menu dropdown-menu-end shadow border-0"
                  style="border-radius: 8px"
                >
                  <!-- <li>
                    <button class="dropdown-item" @click="viewDetail(notification)">
                      <i class="fa-solid fa-circle-info me-2 text-primary"></i>
                      See Details
                    </button>
                  </li> -->
                  <!-- <li><hr class="dropdown-divider" /></li> -->

                  <li>
                    <button
                      class="dropdown-item text-danger"
                      @click="handleDelete(notification.id)"
                    >
                      <i class="fa-solid fa-trash me-2"></i>
                      Delete
                    </button>
                  </li>
                </ul>
              </div>
            </div>

            <div class="d-flex align-items-center text-muted small">
              <i class="fa-regular fa-clock me-2"></i>
              <span>{{ formatDate(notification.notificationTime) }}</span>
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
      statistical: {},
      isLoading: false,
      notifications: [],
      search: "",
      selectedStatus: "",
    };
  },

  mounted() {
    this.loadNotificationStatistics();
    this.loadNotificationData();
  },

  computed: {
    // Đảo ngược thứ tự mảng
    sortedNotifications() {
      return [...this.notifications].reverse();
    },
  },

  watch: {
    notifications: {
      handler(newVal) {
        console.log("Notifications changed:", newVal);
        console.log("Length:", newVal?.length);
      },
      immediate: true,
      deep: true,
    },
  },

  methods: {
    loadNotificationStatistics() {
      axios
        .get("http://localhost:8081/api/admin/notifications/thong-ke", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.statistical = res.data.data;
        })
        .catch((err) => {
          console.error("Lỗi thống kê:", err);
        });
    },

    loadNotificationData() {
      this.isLoading = true;
      axios
        .get("http://localhost:8081/api/admin/notifications/lay-du-lieu", {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          const payload = res.data?.data;
          if (Array.isArray(payload)) {
            this.notifications = payload;
          } else if (payload && Array.isArray(payload.content)) {
            // Một số API trả về { data: { content: [], totalPages, ... } }
            this.notifications = payload.content;
          } else {
            this.notifications = [];
          }
          console.log("Đã tải:", this.notifications.length, "thông báo");
        })
        .catch((err) => {
          console.error("Lỗi tải danh sách:", err);
          this.notifications = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Hàm xử lý khi bấm Xem chi tiết
    viewDetail(notification) {
      console.log("Xem chi tiết ID:", notification.id);

      alert("Xem chi tiết: " + notification.title);
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);

      // Tùy chọn định dạng (Format: Oct 22, 2025, 02:30 PM)
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short", // "short" = Oct, "long" = October, "numeric" = 10
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true, // true = AM/PM, false = 24h
      });
    },

    convertStatus(status) {
      switch (status) {
        case 1:
          return "Sent";
        case 0:
          return "Failed";
        default:
          return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 0:
          return "bg-danger-subtle border-danger-subtle text-danger";
        // default:
        //   return "bg-secondary-subtle border-secondary-subtle text-secondary";
      }
    },

    handleSearch() {
      // Xóa bộ đếm cũ nếu người dùng gõ tiếp khi chưa hết giờ
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }

      // Thiết lập bộ đếm mới (ví dụ: chờ 500ms)
      this.searchTimeout = setTimeout(() => {
        this.performSearchApi();
      }, 500);
    },

    performSearchApi() {
      if (!this.search.trim()) {
        this.loadNotificationData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/notifications/tim-kiem?q=${this.search}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          const payload = res.data && res.data.data ? res.data.data : res.data;
          this.notifications = Array.isArray(payload) ? payload : [];

          // console.log("Kết quả tìm kiếm:", this.notifications);
        })
        .catch((err) => {
          console.error("Error:", err);
          this.notifications = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleFilter() {
      if (this.selectedStatus === "") {
        this.loadNotificationData();
        return;
      }

      this.isLoading = true;

      axios
        .get(`http://localhost:8081/api/admin/notifications/loc-theo-trang-thai`, {
          params: { status: this.selectedStatus }, // Tự động tạo ?status=...
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          const payload = res.data?.data;

          if (Array.isArray(payload)) {
            this.notifications = payload;
          } else if (payload && Array.isArray(payload.content)) {
            this.notifications = payload.content;
          } else {
            this.notifications = [];
          }
          console.log(`Đã lọc theo status ${this.selectedStatus}:`, this.notifications.length);
        })
        .catch((err) => {
          console.error("Error:", err);
          this.notifications = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    // Xóa
    handleDelete(notiId) {
      if (!confirm(`Are you sure you want to delete this notification?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/notifications/xoa/${notiId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadNotificationData();
        })
        .catch((err) => {
          console.error("Lỗi khi xóa:", err);
          const message = err.response?.data?.message || "Có lỗi xảy ra khi xóa!";
          alert(message);
        });
    },
  },
};
</script>
