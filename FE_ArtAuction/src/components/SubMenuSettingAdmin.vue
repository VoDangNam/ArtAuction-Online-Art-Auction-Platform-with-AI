<!-- menu phụ -->
<template>
  <!-- <div class="card" style="width: 18rem">
    <div class="card-body p-0">
      <router-link
        to="/admin/management-setting/general-setting"
        class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
        :class="{ active: isActive('/admin/management-setting/general-setting') }"
      >
        <i class="fa-solid fa-gear"></i>
        <span class="fw-bold text-nowrap d-none d-lg-inline">Cài đặt chung</span>
      </router-link>

      <router-link
        to="/admin/management-setting/payment-setting"
        class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
        :class="{ active: isActive('/admin/management-setting/payment-setting') }"
      >
        <i class="fa-solid fa-gear"></i>
        <span class="fw-bold text-nowrap d-none d-lg-inline">Thanh toán</span>
      </router-link>
    </div>
  </div> -->

  <div class="card w-100">
    <div class="card-body py-lg-3 py-sm-1">
      <div class="row">
        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="/admin/management-setting/general-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/general-setting') }"
          >
            <i class="fa-solid fa-gear"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">General</span>
          </router-link>
        </div>

        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="payment-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/payment-setting') }"
          >
            <i class="fa-solid fa-dollar-sign"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">Payment</span>
          </router-link>
        </div>

        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="notification-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/notification-setting') }"
          >
            <i class="fa-solid fa-bell"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">Notification</span>
          </router-link>
        </div>

        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="email-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/email-setting') }"
          >
            <i class="fa-solid fa-envelope"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">Email</span>
          </router-link>
        </div>

        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="security-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/security-setting') }"
          >
            <i class="fa-solid fa-shield-halved"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">Security</span>
          </router-link>
        </div>

        <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
          <router-link
            to="database-setting"
            class="submenu-admin-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3"
            :class="{ active: isActive('/admin/management-setting/database-setting') }"
          >
            <i class="fa-solid fa-database"></i>
            <span class="fw-bold text-nowrap d-none d-lg-inline">Database</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SubMenuSettingAdmin",
  methods: {
    isActive(path) {
      return this.$route.path.startsWith(path);
    },
  },
};
</script>

<style></style>
