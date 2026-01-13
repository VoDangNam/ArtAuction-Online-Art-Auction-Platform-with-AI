<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="text-primary fw-bold mb-1">Manage Invoices</h4>
      <p class="text-body-secondary mb-0">Track and manage all invoices in the system</p>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-sm-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Total Bill</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.totalInvoices }}</h3>
              </div>
              <div
                class="bg-secondary-subtle text-primary rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-file-lines fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total invoices generated</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Paid</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.paidInvoices }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
            <small class="text-success fw-medium">Successfully paid</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Waiting</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.pendingInvoices }}</h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-clock fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Pending payment</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-danger">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Overdue</h6>
                <h3 class="card-text fw-bold mb-0 text-dark">{{ statistics.failedInvoices }}</h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-ban fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">Action required</small>
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
                placeholder="Search invoices, buyers..."
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
                              :value="null"
                              v-model="filterForm.paymentStatus"
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusAll"
                            />
                            <label class="form-check-label text-success" for="statusActive"
                              >● All
                            </label>
                          </div>
                          <div class="form-check mb-2">
                            <input
                              :value="1"
                              v-model="filterForm.paymentStatus"
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusPaid"
                            />
                            <label class="form-check-label text-success" for="statusActive"
                              >● Paid
                            </label>
                          </div>
                          <div class="form-check mb-2">
                            <input
                              :value="0"
                              v-model="filterForm.paymentStatus"
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusPending"
                            />
                            <label class="form-check-label text-warning" for="statusLocked"
                              >● Pending
                            </label>
                          </div>
                          <div class="form-check mb-2">
                            <input
                              :value="2"
                              v-model="filterForm.paymentStatus"
                              class="form-check-input"
                              type="radio"
                              name="statusFilter"
                              id="statusOverdue"
                            />
                            <label class="form-check-label text-danger" for="statusLocked"
                              >● Overdue
                            </label>
                          </div>
                        </div>
                      </div>

                      <div>
                        <label class="form-label x-small fw-bold text-secondary"
                          >Payment method</label
                        >
                        <select
                          class="form-select shadow-none bg-light border-0"
                          v-model="filterForm.paymentMethod"
                        >
                          <option selected value="">All</option>
                          <option value="banking">Bank transfer</option>
                          <option value="visa">E-wallet</option>
                        </select>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2">
                        <i class="fa-solid fa-dollar-sign me-1"></i> Total amount (USD)
                      </label>

                      <div class="d-flex flex-wrap gap-2 mb-2">
                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          :class="{
                            'active-pill':
                              filterForm.totalAmountMaxUSD === 100 &&
                              filterForm.totalAmountMinUSD === 0,
                          }"
                          @click="setTotalAmountRangeUSD(0, 100)"
                          style="font-size: 0.75rem"
                        >
                          &lt; $100
                        </button>

                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          :class="{
                            'active-pill':
                              filterForm.totalAmountMinUSD === 100 &&
                              filterForm.totalAmountMaxUSD === 1000,
                          }"
                          @click="setTotalAmountRangeUSD(100, 1000)"
                          style="font-size: 0.75rem"
                        >
                          $100 - $1k
                        </button>

                        <button
                          class="btn btn-sm btn-light border text-secondary"
                          :class="{
                            'active-pill':
                              filterForm.totalAmountMinUSD === 1000 &&
                              !filterForm.totalAmountMaxUSD,
                          }"
                          @click="setTotalAmountRangeUSD(1000, null)"
                          style="font-size: 0.75rem"
                        >
                          &gt; $1k
                        </button>
                      </div>
                      <div class="input-group">
                        <input
                          type="number"
                          v-model="filterForm.totalAmountMinUSD"
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
                          v-model="filterForm.totalAmountMaxUSD"
                        />
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
                          v-model="filterForm.dateFrom"
                        />
                        <span class="input-group-text bg-light text-secondary">To</span>
                        <input
                          type="date"
                          class="form-control shadow-none"
                          v-model="filterForm.dateTo"
                        />
                      </div>

                      <!-- <div class="form-check mt-2">
                        <input class="form-check-input" type="checkbox" id="filterPaidDate" />
                        <label class="form-check-label small text-secondary" for="filterPaidDate">
                          Áp dụng cho ngày thanh toán (Paid Date)
                        </label>
                      </div> -->
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
                  Buyer ID
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Artwork ID
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold text-dark text-uppercase x-small border-0 text-end pe-4"
                >
                  Price
                </th>
                <th
                  scope="col"
                  class="py-3 fw-bold text-dark text-uppercase x-small border-0 text-end pe-4"
                >
                  Total
                </th>
                <th scope="col" class="py-3 fw-bold text-dark text-uppercase x-small border-0">
                  Payment Method
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
              <template v-for="(v, i) in invoices" :key="i">
                <tr class="transition-bg border-bottom border-light-subtle">
                  <td class="ps-4 py-3 border-0">
                    <span
                      class="badge bg-light text-dark border border-light-subtle rounded-pill fw-normal"
                    >
                      <i class="fa-regular fa-user me-1 text-secondary"></i>{{ v.userId }}
                    </span>
                  </td>

                  <td class="py-3 border-0">
                    <span
                      class="badge bg-light text-secondary border border-light-subtle rounded-pill fw-normal"
                    >
                      #{{ v.artworkId }}
                    </span>
                  </td>

                  <td class="py-3 border-0 text-end pe-4 text-secondary">
                    {{ formatCurrency(v.amount) }}
                  </td>

                  <td class="py-3 border-0 text-end pe-4">
                    <span class="fw-bold text-primary">{{ formatCurrency(v.totalAmount) }}</span>
                  </td>

                  <td class="py-3 border-0">
                    <span class="d-inline-flex align-items-center gap-2 text-dark">
                      <div
                        class="bg-secondary-subtle rounded-circle p-1 d-flex justify-content-center align-items-center"
                        style="width: 24px; height: 24px"
                      >
                        <i class="fa-regular fa-credit-card text-secondary small"></i>
                      </div>
                      {{ v.paymentMethod }}
                    </span>
                  </td>

                  <td class="py-3 border-0 small text-muted">
                    {{ formatDate(v.createdAt) }}
                  </td>

                  <td class="py-3 border-0 text-center">
                    <span
                      class="badge rounded-pill border fw-medium px-3 py-2"
                      :class="getStatusClass(v.invoiceStatus)"
                    >
                      <i class="fa-solid fa-circle fa-2xs me-1 opacity-75"></i>
                      {{ convertStatus(v.invoiceStatus) }}
                    </span>
                  </td>

                  <td class="text-center py-3 border-0">
                    <div class="dropdown">
                      <button
                        class="btn btn-sm btn-light btn-action rounded-circle border-0"
                        type="button"
                        data-bs-toggle="dropdown"
                        data-bs-display="static"
                        aria-expanded="false"
                        style="width: 32px; height: 32px"
                        @click.stop="toggleDropdown(v.id)"
                      >
                        <i class="fa-solid fa-ellipsis-vertical text-secondary"></i>
                      </button>

                      <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3 mt-2">
                        <li>
                          <button
                            class="dropdown-item py-2 text-danger"
                            @click="handleDelete(v.id)"
                          >
                            <i class="fa-regular fa-trash-can me-2"></i>Delete Invoice
                          </button>
                        </li>
                      </ul>
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
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      invoices: [],
      isLoading: false,
      search: "",
      statistics: {},
      searchTimeout: null,

      filterForm: {
        paymentStatus: null,
        invoiceStatus: null,
        paymentMethod: "",
        totalAmountRange: "",
        totalAmountMinUSD: null,
        totalAmountMaxUSD: null,
        dateFrom: "",
        dateTo: "",
      },
    };
  },

  mounted() {
    this.loadInvoiceData();
    this.loadInvoiceStatistical();
    document.addEventListener("click", this.closeDropdown);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
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

    loadInvoiceData() {
      axios
        .get("http://localhost:8081/api/admin/invoices/lay-du-lieu", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.invoices = res.data.data;
          console.log("test", res.data.data || []);
        })
        .catch((err) => {
          console.log("lỗi");

          console.error(err);
        });
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);

      // Tùy chọn định dạng (Format: Oct 22, 2025, 02:30 PM)
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
        case 0:
          return "Pending";
        case 1:
          return "Paid";
        case 2:
          return "Overdue";
        // default:
        //   return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 0:
          return "bg-warning-subtle border-warning-subtle text-warning-emphasis";
        case 2:
          return "bg-danger-subtle border-danger-subtle text-danger";
        // case "Cancelled":
        //   return "bg-secondary-subtle border-secondary-subtle text-secondary";
      }
    },

    confirmPayment(invoice) {
      if (confirm(`Confirmation of receipt of full payment from ${invoice.buyer}?`)) {
        invoice.status = "Paid";
      }
    },

    cancelInvoice(invoice) {
      if (confirm("Are you sure you want to CANCEL this invoice?")) {
        invoice.status = "Cancelled";
      }
    },

    handleSearch() {
      //Xóa bộ đếm cũ nếu người dùng gõ tiếp khi chưa hết giờ
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
        this.loadInvoiceData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/invoices/tim-kiem?q=${this.search}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.invoices = res.data.data;
          console.log("Kết quả tìm kiếm:", this.invoices);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.invoices = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleDelete(invoiceId) {
      if (!confirm(`Are you sure you want to delete this invoice?`)) return;
      axios
        .delete(`http://localhost:8081/api/admin/invoices/xoa/${invoiceId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadInvoiceData();
        })
        .catch((err) => {
          console.error("Lỗi khi xóa:", err);
          const message = err.response?.data?.message || "An error occurred while deleting!";
          alert(message);
        });
    },

    //  card thống kê
    loadInvoiceStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/invoices/thong-ke`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.statistics = res.data.data;
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

      let minUSD =
        this.filterForm.totalAmountMinUSD !== null && this.filterForm.totalAmountMinUSD !== ""
          ? Number(this.filterForm.totalAmountMinUSD)
          : null;

      let maxUSD =
        this.filterForm.totalAmountMaxUSD !== null && this.filterForm.totalAmountMaxUSD !== ""
          ? Number(this.filterForm.totalAmountMaxUSD)
          : null;

      const payload = {
        paymentStatus: this.filterForm.paymentStatus,
        invoiceStatus: this.filterForm.invoiceStatus,
        paymentMethod: this.filterForm.paymentMethod === "" ? null : this.filterForm.paymentMethod,

        // Gửi giá trị USD trực tiếp
        totalAmountMin: minUSD,
        totalAmountMax: maxUSD,

        dateFrom: this.filterForm.dateFrom ? `${this.filterForm.dateFrom}T00:00:00` : null,
        dateTo: this.filterForm.dateTo ? `${this.filterForm.dateTo}T23:59:59` : null,
      };

      console.log("Payload lọc (USD):", payload);

      axios
        .post("http://localhost:8081/api/admin/invoices/loc-hoa-don", payload, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          this.invoices = res.data.data || [];
        })
        .catch((err) => {
          console.error("Lỗi bộ lọc:", err);
          this.invoices = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    resetFilter() {
      this.filterForm = {
        paymentStatus: null,
        invoiceStatus: null,
        paymentMethod: "",
        totalAmountMinUSD: null,
        totalAmountMaxUSD: null,
        dateFrom: "",
        dateTo: "",
      };

      this.loadInvoiceData();
    },

    // Helper set nhanh khoảng giá
    setTotalAmountRangeUSD(min, max) {
      // Nếu click lại nút đang chọn thì hủy chọn (reset)
      if (this.filterForm.totalAmountMinUSD === min && this.filterForm.totalAmountMaxUSD === max) {
        this.filterForm.totalAmountMinUSD = null;
        this.filterForm.totalAmountMaxUSD = null;
      } else {
        // Gán giá trị vào ô input
        this.filterForm.totalAmountMinUSD = min;
        this.filterForm.totalAmountMaxUSD = max;
      }
    },
    toggleDropdown(id) {
      if (this.activeDropdownId === id) {
        this.activeDropdownId = null;
      } else {
        this.activeDropdownId = id;
      }
    },
  },
};
</script>

<style></style>
