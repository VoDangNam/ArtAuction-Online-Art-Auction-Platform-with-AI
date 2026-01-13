<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-white shadow-sm rounded-3 px-3 mt-3 mb-3">
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-3">
        <img src="../../../assets/img/Logo_AA.png" class="imgLogo" alt="" />
        <span class="fw-semibold"><span class="text-success-bright fw-semibold">Art</span>Auction</span>
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse bg-white p-3 rounded" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto gap-lg-4 gap-3">
          <li class="nav-item">
            <router-link v-if="user" to="/client/home" class="nav-link py-0"
              :class="{ active: $route.path === '/client/home' }" aria-current="page">
              Home
            </router-link>
            <router-link v-else to="/" class="nav-link py-0" :class="{ active: $route.path === '/' }"
              aria-current="page">
              Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/client/auction" class="nav-link py-0"
              :class="{ active: $route.path === '/client/auction' }">
              Auction
            </router-link>
          </li>
          <li class="nav-item">
            <a
              href="#"
              @click.prevent="navigateToRegisterArtwork"
              class="nav-link py-0"
              :class="{ active: $route.path === '/client/register-artwork' }">
              Launch
            </a>
          </li>
          <li class="nav-item">
            <router-link to="/about-us" class="nav-link py-0" :class="{ active: $route.path === '/about-us' }">
              About us
            </router-link>
          </li>
        </ul>
      </div>
      <div class="d-flex align-items-center gap-4">
        <!-- Loading state -->
        <!-- <div v-if="isLoading" class="d-flex align-items-center gap-2">
          <div class="spinner-border spinner-border-sm text-success" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted">Đang tải...</span>
        </div> -->

        <!-- User logged in -->
        <template v-if="user.check">
          <!-- notify -->
          <div class="dropdown">
            <button
              class="btn btn-link dropdown-toggle dropdown-toggle-no-caret d-flex justify-content-center align-items-center position-relative p-2 border-0"
              type="button"
              :id="'notificationDropdown-' + _uid"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              style="text-decoration: none; min-width: 40px; min-height: 40px;"
              @click="handleNotificationClick">
              <img src="/src/assets/img/icon-bell.png" class="icon-bell" style="width: 24px; height: 24px; pointer-events: none;" />
              <span v-if="unreadCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                style="font-size: 10px; padding: 3px 6px; pointer-events: none; z-index: 1;">
                {{ unreadCount > 99 ? '99+' : unreadCount }}
              </span>
            </button>
            <!-- Notification Dropdown -->
            <div
              :id="'notificationDropdownMenu-' + _uid"
              class="dropdown-menu dropdown-menu-end dropdown-menu-lg mt-2 p-0 overflow-auto border-2 border-success shadow"
              style="max-height: 500px; width: 380px;"
              :aria-labelledby="'notificationDropdown-' + _uid">
              <div class="p-3 border-bottom bg-light sticky-top">
                <h6 class="m-0 fw-bold text-success">Notifications</h6>
              </div>
              <div v-if="notifications.length === 0" class="p-4 text-center text-muted">
                <i class="fa-regular fa-bell-slash fa-2x mb-2"></i>
                <p class="m-0 small">No notifications yet</p>
              </div>
              <div v-for="notification in notifications" :key="notification.id" class="notification-item p-3 border-bottom"
                :class="{ 'notification-unread': !notification.isRead }"
                @click="markAsRead(notification.id)">
                <div class="d-flex gap-2 align-items-start">
                  <!-- icon -->
                  <div
                    class="notification-icon d-flex align-items-center justify-content-center rounded-circle text-white flex-shrink-0"
                    :class="getNotificationIconClass(notification.title)">
                    <i :class="getNotificationIcon(notification.title)" class="fs-6"></i>
                  </div>
                  <!-- content -->
                  <div class="flex-grow-1 overflow-hidden">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <p class="m-0 fw-semibold notification-title">{{ notification.title }}</p>
                      <!-- <button class="btn btn-sm p-0 text-muted" style="line-height: 1;">
                        <i class="fa-solid fa-ellipsis-vertical"></i>
                      </button> -->
                    </div>
                    <p class="notification-content text-dark small m-0 mb-2">
                      {{ truncateText(notification.notificationContent, 120) }}
                    </p>
                    <div class="d-flex justify-content-between align-items-center text-muted" style="font-size: 11px">
                      <span class="notification-time">
                        <i class="fa-regular fa-clock me-1"></i>{{ formatTime(notification.notificationTime) }}
                      </span>
                      <span class="notification-date">
                        {{ formatDate(notification.notificationTime) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="d-flex gap-2 action-buttons">
            <div class="dropdown">
              <div class="dropdown-toggle dropdown-toggle-no-caret" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                <div class="d-flex gap-3 align-items-center">
                  <!-- <img src="../../../assets/img/avt.png" class="img-avatar" alt="" /> -->
                  <img :src="avatarSrc" class="img-avatar" alt="" />
                </div>
              </div>
              <ul class="dropdown-menu dropdown-menu-end mt-2 p-3 border-2 border-success shadow overflow-hidden">
                <li>
                  <div class="card bg-accent shadow-sm mb-2">
                    <div class="card-body p-2 d-flex align-items-center gap-3">
                      <img :src="avatarSrc" class="img-avatar" alt="" />
                      <div class="d-flex align-content-center flex-column">
                        <p class="fw-bold text-success mb-1">
                          {{ user.name }}
                        </p>
                        <p class="text-success m-0">{{ user.email }}</p>
                      </div>
                    </div>
                  </div>
                </li>
                <li>
                  <router-link to="/client/profile"
                    class="dropdown-item d-flex align-items-center gap-3 py-2 px-4 mt-2 mb-1">
                    <i class="bi bi-person fa-xl me-2"></i>
                    <p class="m-0">Profile</p>
                  </router-link>
                </li>
                <!-- <li>
                  <router-link to="/client/payment"
                    class="dropdown-item d-flex align-items-center gap-3 py-2 px-4 mt-2 mb-1">
                    <i class="bi bi-credit-card fa-xl me-2"></i>
                    <p class="m-0">Payment</p>
                  </router-link>
                </li> -->
                <!-- <li>
                  <router-link to="" class="dropdown-item d-flex align-items-center gap-3 py-2 px-4 mt-2 mb-1">
                    <i class="bi bi-gear fa-xl me-2"></i>
                    <p class="m-0">Setting</p>
                  </router-link>
                </li> -->
                <li>
                  <a href="#" class="dropdown-item d-flex align-items-center gap-3 py-2 px-4 mt-2 mb-1 text-danger"
                    data-bs-toggle="modal" data-bs-target="#logoutConfirmModal">
                    <i class="bi bi-box-arrow-right fa-xl me-2"></i>
                    <p class="m-0">Log out</p>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </template>

        <!-- User not logged in -->
        <div v-else class="d-flex gap-2">
          <router-link to="/register">
            <button class="btn btn-outline-success">Sign up</button>
          </router-link>
          <router-link to="/login">
            <button class="btn btn-success">Sign in</button>
          </router-link>
        </div>
      </div>
    </nav>
  </div>
  <!-- Logout Confirm Modal moved to body using Teleport to avoid stacking context issues -->
  <teleport to="body">
    <div class="modal fade" id="logoutConfirmModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="logoutModalLabel">Confirm logout</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">Are you sure you want to log out of your current account?</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="performLogout" data-bs-dismiss="modal">
              Log out
            </button>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>
<script>
import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
import defaultAvatar from "../../../assets/img/avt.png";
const toaster = createToaster({ position: "bottom-right" });

export default {
  data() {
    return {
      user: {},
      // isLoading: true,

      isNotificationOpen: false,

      notifications: [],

      loading: false,
      error: null,
      defaultAvatar: defaultAvatar,
    };
  },
  computed: {
    avatarSrc() {
      return this.user.avt || this.defaultAvatar;
    },
    unreadCount() {
      return this.notifications.filter(n => !n.isRead).length;
    },
  },
  mounted() {
    this.fetchNotificationsbyId();

    const rawAvt = localStorage.getItem("avatar_kh");
    const avt = (!rawAvt || rawAvt === "null" || rawAvt === "undefined") ? "" : rawAvt;

    this.user = {
      name: localStorage.getItem("name_kh"),
      email: localStorage.getItem("email_kh"),
      check: localStorage.getItem("check_kh"),
      avt: avt,
    };
    console.log("menu", this.user);

    window.addEventListener("avatar-updated", this.handleAvatarUpdate);

    // Khởi tạo lại Bootstrap dropdown sau khi component mount
    this.$nextTick(() => {
      this.initDropdowns();
    });
  },
  updated() {
    // Khởi tạo lại dropdown sau khi component update (ví dụ khi notifications thay đổi)
    this.$nextTick(() => {
      this.initDropdowns();
    });
  },
  beforeUnmount() {
    window.removeEventListener("avatar-updated", this.handleAvatarUpdate);
  },
  methods: {
    // Khởi tạo lại Bootstrap dropdowns
    initDropdowns() {
      // Kiểm tra Bootstrap có sẵn không (có thể là window.bootstrap hoặc global bootstrap)
      const Bootstrap = window.bootstrap || (typeof bootstrap !== 'undefined' ? bootstrap : null);

      if (Bootstrap && Bootstrap.Dropdown) {
        const dropdownElement = document.getElementById(`notificationDropdown-${this._uid}`);
        if (dropdownElement) {
          try {
            // Dispose existing instance nếu có
            const existingInstance = Bootstrap.Dropdown.getInstance(dropdownElement);
            if (existingInstance) {
              existingInstance.dispose();
            }
            // Khởi tạo lại dropdown
            new Bootstrap.Dropdown(dropdownElement);
          } catch (error) {
            console.warn('Error initializing dropdown:', error);
          }
        }
      }
    },

    // Handle click để đảm bảo dropdown mở được (fallback nếu Bootstrap không hoạt động)
    handleNotificationClick(event) {
      // Chỉ fallback nếu Bootstrap dropdown không hoạt động
      const Bootstrap = window.bootstrap || (typeof bootstrap !== 'undefined' ? bootstrap : null);
      if (Bootstrap && Bootstrap.Dropdown) {
        // Để Bootstrap xử lý, không làm gì thêm
        return;
      }

      // Fallback manual toggle chỉ khi Bootstrap không có
      const dropdownElement = event.currentTarget;
      const dropdownMenu = document.getElementById(`notificationDropdownMenu-${this._uid}`);

      if (dropdownMenu) {
        event.preventDefault();
        event.stopPropagation();

        const isShown = dropdownMenu.classList.contains('show');

        // Đóng tất cả dropdowns khác trước
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
          if (menu !== dropdownMenu) {
            menu.classList.remove('show');
            const btn = document.querySelector(`[aria-expanded="true"]`);
            if (btn && btn !== dropdownElement) {
              btn.setAttribute('aria-expanded', 'false');
            }
          }
        });

        // Toggle dropdown hiện tại
        if (isShown) {
          dropdownMenu.classList.remove('show');
          dropdownElement.setAttribute('aria-expanded', 'false');
        } else {
          dropdownMenu.classList.add('show');
          dropdownElement.setAttribute('aria-expanded', 'true');
        }
      }
    },

    // Navigate to Register Artwork với force reload nếu role = 1
    navigateToRegisterArtwork() {
      const userRole = this.getUserRole();
      console.log('👤 User role:', userRole);

      // Nếu role = 1 (seller), force reload
      if (userRole === 1) {
        console.log('🔄 Role = 1, force reloading page...');
        window.location.href = '/client/register-artwork';
      } else {
        // Role khác, dùng router bình thường
        this.$router.push('/client/register-artwork');
      }
    },

    // Lấy role từ token
    getUserRole() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return null;

        const parts = token.split(".");
        if (parts.length < 2) return null;

        const payload = JSON.parse(decodeURIComponent(escape(window.atob(parts[1]))));
        return payload.role || payload.roleId || null;
      } catch (error) {
        console.error('Error getting user role:', error);
        return null;
      }
    },

    handleAvatarUpdate(event) {
      const newAvatar = event.detail.avatar;
      console.log("Avatar updated:", newAvatar);

      this.user.avt = newAvatar;

      localStorage.setItem("avatar_kh", newAvatar);
    },

    performLogout() {
      const token = localStorage.getItem("token");
      const finish = () => {

        localStorage.removeItem("token");
        localStorage.removeItem("name_kh");
        localStorage.removeItem("email_kh");
        localStorage.removeItem("check_kh");
        this.user = null;
        // this.$toast.success("Logout successful");

        this.$router.push("/login");

      };

      if (!token) {
        finish();
        return;
      }

      axios
        .post(
          "http://localhost:8081/api/auth/logout", {}, {
          headers: { Authorization: "Bearer " + token }
        }
        )
        .then(() => {
          console.log("Logout successful");
          toaster.success("Logout successful");
          setTimeout(() => {
            finish();
          }, 300);


        })
        .catch(() => {
          // Dù lỗi vẫn xóa local và chuyển trang để đảm bảo UX
          finish();

        });
    },
    fetchNotificationsbyId() {
      axios
        .get("http://localhost:8081/api/notification/my-notification", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.notifications = res.data;
          console.log("notify", this.notifications);
        })
        .catch((err) => {
          this.error = err.message;
        });
    },

    markAsRead(notificationId) {
      const notification = this.notifications.find((n) => n.id === notificationId);
      if (notification && !notification.isRead) {
        notification.isRead = true;
        notification.status = "READ";

        // Gửi request update về backend (nếu có API update)
        // axios.put(
        //   "http://localhost:8081/api/notification/${notificationId}/read",
        //   {},
        //   {
        //     headers: {
        //       Authorization: "Bearer " + localStorage.getItem("key_admin"),
        //     },
        //   }
        // );
      }
    },
    formatTime(value) {
      if (!value) return "";
      try {
        return new Date(value).toLocaleTimeString("vi-VN");
      } catch (e) {
        return "";
      }
    },
    formatDate(value) {
      if (!value) return "";
      try {
        return new Date(value).toLocaleDateString("vi-VN");
      } catch (e) {
        return "";
      }
    },
    toggleNotification() {
      this.isNotificationOpen = !this.isNotificationOpen;
      if (this.isNotificationOpen) {
        this.fetchNotifications();
      }
    },

    // Truncate text to specified length
    truncateText(text, maxLength = 100) {
      if (!text) return "";
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + "...";
    },

    // Get icon based on notification type
    getNotificationIcon(title) {
      if (!title) return "fa-regular fa-bell";
      const lowerTitle = title.toLowerCase();

      if (lowerTitle.includes("thắng") || lowerTitle.includes("win")) {
        return "fa-solid fa-trophy";
      } else if (lowerTitle.includes("approved") || lowerTitle.includes("chấp nhận")) {
        return "fa-solid fa-circle-check";
      } else if (lowerTitle.includes("seller") || lowerTitle.includes("người bán")) {
        return "fa-solid fa-palette";
      } else if (lowerTitle.includes("bid") || lowerTitle.includes("đấu giá")) {
        return "fa-solid fa-gavel";
      } else if (lowerTitle.includes("payment") || lowerTitle.includes("thanh toán")) {
        return "fa-solid fa-credit-card";
      }
      return "fa-regular fa-bell";
    },

    // Get icon background class
    getNotificationIconClass(title) {
      if (!title) return "bg-secondary";
      const lowerTitle = title.toLowerCase();

      if (lowerTitle.includes("thắng") || lowerTitle.includes("win")) {
        return "bg-warning";
      } else if (lowerTitle.includes("approved") || lowerTitle.includes("chấp nhận")) {
        return "bg-success";
      } else if (lowerTitle.includes("seller") || lowerTitle.includes("người bán")) {
        return "bg-info";
      } else if (lowerTitle.includes("bid") || lowerTitle.includes("đấu giá")) {
        return "bg-primary";
      } else if (lowerTitle.includes("payment") || lowerTitle.includes("thanh toán")) {
        return "bg-danger";
      }
      return "bg-secondary";
    },
  },
};
</script>
<style scoped>
/* Bell icon button */
.btn-link.dropdown-toggle {
  background: none !important;
  box-shadow: none !important;
  outline: none !important;
}

.btn-link.dropdown-toggle:hover,
.btn-link.dropdown-toggle:focus,
.btn-link.dropdown-toggle:active {
  background: none !important;
  box-shadow: none !important;
  outline: none !important;
}

/* Hide dropdown caret arrow */
.dropdown-toggle-no-caret::after {
  display: none !important;
}

.icon-bell {
  cursor: pointer;
  transition: transform 0.2s ease;
  pointer-events: none; /* Đảm bảo click vào icon không bị chặn */
}

.icon-bell:hover {
  transform: scale(1.1);
}

/* Đảm bảo notification button có đủ clickable area */
.dropdown > button[data-bs-toggle="dropdown"] {
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.dropdown > button[data-bs-toggle="dropdown"]:focus {
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
}

/* Notification styles */
.notification-item {
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffffff;
}

.notification-item:hover {
  background-color: #f8f9fa;
}

.notification-unread {
  background-color: #e6fbfa !important;
}

.notification-unread:hover {
  background-color: #d4f4f0 !important;
}

.notification-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  font-size: 18px;
}

.notification-title {
  font-size: 14px;
  color: #212529;
  line-height: 1.4;
}

.notification-content {
  font-size: 13px;
  color: #6c757d;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.notification-time,
.notification-date {
  display: inline-flex;
  align-items: center;
}

/* Dropdown menu */
.dropdown-menu-lg {
  min-width: 380px;
}

/* Scrollbar styling */
.dropdown-menu::-webkit-scrollbar {
  width: 6px;
}

.dropdown-menu::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.dropdown-menu::-webkit-scrollbar-thumb {
  background: #198754;
  border-radius: 3px;
}

.dropdown-menu::-webkit-scrollbar-thumb:hover {
  background: #157347;
}

/* Badge for unread notifications */
.dropdown-notification::after {
  content: attr(data-count);
  position: absolute;
  top: -5px;
  right: -5px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive */
@media (max-width: 576px) {
  .dropdown-menu-lg {
    min-width: 320px;
    max-width: 90vw;
  }

  .notification-content {
    font-size: 12px;
  }
}
</style>
