<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-1">Dashboard</h4>
      <p class="text-body-secondary mb-0">Overview of the painting auction system</p>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-sm-6 col-xl-4">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase card-subtitle text-secondary fw-bold mb-1">
                  Total Users
                </h6>
                <h3 class="fw-bolder mb-0 text-dark fs-3">
                  {{ statistics?.totalUsers?.total }}
                </h3>
              </div>
              <div
                class="bg-secondary bg-opacity-10 text-primary rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-users fs-4"></i>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <small class="text-secondary fw-medium small">Total registered users</small>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-info">
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase card-subtitle text-secondary fw-bold mb-1">Artwork</h6>
                <h3 class="fw-bolder mb-0 text-dark fs-3">
                  {{ statistics?.totalArtworks?.total }}
                </h3>
              </div>
              <div
                class="bg-info bg-opacity-10 text-info rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-image fs-4"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium small">Total number of works</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase card-subtitle text-secondary fw-bold mb-1">
                  Auction Rooms
                </h6>
                <h3 class="fw-bolder mb-0 text-dark fs-3">
                  {{ statistics?.totalAuctionRooms }}
                </h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-hammer fs-4"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium small">Active auction rooms</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase card-subtitle text-secondary fw-bold mb-1">Bidding</h6>
                <h3 class="fw-bolder mb-0 text-dark fs-3">
                  {{ statistics?.totalBids?.total }}
                </h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-chart-line fs-4"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium small">Total bids placed</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-4">
        <div
          class="card border-0 shadow-sm border-start border-4 border-secondary h-100 card-hover bg-gradient-primary"
        >
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase fw-bold x-small mb-1 ls-1 opacity-75">Revenue</h6>
                <h3 class="fw-bolder mb-0 fs-3">
                  {{ formatCurrency(statistics?.revenue?.total) }}
                </h3>
              </div>
              <div
                class="bg-white bg-opacity-25 text-white rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-dollar-sign fs-4"></i>
              </div>
            </div>
            <small class="fw-medium opacity-75 small">Total platform revenue</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-dark">
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-uppercase text-secondary fw-bold x-small mb-1 ls-1">
                  Active Users
                </h6>
                <h3 class="fw-bolder mb-0 text-dark fs-3">
                  {{ statistics?.activeUsers || 0 }}
                </h3>
              </div>
              <div
                class="bg-dark bg-opacity-10 text-dark rounded-3 d-flex align-items-center justify-content-center p-2"
                style="width: 42px; height: 42px"
              >
                <i class="fa-solid fa-user-check fs-4"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium small">Currently active</small>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-xl-6">
        <div class="card border-0 rounded-4 h-100 overflow-hidden">
          <div
            class="card-header bg-primary bg-gradient text-white py-3 border-0 d-flex align-items-center justify-content-between"
          >
            <div class="d-flex align-items-center gap-2">
              <div
                class="bg-white bg-opacity-25 rounded-circle p-2 d-flex justify-content-center align-items-center"
                style="width: 32px; height: 32px"
              >
                <i class="fa-solid fa-gavel"></i>
              </div>
              <h5 class="fw-bold mb-0">Nearby Auction Rooms</h5>
            </div>
            <span class="badge bg-white text-primary rounded-pill"
              >{{ topAuctionRooms ? topAuctionRooms.length : 0 }} Room</span
            >
          </div>

          <div class="card-body p-0">
            <div class="table-responsive text-nowrap custom-scrollbar" style="max-height: 450px">
              <table class="table table-hover align-middle text-nowrap mb-0 w-100">
                <thead
                  class="bg-light sticky-top shadow-sm border-bottom border-light-subtle"
                  style="z-index: 5"
                >
                  <tr>
                    <th
                      scope="col"
                      class="ps-4 py-3 fw-bold text-secondary text-uppercase x-small border-0"
                    >
                      Room Info
                    </th>
                    <th
                      scope="col"
                      class="py-3 fw-bold text-secondary text-uppercase x-small border-0"
                    >
                      Featured Item
                    </th>
                    <th
                      scope="col"
                      class="py-3 fw-bold text-secondary text-uppercase x-small text-center border-0"
                    >
                      Status
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-if="isLoading">
                    <td colspan="3" class="text-center py-5 text-muted border-0">Loading...</td>
                  </tr>
                  <tr v-else-if="!topAuctionRooms || topAuctionRooms.length === 0">
                    <td colspan="3" class="text-center py-5 text-muted border-0">
                      No rooms found.
                    </td>
                  </tr>

                  <template v-for="(room, index) in topAuctionRooms" :key="room.id">
                    <tr
                      class="cursor-pointer transition-bg border-bottom border-light-subtle"
                      :class="{ 'bg-primary-subtle': activeRoomId === room.id }"
                      data-bs-toggle="collapse"
                      :data-bs-target="'#room-' + room.id"
                      aria-expanded="false"
                      @click="toggleRoom(room.id)"
                    >
                      <td class="ps-4 py-3 border-0">
                        <div class="d-flex align-items-center gap-3">
                          <i
                            class="fa-solid fa-chevron-right text-muted transition-icon"
                            :class="{ 'rotate-90 text-primary': activeRoomId === room.id }"
                            style="font-size: 0.75rem"
                          ></i>
                          <div>
                            <span class="d-block fw-bold text-dark">{{ room.roomName }}</span>
                            <span
                              class="badge bg-light text-secondary border border-light-subtle rounded-pill mt-1"
                              style="font-size: 0.65rem"
                              >ID: #{{ room.id }}</span
                            >
                          </div>
                        </div>
                      </td>
                      <td class="py-3 border-0">
                        <div class="d-flex align-items-center">
                          <div class="position-relative me-3">
                            <img
                              :src="room.sessions?.[0]?.avtArtwork"
                              class="rounded-3 shadow-sm border border-light-subtle object-fit-cover"
                              style="width: 48px; height: 48px"
                            />
                            <!-- <span
                              class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger border border-white"
                              v-if="room.sessions && room.sessions.length > 1"
                              >+{{ room.sessions.length - 1 }}</span
                            > -->
                          </div>
                          <div class="d-flex flex-column" style="max-width: 150px">
                            <span
                              class="fw-bold text-dark text-truncate d-block"
                              style="font-size: 0.9rem"
                              >{{ room.sessions?.[0]?.artworkTitle || "Unknown" }}</span
                            >
                            <small class="text-muted" style="font-size: 0.75rem"
                              ><i class="fa-solid fa-layer-group me-1"></i
                              >{{ room.sessions ? room.sessions.length : 0 }} items</small
                            >
                          </div>
                        </div>
                      </td>
                      <td class="text-center py-3 border-0">
                        <span
                          class="badge rounded-pill px-3 py-2 fw-medium shadow-sm"
                          :class="getStatusClass(room.status)"
                          >{{ convertStatus(room.status) }}</span
                        >
                      </td>
                    </tr>

                    <tr>
                      <td colspan="3" class="p-0 border-0">
                        <div class="collapse bg-body-tertiary" :id="'room-' + room.id">
                          <div class="p-3 ps-5 border-start border-2 border-secondary-subtle ms-0">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                              <h6 class="fw-bold text-primary small text-uppercase mb-0">
                                <i class="fa-solid fa-list-ul me-2"></i>Auction Session List
                              </h6>
                              <!-- <button
                                class="btn btn-sm btn-link text-decoration-none p-0 text-secondary"
                                style="font-size: 0.8rem"
                              >
                                View Room <i class="fa-solid fa-arrow-right ms-1"></i>
                              </button> -->
                            </div>

                            <div class="card border-0 shadow-sm rounded-3 overflow-hidden">
                              <table class="table table-sm table-striped mb-0 align-middle">
                                <thead class="table-light text-secondary small">
                                  <tr>
                                    <th class="ps-3 py-2 border-0">Item</th>
                                    <th class="text-end py-2 pe-3 border-0">Current Bid</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="(session, sIndex) in room.sessions" :key="session.id">
                                    <td class="ps-3 py-2 border-0">
                                      <div class="d-flex align-items-center">
                                        <span
                                          class="badge bg-white text-secondary border border-light-subtle me-2 shadow-sm"
                                          style="width: 24px"
                                          >{{ sIndex + 1 }}</span
                                        >
                                        <img
                                          :src="session.avtArtwork"
                                          class="rounded-circle border border-light-subtle me-2"
                                          style="width: 28px; height: 28px; object-fit: cover"
                                          @error="
                                            $event.target.src = '/src/assets/img/default-art.png'
                                          "
                                        />
                                        <span
                                          class="fw-medium text-dark small text-truncate"
                                          style="max-width: 180px"
                                          >{{ session.artworkTitle }}</span
                                        >
                                      </div>
                                    </td>
                                    <td class="text-end py-2 pe-3 border-0">
                                      <span class="fw-bold text-success small">{{
                                        formatCurrency(session.currentPrice)
                                      }}</span>
                                    </td>
                                  </tr>
                                  <tr v-if="!room.sessions || room.sessions.length === 0">
                                    <td
                                      colspan="2"
                                      class="text-center text-muted small py-3 border-0"
                                    >
                                      No items.
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-6 animate-fade-in">
        <div class="card border-0 rounded-4 h-100 overflow-hidden">
          <div
            class="card-header bg-primary bg-gradient text-white py-3 border-0 d-flex align-items-center justify-content-between"
          >
            <div class="d-flex align-items-center gap-2">
              <div
                class="bg-white bg-opacity-25 rounded-circle p-2 d-flex justify-content-center align-items-center"
                style="width: 32px; height: 32px"
              >
                <i class="fa-solid fa-user-plus"></i>
              </div>
              <h5 class="fw-bold mb-0">New Users</h5>
            </div>
            <span class="badge bg-white text-primary rounded-pill"
              >{{ newUsers ? newUsers.length : 0 }} Recent</span
            >
          </div>

          <div class="card-body p-0">
            <div class="table-responsive text-nowrap custom-scrollbar" style="max-height: 450px">
              <table class="table table-hover align-middle text-nowrap mb-0 w-100">
                <thead
                  class="bg-light sticky-top shadow-sm border-bottom border-light-subtle"
                  style="z-index: 5"
                >
                  <tr>
                    <th
                      scope="col"
                      class="ps-4 py-3 fw-bold text-secondary text-uppercase x-small border-0"
                    >
                      User Profile
                    </th>
                    <th
                      scope="col"
                      class="py-3 fw-bold text-secondary text-uppercase x-small border-0"
                    >
                      Joined Date
                    </th>
                    <th
                      scope="col"
                      class="py-3 fw-bold text-secondary text-uppercase x-small text-center border-0"
                    >
                      Status
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-if="isLoading">
                    <td colspan="3" class="text-center py-5 text-muted border-0">
                      <div
                        class="spinner-border spinner-border-sm text-primary mb-2"
                        role="status"
                      ></div>
                      <p class="mb-0 small">Loading users...</p>
                    </td>
                  </tr>

                  <tr v-else-if="!newUsers || newUsers.length === 0">
                    <td colspan="3" class="text-center py-5 text-muted border-0">
                      <i class="fa-regular fa-user fs-1 mb-2 opacity-25"></i>
                      <p class="mb-0">No new users registered.</p>
                    </td>
                  </tr>

                  <tr
                    v-for="user in newUsers"
                    :key="user.id"
                    class="transition-bg border-bottom border-light-subtle"
                  >
                    <td class="ps-4 py-3 border-0">
                      <div class="d-flex align-items-center gap-3">
                        <div class="position-relative">
                          <img
                            :src="user.avt"
                            class="rounded-circle border border-light-subtle shadow-sm object-fit-cover"
                            style="width: 40px; height: 40px"
                          />
                        </div>
                        <div class="d-flex flex-column">
                          <span class="fw-bold text-dark" style="font-size: 0.9rem">{{
                            user.username
                          }}</span>
                          <small class="text-muted" style="font-size: 0.75rem">{{
                            user.email
                          }}</small>
                        </div>
                      </div>
                    </td>

                    <td class="py-3 border-0">
                      <div class="d-flex align-items-center text-secondary">
                        <i class="fa-regular fa-calendar me-2 small opacity-50"></i>
                        <span class="fw-medium small">{{ formatDate(user.createdAt) }}</span>
                      </div>
                    </td>

                    <td class="text-center py-3 border-0">
                      <span
                        class="badge rounded-pill px-3 py-2 fw-medium shadow-sm"
                        :class="getStatusClassUser(user.status)"
                      >
                        {{ convertStatusUser(user.status) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-12">
      <div class="card border-0 shadow rounded-4 h-100 overflow-hidden">
        <div
          class="card-header bg-primary bg-gradient text-white py-3 border-0 d-flex align-items-center justify-content-between"
        >
          <div class="d-flex align-items-center gap-2">
            <div
              class="bg-white bg-opacity-25 rounded-circle p-2 d-flex justify-content-center align-items-center"
              style="width: 32px; height: 32px"
            >
              <i class="fa-solid fa-trophy"></i>
            </div>
            <h5 class="fw-bold mb-0">The Most Expensive Works</h5>
          </div>
          <span class="badge bg-white text-primary rounded-pill"
            >Top {{ topArtworks ? topArtworks.length : 0 }}</span
          >
        </div>

        <div class="card-body p-0">
          <div class="table-responsive text-nowrap custom-scrollbar" style="max-height: 450px">
            <table class="table table-hover align-middle text-nowrap mb-0 w-100">
              <thead
                class="bg-light sticky-top shadow-sm border-bottom border-light-subtle"
                style="z-index: 5"
              >
                <tr>
                  <th
                    scope="col"
                    class="ps-4 py-3 fw-bold text-secondary text-uppercase x-small border-0"
                  >
                    Artwork Info
                  </th>
                  <th
                    scope="col"
                    class="py-3 fw-bold text-secondary text-uppercase x-small border-0"
                  >
                    Type
                  </th>
                  <th
                    scope="col"
                    class="py-3 fw-bold text-secondary text-uppercase x-small border-0"
                  >
                    Winner
                  </th>
                  <th
                    scope="col"
                    class="py-3 fw-bold text-secondary text-uppercase x-small text-end pe-4 border-0"
                  >
                    Highest Price
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr v-if="isLoading">
                  <td colspan="4" class="text-center py-5 text-muted border-0">
                    <div
                      class="spinner-border spinner-border-sm text-primary mb-2"
                      role="status"
                    ></div>
                    <p class="mb-0 small">Loading rankings...</p>
                  </td>
                </tr>

                <tr v-else-if="!topArtworks || topArtworks.length === 0">
                  <td colspan="4" class="text-center py-5 text-muted border-0">
                    <i class="fa-solid fa-award fs-1 mb-2 opacity-25"></i>
                    <p class="mb-0">No data available.</p>
                  </td>
                </tr>

                <tr
                  v-for="(art, index) in topArtworks"
                  :key="art.id"
                  class="transition-bg border-bottom border-light-subtle"
                >
                  <td class="ps-4 py-3 border-0">
                    <div class="d-flex align-items-center gap-3">
                      <div class="fw-bold text-secondary opacity-50" style="width: 20px">
                        {{ index + 1 }}
                      </div>

                      <img
                        :src="art.artworkImageUrl"
                        class="rounded-3 shadow-sm border border-light-subtle object-fit-cover"
                        style="width: 48px; height: 48px"
                        alt="art"
                        loading="lazy"
                      />
                      <div class="d-flex flex-column">
                        <span class="fw-bold text-dark text-truncate" style="max-width: 200px">{{
                          art.artworkTitle
                        }}</span>
                        <span
                          class="badge bg-light text-secondary border border-light-subtle rounded-pill mt-1"
                          style="width: fit-content; font-size: 0.65rem"
                        >
                          ID: #{{ art.sessionId }}
                        </span>
                      </div>
                    </div>
                  </td>

                  <td class="py-3 border-0">
                    <span
                      class="badge bg-info-subtle text-info-emphasis border border-info-subtle rounded-pill fw-medium px-3"
                    >
                      {{ art.paintingGenre }}
                    </span>
                  </td>

                  <td class="py-3 border-0">
                    <div class="d-flex align-items-center text-dark">
                      <div
                        class="bg-secondary-subtle rounded-circle p-1 d-flex justify-content-center align-items-center me-2"
                        style="width: 24px; height: 24px"
                      >
                        <i class="fa-regular fa-user small text-secondary"></i>
                      </div>
                      <span class="fw-medium">{{ art.winnerName }}</span>
                    </div>
                  </td>

                  <td class="text-end py-3 pe-4 border-0">
                    <span class="fw-bold text-success fs-6">
                      {{ formatCurrency(art.totalAmount) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminLive",
  data() {
    return {
      statistics: {},
      isLoading: false,
      topAuctionRooms: [],
      newUsers: [],
      topArtworks: [],
    };
  },

  mounted() {
    this.loadInvoiceStatistical();
    this.loadTopAuction();
    this.loadUserData();
    this.loadArtworkData();
  },

  methods: {
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

    //  card thống kê
    loadInvoiceStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/dashboard/thong-ke`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          if (res.data && res.data.data) {
            this.statistics = res.data.data;
          } else {
            this.statistics = {};
          }
          console.log("Kết quả tìm kiếm:", this.statistics);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.statistics = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    //
    loadTopAuction() {
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/dashboard/top-auction-rooms`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          console.log("API Response Gốc:", res.data);

          if (res.data && Array.isArray(res.data.data)) {
            this.topAuctionRooms = res.data.data;
          } else {
            // Fallback nếu API trả về mảng trực tiếp
            this.topAuctionRooms = res.data;
          }

          console.log("Mảng phòng đấu giá (Final):", this.topAuctionRooms);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.topAuctionRooms = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    convertStatus(status) {
      switch (status) {
        case 0:
          return "Finished";
        case 1:
          return "Live";
        case 2:
          return "Upcoming";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 1:
          return "bg-danger-subtle text-danger border-danger-subtle";
        case 2:
          return "bg-warning-subtle text-warning-emphasis border-warning-subtle";
        case 0:
          return "bg-secondary-subtle text-secondary border-secondary-subtle";
      }
    },

    // new users
    loadUserData() {
      axios
        .get(`http://localhost:8081/api/admin/dashboard/top-new-users`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.newUsers = res.data;
          console.log(this.newUsers);
        })
        .catch((err) => {
          console.error(err);
        });
    },

    convertStatusUser(status) {
      switch (status) {
        case 1:
          return "Active";
        case 0:
          return "Inactive";
        default:
          return "Unknown";
      }
    },
    getStatusClassUser(status) {
      switch (status) {
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 0:
          return "bg-secondary-subtle border-secondary-subtle text-secondary";
        // default:
        //   return "bg-secondary-subtle border-secondary-subtle text-secondary";
      }
    },

    // Top 10 Session có giá cao nhất
    loadArtworkData() {
      axios
        .get("http://localhost:8081/api/admin/dashboard/top-sessions", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.topArtworks = res.data;
          console.log(this.topArtworks);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>
