<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="text-primary fw-bold mb-1">Analysis & Reporting</h4>
      <p class="text-body-secondary mb-0">Hệ thống báo cáo chi tiết</p>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-secondary fw-bold mb-1">New Users</h6>
                <h3 class="fw-bold mb-0 text-dark">
                  <span v-if="loading" class="placeholder" style="width: 80px"></span>
                  <span v-else>{{ formatNumber(stats.data?.totalUsers?.currentMonth || 0) }}</span>
                </h3>
              </div>
              <div
                class="bg-secondary-subtle bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-users fs-5"></i>
              </div>
            </div>
            <small class="fw-medium" :class="stats.data?.totalUsers?.increase ? 'text-success' : 'text-danger'">
              <i :class="stats.data?.totalUsers?.increase ? 'fa-solid fa-arrow-trend-up' : 'fa-solid fa-arrow-trend-down'"></i>
              {{ Math.abs(stats.data?.totalUsers?.percentage || 0).toFixed(1) }}% vs last month
            </small>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-secondary fw-bold mb-1">Revenue</h6>
                <h3 class="fw-bold mb-0 text-dark">
                  <span v-if="loading" class="placeholder" style="width: 80px"></span>
                  <span v-else>{{ formatRevenue(stats.data?.revenue?.currentMonth || 0) }}</span>
                </h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-dollar-sign fs-5"></i>
              </div>
            </div>
            <small class="fw-medium" :class="stats.data?.revenue?.increase ? 'text-success' : 'text-danger'">
              <i :class="stats.data?.revenue?.increase ? 'fa-solid fa-arrow-trend-up' : 'fa-solid fa-arrow-trend-down'"></i>
              {{ Math.abs(stats.data?.revenue?.percentage || 0).toFixed(1) }}% vs last month
            </small>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-secondary fw-bold mb-1">Auctions</h6>
                <h3 class="fw-bold mb-0 text-dark">
                  <span v-if="loading" class="placeholder" style="width: 60px"></span>
                  <span v-else>{{ formatNumber(stats.data?.totalAuctionRooms || 0) }}</span>
                </h3>
              </div>
              <div
                class="bg-warning bg-opacity-10 text-warning-emphasis rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-gavel fs-5"></i>
              </div>
            </div>
            <small class="text-secondary">Total auction rooms</small>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h6 class="text-secondary fw-bold mb-1">Total Bids</h6>
                <h3 class="fw-bold mb-0 text-dark">
                  <span v-if="loading" class="placeholder" style="width: 80px"></span>
                  <span v-else>{{ formatNumber(stats.data?.totalBids?.currentMonth || 0) }}</span>
                </h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-circle d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-hand-holding-dollar fs-5"></i>
              </div>
            </div>
            <small class="fw-medium" :class="stats.data?.totalBids?.increase ? 'text-success' : 'text-danger'">
              <i :class="stats.data?.totalBids?.increase ? 'fa-solid fa-arrow-trend-up' : 'fa-solid fa-arrow-trend-down'"></i>
              {{ Math.abs(stats.data?.totalBids?.percentage || 0).toFixed(1) }}% vs last month
            </small>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm mb-4 overflow-hidden">
      <div class="card-body p-2">
        <ul class="nav nav-pills nav-fill gap-2 flex-column flex-sm-row">
          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/revenues"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-chart-line me-2 fs-6"></i> Doanh Thu
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/users"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-user-group me-2 fs-6"></i> Người Dùng
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/artworks"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-image"></i> Tác phẩm
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/auctions"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-gavel me-2 fs-6"></i> Phòng Đấu Giá
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/bids"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-hand-holding-dollar me-2 fs-6"></i> Lượt Đấu Giá
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/management-statistical/reports"
              class="nav-link fw-bold py-2 px-3 rounded-3 text-secondary transition-all"
              active-class="bg-info-subtle text-white shadow-sm"
            >
              <i class="fa-solid fa-triangle-exclamation me-2 fs-6"></i> Báo Cáo
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StatisticalDashboard',
  data() {
    return {
      stats: {
        newUsers: 0,
        newUsersPercentage: 0,
        revenue: 0,
        revenuePercentage: 0,
        activeAuctions: 0,
        totalBids: 0,
        bidsToday: 0,
      },
      loading: true,
    };
  },
  mounted() {
    this.fetchDashboardStats();
  },
  methods: {
    async fetchDashboardStats() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          'http://localhost:8081/api/admin/dashboard/thong-ke',
          {
            headers: {
              Authorization: token ? `Bearer ${token}` : '',
            },
          }
        );

        if (response.data) {
          this.stats = response.data;
        }
      } catch (error) {
        console.error('Error fetching dashboard statistics:', error);
      } finally {
        this.loading = false;
      }
    },
    formatNumber(num) {
      return new Intl.NumberFormat('en-US').format(num);
    },
    formatRevenue(amount) {
      const millions = amount / 1000000;
      return millions >= 1 ? `${millions.toFixed(0)}M` : `${(amount / 1000).toFixed(0)}K`;
    },
  },
};
</script>

<style scoped></style>
