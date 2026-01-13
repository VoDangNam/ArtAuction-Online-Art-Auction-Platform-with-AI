<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="text-primary fw-bold mb-1">Report Management</h4>
      <p class="text-body-secondary mb-0">Handle violation reports and complaints from users</p>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-sm-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">General report</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.totalReports }}</h3>
              </div>
              <div
                class="bg-secondary-subtle text-primary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-file-lines fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total reports submitted</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Pending</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.pendingReports }}</h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-clock fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">Need to consider</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-info">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">In progress</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">
                  {{ statistics.investigatingReports }}
                </h3>
              </div>
              <div
                class="bg-info bg-opacity-10 text-info-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-hourglass-start fs-5"></i>
              </div>
            </div>
            <small class="text-body-secondary fw-medium">Under investigation</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Resolved</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.resolvedReports }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
            <small class="text-success fw-medium">Successfully handled</small>
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
                type="text"
                class="form-control bg-transparent border-0 shadow-none"
                placeholder="Search for report..."
                @input="handleSearch"
              />
            </div>
          </div>
          <div class="col-12 col-md-6 col-lg-8 text-md-end">
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
                      Invoice filter
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
                      <div class="mb-3">
                        <label class="form-label fw-bold text-uppercase small text-secondary mb-2"
                          >Status</label
                        >
                        <div class="bg-light rounded-3 p-3 border">
                          <div class="form-check mb-2">
                            <input
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusPaid"
                              :value="2"
                              v-model="filter.reportStatuses"
                            />
                            <label class="form-check-label text-success" for="statusActive"
                              >● Resolved
                            </label>
                          </div>
                          <div class="form-check mb-2">
                            <input
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusPending"
                              :value="0"
                              v-model="filter.reportStatuses"
                            />
                            <label class="form-check-label text-warning" for="statusLocked"
                              >● Pending
                            </label>
                          </div>
                          <div class="form-check mb-2">
                            <input
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusOverdue"
                              :value="1"
                              v-model="filter.reportStatuses"
                            />
                            <label class="form-check-label text-danger" for="statusLocked"
                              >● Investigating
                            </label>
                          </div>
                        </div>
                      </div>
                      <div class="mb-4">
                        <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                          Object Type
                        </label>
                        <div class="row g-2">
                          <div class="col-6">
                            <input
                              type="checkbox"
                              class="btn-check"
                              id="typeUser"
                              :value="1"
                              v-model="filter.objectTypes"
                              autocomplete="off"
                            />
                            <label
                              class="btn btn-outline-secondary btn-sm w-100 text-start"
                              for="typeUser"
                            >
                              <i class="fa-solid fa-user me-1"></i> User
                            </label>
                          </div>
                          <div class="col-6">
                            <input
                              type="checkbox"
                              class="btn-check"
                              id="typeArtwork"
                              :value="2"
                              v-model="filter.objectTypes"
                              autocomplete="off"
                            />
                            <label
                              class="btn btn-outline-secondary btn-sm w-100 text-start"
                              for="typeArtwork"
                            >
                              <i class="fa-solid fa-image me-1"></i> Artwork
                            </label>
                          </div>
                          <div class="col-6">
                            <input
                              type="checkbox"
                              class="btn-check"
                              id="typeAuction"
                              :value="3"
                              v-model="filter.objectTypes"
                              autocomplete="off"
                            />
                            <label
                              class="btn btn-outline-secondary btn-sm w-100 text-start"
                              for="typeAuction"
                            >
                              <i class="fa-solid fa-gavel me-1"></i> Auction Room
                            </label>
                          </div>
                          <div class="col-6">
                            <input
                              type="checkbox"
                              class="btn-check"
                              id="typeAi"
                              :value="4"
                              v-model="filter.objectTypes"
                              autocomplete="off"
                            />
                            <label
                              class="btn btn-outline-secondary btn-sm w-100 text-start"
                              for="typeAi"
                            >
                              <i class="fa-solid fa-robot me-1"></i> AI Artwork
                            </label>
                          </div>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-2">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-regular fa-calendar-check me-1"></i> Creation time
                      </label>

                      <div class="input-group input-group-sm">
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
          </div>
        </div>

        <div class="table-responsive overflow-y-auto custom-scrollbar" style="max-height: 500px">
          <table class="table table-hover align-middle text-nowrap mb-0">
            <thead class="bg-light sticky-top shadow-sm border-bottom border-light-subtle">
              <tr>
                <th scope="col" class="ps-4 py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Annunciator
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Object Type
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Object ID
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold text-dark text-uppercase x-small border-0"
                  style="max-width: 300px"
                >
                  Content
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Created At
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold text-dark text-uppercase x-small border-0 text-center"
                >
                  Status
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
              <tr
                v-for="item in reports"
                :key="item.id"
                class="transition-bg border-bottom border-light-subtle"
              >
                <td class="ps-4 py-3 border-0">
                  <div class="d-flex align-items-center gap-3">
                    <img
                      :src="item.reporterAvatar"
                      class="bg-secondary-subtle text-primary rounded-circle d-flex align-items-center justify-content-center fw-bold border border-2 border-white shadow-sm"
                      style="width: 40px; height: 40px"
                    />

                    <div class="d-flex flex-column">
                      <span class="fw-medium text-dark">{{ item.reporterName }}</span>
                      <span
                        class="badge bg-light text-secondary border border-light-subtle rounded-pill mt-1"
                        style="width: fit-content; font-size: 0.65rem"
                      >
                        ID: #{{ item.reporterId }}
                      </span>
                    </div>
                  </div>
                </td>

                <td class="py-3 border-0">
                  <span
                    class="badge bg-light text-dark border border-light-subtle rounded-pill fw-normal px-3 py-2"
                  >
                    <i class="fa-regular fa-folder me-2 text-secondary"></i>{{ item.reportTarget }}
                  </span>
                </td>

                <td class="py-3 border-0 fw-medium text-primary">
                  {{ item.objectId }}
                </td>

                <td
                  class="py-3 border-0 text-truncate"
                  style="max-width: 250px"
                  :title="item.content"
                >
                  <span class="text-secondary small">{{ item.reportReason }}</span>
                </td>

                <td class="py-3 border-0 small text-muted">
                  {{ formatDate(item.createdAt) }}
                </td>

                <td class="py-3 border-0 text-center">
                  <span
                    class="badge rounded-pill border fw-medium px-3 py-2"
                    :class="getStatusClass(item.reportStatus)"
                  >
                    <i class="fa-solid fa-circle fa-2xs me-1 opacity-75"></i>
                    {{ convertStatus(item.reportStatus) }}
                  </span>
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
                        <button class="dropdown-item py-2">
                          <i class="fa-regular fa-eye me-2 text-primary"></i>See details
                        </button>
                      </li>
                      <li><hr class="dropdown-divider my-1" /></li> -->
                      <!-- <li>
                        <button class="dropdown-item py-2">
                          <i class="fa-solid fa-triangle-exclamation me-2"></i>Warning
                        </button>
                      </li>
                      <li>
                        <button class="dropdown-item py-2 text-danger">
                          <i class="fa-solid fa-ban me-2"></i>Block User
                        </button>
                      </li> -->
                      <li>
                        <button
                          class="dropdown-item py-2 text-danger"
                          @click="handleDelete(item.id)"
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
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      reports: [],
      isLoading: false,
      statistics: [],
      filter: {
        reportStatuses: null,
        objectTypes: [],
        createdAtFrom: "",
        createdAtTo: "",
      },
    };
  },
  mounted() {
    this.loadReportData();
    this.loadReportStatistical();
  },
  methods: {
    loadReportData() {
      this.isLoading = true;
      axios
        .get("http://localhost:8081/api/admin/reports/lay-du-lieu", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.reports = res.data.data;
          console.log("Data Loaded:", this.reports);
        })
        .catch((err) => {
          console.error("Error loading rooms:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    convertStatus(status) {
      switch (status) {
        case 0:
          return "Pending";
        case 1:
          return "Investigating";
        case 2:
          return "Resolved";
        default:
          return "Unknown";
      }
    },

    // Lấy màu trạng thái - Cập nhật style cho Badge Pill
    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-warning-subtle text-warning-emphasis border-warning-subtle";
        case 1:
          return "bg-danger-subtle text-danger border-danger-subtle";
        case 2:
          return "bg-success-subtle text-success border-success-subtle";
        default:
          return "bg-light text-dark border-light";
      }
    },

    handleDelete(reportId) {
      if (!confirm(`Are you sure you want to delete this report?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/reports/xoa/${reportId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadReportData();
        })
        .catch((err) => {
          console.error("Error:", err);
          const message = err.response?.data?.message || "Error!";
          alert(message);
        });
    },

    handleSearch() {
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
        this.loadReportData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/reports/tim-kiem?q=${this.search}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.artworks = res.data;
          console.log("Kết quả tìm kiếm:", this.artworks);
        })
        .catch((err) => {
          console.error("Error:", err);
          this.artworks = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    loadReportStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/reports/thong-ke`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.statistics = res.data.data;
          console.log("Kết quả tìm kiếm:", this.statistics);
        })
        .catch((err) => {
          console.error("Error:", err);
          this.statistics = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);

      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    },

    handleFilter() {
      let statusValue = this.filter.reportStatuses;
      let statusesToSend = statusValue !== null && statusValue !== undefined ? [statusValue] : null;

      const payload = {
        reportStatuses: statusesToSend,
        objectTypes: this.filter.objectTypes.length > 0 ? this.filter.objectTypes : null,
        createdAtFrom: this.filter.createdAtFrom || null,
        createdAtTo: this.filter.createdAtTo || null,
      };

      console.log("Filter Payload:", payload);

      axios
        .post("http://localhost:8081/api/admin/reports/loc-bao-cao", payload, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          this.reports = res.data.data || res.data;
        })
        .catch((err) => {
          console.error("Lỗi lọc báo cáo:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    resetFilter() {
      this.filter = {
        reportStatuses: null,
        objectTypes: [],
        createdAtFrom: "",
        createdAtTo: "",
      };

      this.loadReportData();
    },
  },
};
</script>
