<template>
  <div class="container py-4">
    <div
      class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center mb-4 gap-3"
    >
      <div>
        <div class="d-flex align-items-center gap-3 mb-1">
          <h4 class="fw-bold text-primary mb-0">{{ roomDetail.roomName }}</h4>
          <span
            class="badge bg-secondary bg-opacity-10 text-primary border border-secondary border-opacity-10"
          >
            ID: {{ roomDetail.id }}
          </span>
          <span
            class="badge bg-danger text-white border border-danger px-3 rounded-pill animate-pulse"
            :class="getStatusClass(roomDetail.status)"
          >
            <i class="fa-solid fa-circle me-1" style="font-size: 0.5rem"></i>
            {{ convertStatus(roomDetail.status) }}
          </span>
        </div>
        <p class="text-body-secondary mb-0">
          <i class="fa-regular fa-user-circle me-1"></i>Admin phụ trách:
          <span class="fw-medium text-dark">{{ roomDetail.admin?.fullName }}</span>
        </p>
      </div>

      <div class="d-flex gap-2">
        <div>
          <router-link
            :to="`/admin/edit-auction-room/${roomDetail.id}`"
            v-if="roomDetail.status === 0"
            class="btn btn-outline-secondary fw-medium shadow-sm px-3"
          >
            <i class="fa-solid fa-pen-to-square me-2"></i>Edit
          </router-link>

          <button
            v-else
            class="btn btn-outline-secondary fw-medium shadow-sm px-3 opacity-50"
            style="cursor: not-allowed"
          >
            <i class="fa-solid fa-pen-to-square me-2"></i>Edit
          </button>
        </div>
        <div>
          <router-link v-if="roomDetail.status === 1" class="btn btn-danger fw-bold shadow-sm px-4">
            <i class="fa-solid fa-video me-2"></i>Enter Live Room
          </router-link>

          <button
            v-else
            class="btn btn-danger fw-bold shadow-sm px-4 opacity-50"
            style="cursor: not-allowed"
          >
            <i class="fa-solid fa-video me-2"></i>Enter Live Room
          </button>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-3 mb-4">
      <div class="card-body p-4">
        <div class="row g-4">
          <div class="col-12 col-lg-8 border-end-lg">
            <h6 class="fw-bold text-secondary small mb-3">
              <i class="fa-solid fa-circle-info me-2"></i>General information
            </h6>
            <p class="text-muted mb-4">{{ roomDetail.description }}</p>

            <div class="d-flex gap-4">
              <div class="d-flex align-items-center">
                <div
                  class="bg-secondary bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center me-3"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-solid fa-calendar-days"></i>
                </div>
                <div>
                  <small class="text-secondary d-block x-small fw-bold">BEGIN</small>
                  <span class="fw-medium">{{ formatDate(roomDetail.startedAt) }}</span>
                </div>
              </div>
              <div class="d-flex align-items-center">
                <div
                  class="bg-warning bg-opacity-10 text-warning rounded-circle d-flex align-items-center justify-content-center me-3"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-solid fa-flag-checkered"></i>
                </div>
                <div>
                  <small class="text-secondary d-block x-small fw-bold">END (EXPECTED)</small>
                  <span class="fw-medium">{{ formatDate(roomDetail.estimatedEndTime) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-4 ps-lg-4">
            <h6 class="fw-bold text-secondary small mb-3">
              <i class="fa-solid fa-chart-pie me-2"></i>Real-time statistics
            </h6>
            <div class="row g-3">
              <div class="col-6">
                <div class="p-3 bg-light rounded-3 text-center border">
                  <i class="fa-solid fa-users text-primary fs-4 mb-2"></i>
                  <h4 class="fw-bold mb-0">{{ roomDetail.totalMembers }}</h4>
                  <small class="text-muted">Participants</small>
                </div>
              </div>
              <div class="col-6">
                <div
                  class="p-3 bg-danger bg-opacity-10 rounded-3 text-center border border-danger border-opacity-10"
                >
                  <i class="fa-solid fa-eye text-danger fs-4 mb-2"></i>
                  <h4 class="fw-bold text-danger mb-0">{{ roomDetail.viewCount }}</h4>
                  <small class="text-danger opacity-75">Viewer</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex align-items-center justify-content-between mb-3">
      <h5 class="fw-bold text-dark mb-0">
        <i class="fa-solid fa-images me-2 text-info"></i>List of works
      </h5>
      <!-- <div class="input-group" style="width: 250px">
        <span class="input-group-text bg-white border-end-0"
          ><i class="fa-solid fa-magnifying-glass text-muted"></i
        ></span>
        <input
          type="text"
          class="form-control border-start-0 ps-0 shadow-none"
          placeholder="Tìm tên tranh..."
        />
      </div> -->
    </div>

    <div class="row g-3">
      <div class="col-12 col-md-6 col-lg-4 col-xl-3" v-for="art in artworks" :key="art.artworkId">
        <div
          class="card h-100 border-0 shadow-sm rounded-3 overflow-hidden position-relative group-hover-effect"
        >
          <div
            class="position-absolute top-0 end-0 m-2 badge rounded-pill px-3 py-2 z-1 shadow-sm"
            :class="getStatusBadgeClass(art.status).class"
          >
            {{ getStatusBadgeClass(art.status).text }}
          </div>

          <div class="ratio ratio-4x3 bg-light">
            <img :src="art.avtArtwork" class="object-fit-cover w-100 h-100" :alt="art.name" />
          </div>

          <div class="card-body p-3 d-flex flex-column">
            <div class="mb-2">
              <small class="text-muted" style="font-size: 0.75rem">ID: {{ art.artworkId }}</small>
              <h6 class="fw-bold text-dark text-truncate mb-1" :title="art.name">
                {{ art.artworkName }}
              </h6>
              <small class="text-primary"
                ><i class="fa-solid fa-paintbrush me-1"></i>{{ art.author }}</small
              >
            </div>

            <div class="mt-auto pt-3 border-top">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="text-secondary small">Starting price:</span>
                <span class="fw-medium text-secondary">{{
                  formatCurrency(art.startingPrice)
                }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-dark small fw-bold">Current price:</span>
                <span
                  class="fw-bold fs-6"
                  :class="art.status === 'bidding' ? 'text-danger' : 'text-success'"
                >
                  {{ formatCurrency(art.currentPrice) }}
                </span>
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
      roomId: null,
      isLoading: false,
      roomDetail: {},
      artworks: [],
    };
  },

  mounted() {
    // Lấy ID từ URL (giả sử route là /admin/auction-detail/:id)
    this.roomId = this.$route.params.id;

    //Gọi API nếu có id
    if (this.roomId) {
      this.loadRoomDetail(this.roomId);
    }
  },
  methods: {
    loadRoomDetail() {
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/auction-rooms/${this.roomId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.roomDetail = res.data;
          this.artworks = res.data.artworks;
          console.log("Data loaded:", this.roomDetail);
        })
        .catch((err) => {
          console.error(err);
        });
    },

    formatCurrency(value) {
      if (value === null || value === undefined || value === "") {
        return "0 ₫";
      }
      // Trả về định dạng: 100.000 ₫
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
      }).format(value);
    },

    getStatusBadgeClass(status) {
      switch (status) {
        case 1:
          return { class: "bg-danger text-white animate-pulse", text: "In process" };
        case 0:
          return { class: "bg-success text-white", text: "Completed" };
        default:
          return { class: "bg-secondary bg-opacity-75 text-white", text: "Coming soon" };
      }
    },
    convertStatus(status) {
      switch (status) {
        case 2:
          return "Finished";
        case 1:
          return "In progress";
        case 0:
          return "Coming soon";
        default:
          return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-warning-subtle text-warning-emphasis border-warning-subtle"; // Coming soon
        case 1:
          return "bg-danger-subtle text-danger border-danger-subtle"; // Live
        case 2:
          return "bg-secondary-subtle text-secondary border-secondary-subtle"; // Ended
        default:
          return "bg-light text-dark border";
      }
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
  },
};
</script>

<style scoped></style>
