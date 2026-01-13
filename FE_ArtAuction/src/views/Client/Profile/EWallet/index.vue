<template>
  <div class="container">
    <!-- card balance -->
    <div class="row">
      <div class="col-lg-9 col-md-12 d-flex">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <h6 class="card-subtitle text-secondary">Available Balance</h6>
              <i @click="toggleHidden"
                :class="isHidden ? 'fa-solid fa-eye-slash text-body-secondary' : 'fa-solid fa-eye text-body-secondary'"></i>
            </div>
            <div class="mt-2 fs-5">
              <span v-if="isHidden">*******</span>
              <span v-else>{{ Number(balance || 0).toLocaleString('vi-VN') }} ₫</span>
            </div>
          </div>
        </div>
      </div>
      <div class="col-3">
        <div class="card">
          <div class="card-body">
            <button type="button"
              class="btn btn-light btn-transaction border border-success w-100 d-flex flex-column align-items-center justify-content-center"
              data-bs-toggle="modal" data-bs-target="#NapModal">
              <i class="fa-solid fa-plus"></i>
              <p class="mb-0">Deposit</p>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- hành động -->

    <!-- history (demo) -->
    <div class="card mt-3 mb-5">
      <div class="card-body">
        <h6>Transaction History</h6>
        <template v-if="loadWallet && loadWallet.length > 0">
          <div v-for="(v,i) in loadWallet" :key="i" class="d-flex justify-content-between align-items-center border rounded p-3 mb-2">
            <div class="d-flex align-items-center">
              <div class="rounded-circle bg-light d-flex justify-content-center align-items-center me-3"
                style="width:32px;height:32px">
                <i class="bi bi-arrow-up-right text-success"></i>
              </div>
              <div>
                <div class="fw-bold">Deposit from VietQR</div>
                <small class="text-muted d-block">{{ v.id }}</small>
                <small class="text-muted">{{ formatDate(v.updatedAt) }}</small>
              </div>
            </div>
            <div class="text-end">
              <div class="fw-bold text-success">+{{ formatCurrency(v.balance) }}</div>
              <span v-if="v.status === 1" class="badge bg-light text-success border border-success">Success</span>
              <span v-else class="badge bg-light text-warning border border-warning">Pending</span>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="text-center text-muted py-4">
            <p class="mb-0">No transactions yet</p>
          </div>
        </template>

      </div>
    </div>
    <!-- Modal -->
    <div class="modal fade" id="NapModal" tabindex="-1" aria-labelledby="NapModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="NapModalLabel">Enter Deposit Amount</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-lg-7">
                <div class="mb-3">
                  <label class="form-label">Amount</label>
                  <input v-model="nap.amount" type="" class="form-control" placeholder="Example: 200000" />
                  <small class="text-muted">Minimum 10,000 ₫</small>
                </div>

                <div class="mb-3">
                  <label class="form-label">Transfer Content (Optional)</label>
                  <input v-model="nap.note" type="text" class="form-control"
                    placeholder="If left empty, system will generate automatically" />
                </div>
              </div>
              <div class="col-lg-5">
                <!-- <img :src="nap.qrUrl" alt="QR Code" class="img-fluid" /> -->
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-success" @click="NapAndOpenQr" :disabled="isCreatingQR">
              <span v-if="isCreatingQR" class="spinner-border spinner-border-sm me-2"></span>
              {{ isCreatingQR ? 'Generating QR...' : 'Confirm' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- QR Modal -->
    <div class="modal fade" id="QRModal" tabindex="-1" aria-labelledby="QRModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-6" id="QRModalLabel">Scan QR Code to Deposit</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <template v-if="nap.qrUrl">
              <img :src="nap.qrUrl" alt="QR Code" class="img-fluid rounded mb-3" style="max-width:320px;" />
              <div class="small text-muted">Transaction ID: {{ nap.transactionId || '—' }}</div>
            </template>
            <template v-else>
              <div class="d-flex justify-content-center py-5">
                <div class="spinner-border" role="status"></div>
              </div>
              <div class="small text-muted">Generating QR…</div>
            </template>
            <p v-if="statusMessage?.status === 0" class="mb-0 text-warning mt-3">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ statusMessage?.message || "Transaction not confirmed" }}
            </p>


          </div>
          <div class="modal-footer">
            <!-- <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Đóng</button> -->
            <button type="button" class="btn btn-success w-100 fs-6" @click="checkTransaction" :disabled="checking">
              <span v-if="checking" class="spinner-border spinner-border-sm me-2"></span>
              {{ checking ? 'Checking...' : 'Check' }}
            </button>
          </div>
        </div>
      </div>
    </div>




  </div>
</template>

<script>
import axios from "axios";
import * as bootstrap from "bootstrap";

export default {
  name: "WalletPage",
  data() {
    return {
      isHidden: true,
      balance: 0,
      frozenBalance: 0,
      showDepositForm: false,
      depositAmount: "",
      depositNote: "",
      loading: false,

      showQR: false,
      qrCodeUrl: "",
      currentTransactionId: "",
      verifying: false,
      verifyMessage: "",
      verifySuccess: false,

      polling: true,
      pollTimer: null,
      pollIntervalSec: 5,


      nap: {
        amount: "",
        note: "",
        qrUrl: "",
        transactionId: ""
      },
      statusMessage: null,
      checking: false,
      isCreatingQR: false,
      modalResetHandlers: {
        nap: null,
        qr: null
      },
      loadWallet: null
    };
  },
  computed: {
    formattedBalance() {
      const n = Number(this.balance || 0);
      return n.toLocaleString("vi-VN") + " ₫";
    },
    formattedFrozenBalance() {
      const n = Number(this.frozenBalance || 0);
      return n.toLocaleString("vi-VN") + " ₫";
    },
  },
  mounted() {
    // Ẩn/hiện số dư theo localStorage
    const saved = localStorage.getItem("wallet_Hidden");
    if (saved !== null) this.isHidden = saved === "true";
    this.fetchWallet();
    this.getWallet();

    // Lắng nghe sự kiện đóng modal để reset dữ liệu
    this.$nextTick(() => {
      const napModalElement = document.getElementById('NapModal');
      const qrModalElement = document.getElementById('QRModal');

      // BỎ reset khi đóng NapModal - tránh xóa qrUrl khi chuyển modal
      // if (napModalElement) {
      //   this.modalResetHandlers.nap = () => {
      //     this.resetModalData();
      //   };
      //   napModalElement.addEventListener('hidden.bs.modal', this.modalResetHandlers.nap);
      // }

      // CHỈ reset khi đóng QRModal
      if (qrModalElement) {
        this.modalResetHandlers.qr = () => {
          console.log("🔄 QRModal closed - resetting data");
          this.resetModalData();
        };
        qrModalElement.addEventListener('hidden.bs.modal', this.modalResetHandlers.qr);
      }
    });
  },
  beforeUnmount() {
    // Cleanup event listeners
    const napModalElement = document.getElementById('NapModal');
    const qrModalElement = document.getElementById('QRModal');

    if (napModalElement && this.modalResetHandlers.nap) {
      napModalElement.removeEventListener('hidden.bs.modal', this.modalResetHandlers.nap);
    }

    if (qrModalElement && this.modalResetHandlers.qr) {
      qrModalElement.removeEventListener('hidden.bs.modal', this.modalResetHandlers.qr);
    }
  },
  // beforeUnmount() {
  //   this.clearPoll();
  // },
  methods: {
    formatCurrency(value) {
      const num = Number(value || 0);
      return num.toLocaleString('vi-VN') + ' ₫';
    },
    formatDate(dateString) {
      if (!dateString) return '';
      try {
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (e) {
        return dateString;
      }
    },
    // Helper method để cleanup modal backdrop
    cleanupModalBackdrop() {
      // Remove all backdrops
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());

      // Reset body
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    },

    async Nap() {
      const raw = (this.nap.amount || "").toString().replace(/[^\d]/g, "");
      const amount = Number(raw);
      if (!amount || amount < 10000) {
        this.$toast.error("Please enter a valid amount (≥ 10,000₫)");
        return false;
      }

      // Reset QR state so the modal shows a spinner while loading
      this.nap.qrUrl = "";
      this.nap.transactionId = "";

      try {
        const res = await axios.post(
          "http://localhost:8081/api/wallets/topups",
          { amount, note: this.nap.note },
          {
            headers: {
              Authorization: "Bearer " + (localStorage.getItem("token") || ""),
            },
          }
        );

        const data = res?.data || {};
        this.nap.transactionId = data.transactionId || "";
        this.nap.qrUrl = data.qrUrl || data.qrImageUrl || "";
        if (data.noteUsed) this.nap.note = data.noteUsed;

        console.log("✅ QR created successfully:", {
          transactionId: this.nap.transactionId,
          qrUrl: this.nap.qrUrl
        });

        return true;
      } catch (error) {
        console.error("❌ Error creating QR:", error);
        this.$toast.error("Unable to generate QR code. Please try again.");
        return false;
      }
    },

    async NapAndOpenQr() {
      this.isCreatingQR = true;

      const ok = await this.Nap();
      if (!ok) {
        this.isCreatingQR = false;
        return;
      }

      // Ẩn NapModal và cleanup backdrop
      const napEl = document.getElementById("NapModal");
      const napModal = bootstrap.Modal.getInstance(napEl);
      if (napModal) {
        napModal.hide();
      }

      // Remove backdrop và reset body
      setTimeout(() => {
        this.cleanupModalBackdrop();
      }, 150);

      // Đợi NapModal đóng xong rồi mở QRModal
      setTimeout(() => {
        const qrEl = document.getElementById("QRModal");
        const qrModal = new bootstrap.Modal(qrEl);
        qrModal.show();
        this.isCreatingQR = false;
      }, 300);
    },

    getWallet() {
      axios
        .get('http://localhost:8081/api/wallets/transactionHistories', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          // API trả về mảng trực tiếp hoặc trong data
          const data = res.data;
          const transactions = Array.isArray(data) ? data : (data.data || []);
          // Đảo ngược mảng để hiển thị giao dịch mới nhất trước (tạo bản sao để không thay đổi mảng gốc)
          this.loadWallet = [...transactions].reverse();

          console.log("Wallet transaction histories:", this.loadWallet);
        })
        .catch((error) => {
          console.error("Error fetching transaction histories:", error);
          this.loadWallet = [];
        });
    },

    // ====== BALANCE ======
    fetchWallet() {
      const userId = this.getCurrentUserId();
      if (!userId) return;
      axios
        .get(
          `http://localhost:8081/api/wallets/getWallet`,
          {
            headers: {
              Authorization: "Bearer " + (localStorage.getItem("token") || "")
            }
          }
        )
        .then((res) => {
          const data = res && res.data ? res.data : {};
          this.balance = data.balance ?? 0;
          this.frozenBalance = data.frozenBalance ?? 0;
        })
        .catch((e) => {
          console.error("Fetch wallet error:", e);
        });
    },

    getCurrentUserId() {
      const token = localStorage.getItem("token");
      if (!token) return "";
      try {
        const base = token.split(".")[1];
        const norm = base.replace(/-/g, "+").replace(/_/g, "/");
        const pad = "=".repeat((4 - (norm.length % 4)) % 4);
        const payload = JSON.parse(atob(norm + pad));
        return (
          payload.userId ||
          payload.id ||
          payload.uid ||
          (payload.user && (payload.user.id || payload.user.userId)) ||
          payload.sub || ""
        );
      } catch (_) {
        return "";
      }
    },

    // ====== UI ======
    toggleHidden() {
      this.isHidden = !this.isHidden;
      localStorage.setItem("wallet_Hidden", String(this.isHidden));
    },

    checkTransaction() {


      this.checking = true;

      axios
        .post(
          `http://localhost:8081/api/wallets/${this.nap.transactionId}/verify-capture`,
          {},
          {
            headers: {
              Authorization: "Bearer " + (localStorage.getItem("token") || ""),
            },
          }
        )
        .then((res) => {
          const data = res && res.data ? res.data : {};

          // Check status (API returns status as number: 0 or 1)
          if (data.status === 1) {
            // Status = 1: Close modal and show toast
            this.$toast.success(data.message || "Deposit successful");
            console.log("data", data);

            this.getWallet();

            this.$nextTick(() => {
              const modalElement = document.getElementById('QRModal');
              if (modalElement) {
                // eslint-disable-next-line no-undef
                const modal = bootstrap.Modal.getInstance(modalElement);
                if (modal) {
                  modal.hide();
                }
              }

              // Cleanup backdrop và reset body sau khi đóng modal
              setTimeout(() => {
                this.cleanupModalBackdrop();
              }, 200);
            });

            this.fetchWallet();
            // Reset statusMessage after closing modal
            this.statusMessage = null;
          } else if (data.status === 0) {
            // Status = 0: Display message in QRModal
            this.statusMessage = data;
          }
        })
        .catch((error) => {
          const errorMessage = error.response?.data?.message || "Unable to check transaction. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.checking = false;
        });
    },

    resetModalData() {
      console.log("🧹 RESET MODAL DATA - clearing nap object");
      // Reset dữ liệu nạp tiền
      this.nap = {
        amount: "",
        note: "",
        qrUrl: "",
        transactionId: ""
      };
      // Reset status message
      this.statusMessage = null;
      // Reset checking state
      this.checking = false;

      // Cleanup backdrop để tránh màn hình đen
      setTimeout(() => {
        this.cleanupModalBackdrop();
      }, 100);
    },

  }
};
</script>

<style>
.btn-transaction:hover {
  box-shadow: 0 0 20px var(--bs-success);
  background-color: white;
}

.overlay {
  z-index: 1050;
}

.modal-box {
  padding: 50px 30px;
  width: 500px;
}

.qr-overlay {
  z-index: 1100;
}

.qr-only {
  width: 300px;
  height: 300px;
  object-fit: contain;
}
</style>
