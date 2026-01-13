<template>
  <div class="row mb-3">
    <div class="col-lg-12">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-lg-12 col-md-6 col-sm-12 d-flex align-items-center justify-content-between">
              <h4 class="text-success fw-bold m-0">Artwork Management</h4>
              <div class="d-flex align-items-center justify-content-between gap-3">
                <div class="d-flex align-items-center gap-3 mb-lg-0 mb-3">
                  <input type="date" class="form-control" v-model="searchForm.dateFrom" @change="handleDateChange">
                  <p class="fw-bold">_</p>
                  <input type="date" class="form-control" v-model="searchForm.dateTo" @change="handleDateChange">
                </div>
                <button class="btn btn-outline-secondary" @click="resetSearch" :disabled="loading" title="Reset search">
                  <i class="fa-solid fa-rotate-left"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading data...</p>
    </div>
    <!-- <div v-else-if="error" class="text-danger">{{ error }}</div> -->
    <div v-else class="row mb-5">
      <!-- Empty state -->
      <div v-if="invoices.length === 0" class="col-12">
        <div class="card">
          <div class="card-body text-center py-5">
            <i class="fa-regular fa-inbox fa-3x text-muted mb-3"></i>
            <h5 class="text-muted mb-2">No data</h5>
            <p class="text-muted m-0">You don't have any invoices yet.</p>
          </div>
        </div>
      </div>

      <!-- List data -->
      <div v-else v-for="item in invoices" :key="item.id" class="col-12 col-lg-6 col-md-6 d-flex">
        <div class="card w-100 overflow-hidden mb-4">
          <div class="card-body d-flex flex-column">
            <div class="row gap-2">
              <div class="col-12 d-flex align-items-center justify-content-between">
                <p class="fs-6  m-0">Id Invoice</p>
                <p class="m-0 fw-bold">{{ item.id }}</p>
              </div>
              <div class="col-12 d-flex align-items-center justify-content-between">
                <p class="fs-6  m-0">Id Room</p>
                <p class="m-0 fw-bold">{{ item.auctionRoomId }}</p>
              </div>
            </div>
            <hr>
            <div class="row ">
              <div class="col-12 d-flex align-items-center justify-content-between mb-2">
                <p class="m-0">Payment Time</p>
                <p class="m-0">{{ item.createdAt }}</p>
              </div>
              <div class="col-6">
                <img :src="item.artworkAvt || item.artworkImageUrl" alt=""
                  class="img-thumbnail img-invoice w-100 object-fit-cover" style="height: 150px;">
              </div>
              <div class="col-6 d-flex flex-column justify-content-between gap-2">
                <div class="d-flex flex-column gap-2">
                  <p class="m-0 fw-bold fs-5">{{ item.artworkTitle }}</p>
                  <p class=" m-0 small text-truncate">{{ item.artworkId }}</p>
                </div>
                <div class="">
                  <div v-if="item.paymentStatus === 1" class="d-flex gap-2">
                    <div class="alert alert-success w-100 fw-bold text-center py-2 m-0" role="alert">
                      <!-- <i class="fa-solid fa-circle-check me-2"></i>  -->
                      Paid
                    </div>
                  </div>
                  <div v-else class="d-flex gap-2">
                    <div class="alert alert-danger w-100 fw-bold text-center py-2 m-0" role="alert">
                      <!-- <i class="fa-solid fa-circle-xmark me-2"></i>  -->
                      Unpaid
                    </div>
                  </div>
                </div>


              </div>
            </div>
            <hr>
            <div class="row mt-auto">
              <div class="col-12 d-flex align-items-center justify-content-between mb-3">
                <p class="m-0 fw-bold text-success">Total </p>
                <p class="m-0 fw-bold">{{ formatCurrency(item.totalAmount) }}</p>
              </div>
              <div class="col-12">
                <div v-if="item.paymentStatus === 1" class="d-flex gap-2">
                  <router-link :to="`/client/payment/${item.auctionRoomId}/${item.id}`" class="w-100">
                    <button class="btn btn-outline-success w-100">View Details</button>
                  </router-link>
                </div>
                <div v-else class="d-flex gap-2">
                  <router-link :to="`/client/payment/${item.auctionRoomId}/${item.id}`" class="w-100">
                    <button class="btn btn-outline-danger w-100">View Details</button>
                  </router-link>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- Pagination Controls -->
  <div class="row my-4" v-if="invoices.length > 0 && totalPages > 1">
    <div class="col-12 d-flex justify-content-center">
      <nav aria-label="Invoice pagination">
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
</template>

<script>
import axios from "axios";

export default {
  name: "ClientInvoices",
  data() {
    return {
      invoices: [],
      loading: false,
      error: null,
      currentPage: 0,
      totalPages: 1,
      pageSize: 6,
      isSearchMode: false,
      searchForm: {
        dateFrom: "",
        dateTo: ""
      },
      dateSearchTimeout: null
    };
  },

  computed: {
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

  methods: {
    formatCurrency(value) {
      const num = Number(value || 0);
      return num.toLocaleString('vi-VN', {
        style: 'currency',
        currency: 'VND',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      });
    },

    fetchInvoices() {
      // Nếu đang ở chế độ search thì không gọi API này
      if (this.isSearchMode) {
        return;
      }

      this.loading = true;
      axios
        .post("http://localhost:8081/api/invoice/my-invoice",
          { page: this.currentPage, size: this.pageSize },
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem("token")
            }
          }
        )
        .then((res) => {
          this.invoices = res.data || [];
          // Ước tính totalPages
          if (this.invoices.length < this.pageSize) {
            this.totalPages = this.currentPage + 1;
          } else {
            this.totalPages = this.currentPage + 2;
          }
          console.log("data loaded invoice", this.invoices);
        })
        .catch((err) => {
          this.error = err.message;
          console.error("Fetch invoices error:", err);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    searchInvoices() {
      // Chỉ search khi đã nhập đủ cả 2 ngày
      if (!this.searchForm.dateFrom || !this.searchForm.dateTo) {
        return;
      }

      this.loading = true;
      this.isSearchMode = true;

      const searchData = {
        dateFrom: this.searchForm.dateFrom,
        dateTo: this.searchForm.dateTo
      };

      axios
        .post("http://localhost:8081/api/invoice/search",
          searchData,
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem("token")
            }
          }
        )
        .then((res) => {
          // API trả về format { success, message, data }
          if (res.data && res.data.success && Array.isArray(res.data.data)) {
            this.invoices = res.data.data;
            this.totalPages = 1; // Search không có pagination
            if (res.data.message) {
              this.$toast.success(res.data.message);
            }
          } else if (Array.isArray(res.data)) {
            // Fallback: nếu response là array trực tiếp
            this.invoices = res.data;
            this.totalPages = 1;
          } else {
            this.invoices = [];
            this.$toast.info("No results found");
          }
          console.log("search results invoice", this.invoices);
        })
        .catch((err) => {
          this.error = err.message;
          console.error("Search invoices error:", err);
          const errorMessage = err.response?.data?.message || "Search failed. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    handleDateChange() {
      // Chỉ search khi đã nhập đủ cả 2 ngày
      if (!this.loading && this.searchForm.dateFrom && this.searchForm.dateTo) {
        clearTimeout(this.dateSearchTimeout);
        this.dateSearchTimeout = setTimeout(() => {
          this.searchInvoices();
        }, 300);
      }
    },

    resetSearch() {
      this.searchForm = {
        dateFrom: "",
        dateTo: ""
      };
      this.isSearchMode = false;
      this.currentPage = 0;
      this.fetchInvoices();
      this.$toast.info("Search reset. Showing all invoices");
    },

    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
        this.fetchInvoices();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++;
        this.fetchInvoices();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },

    goToPage(pageNumber) {
      if (pageNumber >= 0 && pageNumber < this.totalPages && pageNumber !== this.currentPage) {
        this.currentPage = pageNumber;
        this.fetchInvoices();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
  },

  mounted() {
    this.fetchInvoices();
  },
  beforeUnmount() {
    // Cleanup timeout khi component bị hủy
    if (this.dateSearchTimeout) {
      clearTimeout(this.dateSearchTimeout);
    }
  },
};
</script>



<style scoped>
.pagination .page-link {
  color: var(--bs-success);
  border-color: var(--bs-success);
}

.pagination .page-item.active .page-link {
  background-color: var(--bs-success) !important;
  border-color: var(--bs-success) !important;
  color: white !important;
}

.pagination .page-link:hover {
  background-color: var(--bs-success);
  border-color: var(--bs-success);
  color: white;
}

.pagination .page-link:focus {
  box-shadow: none !important;
  outline: none !important;
}

.pagination .page-item.disabled .page-link {
  color: #6c757d;
  border-color: #dee2e6;
}
</style>
