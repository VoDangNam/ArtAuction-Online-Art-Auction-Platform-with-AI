<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100 position-relative">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-primary mb-1">Seller Requests</h4>
        <p class="text-body-secondary mb-0">Review applications to become a seller</p>
      </div>
      <!-- <button class="btn btn-light shadow-sm text-secondary" @click="fetchRequests">
        <i class="fa-solid fa-rotate-right me-2"></i>Refresh
      </button> -->
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-md-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Pending Review</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ stats.pending }}</h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-hourglass-half fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Awaiting approval</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Approved Today</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ stats.approved }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-check-double fs-5"></i>
              </div>
            </div>
            <small class="text-success fw-medium">Processed successfully</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-danger">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Rejected</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ stats.rejected }}</h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-xmark fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">Request denied</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4">
      <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
          <ul class="nav nav-pills nav-fill bg-light p-1 rounded-pill" style="min-width: 300px">
            <li class="nav-item">
              <a
                class="btn rounded-pill fw-medium border-0 w-100"
                :class="
                  currentStatus === 'PENDING'
                    ? 'btn-secondary-subtle fw-bold'
                    : 'btn-light text-secondary'
                "
                @click.prevent="changeStatus('PENDING')"
                style="cursor: pointer"
              >
                Pending
              </a>
            </li>
            <li class="nav-item">
              <a
                class="btn rounded-pill fw-medium border-0 w-100"
                :class="
                  currentStatus === 'APPROVED'
                    ? 'btn-secondary-subtle fw-bold'
                    : 'btn-light text-secondary'
                "
                @click.prevent="changeStatus('APPROVED')"
                style="cursor: pointer"
              >
                Approved
              </a>
            </li>
            <li class="nav-item">
              <a
                class="btn rounded-pill fw-medium border-0 w-100"
                :class="
                  currentStatus === 'REJECTED'
                    ? 'btn-secondary-subtle fw-bold'
                    : 'btn-light text-secondary'
                "
                @click.prevent="changeStatus('REJECTED')"
                style="cursor: pointer"
              >
                Rejected
              </a>
            </li>
          </ul>

          <!-- <div class="input-group" style="max-width: 300px">
            <span class="input-group-text bg-light border-end-0 text-secondary">
              <i class="fa-solid fa-search"></i>
            </span>
            <input
              type="text"
              class="form-control bg-light border-start-0 shadow-none"
              placeholder="Search user ID..."
              v-model="searchQuery"
            />
          </div> -->
        </div>
      </div>

      <div class="card-body px-0">
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-secondary mt-2">Loading requests...</p>
        </div>

        <div v-else-if="filteredRequests.length === 0" class="text-center py-5">
          <img
            src="https://cdn-icons-png.flaticon.com/512/7486/7486754.png"
            alt="Empty"
            width="80"
            class="opacity-50 mb-3"
          />
          <h6 class="text-secondary">No {{ currentStatus.toLowerCase() }} requests found</h6>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-4 text-secondary text-uppercase x-small fw-bold">User</th>
                <th class="text-secondary text-uppercase x-small fw-bold">Created Date</th>
                <th class="text-secondary text-uppercase x-small fw-bold">Summary</th>
                <th class="text-secondary text-uppercase x-small fw-bold">Status</th>
                <th class="pe-4 text-secondary text-uppercase x-small fw-bold">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in tableData" :key="req.id">
                <td class="ps-4">
                  <div class="d-flex align-items-center gap-3">
                    <img
                      :src="req.userAvt || defaultAvatar"
                      class="rounded-circle border"
                      width="40"
                      height="40"
                      style="object-fit: cover"
                    />
                    <div>
                      <div
                        class="fw-bold text-dark text-truncate"
                        style="max-width: 150px"
                        :title="req.userName"
                      >
                        {{ req.userName }}
                      </div>
                      <div class="small text-secondary">ID: {{ req.id.substring(0, 8) }}...</div>
                    </div>
                  </div>
                </td>
                <td class="text-secondary">{{ formatDate(req.createdAt) }}</td>
                <td>
                  <div class="d-flex align-items-center text-muted" style="max-width: 250px">
                    <i class="fa-regular fa-file-lines me-2"></i>
                    <span class="text-truncate">{{ req.reason || "No description provided" }}</span>
                  </div>
                </td>
                <td class="">
                  <span
                    class="badge rounded-pill px-3 py-2 fw-normal"
                    :class="getStatusBadge(req.status)"
                  >
                    {{ req.status }}
                  </span>
                </td>
                <td class="pe-4">
                  <button
                    class="btn btn-sm btn-primary rounded-pill px-3 shadow-sm"
                    @click="openReviewModal(req)"
                  >
                    <i class="fa-solid fa-eye me-1"></i> Review
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="reviewModal"
      tabindex="-1"
      aria-hidden="true"
      data-bs-backdrop="static"
    >
      <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-white border-bottom-0 pt-4 px-4">
            <div class="d-flex align-items-center gap-3">
              <div
                class="bg-secondary-subtle text-primary rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-user-shield fs-5"></i>
              </div>
              <div>
                <h5 class="modal-title fw-bold text-dark mb-0">Review Seller Request</h5>
                <p class="text-body-secondary mb-0 small">Request ID: #{{ selectedRequest.id }}</p>
              </div>
            </div>
            <button
              type="button"
              class="btn-close shadow-none bg-light rounded-circle p-2"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body p-4 bg-light-subtle">
            <div class="row g-4">
              <div class="col-lg-4">
                <div class="card border-0 shadow-sm rounded-4 h-100">
                  <div class="card-body">
                    <h6 class="fw-bold text-uppercase text-secondary x-small mb-3">
                      Applicant Info
                    </h6>
                    <div class="text-center mb-4">
                      <img
                        :src="selectedRequest.userAvt || defaultAvatar"
                        class="rounded-circle border mb-2"
                        width="100"
                        height="100"
                        style="object-fit: cover"
                      />
                      <h5 class="fw-bold mb-0 text-break">{{ selectedRequest.userName }}</h5>
                      <span class="text-secondary small"
                        >User ID: {{ selectedRequest.userId }}</span
                      >

                      <hr class="border-secondary opacity-10 my-3" />

                      <!-- <div class="d-flex justify-content-between px-2">
                        <span class="small text-muted">Email:</span>
                        <span class="small fw-bold">{{ selectedRequest.userEmail || "N/A" }}</span>
                      </div>
                      <div class="d-flex justify-content-between px-2 mt-2">
                        <span class="small text-muted">Phone:</span>
                        <span class="small fw-bold">{{ selectedRequest.userPhone || "N/A" }}</span>
                      </div> -->
                    </div>

                    <h6 class="fw-bold text-uppercase text-secondary x-small mb-2 mt-4">
                      Description / Letter
                    </h6>
                    <div
                      class="p-3 bg-light rounded-3 border text-secondary"
                      style="min-height: 100px; font-size: 0.95rem"
                    >
                      {{ selectedRequest.reason || "User did not provide a description." }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-lg-8">
                <div class="card border-0 shadow-sm rounded-4 mb-3">
                  <div
                    class="card-header bg-white border-0 pt-3 pb-0 d-flex justify-content-between align-items-center"
                  >
                    <h6 class="fw-bold text-uppercase text-secondary x-small mb-0">
                      <i class="fa-solid fa-images me-1"></i> Verification Documents
                    </h6>
                    <span
                      class="badge bg-light text-secondary border"
                      v-if="selectedRequest.images"
                    >
                      {{ selectedRequest.images.length }} files
                    </span>
                  </div>

                  <div class="card-body p-3">
                    <div v-if="selectedRequest.images && selectedRequest.images.length > 0">
                      <div
                        class="bg-dark rounded-3 position-relative d-flex align-items-center justify-content-center mb-2 overflow-hidden"
                        style="height: 350px; cursor: zoom-in"
                        @click="openFullscreen(selectedRequest.images[activeImageIndex])"
                      >
                        <img
                          :src="selectedRequest.images[activeImageIndex]"
                          class="img-fluid"
                          style="max-height: 100%; object-fit: contain"
                          alt="Main document"
                        />
                        <div
                          class="position-absolute bottom-0 w-100 bg-black bg-opacity-50 text-white text-center py-1 small user-select-none"
                        >
                          <i class="fa-solid fa-expand me-1"></i> Click to view fullscreen
                        </div>
                      </div>

                      <div
                        v-if="selectedRequest.images.length > 1"
                        class="d-flex gap-2 overflow-auto py-1"
                      >
                        <div
                          v-for="(img, index) in selectedRequest.images"
                          :key="index"
                          class="rounded-2 border position-relative"
                          :class="
                            activeImageIndex === index
                              ? 'border-primary border-2 opacity-100'
                              : 'opacity-50 border-light'
                          "
                          style="
                            width: 70px;
                            height: 70px;
                            min-width: 70px;
                            cursor: pointer;
                            transition: all 0.2s;
                          "
                          @click="activeImageIndex = index"
                        >
                          <img :src="img" class="w-100 h-100 rounded-2" style="object-fit: cover" />
                        </div>
                      </div>
                    </div>

                    <div v-else class="text-center py-5 bg-light rounded-3 border border-dashed">
                      <div class="text-secondary opacity-25 mb-2">
                        <i class="fa-regular fa-image fa-3x"></i>
                      </div>
                      <p class="text-muted small mb-0">No documents uploaded.</p>
                    </div>
                  </div>
                </div>

                <div
                  class="card border-0 shadow-sm rounded-4"
                  v-if="selectedRequest.status === 'PENDING'"
                >
                  <div class="card-body">
                    <h6 class="fw-bold text-uppercase text-secondary x-small mb-2">
                      Admin Processing
                    </h6>
                    <div class="form-floating mb-3">
                      <textarea
                        class="form-control"
                        placeholder="Leave a note here"
                        id="adminNote"
                        v-model="adminNote"
                        style="height: 100px"
                      ></textarea>
                      <label for="adminNote">Reason / Note (Required for rejection)</label>
                    </div>
                    <div class="d-flex justify-content-end gap-2">
                      <button
                        class="btn btn-outline-danger px-4 rounded-pill fw-bold"
                        @click="handleReject"
                        :disabled="isProcessing"
                      >
                        <i class="fa-solid fa-xmark me-2"></i>Reject
                      </button>
                      <button
                        class="btn btn-success px-4 rounded-pill fw-bold text-white"
                        @click="handleApprove"
                        :disabled="isProcessing"
                      >
                        <i class="fa-solid fa-check me-2"></i>Approve Seller
                      </button>
                    </div>
                  </div>
                </div>

                <div class="card border-0 shadow-sm rounded-4" v-else>
                  <div class="card-body">
                    <div
                      class="alert mb-0"
                      :class="
                        selectedRequest.status === 'APPROVED' ? 'alert-success' : 'alert-danger'
                      "
                    >
                      <h6 class="fw-bold mb-1">
                        <i
                          class="fa-solid"
                          :class="
                            selectedRequest.status === 'APPROVED'
                              ? 'fa-circle-check'
                              : 'fa-circle-xmark'
                          "
                        ></i>
                        Request {{ selectedRequest.status }}
                      </h6>
                      <p class="mb-0 small">
                        <strong>Admin Note:</strong>
                        {{ selectedRequest.adminNote || "No note provided" }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="fullscreenImage"
        class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center"
        style="z-index: 100000 !important; background-color: rgba(0, 0, 0, 0.95); cursor: zoom-out"
        @click.self="closeFullscreen"
      >
        <button
          type="button"
          class="btn-close btn-close-white position-absolute top-0 end-0 m-4 shadow-none fs-4"
          style="z-index: 100001; opacity: 1"
          @click="closeFullscreen"
        ></button>

        <img
          :src="fullscreenImage"
          class="img-fluid shadow-lg rounded-3"
          style="
            max-width: 95vw;
            max-height: 95vh;
            width: auto;
            height: auto;
            object-fit: contain;
            user-select: none;
            pointer-events: auto;
          "
        />
      </div>
    </Teleport>
  </div>
</template>

<script>
import axios from "axios";
import * as bootstrap from "bootstrap";
import defaultAvatar from "../../../assets/img/avt.png";

export default {
  data() {
    return {
      requests: [],
      currentStatus: "PENDING",
      isLoading: false,
      isProcessing: false,
      searchQuery: "",
      selectedRequest: {},
      adminNote: "",
      modalInstance: null,
      activeImageIndex: 0,
      fullscreenImage: null,
    };
  },
  computed: {
    //Tính toán số lượng trực tiếp từ mảng gốc (FE Calculation)
    stats() {
      return {
        pending: this.requests.filter((r) => r.status === "PENDING").length,
        approved: this.requests.filter((r) => r.status === "APPROVED").length,
        rejected: this.requests.filter((r) => r.status === "REJECTED").length,
      };
    },

    // Lọc dữ liệu để hiển thị ra bảng (Kết hợp tìm kiếm + Trạng thái đang chọn)
    tableData() {
      //Lọc theo Tab đang chọn (PENDING/APPROVED...)
      let data = this.requests.filter((r) => r.status === this.currentStatus);

      // Lọc theo ô tìm kiếm (Search) nếu có
      if (this.searchQuery) {
        const lowerSearch = this.searchQuery.toLowerCase();
        data = data.filter(
          (r) =>
            (r.userName && r.userName.toLowerCase().includes(lowerSearch)) ||
            (r.userId && r.userId.toLowerCase().includes(lowerSearch))
        );
      }

      //  Đảo ngược để mới nhất lên đầu
      return data.reverse();
    },
    filteredRequests() {
      if (!this.searchQuery) return this.requests;
      const lowerSearch = this.searchQuery.toLowerCase();
      return this.requests.filter(
        (r) =>
          (r.userName && r.userName.toLowerCase().includes(lowerSearch)) ||
          (r.userId && r.userId.toLowerCase().includes(lowerSearch))
      );
    },
    pendingCount() {
      return this.requests.filter((r) => r.status === "PENDING").length;
    },
  },
  mounted() {
    this.fetchAllData();
  },
  methods: {
    fetchAllData() {
      this.isLoading = true;
      const headers = { Authorization: "Bearer " + localStorage.getItem("token") };
      const url = "http://localhost:8081/api/admin/seller-request";

      // Tạo 3 request lấy riêng lẻ từng trạng thái
      const reqPending = axios.get(url, { params: { status: "PENDING" }, headers });
      const reqApproved = axios.get(url, { params: { status: "APPROVED" }, headers });
      const reqRejected = axios.get(url, { params: { status: "REJECTED" }, headers });

      Promise.all([reqPending, reqApproved, reqRejected])
        .then(([resPending, resApproved, resRejected]) => {
          // Gộp 3 mảng lại thành 1 mảng tổng duy nhất
          const allRawData = [...resPending.data, ...resApproved.data, ...resRejected.data];

          // Map dữ liệu
          this.requests = allRawData.map((item) => ({
            id: item.id,
            userId: item.userId,
            userName: item.userId, // Hoặc item.userName nếu backend có
            userAvt: item.userAvt || defaultAvatar,
            reason: item.description,
            status: item.status,
            adminNote: item.adminNote,
            createdAt: item.updatedAt || item.createdAt,
            images: item.verificationImageUrl ? [item.verificationImageUrl] : [],
          }));
          console.log('📦 Raw API response:', this.requests);

        })
        .catch((err) => {
          console.error("Error fetching data:", err);
          this.requests = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    changeStatus(status) {
      this.currentStatus = status;
      // this.fetchRequests();
    },

    openReviewModal(request) {
      this.selectedRequest = { ...request };
      this.adminNote = request.adminNote || "";
      this.activeImageIndex = 0;

      const modalElement = document.getElementById("reviewModal");
      if (modalElement) {
        this.modalInstance = new bootstrap.Modal(modalElement);
        this.modalInstance.show();
      }
    },

    openFullscreen(imgSrc) {
      if (!imgSrc) return;
      this.fullscreenImage = imgSrc;
      document.body.style.overflow = "hidden";
    },

    closeFullscreen() {
      this.fullscreenImage = null;
      document.body.style.overflow = "";
    },

    handleApprove() {
      if (!confirm("Confirm approve this user to become a seller?")) return;
      this.isProcessing = true;
      const payload = { note: this.adminNote };

      axios
        .put(
          `http://localhost:8081/api/admin/seller-request/${this.selectedRequest.id}/approve`,
          payload,
          { headers: { Authorization: "Bearer " + localStorage.getItem("token") } }
        )
        .then(() => {
          alert("Approved successfully!");
          this.modalInstance.hide();
          this.fetchAllData(); // Load lại để cập nhật thống kê
        })
        .catch((err) => alert("Failed to approve."))
        .finally(() => (this.isProcessing = false));
    },

    handleReject() {
      if (!this.adminNote.trim()) {
        alert("Please provide a reason.");
        return;
      }
      if (!confirm("Confirm reject this request?")) return;
      this.isProcessing = true;
      const payload = { note: this.adminNote };

      axios
        .put(
          `http://localhost:8081/api/admin/seller-request/${this.selectedRequest.id}/reject`,
          payload,
          { headers: { Authorization: "Bearer " + localStorage.getItem("token") } }
        )
        .then(() => {
          alert("Rejected successfully!");
          this.modalInstance.hide();
          this.fetchAllData(); // Load lại để cập nhật thống kê
        })
        .catch((err) => alert("Failed to reject."))
        .finally(() => (this.isProcessing = false));
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

    getStatusBadge(status) {
      switch (status) {
        case "PENDING":
          return "bg-warning-subtle text-warning-emphasis border border-warning-subtle";
        case "APPROVED":
          return "bg-success-subtle text-success border border-success-subtle";
        case "REJECTED":
          return "bg-danger-subtle text-danger border border-danger-subtle";
        default:
          return "bg-light text-secondary border";
      }
    },
  },
};
</script>

<style scoped>
.x-small {
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}
.overflow-auto::-webkit-scrollbar {
  height: 4px;
}
.overflow-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.overflow-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}
</style>
