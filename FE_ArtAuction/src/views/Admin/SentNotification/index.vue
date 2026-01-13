<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-1">Notification Management</h4>
      <p class="text-body-secondary mb-0">Send auction notice to users</p>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <h6 class="fw-bold text-dark mb-3">
            <i class="fa-solid fa-pen-to-square me-2 text-primary"></i>Compose a message
          </h6>
          <div class="form-floating">
            <textarea
              class="form-control bg-light border-0"
              placeholder="Soạn nội dung tin nhắn"
              id="messageContent"
              style="height: 100px"
              v-model="formData.message"
            ></textarea>
            <label for="messageContent" class="text-secondary">Compose message content</label>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <h6 class="fw-bold text-dark mb-3">
            <i class="fa-solid fa-layer-group me-2 text-info"></i>Notification form
          </h6>
          <p class="text-muted small mb-2">Select notification format</p>
          <select class="form-select bg-light border-0" v-model="formData.type">
            <option value="email">Notification via Gmail</option>
            <option value="system">Notification in the System</option>
          </select>
        </div>
      </div>

      <template v-if="formData.type === 'email'">
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body">
            <h6 class="fw-bold text-dark mb-3">
              <i class="fa-solid fa-envelope-open-text me-2 text-primary"></i>Purpose of sending
              Email
            </h6>
            <select class="form-select bg-light border-0" v-model="formData.emailType">
              <option value="auction">Auction room announcement coming soon</option>
              <option value="payment">Payment request notice</option>
            </select>
          </div>
        </div>

        <template v-if="formData.emailType === 'auction'">
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-3">
                <i class="fa-solid fa-circle-info me-2 text-warning"></i>Auction information
              </h6>
              <div class="mb-3">
                <label class="form-label small text-secondary">Auction Room Name</label>
                <input
                  type="text"
                  class="form-control bg-light border-0"
                  v-model="formData.auctionName"
                />
              </div>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label small text-secondary">Auction Day</label>
                  <input
                    type="date"
                    class="form-control bg-light border-0"
                    v-model="formData.auctionDate"
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label small text-secondary">Auction time</label>
                  <input
                    type="time"
                    class="form-control bg-light border-0"
                    v-model="formData.auctionTime"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm mb-4">
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-3">
                <i class="fa-solid fa-calendar-days me-2 text-success"></i>Auction schedule
              </h6>
              <p class="text-muted small mb-3">Related auctions</p>

              <div class="card border-0 bg-light mb-2" v-for="i in 2" :key="i">
                <div class="card-body p-2">
                  <div class="d-flex align-items-center">
                    <div class="rounded overflow-hidden me-3" style="width: 60px; height: 60px">
                      <img
                        src="https://via.placeholder.com/60x60"
                        alt="Art"
                        class="w-100 h-100 object-fit-cover"
                      />
                    </div>
                    <div>
                      <div class="d-flex align-items-center mb-1">
                        <span
                          class="badge bg-primary rounded-circle me-2"
                          style="
                            width: 20px;
                            height: 20px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                          "
                          >1</span
                        >
                        <span class="fw-bold text-dark">Starry Night</span>
                      </div>
                      <div class="small text-secondary">Author: Nguyen Van A</div>
                      <div class="small text-primary fw-bold">Starting price: 50.000đ</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </template>

      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <h6 class="fw-bold text-dark mb-3">
            <i class="fa-solid fa-user-tag me-2 text-danger"></i>Notification recipient
          </h6>

          <div v-if="formData.type === 'email'">
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="sendAllEmail"
                v-model="formData.sendToAll"
              />
              <label class="form-check-label" for="sendAllEmail">Send to all users</label>
            </div>

            <div v-if="!formData.sendToAll">
              <label class="form-label small text-secondary">Enter recipient email</label>
              <input
                type="email"
                class="form-control bg-light border-0"
                placeholder="example@gmail.com"
                v-model="formData.recipientEmail"
              />
            </div>
            <div v-else class="alert alert-primary small py-2">
              <i class="fa-solid fa-users me-2"></i>The notification will be sent to the entire
              email list in the system.
            </div>
          </div>

          <div v-else>
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="sendAllSystem"
                v-model="formData.sendToAll"
              />
              <label class="form-check-label" for="sendAllSystem">Send to all users</label>
            </div>

            <div v-if="!formData.sendToAll">
              <label class="form-label small text-secondary">Enter User ID</label>
              <input
                type="text"
                class="form-control bg-light border-0"
                placeholder="Ví dụ: USR-001, USR-002"
                v-model="formData.recipientId"
              />
              <div class="form-text">Enter the user ID to send push notifications.</div>
            </div>

            <div v-else class="alert alert-primary small py-2">
              <i class="fa-solid fa-rss me-2"></i>Push Notifications will be sent to all user
              devices.
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <h6 class="fw-bold text-dark mb-3">
            <i class="fa-solid fa-comment-dots me-2 text-secondary"></i>Custom messages
          </h6>
          <div class="form-floating">
            <textarea
              class="form-control bg-light border-0"
              placeholder="Thêm tin nhắn riêng"
              id="customNote"
              style="height: 100px"
              v-model="formData.customNote"
            ></textarea>
            <label for="customNote" class="text-secondary"
              >Add private message to notification</label
            >
          </div>
        </div>
      </div>

      <button
        type="submit"
        class="btn btn-primary w-100 py-2 fw-bold text-uppercase shadow-sm"
        style="background-color: #6f42c1; border-color: #6f42c1"
      >
        <i class="fa-solid fa-paper-plane me-2"></i> Send
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        message: "",
        type: "email",
        emailType: "auction",
        auctionName: "",
        auctionDate: "",
        auctionTime: "",
        sendToAll: false,
        recipientEmail: "",
        recipientId: "",
        customNote: "",
      },
    };
  },
  watch: {
    // Reset trạng thái khi đổi hình thức thông báo chính
    "formData.type"() {
      this.formData.sendToAll = false;
      // Nếu chuyển sang email thì reset về mặc định là đấu giá
      if (this.formData.type === "email") {
        this.formData.emailType = "auction";
      }
    },
  },
};
</script>

<style scoped>
.form-control:focus,
.form-select:focus {
  box-shadow: none;
  background-color: #fff !important;
  border: 1px solid #dee2e6 !important;
}
</style>
