<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-1">Artwork Management</h4>
      <p class="text-body-secondary mb-0">Manage all artwork in the system</p>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-sm-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Total work</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalArtworks }}</h3>
              </div>
              <div
                class="bg-secondary-subtle text-primary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-images fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total list of works</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Approved</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.approvedArtworks }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
            <small class="text-success fw-medium">Successfully approved</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Pending</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.pendingArtworks }}</h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-clock fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Awaiting approval</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-danger">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Refused</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.rejectedArtworks }}</h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-ban fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">Policy violation</small>
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
                placeholder="Search artwork..."
                @input="handleSearch"
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
                      Artwork filter
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
                      <div class="row g-2">
                        <div class="col-6">
                          <label class="form-label x-small fw-bold text-secondary">Genre</label>
                          <select
                            class="form-select shadow-none bg-light border-0"
                            v-model="filterForm.paintingGenre"
                          >
                            <option selected value="">All</option>
                            <option value="Abstract">Abstract</option>
                            <option value="Portrait">Portrait</option>
                            <option value="Landscape">Landscape</option>
                            <option value="Modern">Modern</option>
                            <option value="Traditional">Traditional</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-solid fa-tag me-1"></i> Price range (VND)
                      </label>

                      <div class="d-flex flex-wrap gap-2 mb-2">
                        <button
                          class="btn btn-sm btn-light border text-secondary active-pill"
                          style="font-size: 0.75rem"
                          :class="{
                            'active-pill':
                              filterForm.priceMaxUSD === 200 && !filterForm.priceMinUSD,
                          }"
                          @click="setPriceRangeUSD(null, 200)"
                        >
                          &lt; $200
                        </button>
                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          style="font-size: 0.75rem"
                          :class="{
                            'active-pill':
                              filterForm.priceMinUSD === 200 && filterForm.priceMaxUSD === 800,
                          }"
                          @click="setPriceRangeUSD(200, 800)"
                        >
                          $200 - $800
                        </button>
                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          style="font-size: 0.75rem"
                          :class="{
                            'active-pill':
                              filterForm.priceMinUSD === 800 && filterForm.priceMaxUSD === 4000,
                          }"
                          @click="setPriceRangeUSD(800, 4000)"
                        >
                          $800 - $4k
                        </button>
                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          style="font-size: 0.75rem"
                          :class="{
                            'active-pill':
                              filterForm.priceMinUSD === 4000 && !filterForm.priceMaxUSD,
                          }"
                          @click="setPriceRangeUSD(4000, null)"
                        >
                          &gt; $4k
                        </button>
                      </div>

                      <div class="input-group">
                        <input
                          type="number"
                          v-model="filterForm.priceMinUSD"
                          class="form-control shadow-none"
                          placeholder="Min ($)"
                        />
                        <span
                          class="input-group-text bg-white border-start-0 border-end-0 text-secondary"
                          >-</span
                        >
                        <input
                          type="number"
                          class="form-control shadow-none"
                          placeholder="Max ($)"
                          v-model="filterForm.priceMaxUSD"
                        />
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        Approval status
                      </label>
                      <div class="bg-light rounded-3 p-3 border">
                        <div class="form-check mb-2">
                          <input
                            :value="null"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="artStatus"
                            id="stNotAll"
                          />
                          <label class="form-check-label text-secondary" for="stNotApproved">
                            <i class="fa-regular fa-clock me-1"></i> All
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            :value="0"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="artStatus"
                            id="stNotApproved"
                          />
                          <label class="form-check-label text-secondary" for="stNotApproved">
                            <i class="fa-regular fa-clock me-1"></i> Not Approved
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            :value="1"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="artStatus"
                            id="stApproved"
                            checked
                          />
                          <label class="form-check-label text-success fw-medium" for="stApproved">
                            <i class="fa-solid fa-check me-1"></i> Approved
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            :value="2"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="artStatus"
                            id="stAuction"
                          />
                          <label class="form-check-label text-primary fw-medium" for="stAuction">
                            <i class="fa-solid fa-gavel me-1"></i> Up for Auction
                          </label>
                        </div>
                        <div class="form-check">
                          <input
                            :value="3"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="artStatus"
                            id="stRefused"
                          />
                          <label class="form-check-label text-danger" for="stRefused">
                            <i class="fa-solid fa-ban me-1"></i> Refused
                          </label>
                        </div>
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
                <th scope="col" class="ps-4 py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Artwork Info
                </th>
                <th scope="col" class="py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Genre
                </th>
                <th scope="col" class="py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Author
                </th>
                <th scope="col" class="py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Year
                </th>
                <th scope="col" class="py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Size
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold x-small text-dark text-uppercase border-0 text-end pe-4"
                >
                  Start Price
                </th>
                <th scope="col" class="py-3 fw-bold x-small text-dark text-uppercase border-0">
                  Created At
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold x-small text-dark text-uppercase border-0 text-start"
                >
                  Status
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold x-small text-dark text-uppercase border-0 text-center"
                >
                  Action
                </th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="isLoading">
                <td colspan="9" class="text-center py-5 text-muted border-0">
                  <div
                    class="spinner-border spinner-border-sm text-primary mb-2"
                    role="status"
                  ></div>
                  <p class="mb-0 small">Loading artworks...</p>
                </td>
              </tr>

              <tr
                v-for="item in sortedArtworks"
                :key="item.id"
                class="transition-bg border-bottom border-light-subtle"
              >
                <td class="ps-4 py-3 border-0">
                  <div class="d-flex align-items-center gap-3">
                    <div class="position-relative">
                      <img
                        :src="item.avtArtwork"
                        class="rounded-3 border border-light-subtle shadow-sm object-fit-cover bg-light"
                        style="width: 48px; height: 48px"
                        loading="lazy"
                      />
                    </div>
                    <div class="d-flex flex-column">
                      <span
                        class="fw-bold text-dark text-truncate"
                        style="max-width: 200px"
                        :title="item.title"
                      >
                        {{ item.title }}
                      </span>
                      <span
                        class="badge bg-light text-secondary border border-light-subtle rounded-pill mt-1"
                        style="width: fit-content; font-size: 0.65rem"
                      >
                        ID: #{{ item.id }}
                      </span>
                    </div>
                  </div>
                </td>

                <td class="py-3 border-0">
                  <span
                    class="badge bg-info-subtle text-info-emphasis border border-info-subtle rounded-pill fw-normal px-2"
                  >
                    {{ item.paintingGenre }}
                  </span>
                </td>

                <td class="py-3 border-0 text-dark fw-medium">{{ item.author }}</td>

                <td class="py-3 border-0 text-secondary">{{ item.yearOfCreation }}</td>

                <td class="py-3 border-0 text-secondary">{{ item.size }}</td>

                <td class="py-3 border-0 text-end pe-4">
                  <span class="fw-bold text-success">{{ formatCurrency(item.startedPrice) }}</span>
                </td>

                <td class="py-3 border-0 small text-muted">{{ formatDate(item.createdAt) }}</td>

                <td class="py-3 border-0 text-start">
                  <span
                    class="badge rounded-pill border fw-medium px-2 py-1"
                    :class="getStatusClass(item.status)"
                  >
                    <i class="fa-solid fa-circle fa-2xs me-1 opacity-75"></i>
                    {{ convertStatus(item.status) }}
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
                      <li>
                        <RouterLink
                          :to="`/admin/artwork-detail/${item.id}`"
                          class="dropdown-item py-2"
                        >
                          <i class="fa-regular fa-eye me-2 text-primary"></i>See details
                        </RouterLink>
                      </li>
                      <li>
                        <router-link
                          v-if="item.status === 1"
                          :to="`/admin/edit-artwork/${item.id}`"
                          class="dropdown-item py-2"
                        >
                          <i class="fa-regular fa-pen-to-square me-2"></i>Edit
                        </router-link>
                        <span
                          v-else
                          class="dropdown-item py-2 text-muted opacity-50"
                          style="cursor: not-allowed"
                          title="Only upcoming room edits can be made."
                          @click.stop
                          ><i class="fa-regular fa-pen-to-square me-2"></i>Edit
                        </span>
                      </li>
                      <li><hr class="dropdown-divider my-1" /></li>
                      <li>
                        <button
                          class="dropdown-item py-2 text-danger"
                          @click="handleDelete(item.id, item.title)"
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

        <!-- Pagination UI -->
        <div class="d-flex justify-content-between align-items-center mt-3" v-if="totalPages > 0">
          <div class="text-secondary small">
            Showing {{ artworks.length }} of {{ totalElements }} artworks (Page {{ currentPage + 1 }}/{{ totalPages }})
          </div>
          <nav>
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 0 }">
                <a class="page-link" href="#" @click.prevent="prevPage">Previous</a>
              </li>
              
              <li 
                class="page-item" 
                v-for="page in visiblePages" 
                :key="page"
                :class="{ active: currentPage === page }"
              >
                <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page + 1 }}</a>
              </li>
              
              <li class="page-item" :class="{ disabled: currentPage >= totalPages - 1 }">
                <a class="page-link" href="#" @click.prevent="nextPage">Next</a>
              </li>
            </ul>
          </nav>
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
      artworks: [],
      search: "",
      isLoading: false,
      statistics: [],

      filterForm: {
        title: "",
        author: "",
        id: "",
        yearOfCreation: null,

        paintingGenre: "",
        material: "",

        width: null,
        height: null,

        priceRange: "",
        priceMinUSD: null,
        priceMaxUSD: null,

        status: null,
      },

      // Pagination state
      currentPage: 0,
      pageSize: 20,
      totalPages: 0,
      totalElements: 0,
    };
  },
  mounted() {
    this.loadArtworkData();
    this.loadArtworkStatistical();
  },
  computed: {
    // Không cần reverse nữa vì backend sắp xếp rồi
    sortedArtworks() {
      return this.artworks;
    },
    
    // Hiển thị tối đa 5 trang xung quanh trang hiện tại
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      let startPage = Math.max(0, this.currentPage - Math.floor(maxVisible / 2));
      let endPage = Math.min(this.totalPages - 1, startPage + maxVisible - 1);
      
      // Điều chỉnh startPage nếu endPage chạm biên
      if (endPage - startPage + 1 < maxVisible) {
        startPage = Math.max(0, endPage - maxVisible + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      return pages;
    },
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
        case 0:
          return "Not approved";
        case 1:
          return "Approved";
        case 2:
          return "Up for auction";
        case 3:
          return "Refused";
      }
    },

    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-secondary-subtle border-secondary-subtle text-secondary";
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 2:
          return "bg-warning-subtle border-warning-subtle text-warning-emphasis";
        case 3:
          return "bg-danger-subtle border-danger-subtle text-danger";
      }
    },

    loadArtworkData() {
      axios
        .get("http://localhost:8081/api/admin/artworks/lay-du-lieu-tac-pham", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.artworks = res.data;
          console.log(this.artworks);
        })
        .catch((err) => {
          console.error(err);
        });
    },

    // Tối ưu: Load với pagination
    loadArtworkData() {
      this.isLoading = true;
      axios
        .get(
          `http://localhost:8081/api/admin/artworks/lay-du-lieu-tac-pham-phan-trang?page=${this.currentPage}&size=${this.pageSize}`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        )
        .then((res) => {
          this.artworks = res.data.content;
          this.totalPages = res.data.totalPages;
          this.totalElements = res.data.totalElements;
          console.log(`Loaded page ${this.currentPage + 1}/${this.totalPages}, total: ${this.totalElements}`);
        })
        .catch((err) => {
          console.error(err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Chuyển trang
    goToPage(page) {
      if (page < 0 || page >= this.totalPages) return;
      this.currentPage = page;
      this.loadArtworkData();
    },

    nextPage() {
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++;
        this.loadArtworkData();
      }
    },

    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
        this.loadArtworkData();
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
      // Nếu ô tìm kiếm trống thì load lại toàn bộ danh sách
      if (!this.search.trim()) {
        this.loadArtworkData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/artworks/tim-kiem-tac-pham?q=${this.search}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.artworks = res.data;
          console.log("Kết quả tìm kiếm:", this.artworks);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.artworks = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Xóa
    handleDelete(artworkId) {
      if (!confirm(`Are you sure you want to delete this artwork?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/artworks/xoa-tac-pham/${artworkId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadArtworkData();
        })
        .catch((err) => {
          console.error("Lỗi khi xóa:", err);
          const message = err.response?.data?.message || "Có lỗi xảy ra khi xóa!";
          alert(message);
        });
    },

    //  card thống kê
    loadArtworkStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/artworks/thong-ke-tac-pham`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.statistics = res.data;
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

    handleFilter() {
      this.isLoading = true;

      // Debug kiểm tra
      console.log(`Lọc giá (USD): ${this.filterForm.priceMinUSD} - ${this.filterForm.priceMaxUSD}`);

      const payload = {
        title: this.filterForm.title || null,
        author: this.filterForm.author || null,
        yearOfCreation: this.filterForm.yearOfCreation || null,
        paintingGenre: this.filterForm.paintingGenre || null,
        material: this.filterForm.material || null,

        priceRange: null,
        priceMin: this.filterForm.priceMinUSD,
        priceMax: this.filterForm.priceMaxUSD,

        status: this.filterForm.status,
      };

      axios
        .post("http://localhost:8081/api/admin/artworks/loc-tac-pham", payload, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          this.artworks = res.data || [];
        })
        .catch((err) => {
          console.error("Lỗi bộ lọc:", err);
          this.artworks = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    resetFilter() {
      this.filterForm = {
        title: "",
        author: "",
        id: "",
        yearOfCreation: null,
        paintingGenre: "",
        material: "",
        width: null,
        height: null,
        priceRange: "",
        priceMinUSD: null,
        priceMaxUSD: null,
        status: null,
      };
      // Load lại dữ liệu gốc
      this.loadArtworkData();
    },

    setPriceRangeUSD(min, max) {
      // Hàm này nhận vào USD và gán vào form
      this.filterForm.priceMinUSD = min;
      this.filterForm.priceMaxUSD = max;
    },
  },
};
</script>
