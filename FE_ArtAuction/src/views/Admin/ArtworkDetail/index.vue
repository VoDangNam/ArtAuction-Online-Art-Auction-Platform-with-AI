<template>
  <div class="container-fluid py-5 bg-light min-vh-100">
    <div
      v-if="isLoading"
      class="d-flex flex-column align-items-center justify-content-center py-5"
      style="height: 80vh"
    >
      <div
        class="spinner-border text-primary"
        role="status"
        style="width: 3rem; height: 3rem"
      ></div>
      <p class="mt-3 text-secondary fw-medium">Loading artwork details...</p>
    </div>

    <div v-else-if="error" class="container">
      <div class="alert alert-danger border-0 shadow-sm rounded-4 p-4 text-center">
        <i class="fa-solid fa-circle-exclamation fa-2x mb-3 text-danger"></i>
        <h5 class="fw-bold">{{ error }}</h5>
        <button class="btn btn-outline-danger mt-2 rounded-pill px-4" @click="$router.back()">
          Go Back
        </button>
      </div>
    </div>

    <div v-else-if="artwork" class="container-xl">
      <div
        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4 gap-3"
      >
        <div>
          <button
            @click="$router.back()"
            class="btn btn-link text-decoration-none text-secondary p-0 mb-2 fw-medium"
          >
            <i class="fa-solid fa-arrow-left me-2"></i>Back to List
          </button>
          <div class="d-flex align-items-center gap-3">
            <h3 class="fw-bold text-dark mb-0">Artwork Review</h3>
            <span
              class="badge rounded-pill px-3 py-2 border"
              :class="getStatusClass(artwork.status)"
            >
              {{ convertStatus(artwork.status) }}
            </span>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-7 col-xl-8">
          <div class="card border-0 shadow-sm rounded-4 overflow-hidden h-100 bg-dark">
            <div
              class="card-body p-0 d-flex align-items-center justify-content-center position-relative"
              style="min-height: 450px; background-color: #1a1a1a"
            >
              <div id="artworkCarousel" class="carousel slide w-100 h-100" data-bs-ride="false">
                <div class="carousel-inner h-100">
                  <div
                    v-for="(img, index) in allImages"
                    :key="'slide-' + index"
                    class="carousel-item h-100"
                    :class="{ active: index === 0 }"
                  >
                    <div class="d-flex align-items-center justify-content-center h-100 p-4">
                      <img
                        :src="img.src"
                        class="d-block mw-100 mh-100 shadow-lg rounded"
                        :alt="img.alt"
                        style="max-height: 320px; object-fit: contain"
                      />
                    </div>

                    <div class="carousel-caption pb-4" v-if="img.type === 'cert'">
                      <span
                        class="badge bg-warning text-dark border border-warning shadow fw-bold px-3 py-2"
                      >
                        <i class="fa-solid fa-certificate me-2"></i>Certificate / Document
                      </span>
                    </div>
                  </div>

                  <div
                    v-if="!allImages.length"
                    class="d-flex flex-column align-items-center justify-content-center h-100 text-secondary"
                  >
                    <i class="fa-regular fa-image fa-4x mb-3 opacity-50"></i>
                    <p>No images available</p>
                  </div>
                </div>

                <button
                  class="carousel-control-prev"
                  type="button"
                  data-bs-target="#artworkCarousel"
                  data-bs-slide="prev"
                  v-if="allImages.length > 1"
                >
                  <span
                    class="carousel-control-prev-icon bg-black bg-opacity-50 rounded-circle p-3"
                    aria-hidden="true"
                  ></span>
                  <span class="visually-hidden">Previous</span>
                </button>
                <button
                  class="carousel-control-next"
                  type="button"
                  data-bs-target="#artworkCarousel"
                  data-bs-slide="next"
                  v-if="allImages.length > 1"
                >
                  <span
                    class="carousel-control-next-icon bg-black bg-opacity-50 rounded-circle p-3"
                    aria-hidden="true"
                  ></span>
                  <span class="visually-hidden">Next</span>
                </button>
              </div>

              <div
                class="position-absolute bottom-0 start-0 w-100 p-3 d-flex justify-content-center gap-2"
                v-if="allImages.length > 1"
              >
                <button
                  v-for="(img, index) in allImages"
                  :key="'ind-' + index"
                  type="button"
                  data-bs-target="#artworkCarousel"
                  :data-bs-slide-to="index"
                  class="btn p-0 border-2 rounded overflow-hidden opacity-75 hover-opacity-100 transition-base"
                  :class="{ 'border-primary opacity-100': index === 0 }"
                  style="width: 40px; height: 40px"
                >
                  <img :src="img.src" class="w-100 h-100 object-fit-cover" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-5 col-xl-4">
          <div class="d-flex flex-column gap-4 h-100">
            <div class="card border-0 shadow-sm rounded-4">
              <div class="card-body p-4">
                <h5 class="fw-bold text-dark mb-1">{{ artwork.title || "Untitled" }}</h5>
                <p class="text-secondary mb-3">
                  by
                  <span class="fw-bold text-primary">{{ artwork.author || "Unknown Artist" }}</span>
                </p>

                <div class="d-flex gap-2 mb-4">
                  <span class="badge bg-light text-dark border fw-medium px-3 py-2">
                    <i class="fa-solid fa-palette me-1 text-secondary"></i>
                    {{ artwork.paintingGenre || "N/A" }}
                  </span>
                  <span class="badge bg-light text-dark border fw-medium px-3 py-2">
                    <i class="fa-regular fa-clock me-1 text-secondary"></i>
                    {{ artwork.yearOfCreation || "N/A" }}
                  </span>
                </div>

                <div class="bg-light-subtle rounded-3 p-3 border border-light-subtle">
                  <div class="row g-3 text-center">
                    <div class="col-6 border-end">
                      <small class="text-uppercase text-muted x-small fw-bold">Material</small>
                      <div class="fw-semibold text-dark">{{ artwork.material || "—" }}</div>
                    </div>
                    <div class="col-6">
                      <small class="text-uppercase text-muted x-small fw-bold">Dimensions</small>
                      <div class="fw-semibold text-dark">{{ artwork.size || "—" }}</div>
                    </div>
                  </div>
                </div>

                <div class="mt-4">
                  <h6 class="fw-bold text-uppercase text-secondary x-small mb-2">Description</h6>
                  <p
                    class="text-muted small mb-0 lh-base"
                    style="text-align: justify; max-height: 150px; overflow-y: auto"
                  >
                    {{ artwork.description || "No description provided." }}
                  </p>
                </div>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 flex-fill">
              <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
                <h6 class="fw-bold text-uppercase text-primary small mb-0">
                  <i class="fa-solid fa-gavel me-2"></i>Admin Processing
                </h6>
              </div>
              <div class="card-body p-4">
                <div class="mb-4">
                  <div
                    class="alert d-flex align-items-center border-0 mb-0 py-3"
                    :class="
                      artwork.aiVerified
                        ? 'alert-success bg-success-subtle text-success-emphasis'
                        : 'alert-danger bg-danger-subtle text-danger-emphasis'
                    "
                  >
                    <i
                      class="fa-solid fs-4 me-3"
                      :class="artwork.aiVerified ? 'fa-shield-check' : 'fa-shield-xmark'"
                    ></i>
                    <div class="flex-grow-1">
                      <h6 class="fw-bold mb-0">
                        {{ artwork.aiVerified ? "Verified by AI" : "AI Rejected" }}
                      </h6>
                      <small class="opacity-75" style="font-size: 0.75rem"
                        >System Authenticity Check</small
                      >
                    </div>
                  </div>
                </div>

                <label class="form-label fw-bold text-secondary x-small text-uppercase">
                  Starting Price (VND)
                </label>

                <div class="input-group input-group-lg">
                  <span class="input-group-text bg-white border-end-0 text-success fw-bold">₫</span>
                  <input
                    type="number"
                    class="form-control border-start-0 ps-0 fw-bold text-dark fs-4 shadow-none"
                    v-model.number="editedStartingPrice"
                    placeholder="0"
                    min="0"
                    step="1000"
                    :disabled="artwork.status !== 0"
                  />
                </div>
                <div class="mt-2 text-end">
                  <small class="text-muted small">Preview: </small>
                  <small class="text-muted">{{ formatCurrency(editedStartingPrice) }}</small>
                </div>

                <hr class="border-secondary opacity-10 my-4" />

                <div v-if="artwork.status === 0">
                  <div class="d-grid gap-3" v-if="!showRejectReasonInput">
                    <button
                      class="btn btn-primary btn-lg fw-bold shadow-sm"
                      @click="handleApproval('approve')"
                      :disabled="actionLoading === 'approve'"
                    >
                      <span
                        v-if="actionLoading === 'approve'"
                        class="spinner-border spinner-border-sm me-2"
                      ></span>
                      <i class="fa-solid fa-check me-2" v-else></i> Approve Artwork
                    </button>

                    <button
                      class="btn btn-outline-danger fw-bold"
                      @click="showRejectReasonInput = true"
                    >
                      <i class="fa-solid fa-xmark me-2"></i> Reject
                    </button>
                  </div>

                  <div v-else class="animate__animated animate__fadeIn">
                    <label class="form-label fw-bold text-danger small">
                      Reason for Rejection <span class="text-danger">*</span>
                    </label>
                    <textarea
                      class="form-control mb-3 shadow-none bg-light"
                      rows="3"
                      v-model="rejectionReason"
                      placeholder="Please enter the reason why this artwork is rejected..."
                    ></textarea>

                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-light text-secondary flex-fill fw-bold"
                        @click="cancelReject"
                        :disabled="actionLoading === 'reject'"
                      >
                        Cancel
                      </button>
                      <button
                        class="btn btn-danger flex-fill fw-bold shadow-sm"
                        @click="handleApproval('reject')"
                        :disabled="actionLoading === 'reject' || !rejectionReason.trim()"
                      >
                        <span
                          v-if="actionLoading === 'reject'"
                          class="spinner-border spinner-border-sm me-2"
                        ></span>
                        <i class="fa-solid fa-paper-plane me-2" v-else></i> Confirm Reject
                      </button>
                    </div>
                  </div>
                </div>

                <div v-else class="text-center py-2">
                  <span class="text-muted small fst-italic">
                    This artwork has been processed. Current status:
                    <strong>{{ convertStatus(artwork.status) }}</strong>
                  </span>
                </div>
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
  data() {
    return {
      artwork: null,
      isLoading: false,
      error: null,
      actionLoading: "",
      editedStartingPrice: 0,
      exchangeRate: 25400,

      // Thêm biến cho chức năng từ chối
      showRejectReasonInput: false,
      rejectionReason: "",
    };
  },
  computed: {
    artworkImages() {
      if (!this.artwork) return [];
      const gallery =
        this.artwork.artworkImages || this.artwork.images || this.artwork.gallery || [];
      if (Array.isArray(gallery) && gallery.length) {
        return gallery.map((img, index) => {
          if (typeof img === "string") {
            return { src: img, alt: `${this.artwork.title} - ${index + 1}`, type: "art" };
          }
          return {
            src: img.src || img.url,
            alt: img.alt || `Artwork - ${index + 1}`,
            type: "art",
          };
        });
      }
      if (this.artwork.avtArtwork) {
        return [{ src: this.artwork.avtArtwork, alt: this.artwork.title, type: "art" }];
      }
      return [];
    },
    certImages() {
      if (!this.artwork) return [];
      const certificates = this.artwork.certImages || this.artwork.certificates || [];
      if (!Array.isArray(certificates)) return [];
      return certificates.map((img, index) => {
        if (typeof img === "string") {
          return { src: img, alt: `Certificate - ${index + 1}`, type: "cert" };
        }
        return {
          src: img.src || img.url,
          alt: `Certificate - ${index + 1}`,
          type: "cert",
        };
      });
    },
    allImages() {
      return [...this.artworkImages, ...this.certImages];
    },
  },
  created() {
    this.fetchArtwork();
  },
  watch: {
    "$route.params.id"(newId, oldId) {
      if (newId && newId !== oldId) {
        this.fetchArtwork();
      }
    },
  },
  methods: {
    fetchArtwork() {
      const artworkId = this.$route.params.id;
      if (!artworkId) {
        this.error = "Artwork ID is missing.";
        return;
      }
      this.isLoading = true;
      this.error = null;
      axios
        .get(`http://localhost:8081/api/admin/artworks/${artworkId}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.artwork = res.data;
          this.editedStartingPrice = res.data?.startedPrice ?? res.data?.price ?? 0;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response?.data?.message || "Failed to fetch artwork detail.";
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    cancelReject() {
      this.showRejectReasonInput = false;
      this.rejectionReason = "";
    },

    handleApproval(action) {
      if (!this.artwork?.id) return;

      const endpoint =
        action === "approve"
          ? `http://localhost:8081/api/admin/artworks/approve/${this.artwork.id}`
          : `http://localhost:8081/api/admin/artworks/reject/${this.artwork.id}`;

      let payload = {};

      if (action === "approve") {
        const priceVND = Number(this.editedStartingPrice);
        if (!priceVND || priceVND <= 0) {
          window.alert("Vui lòng nhập giá khởi điểm hợp lệ (VND).");
          return;
        }
        // Gửi giá trị VND lên server
        payload = { startedPrice: priceVND };
      } else {
        // Trường hợp từ chối
        if (!this.rejectionReason.trim()) {
          window.alert("Please enter a rejection reason.");
          return;
        }
        // Gửi lý do lên server (API cần hỗ trợ nhận field reason)
        payload = { reason: this.rejectionReason };
      }

      this.actionLoading = action;
      axios
        .post(endpoint, payload, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then(() => {
          window.alert(
            action === "approve"
              ? "Artwork approved successfully."
              : "Artwork rejected successfully."
          );
          // Reset form và load lại dữ liệu
          this.showRejectReasonInput = false;
          this.rejectionReason = "";
          this.fetchArtwork();
        })
        .catch((err) => {
          console.error(err);
          window.alert(err.response?.data?.message || `Failed to ${action} the artwork.`);
        })
        .finally(() => {
          this.actionLoading = "";
        });
    },

    formatCurrency(value) {
      if (value === null || value === undefined || value === "") return "0 ₫";
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
      }).format(value);
    },
    convertStatus(status) {
      switch (status) {
        case 0:
          return "Pending Review";
        case 1:
          return "Approved";
        case 2:
          return "In Auction";
        case 3:
          return "Rejected";
        default:
          return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-warning-subtle text-warning-emphasis border-warning-subtle";
        case 1:
          return "bg-success-subtle text-success border-success-subtle";
        case 2:
          return "bg-primary-subtle text-primary border-primary-subtle";
        case 3:
          return "bg-danger-subtle text-danger border-danger-subtle";
        default:
          return "bg-light text-secondary";
      }
    },
  },
};
</script>

<style scoped>
.transition-base {
  transition: all 0.2s ease-in-out;
}
</style>
