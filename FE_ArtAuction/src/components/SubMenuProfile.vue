<template>
  <!-- menu phụ -->
  <div class="col-lg-3 col-md-12 submenu text-white d-flex flex-column align-items-center mb-3">
    <div class="card w-100">
      <div class="card-body py-lg-3 py-sm-1">
        <div class="row ">
          <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
            <router-link to="/client/profile/art-management"
              class="submenu-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3 justify-content-sm-center justify-content-lg-start "
              :class="{ active: isActive('/client/profile/art-management') }">
              <i class="fa-solid fa-images fa-xl m-lg-0 m-2"></i>
              <span class="fw-bold text-nowrap d-none d-lg-inline">Artworks</span>
            </router-link>
          </div>
          <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
            <router-link to="/client/profile/history"
              class="submenu-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3 justify-content-sm-center justify-content-lg-start "
              :class="{ active: isActive('/client/profile/history') }">
              <i class="fa-solid fa-gavel fa-xl m-lg-0 m-2 flip-x "></i>
              <span class="fw-bold text-nowrap d-none d-lg-inline">Auction</span>
            </router-link>
          </div>
          <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3 mb-lg-2">
            <router-link to="/client/profile/invoices"
              class="submenu-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3 justify-content-sm-center justify-content-lg-start "
              :class="{ active: isActive('/client/profile/invoices') }">
              <i class="fa-solid fa-receipt fa-xl m-lg-0 m-2"></i>
              <span class="fw-bold text-nowrap d-none d-lg-inline">Invoices</span>
            </router-link>
          </div>
          <div class="col-lg-12 col-md-3 col-sm-3 col-xs-3">
            <router-link to="/client/profile/e-wallet"
              class="submenu-item aa-link text-decoration-none d-flex align-items-center gap-4 px-4 py-3 justify-content-sm-center justify-content-lg-start "
              :class="{ active: isActive('/client/profile/e-wallet') }">
              <i class="fa-solid fa-wallet fa-xl m-lg-0 m-2"></i>
              <span class="fw-bold text-nowrap d-none d-lg-inline">E-Wallet</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- nội dung submenu -->
  <div class="col-lg-9 col-md-12">
    <router-view />
  </div>
</template>
<script>
export default {
  name: 'SubMenuProfile',
  methods: {
    isActive(path) {
      return this.$route.path.startsWith(path)
    }
  }
};
</script>
<style scoped>

</style>
