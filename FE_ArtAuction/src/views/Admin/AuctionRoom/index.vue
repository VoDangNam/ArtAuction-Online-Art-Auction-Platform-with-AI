<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4">
      <div class="mb-3 mb-md-0">
        <h4 class="fw-bold text-primary mb-1">Auction Room Management</h4>
        <p class="text-body-secondary mb-0">Overview and control of all auction sessions</p>
      </div>
      <div>
        <router-link to="/admin/add-auction-room" class="btn btn-primary shadow-sm px-4 fw-bold">
          <i class="fa-solid fa-plus me-2"></i>Create Room
        </router-link>
      </div>
    </div>
    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-md-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Total Rooms</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalRooms }}</h3>
              </div>
              <div
                class="bg-secondary-subtle text-primary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-layer-group fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total auction rooms</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-danger">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Live Now</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.runningRooms }}</h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-tower-broadcast fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">
              <i class="fa-solid fa-circle fa-2xs me-1 fa-fade"></i>Currently active
            </small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Upcoming</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.upcomingRooms }}</h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-regular fa-calendar-check fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Scheduled for today</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Finished</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.completedRooms }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-flag-checkered fs-5"></i>
              </div>
            </div>
            <small class="text-success fw-medium">Completed sessions</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 mb-4 overflow-hidden shadow-none">
      <div class="card-body p-2">
        <div class="row g-2 align-items-center">
          <div class="col-12 col-md-8 col-lg-6">
            <div class="input-group bg-light rounded-pill px-2 border-0">
              <span class="input-group-text bg-transparent border-0 text-secondary">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control bg-transparent border-0 shadow-none"
                placeholder="Search for auction room..."
                @input="handleSearch"
              />
            </div>
          </div>
          <div class="col-auto ms-auto pe-2">
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
                      Auction room filter
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
                        <i class="fa-solid fa-signal me-1"></i> Room status
                      </label>

                      <div class="bg-light rounded-3 p-3 border">
                        <div class="form-check mb-2">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            id="stLive"
                            :value="1"
                            v-model="filter.statuses"
                          />
                          <label class="form-check-label text-danger fw-bold" for="stLive">
                            <i
                              class="fa-solid fa-circle fa-beat-fade me-1"
                              style="font-size: 0.5rem"
                            ></i>
                            Live
                          </label>
                        </div>

                        <div class="form-check mb-2">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            id="stComing"
                            :value="0"
                            v-model="filter.statuses"
                          />
                          <label class="form-check-label text-primary fw-medium" for="stComing">
                            <i class="fa-regular fa-clock me-1"></i> Coming Soon
                          </label>
                        </div>

                        <div class="form-check mb-2">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            id="stFinished"
                            :value="2"
                            v-model="filter.statuses"
                          />
                          <label class="form-check-label text-success fw-medium" for="stFinished">
                            <i class="fa-solid fa-flag-checkered me-1"></i> Finished
                          </label>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-regular fa-calendar-days me-1"></i> Time of event
                      </label>

                      <div class="mb-3">
                        <label class="form-label x-small text-secondary fw-bold"
                          >Start Time (From - To)</label
                        >
                        <div class="input-group input-group-sm">
                          <input
                            type="date"
                            class="form-control shadow-none"
                            v-model="filter.startTimeFrom"
                          />
                          <span class="input-group-text bg-light border-0 text-secondary">-</span>
                          <input
                            type="date"
                            class="form-control shadow-none"
                            v-model="filter.startTimeTo"
                          />
                        </div>
                      </div>

                      <!-- <div>
                        <label class="form-label x-small text-secondary fw-bold"
                          >End Time (From - To)</label
                        >
                        <div class="input-group input-group-sm">
                          <input
                            type="date"
                            class="form-control shadow-none"
                            v-model="filter.endTimeFrom"
                          />
                          <span class="input-group-text bg-light border-0 text-secondary">-</span>
                          <input
                            type="date"
                            class="form-control shadow-none"
                            v-model="filter.endTimeTo"
                          />
                        </div>
                      </div> -->
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-2">
                      <div>
                        <label class="form-label x-small text-secondary fw-bold"
                          >Number of participants</label
                        >
                        <div class="btn-group w-100" role="group">
                          <input
                            type="radio"
                            class="btn-check"
                            name="parti"
                            id="partiAll"
                            value="all"
                            v-model="filter.participantsRange"
                          />
                          <label class="btn btn-outline-secondary btn-sm" for="partiAll">All</label>

                          <input
                            type="radio"
                            class="btn-check"
                            name="parti"
                            id="partiLow"
                            value="<10"
                            v-model="filter.participantsRange"
                          />
                          <label class="btn btn-outline-secondary btn-sm" for="partiLow"
                            >&lt; 10</label
                          >

                          <input
                            type="radio"
                            class="btn-check"
                            name="parti"
                            id="partiMid"
                            value="10-50"
                            v-model="filter.participantsRange"
                          />
                          <label class="btn btn-outline-secondary btn-sm" for="partiMid"
                            >10-50</label
                          >

                          <input
                            type="radio"
                            class="btn-check"
                            name="parti"
                            id="partiHigh"
                            value=">50"
                            v-model="filter.participantsRange"
                          />
                          <label class="btn btn-outline-secondary btn-sm" for="partiHigh"
                            >&gt; 50</label
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="offcanvas-footer border-top p-3 bg-white mt-5">
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
                        @click="applyFilter"
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
      </div>
    </div>

    <div
      class="row g-4 overflow-y-auto hide-scrollbar pe-2 animate-fade-in"
      style="max-height: 80vh"
    >
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">Loading rooms...</p>
      </div>

      <div v-else class="col-12" v-for="room in auctionRooms" :key="room.id">
        <router-link
          :to="`/admin/testlivestream/${room.id}`"
          class="card border-0 shadow-sm h-100 text-decoration-none position-relative"
          :class="getBorderClass(room.status)"
          style="cursor: pointer; overflow: visible"
        >
          <div class="dropdown position-absolute top-0 end-0 mt-3 me-3" style="z-index: 100">
            <button
              class="btn btn-light btn-sm rounded-circle shadow-sm d-flex align-items-center justify-content-center"
              type="button"
              data-bs-toggle="dropdown"
              data-bs-display="static"
              aria-expanded="false"
              style="width: 32px; height: 32px; background-color: rgba(255, 255, 255, 0.9)"
              @click.stop="toggleDropdown(room.id)"
            >
              <i class="fa-solid fa-ellipsis text-secondary"></i>
            </button>

            <ul
              class="dropdown-menu dropdown-menu-end border-0 shadow-lg"
              :class="{ show: activeDropdownId === room.id }"
              style="z-index: 1000"
            >
              <li v-if="room.status === 'live' || room.status === 'streaming'">
                <a
                  class="dropdown-item py-2 fw-bold text-danger"
                  href="#"
                  @click.prevent.stop="goToLive(room.id)"
                >
                  <i class="fa-solid fa-video me-2 animate-pulse"></i>Watch Live
                </a>
              </li>

              <li>
                <router-link
                  :to="`/admin/auction-detail/${room.id}`"
                  class="dropdown-item py-2"
                  @click.stop
                >
                  <i class="fa-regular fa-eye me-2 text-primary"></i>See Details
                </router-link>
              </li>
              <li>
                <router-link
                  v-if="room.status === 0"
                  :to="`/admin/edit-auction-room/${room.id}`"
                  class="dropdown-item py-2"
                  @click.stop
                >
                  <i class="fa-solid fa-pen-to-square me-2"></i>Edit
                </router-link>

                <span
                  v-else
                  class="dropdown-item py-2 text-muted opacity-50"
                  style="cursor: not-allowed"
                  title="Only upcoming room edits can be made."
                  @click.stop
                >
                  <i class="fa-solid fa-pen-to-square me-2"></i>Edit
                </span>
              </li>

              <li><hr class="dropdown-divider" /></li>

              <li>
                <a
                  class="dropdown-item py-2 text-secondary"
                  href="#"
                  @click.prevent.stop="deleteRoom(room.id)"
                >
                  <i class="fa-regular fa-trash-can me-2"></i>Delete
                </a>
              </li>
            </ul>
          </div>

          <div class="card-body p-4">
            <div class="row align-items-center gy-4">
              <div class="col-12 col-lg-5 border-end-lg pe-lg-4">
                <div class="d-flex align-items-center gap-3">
                  <div class="position-relative">
                    <img
                      :src="room.imageAuctionRoom"
                      alt="Art"
                      class="rounded-4 shadow-sm object-fit-cover border"
                      style="width: 100px; height: 100px"
                    />
                    <span
                      class="position-absolute bottom-0 start-50 translate-middle-x badge bg-dark bg-opacity-75 rounded-pill border border-white border-opacity-25"
                      style="font-size: 0.6rem; bottom: -8px !important"
                    >
                      ID: {{ room.id }}
                    </span>
                  </div>

                  <div class="overflow-hidden flex-grow-1">
                    <div class="d-flex flex-column gap-1">
                      <h5
                        class="fw-bold text-dark mb-0 text-truncate"
                        style="max-width: 100%"
                        :title="room.roomName"
                      >
                        {{ room.roomName }}
                      </h5>

                      <div class="d-flex align-items-center gap-2 flex-wrap">
                        <span
                          class="badge bg-secondary bg-opacity-10 text-secondary border border-secondary border-opacity-10 rounded-pill px-2"
                        >
                          <i class="fa-solid fa-tag me-1 text-opacity-75"></i>{{ room.type }}
                        </span>

                        <span
                          class="badge rounded-pill px-2 py-1 fw-semibold"
                          :class="getStatusClass(room.status)"
                        >
                          {{ convertStatus(room.status) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-lg-7 ps-lg-4">
                <div class="bg-light bg-opacity-50 rounded-4 p-3 border border-light-subtle">
                  <div class="row g-3 align-items-center text-center text-md-start">
                    <div class="col-4 col-md-4 border-end border-secondary border-opacity-10">
                      <span
                        class="text-uppercase text-secondary fw-bold"
                        style="font-size: 0.65rem; letter-spacing: 0.5px"
                      >
                        Start Time
                      </span>
                      <div
                        class="d-flex align-items-center justify-content-center justify-content-md-start gap-2 mt-1"
                      >
                        <i class="fa-regular fa-clock text-primary opacity-75"></i>
                        <span class="text-dark fw-medium small lh-1">
                          {{ formatDate(room.startedAt) }}
                        </span>
                      </div>
                    </div>

                    <div class="col-4 col-md-4 border-end border-secondary border-opacity-10">
                      <span
                        class="text-uppercase text-secondary fw-bold"
                        style="font-size: 0.65rem; letter-spacing: 0.5px"
                      >
                        Participants
                      </span>
                      <div
                        class="d-flex align-items-center justify-content-center justify-content-md-start gap-2 mt-1"
                      >
                        <div class="position-relative">
                          <i class="fa-solid fa-users text-info fs-5"></i>
                          <span
                            class="position-absolute top-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle"
                            style="width: 8px; height: 8px"
                          ></span>
                        </div>
                        <span class="fw-bold text-dark fs-5">{{ room.totalMembers }}</span>
                      </div>
                    </div>

                    <div class="col-4 col-md-4">
                      <span
                        class="text-uppercase text-secondary fw-bold"
                        style="font-size: 0.65rem; letter-spacing: 0.5px"
                      >
                        Estimated End Time
                      </span>
                      <div
                        class="d-flex align-items-center justify-content-center justify-content-md-start gap-2 mt-1"
                      >
                        <i class="fa-solid fa-hourglass-half text-danger opacity-75"></i>
                        <span class="text-dark fw-medium small lh-1">
                          {{ formatDate(room.estimatedEndTime) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <div v-if="!isLoading && auctionRooms.length === 0" class="text-center py-5">
        <p class="text-muted">No auction rooms found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuctionRoomManagement",
  data() {
    return {
      auctionRooms: [],
      isLoading: false,
      search: "",
      statistics: "",
      activeDropdownId: null,
      searchTimeout: null,

      // Dữ liệu cho bộ lọc
      filter: {
        statuses: [], // Mảng chứa các value [0, 1, 2]
        startTimeFrom: null,
        startTimeTo: null,
        endTimeFrom: null,
        endTimeTo: null,
        participantsRange: "all",
      },
    };
  },
  mounted() {
    this.loadAuctionData();
    this.loadAuctionStatistical();
    document.addEventListener("click", this.closeDropdown);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
  },

  methods: {
    toggleDropdown(id) {
      if (this.activeDropdownId === id) {
        this.activeDropdownId = null;
      } else {
        this.activeDropdownId = id;
      }
    },
    closeDropdown() {
      this.activeDropdownId = null;
    },
    handleSearch() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      this.searchTimeout = setTimeout(() => {
        this.performSearchApi();
      }, 500);
    },
    performSearchApi() {
      if (!this.search.trim()) {
        this.loadAuctionData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/auction-rooms/tim-kiem?q=${this.search}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.auctionRooms = res.data;
        })
        .catch((err) => {
          console.error("Search error:", err);
          this.auctionRooms = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    applyFilter() {
      this.isLoading = true;

      const payload = {
        statuses: this.filter.statuses.length > 0 ? this.filter.statuses : null,

        startTimeFrom: this.filter.startTimeFrom ? `${this.filter.startTimeFrom}T00:00:00` : null,
        startTimeTo: this.filter.startTimeTo ? `${this.filter.startTimeTo}T23:59:59` : null,

        endTimeFrom: this.filter.endTimeFrom ? `${this.filter.endTimeFrom}T00:00:00` : null,
        endTimeTo: this.filter.endTimeTo ? `${this.filter.endTimeTo}T23:59:59` : null,

        participantsRange:
          this.filter.participantsRange === "all" ? null : this.filter.participantsRange,
      };

      axios
        .post("http://localhost:8081/api/admin/auction-rooms/loc-phong-dau-gia", payload, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.auctionRooms = res.data;
          // Đóng search nếu đang search để tránh nhầm lẫn
          this.search = "";
        })
        .catch((err) => {
          console.error("Filter Error:", err);
          alert("Failed to filter auction rooms.");
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    resetFilter() {
      // Reset về giá trị mặc định
      this.filter = {
        statuses: [],
        startTimeFrom: null,
        startTimeTo: null,
        endTimeFrom: null,
        endTimeTo: null,
        participantsRange: "all",
      };

      // Gọi lại load data gốc
      this.loadAuctionData();
    },

    // --- CÁC HÀM API KHÁC (GIỮ NGUYÊN) ---
    loadAuctionData() {
      this.isLoading = true;
      axios
        .get("http://localhost:8081/api/admin/auction-rooms/lay-du-lieu", {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.auctionRooms = res.data;
        })
        .catch((err) => {
          console.error("Error loading rooms:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    loadAuctionStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/auction-rooms/thong-ke`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          this.statistics = res.data;
        })
        .catch((err) => {
          console.error("Lỗi thống kê:", err);
        });
    },
    deleteRoom(roomId) {
      if (!confirm(`Are you sure you want to delete this room?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/auction-rooms/xoa/${roomId}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadAuctionData();
        })
        .catch((err) => {
          const message = err.response?.data?.message || "An error occurred while deleting!";
          alert(message);
        });
    },

    // --- HELPER FUNCTIONS ---
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
    convertStatus(status) {
      switch (status) {
        case 2:
          return "Finished";
        case 1:
          return "Live";
        case 0:
          return "Coming soon";
        default:
          return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-warning-subtle text-warning-emphasis border-warning-subtle";
        case 1:
          return "bg-danger-subtle text-danger border-danger-subtle";
        case 2:
          return "bg-secondary-subtle text-secondary border-secondary-subtle";
        default:
          return "";
      }
    },
    getBorderClass(status) {
      switch (status) {
        case 2:
          return "border-start border-4 border-warning";
        case 1:
          return "border-start border-4 border-danger";
        case 0:
          return "border-start border-4 border-secondary";
        default:
          return "";
      }
    },
  },
};
</script>
<style></style>
