<template>
  <div class="card border-0 shadow-sm h-100">
    <div
      class="card-header bg-white border-0 pt-4 px-4 pb-0 d-flex justify-content-between align-items-center flex-wrap gap-2"
    >
      <div>
        <h5 class="fw-bold text-success mb-1">Artwork Statistics</h5>
        <p class="text-muted small mb-0">Số lượng tác phẩm được thêm</p>
      </div>
      <div class="d-flex gap-2 align-items-center flex-wrap">
        <div class="input-group input-group-sm shadow-sm" style="width: 180px">
          <span class="input-group-text bg-white border-end-0">
            <i class="fa-regular fa-calendar"></i>
          </span>
          <input
            type="date"
            class="form-control border-start-0 ps-0"
            v-model="startDate"
            @change="validateDates"
            :max="endDate || undefined"
            placeholder="Từ ngày"
          />
        </div>
        <span class="text-muted fw-bold">-</span>
        <div class="input-group input-group-sm shadow-sm" style="width: 180px">
          <span class="input-group-text bg-white border-end-0">
            <i class="fa-regular fa-calendar"></i>
          </span>
          <input
            type="date"
            class="form-control border-start-0 ps-0"
            v-model="endDate"
            @change="validateDates"
            :min="startDate || undefined"
            placeholder="Đến ngày"
          />
        </div>
        <button
          class="btn btn-success btn-sm"
          @click="updateChart"
          :disabled="!startDate || !endDate || loading"
        >
          <i class="fa-solid fa-search me-1"></i>
          Xem
        </button>
      </div>
    </div>

    <div class="card-body px-4 pb-4">
      <div v-if="!startDate || !endDate" class="text-center py-5 text-muted bg-light rounded mt-3">
        <i class="fa-solid fa-filter fs-1 mb-3 opacity-25"></i>
        <p class="mb-0">Vui lòng chọn khoảng thời gian để xem thống kê tác phẩm</p>
      </div>
      <div v-else-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Đang tải dữ liệu...</p>
      </div>
      <div v-else-if="error" class="text-center py-5 text-danger">
        <i class="fa-solid fa-exclamation-triangle fs-1 mb-3"></i>
        <p>{{ error }}</p>
      </div>
      <div v-else style="height: 400px; position: relative">
        <canvas id="artworkChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import { getArtworksStats } from "@/services/statisticsService";
Chart.register(...registerables);

export default {
  name: "ArtworkStats",
  data() {
    return {
      chart: null,
      startDate: "",
      endDate: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    validateDates() {
      if (this.startDate && this.endDate && this.startDate > this.endDate) {
        this.error = "Ngày bắt đầu phải trước ngày kết thúc";
        return false;
      }
      this.error = null;
      return true;
    },
    async updateChart() {
      if (!this.startDate || !this.endDate) return;
      if (!this.validateDates()) return;

      this.loading = true;
      this.error = null;

      try {
        const response = await getArtworksStats(this.startDate, this.endDate);

        if (response && response.status === 1) {
          const chartData = response.data || [];
          
          // Set loading false BEFORE rendering chart
          this.loading = false;
          
          // Wait for DOM to update, then render chart
          await this.$nextTick();
          this.renderChart(chartData);
        } else {
          this.error = response?.message || "Không thể tải dữ liệu tác phẩm";
          this.loading = false;
        }
      } catch (err) {
        console.error("Error fetching artwork stats:", err);
        this.error = err.response?.data?.message || "Có lỗi xảy ra khi tải dữ liệu";
        this.loading = false;
      }
    },
    renderChart(data) {
      if (this.chart) this.chart.destroy();

      if (!data || data.length === 0) {
        this.error = "Không có dữ liệu trong khoảng thời gian đã chọn";
        return;
      }

      const ctx = document.getElementById("artworkChart");
      if (!ctx) return;

      const labels = data.map((item) => item.date || "");
      const counts = data.map((item) => item.count || 0);

      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Số lượng tác phẩm",
              data: counts,
              backgroundColor: "#198754",
              borderRadius: 4,
              borderWidth: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return ` ${context.parsed.y} tác phẩm`;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { borderDash: [2, 4] },
              ticks: {
                stepSize: 1,
              },
            },
            x: { grid: { display: false } },
          },
        },
      });
    },
  },
  beforeUnmount() {
    if (this.chart) this.chart.destroy();
  },
};
</script>
