<template>
  <div class="container mt-3">

    <!-- ========== Carousel ========== -->
    <div class="row mb-5">
      <div class="col-12">
        <div id="carouselExampleIndicators" class="carousel slide carousel-fade rounded-4 overflow-hidden"
          data-bs-ride="carousel" data-bs-interval="2000">
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"
              aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"
              aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"
              aria-label="Slide 3"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="3"
              aria-label="Slide 3"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="4"
              aria-label="Slide 3"></button>
          </div>
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="https://i.pinimg.com/736x/88/cd/21/88cd216810a2be6669f35bea9c98293c.jpg" class="d-block w-100"
                style="height: 450px;" alt="...">
            </div>
            <div class="carousel-item">
              <img src="https://i.pinimg.com/1200x/36/19/09/36190987c6cd3c29ec4f1ac202decbf1.jpg" class="d-block w-100"
                style="height: 450px;" alt="...">
            </div>
            <div class="carousel-item">
              <img src="https://i.pinimg.com/736x/c5/8d/17/c58d170aa6f5dd02eae800c604e94c69.jpg" class="d-block w-100"
                style="height: 450px;" alt="...">
            </div>
            <div class="carousel-item">
              <img src="https://i.pinimg.com/1200x/77/e5/c5/77e5c5b3543c4312a06d8279aa0add6a.jpg" class="d-block w-100"
                style="height: 450px;" alt="...">
            </div>
            <div class="carousel-item">
              <img src="https://i.pinimg.com/1200x/ca/b4/30/cab4302b07b4c54695c3affacfcf63e3.jpg" class="d-block w-100"
                style="height: 450px;" alt="...">
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
            data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
            data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
        <!-- <img src="/src/assets/img/3.png" alt="banner" class="img-fluid w-100 rounded" style="height: 300px" /> -->
      </div>
    </div>

    <div class="row mb-5">
      <!-- ========== Tiêu đề ========== -->
      <div class="col-lg-6 d-flex flex-column gap-3">
        <h2 class="fw-bold text-success mb-0">Discover Extraordinary Art</h2>
        <p class="text-muted m-0">Bid on exclusive artworks from famous and emerging artists worldwide</p>
        <p class="text-muted m-0">Join a global community of collectors and creators</p>
      </div>

      <!-- ========== Thanh search + filter + tag ========== -->
      <div class="col-lg-6 d-flex flex-column gap-3">
        <div class="row">
          <div class="col-12 mb-3">
            <div class="input-group">
              <input type="text" class="form-control border-success"
                placeholder="Search by ID, name, or type (Landscape/Portrait/Folk)"
                v-model="searchForm.searchText" @keydown.enter.prevent="searchAuctions">
              <button class="btn btn-success px-4 fw-bold" @click="searchAuctions" :disabled="isSearching">
                Search
              </button>
            </div>
          </div>
          <div class="col-8 mt-3">
            <div class=" d-flex gap-3 align-items-center">
              <input type="date" class="form-control" v-model="searchForm.dateFrom" placeholder="From date" @change="handleDateChange">
              <p class="fw-bold">_</p>
              <input type="date" class="form-control" v-model="searchForm.dateTo" placeholder="To date" @change="handleDateChange">
            </div>
          </div>
          <div class="col-4 d-flex align-items-end gap-3">
            <button class="btn btn-success w-100" @click="searchAuctions" :disabled="isSearching">
              <i class="fa-solid fa-filter"></i>
            </button>
            <button class="btn btn-secondary w-100" @click="resetSearch" :disabled="isSearching">
              <i class="fa-solid fa-rotate-left"></i>
            </button>
          </div>
        </div>


      </div>


    </div>



    <div class="row mb-4">
      <div class="col-lg-6">
        <ul class="nav nav-tabs border-0 gap-2 flex-wrap row">
          <li class="nav-item col-lg-5">
            <button class="nav-link w-100 fw-semibold auction-tab" :class="{ 'active': activeAuctionTab === 'ongoing' }"
              @click="activeAuctionTab = 'ongoing'">
              <i class="fa-solid fa-broadcast-tower me-2"></i>Ongoing
              <!-- <span class="badge ms-2"
                :class="activeAuctionTab === 'ongoing' ? 'text-bg-success text-light' : 'bg-light text-secondary'">
                {{ ongoingAuctions.length }}
              </span> -->
            </button>
          </li>
          <li class="nav-item col-lg-5">
            <button class="nav-link w-100 fw-semibold auction-tab"
              :class="{ 'active': activeAuctionTab === 'upcoming' }" @click="activeAuctionTab = 'upcoming'">
              <i class="fa-solid fa-clock me-2"></i>Upcoming
              <!-- <span class="badge ms-2"
                :class="activeAuctionTab === 'upcoming' ? 'text-bg-success text-light' : 'bg-light text-secondary'">
                {{ upcomingAuctions.length }}
              </span> -->
            </button>
          </li>
        </ul>
      </div>
      <!-- ========== Tag ========== -->
      <div class="col-lg-6">
        <div class="row py-2">
          <template v-for="tag in tags" :key="tag">
            <div class="col-4 d-flex align-items-center">
              <button type="button" class="btn w-100 fw-bold"
                :class="selectedTag === tag ? 'btn-success' : 'btn-outline-success'"
                :disabled="isSearching"
                @click="selectTag(tag)">
                <i v-if="isSearching && selectedTag === tag" class="fas fa-spinner fa-spin me-1"></i>
                {{ tag }}
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>


    <!-- Danh sách buổi đấu giá -->
    <div class="row">
      <!-- Hiển thị loading khi đang search -->
      <div v-if="isSearching" class="col-12">
        <div class="text-center py-5">
          <div class="spinner-border text-success mb-3" role="status" style="width: 3rem; height: 3rem;">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="text-muted">Searching auctions...</p>
        </div>
      </div>

      <!-- Hiển thị thông báo khi không tìm thấy kết quả -->
      <div v-else-if="isSearchMode && displayedAuctions.length === 0" class="col-12">
        <div class="text-center py-5">
          <i class="fa-solid fa-magnifying-glass fa-3x text-muted mb-3"></i>
          <h4 class="text-muted mb-2">No matching results found</h4>
          <p class="text-muted">Please try again with different search criteria</p>
          <button class="btn btn-success mt-3" @click="resetSearch">
            <i class="fa-solid fa-rotate-left me-2"></i>View all
          </button>
        </div>
      </div>

      <!-- Danh sách auction cards -->
      <template v-else v-for="auction in displayedAuctions" :key="auction.id">
        <!-- Card đấu giá -->
        <div class="col-lg-3 col-md-6 col-12 mb-4 d-flex">
          <div class="card p-0 overflow-hidden auction-card">
            <div class="p-0 position-relative">
              <img :src="auction.imageAuctionRoom" class="img-auction" alt="" loading="lazy">

              <div class="">
                <span v-if="auction.status === 1"
                  class="badge position-absolute top-0 start-0 m-3 bg-danger px-3">LIVE</span>
                <span v-else-if="auction.status === 2"
                  class="badge position-absolute top-0 start-0 m-3 bg-warning px-3 text-dark">In a few mins</span>
              </div>

              <span v-if="auction.status === 1"
                class="badge position-absolute top-0 end-0 m-3 bg-success px-3">{{ getElapsedTime(auction) }}</span>
              <!-- <span v-if="auction.status === 1" class="badge position-absolute bottom-0 end-0 m-3 bg-success">{{
                auction.viewCount }}
                bidders</span> -->
            </div>

            <!-- Nội dung card -->
            <div class="card-body d-flex flex-column gap-3">
              <div class="d-flex flex-column gap-2">
                <p class="fw-bold m-0 text-success fs-5 title-clamp"> {{ auction.roomName }} </p>
                <p class="m-0 text-muted small"> {{ auction.id }} </p>
                <div class="d-flex gap-2 align-items-center justify-content-between">
                  <span class="m-0">Category</span>
                  <span class="m-0"> {{ auction.type }} </span>
                </div>
                <p class="m-0 small description-clamp"> {{ auction.description }} </p>
              </div>
              <div class="mt-auto">
                <button
                  v-if="auction.status === 1"
                  @click="joinAuctionRoom(auction.id)"
                  class="btn btn-success w-100">
                  Join ArtAuction
                </button>

                <router-link v-else-if="auction.status === 2" :to="`/client/Regis-auct-room/${auction.id}`" class="w-100">
                  <button class="btn btn-warning w-100">Reserve Spot</button>
                  </router-link>

                <button v-else class="btn btn-secondary w-100 disabled">View Auction</button>
              </div>


            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Pagination Controls -->
    <!-- Chỉ hiển thị pagination khi không ở chế độ tìm kiếm và có nhiều hơn 1 trang -->
    <div class="row my-4" v-if="!isSearchMode && totalPages > 1">
      <div class="col-12 d-flex justify-content-center">
        <nav aria-label="Auction pagination">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 0 }">
              <a class="page-link px-4" href="#" @click.prevent="prevPage">
                <i class="fa-solid fa-angle-left"></i>
              </a>
            </li>
            <li class="page-item" v-for="page in displayedPageNumbers" :key="page"
              :class="{ active: page === currentPage + 1 }">
              <a class="page-link" href="#" @click.prevent="goToPage(page - 1)">
                {{ page }}
              </a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage >= totalPages - 1 }">
              <a class="page-link px-4" href="#" @click.prevent="nextPage">
                <i class="fa-solid fa-angle-right"></i>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>

</template>
<script>

import axios from "axios";
export default {
  data() {
    return {
      ongoingAuctions: [],
      upcomingAuctions: [],
      tags: ["Landscape", "Portrait", "Folk"],
      activeAuctionTab: 'ongoing',
      selectedTag: null,

      // Form tìm kiếm
      searchForm: {
        searchText: "", // Input duy nhất cho id, name, và type
        dateFrom: "",
        dateTo: ""
      },
      isSearching: false,
      isSearchMode: false, // Đánh dấu đang ở chế độ tìm kiếm
      dateSearchTimeout: null, // Timeout cho auto search khi thay đổi date

      // Pagination cho ongoing
      ongoingCurrentPage: 0,
      ongoingPageSize: 12,
      ongoingTotalPages: 0,
      ongoingTotalElements: 0,

      // Pagination cho upcoming
      upcomingCurrentPage: 0,
      upcomingPageSize: 12,
      upcomingTotalPages: 0,
      upcomingTotalElements: 0,

      // Kết quả tìm kiếm
      searchResults: [],

      // Auto-refresh intervals
      ongoingRefreshInterval: null,
      upcomingRefreshInterval: null,

      // Current time for elapsed time calculation
      currentTime: new Date(),
      currentTimeInterval: null
    };
  },

  computed: {
    displayedAuctions() {
      // Nếu đang ở chế độ tìm kiếm, filter kết quả theo tab đang chọn
      if (this.isSearchMode) {
        // Tab Ongoing: chỉ hiển thị status = 1 (đang diễn ra)
        if (this.activeAuctionTab === 'ongoing') {
          return this.searchResults.filter(auction => auction.status === 1);
        }
        // Tab Upcoming: chỉ hiển thị status = 2 (sắp diễn ra)
        else if (this.activeAuctionTab === 'upcoming') {
          return this.searchResults.filter(auction => auction.status === 2);
        }
        // Mặc định trả về tất cả kết quả
        return this.searchResults;
      }
      // Ngược lại hiển thị theo tab (không search)
      if (this.activeAuctionTab === 'upcoming') return this.upcomingAuctions;
      return this.ongoingAuctions;
    },
    currentPage() {
      return this.activeAuctionTab === 'upcoming' ? this.upcomingCurrentPage : this.ongoingCurrentPage;
    },
    totalPages() {
      return this.activeAuctionTab === 'upcoming' ? this.upcomingTotalPages : this.ongoingTotalPages;
    },
    totalElements() {
      return this.activeAuctionTab === 'upcoming' ? this.upcomingTotalElements : this.ongoingTotalElements;
    },
    displayedPageNumbers() {
      const pages = [];
      const maxPagesToShow = 5;
      let startPage = Math.max(1, this.currentPage + 1 - Math.floor(maxPagesToShow / 2));
      let endPage = Math.min(this.totalPages, startPage + maxPagesToShow - 1);

      if (endPage - startPage < maxPagesToShow - 1) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      return pages;
    }
  },

  watch: {
    activeAuctionTab(newTab) {
      // Nếu đang ở chế độ tìm kiếm, không cần reload vì đã filter trong computed
      if (this.isSearchMode) {
        return;
      }
      // Khi chuyển tab, reset về trang đầu nếu chưa có dữ liệu
      if (newTab === 'ongoing' && this.ongoingAuctions.length === 0) {
        this.getOngoingAuctions();
      } else if (newTab === 'upcoming' && this.upcomingAuctions.length === 0) {
        this.getUpcomingAuctions();
      }
    }
  },

  mounted() {
    // Load cả 2 loại auctions khi khởi động
    this.getOngoingAuctions();
    this.getUpcomingAuctions();

    // Bắt đầu auto-refresh mỗi 5 giây
    this.startAutoRefresh();

    // Cập nhật thời gian hiện tại mỗi giây để tính elapsed time
    this.currentTimeInterval = setInterval(() => {
      this.currentTime = new Date();
    }, 1000);
  },
  beforeUnmount() {
    // Cleanup timeout khi component bị hủy
    if (this.dateSearchTimeout) {
      clearTimeout(this.dateSearchTimeout);
    }

    // Dừng auto-refresh khi component bị hủy
    this.stopAutoRefresh();

    // Dừng current time interval
    if (this.currentTimeInterval) {
      clearInterval(this.currentTimeInterval);
    }
  },

  methods: {
    getOngoingAuctions() {
      const token = localStorage.getItem('token');
      const requestBody = {
        page: this.ongoingCurrentPage,
        size: this.ongoingPageSize
      };

      console.log('🔍 [ONGOING] Sending pagination request:', requestBody);

      axios
        .post("http://localhost:8081/api/auctionroom/ongoing", requestBody, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        .then((res) => {
          console.log('✅ [ONGOING] API Response received:', res.data);

          if (res.data && Array.isArray(res.data)) {
            const filteredRooms = res.data.filter(room => room.status !== 0);

            const getSortValue = (room) => {
              const dateField = room.createdAt || room.startTime || room.updatedAt;
              if (dateField) {
                const timestamp = new Date(dateField).getTime();
                return Number.isNaN(timestamp) ? 0 : timestamp;
              }
              return room.id || 0;
            };
            this.ongoingAuctions = filteredRooms.sort((a, b) => getSortValue(b) - getSortValue(a));

            this.ongoingTotalElements = (this.ongoingCurrentPage * this.ongoingPageSize) + res.data.length;

            if (res.data.length === this.ongoingPageSize) {
              this.ongoingTotalPages = this.ongoingCurrentPage + 2;
            } else {
              this.ongoingTotalPages = this.ongoingCurrentPage + 1;
            }

            console.log('✅ [ONGOING] Final list:', this.ongoingAuctions.length, 'items');
          } else {
            console.warn('⚠️ [ONGOING] Response is not an array:', typeof res.data);
          }
        })
        .catch((err) => {
          console.error('❌ [ONGOING] API Error:', err);
          this.$toast.error("Không thể tải danh sách đấu giá đang diễn ra!");
        });
    },

    getUpcomingAuctions() {
      const token = localStorage.getItem('token');
      const requestBody = {
        page: this.upcomingCurrentPage,
        size: this.upcomingPageSize
      };

      console.log('🔍 [UPCOMING] Sending pagination request:', requestBody);

      axios
        .post("http://localhost:8081/api/auctionroom/upcoming", requestBody, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        .then((res) => {
          console.log('✅ [UPCOMING] API Response received:', res.data);

          if (res.data && Array.isArray(res.data)) {
            const filteredRooms = res.data.filter(room => room.status !== 0);

            const getSortValue = (room) => {
              const dateField = room.createdAt || room.startTime || room.updatedAt;
              if (dateField) {
                const timestamp = new Date(dateField).getTime();
                return Number.isNaN(timestamp) ? 0 : timestamp;
              }
              return room.id || 0;
            };
            this.upcomingAuctions = filteredRooms.sort((a, b) => getSortValue(b) - getSortValue(a));

            this.upcomingTotalElements = (this.upcomingCurrentPage * this.upcomingPageSize) + res.data.length;

            if (res.data.length === this.upcomingPageSize) {
              this.upcomingTotalPages = this.upcomingCurrentPage + 2;
            } else {
              this.upcomingTotalPages = this.upcomingCurrentPage + 1;
            }

            console.log('✅ [UPCOMING] Final list:', this.upcomingAuctions.length, 'items');
          } else {
            console.warn('⚠️ [UPCOMING] Response is not an array:', typeof res.data);
          }
        })
        .catch((err) => {
          console.error('❌ [UPCOMING] API Error:', err);
          this.$toast.error("Không thể tải danh sách đấu giá sắp diễn ra!");
        });
    },

    nextPage() {
      if (this.activeAuctionTab === 'ongoing') {
        if (this.ongoingCurrentPage < this.ongoingTotalPages - 1) {
          this.ongoingCurrentPage++;
          this.getOngoingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } else {
        if (this.upcomingCurrentPage < this.upcomingTotalPages - 1) {
          this.upcomingCurrentPage++;
          this.getUpcomingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    },

    prevPage() {
      if (this.activeAuctionTab === 'ongoing') {
        if (this.ongoingCurrentPage > 0) {
          this.ongoingCurrentPage--;
          this.getOngoingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } else {
        if (this.upcomingCurrentPage > 0) {
          this.upcomingCurrentPage--;
          this.getUpcomingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    },

    goToPage(pageNumber) {
      if (this.activeAuctionTab === 'ongoing') {
        if (pageNumber >= 0 && pageNumber <= this.ongoingTotalPages - 1) {
          this.ongoingCurrentPage = pageNumber;
          this.getOngoingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } else {
        if (pageNumber >= 0 && pageNumber <= this.upcomingTotalPages - 1) {
          this.upcomingCurrentPage = pageNumber;
          this.getUpcomingAuctions();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    },

    goToFirstPage() {
      this.goToPage(0);
    },

    goToLastPage() {
      const lastPage = this.activeAuctionTab === 'ongoing'
        ? this.ongoingTotalPages - 1
        : this.upcomingTotalPages - 1;
      this.goToPage(lastPage);
    },
    goToRoom(id) {
      if (!id) return;
      this.$router.push({
        name: 'auction-room',
        params: { id }
      });
    },

    // ========== TÌM KIẾM AUCTION ROOM ==========
    searchAuctions() {
      // Kiểm tra nếu đang tìm kiếm thì không làm gì
      if (this.isSearching) {
        return;
      }

      // Lấy token từ localStorage
      const token = localStorage.getItem('token');
      if (!token) {
        this.$toast.error("Please login to search");
        return;
      }

      // Chuẩn bị dữ liệu tìm kiếm theo format API search-public
      const searchText = this.searchForm.searchText?.trim() || "";

      // Kiểm tra xem searchText có phải là tag (Landscape/Portrait/Folk) không
      const tagList = ["Landscape", "Portrait", "Folk"];
      const isTag = tagList.some(tag => tag.toLowerCase() === searchText.toLowerCase());

      // Chuẩn bị searchData theo format API: { id, name, type, dateFrom, dateTo }
      const searchData = {
        id: "",
        name: "",
        type: "",
        dateFrom: "",
        dateTo: ""
      };

      // Xử lý type: ưu tiên selectedTag, sau đó là searchText nếu là tag
      if (this.selectedTag) {
        searchData.type = this.selectedTag;
      } else if (isTag && searchText) {
        searchData.type = searchText;
      }

      // Xử lý id và name: nếu searchText không phải là tag
      // Gửi vào cả id và name để server tự tìm trong cả 2 trường
      if (searchText && !isTag) {
        // Nếu searchText có vẻ là ID (bắt đầu bằng ACR-), ưu tiên set vào id
        if (searchText.toUpperCase().startsWith('ACR-')) {
          searchData.id = searchText;
        } else {
          // Nếu không phải ID thì set vào name (có thể là tên phòng)
          searchData.name = searchText;
        }
      }

      // Thêm dateFrom và dateTo nếu có
      if (this.searchForm.dateFrom) {
        searchData.dateFrom = this.searchForm.dateFrom;
      }
      if (this.searchForm.dateTo) {
        searchData.dateTo = this.searchForm.dateTo;
      }

      // Kiểm tra xem có ít nhất một điều kiện tìm kiếm không
      const hasSearchCriteria = searchData.id || searchData.name || searchData.type || searchData.dateFrom || searchData.dateTo;
      if (!hasSearchCriteria) {
        this.$toast.info("Please enter at least one search criteria");
        return;
      }

      // Bắt đầu tìm kiếm
      this.isSearching = true;
      this.isSearchMode = true;

      console.log('🔍 [SEARCH] Sending search request:', searchData);

      // Hiển thị thông báo đang lọc theo type nếu có
      if (searchData.type) {
        console.log(`🏷️ Filtering by type: ${searchData.type}`);
      }

      axios
        .post("http://localhost:8081/api/auctionroom/search-public", searchData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        .then((res) => {
          console.log('✅ [SEARCH] API Response received:', res.data);

          // API search-public trả về array trực tiếp
          if (Array.isArray(res.data)) {
            this.searchResults = res.data.filter(room => room.status !== 0);
            if (this.searchResults.length > 0) {
              const filterMsg = searchData.type ? ` with type "${searchData.type}"` : '';
              this.$toast.success(`Found ${this.searchResults.length} auction room(s)${filterMsg}`);
            } else {
              this.$toast.info("No results found");
            }
          } else {
            this.searchResults = [];
            this.$toast.info("No results found");
          }

          console.log('✅ [SEARCH] Final results:', this.searchResults.length, 'items');
        })
        .catch((err) => {
          console.error('❌ [SEARCH] API Error:', err);
          this.searchResults = [];
          const errorMessage = err.response?.data?.message || "Search failed. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.isSearching = false;
        });
    },

    // Reset tìm kiếm và quay về danh sách ban đầu
    resetSearch() {
      // Reset form tìm kiếm
      this.searchForm = {
        searchText: "",
        dateFrom: "",
        dateTo: ""
      };
      this.selectedTag = null;
      this.isSearchMode = false;
      this.searchResults = [];

      // Reload lại danh sách ban đầu
      if (this.activeAuctionTab === 'ongoing') {
        this.ongoingCurrentPage = 0;
        this.getOngoingAuctions();
      } else {
        this.upcomingCurrentPage = 0;
        this.getUpcomingAuctions();
      }

      this.$toast.info("Search reset. Showing all auctions");
    },

    // Chọn tag để filter
    selectTag(tag) {
      if (this.selectedTag === tag) {
        // Nếu click lại tag đang chọn thì bỏ chọn
        this.selectedTag = null;
        // Reset search khi bỏ chọn tag
        this.resetSearch();
        this.$toast.info(`Filter cleared`);
      } else {
        this.selectedTag = tag;
        console.log(`🏷️ Tag selected: ${tag}`);
        // Tự động tìm kiếm khi chọn tag
        this.searchAuctions();
      }
    },

    // Xử lý khi thay đổi date - tự động search khi đủ cả 2 ngày
    handleDateChange() {
      // Chỉ tự động search nếu không đang trong quá trình search
      if (!this.isSearching) {
        // Delay nhỏ để tránh search quá nhiều lần khi người dùng đang chọn cả 2 ngày
        clearTimeout(this.dateSearchTimeout);
        this.dateSearchTimeout = setTimeout(() => {
          // Chỉ search khi đã nhập đủ cả 2 ngày
          const hasBothDates = this.searchForm.dateFrom && this.searchForm.dateTo;

          // Kiểm tra xem có điều kiện tìm kiếm không (cả 2 ngày hoặc các điều kiện khác)
          const hasSearchCriteria = hasBothDates ||
                                    this.searchForm.searchText ||
                                    this.selectedTag;

          if (hasSearchCriteria) {
            this.searchAuctions();
          }
        }, 300);
      }
    },

    // Bắt đầu auto-refresh mỗi 5 giây
    startAutoRefresh() {
      console.log('🔄 Starting auto-refresh every 5 seconds');

      // Refresh ongoing auctions mỗi 5 giây
      this.ongoingRefreshInterval = setInterval(() => {
        console.log('🔄 Auto-refreshing ongoing auctions...');
        this.getOngoingAuctions();
      }, 5000);

      // Refresh upcoming auctions mỗi 5 giây
      this.upcomingRefreshInterval = setInterval(() => {
        console.log('🔄 Auto-refreshing upcoming auctions...');
        this.getUpcomingAuctions();
      }, 5000);
    },

    // Dừng auto-refresh
    stopAutoRefresh() {
      console.log('⏹️ Stopping auto-refresh');

      if (this.ongoingRefreshInterval) {
        clearInterval(this.ongoingRefreshInterval);
        this.ongoingRefreshInterval = null;
      }

      if (this.upcomingRefreshInterval) {
        clearInterval(this.upcomingRefreshInterval);
        this.upcomingRefreshInterval = null;
      }
    },

    // Join auction room với force reload
    joinAuctionRoom(auctionId) {
      console.log('🚀 Navigating to auction room with reload:', auctionId);
      // Sử dụng window.location.href thay vì router.push để force reload trang
      window.location.href = `/client/auction-room/${auctionId}`;
    },

    // Tính thời gian đã trôi qua từ khi phòng bắt đầu (chỉ cho status = 1)
    getElapsedTime(auction) {
      if (!auction || auction.status !== 1) {
        return '0\'';
      }

      // Thử các trường có thể chứa thời gian bắt đầu (theo thứ tự ưu tiên)
      let timeField = null;
      let usedFieldName = '';

      if (auction.startTime) {
        timeField = auction.startTime;
        usedFieldName = 'startTime';
      } else if (auction.liveStartTime) {
        timeField = auction.liveStartTime;
        usedFieldName = 'liveStartTime';
      } else if (auction.actualStartTime) {
        timeField = auction.actualStartTime;
        usedFieldName = 'actualStartTime';
      } else if (auction.startedAt) {
        timeField = auction.startedAt;
        usedFieldName = 'startedAt';
      } else if (auction.updatedAt) {
        timeField = auction.updatedAt;
        usedFieldName = 'updatedAt';
      } else if (auction.createdAt) {
        timeField = auction.createdAt;
        usedFieldName = 'createdAt';
      }

      if (!timeField) {
        // Chỉ log một lần để debug
        if (!this._noTimeFieldLogged) {
          this._noTimeFieldLogged = true;
          console.error('❌ [ELAPSED TIME] No time field available. Fields:', Object.keys(auction));
        }
        return '0\'';
      }

      // Log một lần để thông báo field nào đang được dùng
      if (!this._timeFieldInUse) {
        this._timeFieldInUse = usedFieldName;
        console.info(`ℹ️ [ELAPSED TIME] Using "${usedFieldName}" field for live timer calculation`);
        if (usedFieldName !== 'startTime') {
          console.warn(`⚠️ Backend không gửi field "startTime". Đang dùng "${usedFieldName}" - có thể không chính xác 100%`);
        }
      }

      try {
        const startTime = new Date(timeField);
        if (isNaN(startTime.getTime())) {
          console.error('❌ [ELAPSED TIME] Invalid date format:', timeField);
          return '0\'';
        }

        // Sử dụng currentTime để component tự động cập nhật mỗi giây
        const elapsedMinutes = Math.floor((this.currentTime - startTime) / 1000 / 60); // Tính số phút

        if (elapsedMinutes < 0) {
          return '0:00';
        }

        // Tính giờ và phút
        const hours = Math.floor(elapsedMinutes / 60);
        const minutes = elapsedMinutes % 60;

        // Format phút với 2 chữ số (VD: 2 → "02", 15 → "15")
        const paddedMinutes = minutes.toString().padStart(2, '0');

        // Hiển thị theo format H:MM (VD: "3:02", "1:30", "0:45")
        return `${hours}:${paddedMinutes}`;
      } catch (error) {
        console.error('❌ Error calculating elapsed time:', error);
        return '0\'';
      }
    }
  }
};

</script>
<style scoped>
.auction-tab {
  border: 0 !important;
  outline: none;
  color: #6c757d;
  background: transparent;
  padding: 0.75rem 1rem;
  transition: color 0.2s ease,
    box-shadow 0.25s ease,
    transform 0.25s ease;
}

.auction-tab:not(.active):hover {
  color: #0f584f;
}

.auction-tab.active {
  color: #0f584f;
  background: transparent;
  position: relative;
}

.auction-tab.active::after {
  content: '';
  display: block;
  height: 4px;
  background: #0f584f;
  border-radius: 999px;
  margin-top: 0.4rem;
}

.auction-tab:focus-visible {
  outline: none;
  box-shadow: none;
}

/* Pagination Styling */
.pagination {
  --bs-pagination-color: #0f584f;
  --bs-pagination-border-color: #0f584f;
  --bs-pagination-hover-color: #fff;
  --bs-pagination-hover-bg: #0f584f;
  --bs-pagination-hover-border-color: #0f584f;
  --bs-pagination-focus-color: #0f584f;
  --bs-pagination-focus-bg: #e9ecef;
  --bs-pagination-active-color: #fff !important;
  --bs-pagination-active-bg: #0f584f !important;
  --bs-pagination-active-border-color: #0f584f !important;
  --bs-pagination-disabled-color: #6c757d;
  --bs-pagination-disabled-bg: #fff;
  --bs-pagination-disabled-border-color: #dee2e6;
}

.page-link {
  font-weight: 500;
  transition: all 0.2s ease;
}

.page-link:hover {
  color: #fff !important;
}

.page-item.active .page-link {
  background-color: #0f584f !important;
  border-color: #0f584f !important;
  color: #fff !important;
  z-index: 3;
}

.page-link:focus,
.page-item.active .page-link:focus {
  box-shadow: none !important;
  outline: none !important;
}

.page-item:not(:first-child) .page-link {
  margin-left: -1px;
}

/* Disabled state */
.page-item.disabled .page-link {
  background-color: #f8f9fa !important;
  border-color: #dee2e6 !important;
  color: #adb5bd !important;
  cursor: not-allowed !important;
  pointer-events: none;
}

.page-item.disabled .page-link:hover {
  background-color: #f8f9fa !important;
  color: #adb5bd !important;
}
</style>

