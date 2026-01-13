<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4">
      <div class="mb-3 mb-md-0">
        <h4 class="fw-bold text-primary mb-1">
          <i class="fa-regular fa-calendar-days me-2"></i>Auction Schedule
        </h4>
        <p class="text-body-secondary mb-0">Manage and track auctions</p>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-white bg-white border shadow-sm text-secondary fw-medium"
          @click="goToToday"
        >
          Today
        </button>
      </div>
    </div>

    <div class="card border-0 shadow-sm mb-4 rounded-4">
      <div class="card-body py-2">
        <div class="row align-items-center g-3">
          <div class="col-12 col-md-5 d-flex align-items-center gap-3">
            <div class="btn-group">
              <button class="btn btn-light rounded-circle border" @click="prevMonth">
                <i class="fa-solid fa-chevron-left"></i>
              </button>
              <button class="btn btn-light rounded-circle border ms-2" @click="nextMonth">
                <i class="fa-solid fa-chevron-right"></i>
              </button>
            </div>
            <h4 class="mb-0 fw-bold text-dark text-uppercase">
              {{ formattedHeaderDate }}
            </h4>
          </div>
          <div
            class="col-12 col-md-7 d-flex align-items-center justify-content-md-end gap-3 flex-wrap"
          >
            <div class="d-flex align-items-center gap-2">
              <span class="badge bg-danger rounded-circle p-1"> </span
              ><small class="text-secondary bg-danger px-2 rounded-2 text-light">Live</small>
            </div>
            <div class="d-flex align-items-center gap-2">
              <span class="badge bg-warning text-dark rounded-circle p-1"> </span
              ><small class="text-secondary bg-warning px-2 rounded-2 text-dark"
                >Comming soon</small
              >
            </div>
            <div class="d-flex align-items-center gap-2">
              <span class="badge bg-secondary rounded-circle p-1"> </span
              ><small class="text-secondary bg-secondary px-2 rounded-2 text-light">Finished</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-bordered mb-0" style="table-layout: fixed">
            <thead class="bg-light text-center">
              <tr>
                <th
                  v-for="day in weekDays"
                  :key="day"
                  class="py-3 text-uppercase text-secondary small fw-bold"
                  style="width: 14.28%"
                >
                  {{ day }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(week, wIndex) in calendarGrid" :key="wIndex">
                <td
                  v-for="(dateObj, dIndex) in week"
                  :key="dIndex"
                  class="p-2 align-top cell-hover position-relative transition-base"
                  :class="getCellClass(dateObj)"
                  style="height: 130px; cursor: pointer"
                  @click="selectDate(dateObj)"
                >
                  <div class="d-flex justify-content-between align-items-start mb-1">
                    <span
                      class="fw-bold small rounded-circle d-flex align-items-center justify-content-center"
                      :class="isToday(dateObj) ? 'bg-primary text-white shadow-sm' : ''"
                      style="width: 28px; height: 28px"
                      >{{ dateObj.date.getDate() }}</span
                    >
                    <!-- <small class="text-muted opacity-0 add-icon"
                      ><i class="fa-solid fa-plus"></i
                    ></small> -->
                  </div>
                  <div
                    class="d-flex flex-column gap-1 overflow-y-auto custom-scrollbar hide-scrollbar"
                    style="max-height: 100px"
                  >
                    <div
                      v-for="event in getEventsForDate(dateObj.date)"
                      :key="event.id"
                      class="badge text-start fw-normal text-truncate w-100 p-1 border shadow-sm event-badge flex-shrink-0"
                      :class="getEventColorClass(event.status)"
                      @click.stop="viewEvent(event)"
                      :title="event.title"
                    >
                      <span class="fw-bold me-1">{{ event.time }}</span> {{ event.title }}
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="viewEventModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold text-primary">Auction details</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              id="closeViewModalBtn"
              @click="closeModal"
            ></button>
          </div>
          <div class="modal-body pt-2" v-if="selectedEvent">
            <div class="card bg-light border-0 mb-3">
              <div class="card-body">
                <h5 class="fw-bold mb-1">{{ selectedEvent.title }}</h5>
                <p class="text-muted small mb-0">ID: #EVT-{{ selectedEvent.id }}</p>
              </div>
            </div>
            <div class="d-flex align-items-center justify-content-between mb-3 p-2 border rounded">
              <span class="fw-bold text-secondary">Status</span>
              <span
                class="badge rounded-pill px-3 py-2"
                :class="getEventColorClass(selectedEvent.status)"
              >
                {{ getStatusText(selectedEvent.status) }}
              </span>
            </div>
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item px-0 d-flex justify-content-between">
                <span><i class="fa-regular fa-calendar me-2 text-secondary"></i>Date</span>
                <span class="fw-medium">{{ formatDate(selectedEvent.date) }}</span>
              </li>
              <li class="list-group-item px-0 d-flex justify-content-between">
                <span><i class="fa-regular fa-clock me-2 text-secondary"></i>Time</span>
                <span class="fw-medium">{{ selectedEvent.time }} </span>
              </li>
            </ul>
          </div>
          <div class="modal-footer border-0 bg-light">
            <button
              type="button"
              class="btn btn-outline-secondary"
              data-bs-dismiss="modal"
              @click="closeModal"
            >
              Close
            </button>
            <button
              v-if="selectedEvent && selectedEvent.status === 'live'"
              class="btn btn-danger fw-bold"
              @click="goToLive(selectedEvent.id)"
            >
              Enter Live Room
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuctionSchedule",
  data() {
    return {
      weekDays: ["Sun", "Mon", "Tues", "Wed", "Thu", "Fri", "Saturday"],
      currentDate: new Date(),

      // Danh sách sự kiện (sẽ được load từ API)
      events: [],

      selectedEvent: null,
      isLoading: false,
    };
  },

  computed: {
    // --- Logic tính toán lịch (Giữ nguyên) ---
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    calendarGrid() {
      const year = this.currentYear;
      const month = this.currentMonth;
      const firstDay = new Date(year, month, 1);
      const startDayOfWeek = firstDay.getDay();
      const startDate = new Date(firstDay);
      startDate.setDate(startDate.getDate() - startDayOfWeek);

      const weeks = [];
      let currentWeek = [];

      for (let i = 0; i < 42; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        currentWeek.push({
          date: date,
          isCurrentMonth: date.getMonth() === month,
        });
        if (currentWeek.length === 7) {
          weeks.push(currentWeek);
          currentWeek = [];
        }
      }
      return weeks;
    },
    formattedHeaderDate() {
      const date = new Date(this.currentYear, this.currentMonth);
      // 'en-US' -> Tiếng Anh, month: 'long' -> November
      return date.toLocaleDateString("en-US", { month: "long", year: "numeric" });
    },
  },

  mounted() {
    this.fetchAllAuctionRooms();
  },

  methods: {
    fetchAllAuctionRooms() {
      this.isLoading = true;
      axios
        .get("http://localhost:8081/api/admin/auction-rooms/lay-du-lieu", {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          const rawData = res.data;
          console.log("Dữ liệu gốc từ API:", rawData);

          // Map dữ liệu từ API sang cấu trúc của Lịch
          this.events = rawData.map((room) => {
            // Xử lý ngày giờ: Tách ngày (YYYY-MM-DD) và giờ (HH:mm) từ startedAt
            let dateStr = "";
            let timeStr = "";

            if (room.startedAt) {
              const dateObj = new Date(room.startedAt);
              // Format YYYY-MM-DD cho so sánh lịch
              const y = dateObj.getFullYear();
              const m = String(dateObj.getMonth() + 1).padStart(2, "0");
              const d = String(dateObj.getDate()).padStart(2, "0");
              dateStr = `${y}-${m}-${d}`;

              // Format HH:mm cho hiển thị giờ
              const hh = String(dateObj.getHours()).padStart(2, "0");
              const mm = String(dateObj.getMinutes()).padStart(2, "0");
              timeStr = `${hh}:${mm}`;
            }

            return {
              id: room.id,
              title: room.roomName,
              date: dateStr,
              time: timeStr,
              // Map trạng thái số sang chữ để dùng class màu sắc
              // 0: ended, 1: live, 2: upcoming
              status: this.mapStatus(room.status),

              // Các thông tin phụ để hiển thị modal chi tiết
              originalStatus: room.status,
              type: room.type,
              totalMembers: room.totalMembers,
              startedAt: room.startedAt,
            };
          });
        })
        .catch((err) => {
          console.error("Lỗi tải lịch trình:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // --- 2. Xử lý Modal (Không dùng Bootstrap JS để tránh lỗi) ---
    viewEvent(event) {
      this.selectedEvent = event;

      // Mở modal bằng CSS thủ công
      const modal = document.getElementById("viewEventModal");
      if (modal) {
        modal.classList.add("show");
        modal.style.display = "block";
        modal.style.backgroundColor = "rgba(0,0,0,0.5)"; // Tạo nền tối mờ
        document.body.classList.add("modal-open"); // Khóa cuộn trang
      }
    },

    closeModal() {
      const modal = document.getElementById("viewEventModal");
      if (modal) {
        modal.classList.remove("show");
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
      }
    },

    // --- Helpers ---
    mapStatus(status) {
      switch (status) {
        case 1:
          return "live"; // Đang diễn ra
        case 0:
          return "upcoming"; // Sắp tới
        case 2:
          return "ended"; // Đã kết thúc
        default:
          return "ended";
      }
    },

    getEventsForDate(date) {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, "0");
      const d = String(date.getDate()).padStart(2, "0");
      const dateStr = `${y}-${m}-${d}`;
      return this.events.filter((e) => e.date === dateStr);
    },

    getEventColorClass(status) {
      switch (status) {
        case "live":
          return "bg-danger text-white border-danger";
        case "upcoming":
          return "bg-warning text-dark border-warning";
        case "ended":
          return "bg-secondary text-white border-secondary";
        default:
          return "bg-light text-dark";
      }
    },

    getStatusText(status) {
      const map = { live: "In process", upcoming: "Comming soon", ended: "Finished" };
      return map[status] || status;
    },

    formatDate(dateStr) {
      if (!dateStr) return "---";
      const [y, m, d] = dateStr.split("-");
      return `${d}/${m}/${y}`;
    },

    // --- Calendar Navigation ---
    prevMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
    },
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
    },
    goToToday() {
      this.currentDate = new Date();
    },
    isToday(dateObj) {
      return dateObj.date.toDateString() === new Date().toDateString();
    },
    getCellClass(dateObj) {
      return dateObj.isCurrentMonth ? "bg-white" : "bg-light-subtle text-muted";
    },

    // Placeholder function cho click ngày
    selectDate(dateObj) {
      console.log("Selected date:", dateObj.date);
    },

    // Chuyển hướng vào phòng live
    goToLive(id) {
      // Xử lý chuyển trang nếu cần
      this.closeModal();
      this.$router.push(`/admin/testlivestream/${id}`);
    },
  },
};
</script>

<style scoped></style>
