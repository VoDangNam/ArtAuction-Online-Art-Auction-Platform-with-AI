<template>
  <!-- <div class="container"> -->
  <div class="row mx-3 my-3 d-flex align-items-stretch" style="height: calc(100vh - 60px)">
    <div class="col-lg-8 d-flex">
      <div class="card p-0">
        <div class="card-body p-0">
          <!-- Đặt vào phần LIVESTREAM Ở ĐÂY của cột trái -->

          <div v-if="error" class="">
            <p>{{ error }}</p>
          </div>
          <div v-else class="" ref="chatRoomElement" style="height: 95vh; width: 100%">
            <!-- <p v-if="loading">Loading live stream...</p> -->
            <!-- <div v-else id="live-stream-container" style="height: 80vh; width: 100%; background-color: #000;"></div> -->
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-4 d-flex ps-0">
      <div class="card p-0">
        <div class="card-body ps-1 pe-0">
          <div class="tabs-wrapper d-flex gap-0">
            <div class="tab-content flex-grow-1 content-box" id="auctionTabsContent">
              <!-- Tab 1: Bidding -->
              <div class="tab-pane fade show active" id="bidding" role="tabpanel" aria-labelledby="bidding-tab">
                <div class="row px-2">
                  <!-- time-start-current -->
                  <div class="col-lg-12 mb-3 mt-3 mt-lg-0">
                    <div class="card border border-2 border-success shadow-sm p-0">
                      <div class="card-body py-2">
                        <div class="alert alert-success mb-2 py-2 text-center" role="alert">
                          <strong>{{ roomID }}</strong>
                        </div>

                        <div class="row text-center">
                          <div class="col-4 p-0">
                            <div class="border-end">
                              <p class="m-1">Time</p>
                              <p class="fw-bold text-danger m-0">{{ countdownDisplay }}</p>
                            </div>
                          </div>
                          <div class="col-4 p-0">
                            <div class="border-end">
                              <p class="m-1">Start</p>
                              <p class="fw-bold m-0">
                                {{ formatUSD(artworkSession.startingPrice) }}
                              </p>
                            </div>
                          </div>
                          <div class="col-4 p-0">
                            <p class="m-1">Current</p>
                            <p class="fw-bold text-success m-0">
                              {{ formatUSD(artworkSession.currentPrice) }}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- user-hight bid -->
                  <div class="col-lg-12 mb-3">
                    <div class="card p-0">
                      <div class="card-body">
                        <div class="d-flex justify-content-between">
                          <p class="m-0">Username</p>
                          <p class="m-0">Hight</p>
                        </div>
                        <hr class="my-2 fw-bold" />
                        <div class="d-flex justify-content-between">
                          <p class="m-0">{{ artworkSession.highestBidderUsername }}</p>
                          <!-- <p class="m-0">{{ artworkSession.winnerId }}</p> -->
                          <!-- <p class="m-0">{{ winnerName }}</p> -->
                          <p class="m-0 fw-bold text-success">
                            {{ formatUSD(artworkSession.currentPrice) }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- đặt giá nhanh - chỉ hiển thị khi user trong room (status === 1) -->
                  <template v-if="userCheckInRoomStatus === 1">
                    <div v-for="(value, index) in quickBidButtons" :key="index"
                      :class="index < 3 ? 'col-4 mb-2' : 'col-4'">
                      <div class="card p-0 quick-bid-btn" :class="{ 'quick-bid-active': selectedQuickBid === value }"
                        @click="setQuickBid(value)">
                        <div class="card-body py-2 text-center">
                          <p class="m-0">{{ formatUSD(value) }}</p>
                        </div>
                      </div>
                    </div>

                    <!-- đặt giá -->
                    <div class="col-lg-12 mt-3">
                      <div class="input-group border border-2 border-success rounded-3 shadow-sm">
                        <input v-model="bidAmount" type="number" class="form-control"
                          :placeholder="'minimum is ' + formatUSD(artworkSession.bidStep)" aria-label="Bid Amount"
                          aria-describedby="button-bid" />
                        <button @click="datGia" class="btn btn-success" :disabled="isPlacingBid">
                          <i v-if="isPlacingBid" class="fas fa-spinner fa-spin me-2"></i>
                          <i v-else class="fas fa-gavel me-2"></i>
                          {{ isPlacingBid ? "Đang đặt giá..." : "Place" }}
                        </button>
                      </div>
                    </div>
                  </template>

                  <!-- detail-artwork -->
                  <div class="col-lg-12 mt-3">
                    <div class="card bg-transparent border border-2 border-success shadow-sm p-0" data-bs-toggle="modal"
                      data-bs-target="#exampleModal">
                      <div class="card-body d-flex justify-content-center align-items-center gap-2 p-2">
                        <img :src="artworkSession.imageUrl ||
                          'https://i.pinimg.com/736x/8b/a0/d6/8ba0d6ee7608f8caa427a819de41638a.jpg'
                          " class="img-thumbnail" style="max-height: 250px;" alt="" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Tab 2: Chat - chỉ hiển thị khi user trong room (status === 1) -->
              <div v-if="userCheckInRoomStatus === 1" class="tab-pane fade chat-tab-pane" id="chat" role="tabpanel" aria-labelledby="chat-tab">
                <div class="row h-100 m-0">
                  <div class="col-lg-12 h-100 p-0">
                    <div class="card p-0 border border-2 border-success shadow-sm h-100 d-flex flex-column">
                      <div class="card-header bg-success text-white py-3">
                        <div class="d-flex justify-content-between align-items-center">
                          <div class="d-flex align-items-center gap-2">
                            <i class="fa-solid fa-comments fa-lg"></i>
                            <h5 class="mb-0">Live Chat</h5>
                          </div>
                          <div class="d-flex gap-2">
                            <span class="badge bg-white text-success">
                              <i class="fa-solid fa-users me-1"></i>{{ messages.length }} messages
                            </span>
                          </div>
                        </div>
                      </div>
                      <div class="card-body chat-content p-3 flex-grow-1" ref="chatMessages" style="
                          overflow-y: auto;
                          background-color: #f8f9fa;
                          display: flex;
                          flex-direction: column;
                        ">
                        <div style="flex: 1; min-height: 0"></div>
                        <template v-for="(m, idx) in messages" :key="idx">
                          <!-- Message from others -->
                          <div v-if="!m.mine" class="mb-3">
                            <div class="d-flex align-items-start">
                              <div
                                class="avatar-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2"
                                style="
                                  width: 36px;
                                  height: 36px;
                                  min-width: 36px;
                                  border-radius: 50%;
                                  font-size: 14px;
                                  font-weight: bold;
                                ">
                                {{ (m.senderName || "A").charAt(0).toUpperCase() }}
                              </div>
                              <div class="flex-grow-1">
                                <div class="d-flex align-items-center gap-2 mb-1">
                                  <small class="fw-semibold text-dark">{{
                                    m.senderName || "Admin"
                                    }}</small>
                                  <button v-if="
                                    isAdmin &&
                                    m.senderId &&
                                    m.senderId !== adminId &&
                                    m.senderId !== adminEmail
                                  " class="btn btn-link btn-sm ms-2 p-0 text-decoration-none"
                                    @click="replyToUser(m.senderId)" title="Reply this user">
                                    <i class="fa-solid fa-reply"></i> Reply
                                  </button>
                                </div>
                                <div class="d-flex gap-2 align-items-end justify-content-start">
                                  <div class="chat-bubble-left">
                                    {{ m.text }}
                                  </div>
                                  <small class="text-muted" style="font-size: 0.75rem">{{
                                    m.time
                                    }}</small>
                                </div>
                              </div>
                            </div>
                          </div>

                          <!-- My message -->
                          <div v-else class="mb-3">
                            <div class="d-flex align-items-start justify-content-end">
                              <div class="flex-grow-1 text-end">
                                <div class="d-flex align-items-center gap-2 justify-content-end mb-1">
                                  <small class="fw-semibold text-dark">{{
                                    m.senderName || "You"
                                    }}</small>
                                </div>

                                <div class="d-flex gap-2 align-items-end justify-content-end">
                                  <small class="text-muted" style="font-size: 0.75rem">{{
                                    m.time
                                    }}</small>
                                  <div class="chat-bubble-right">
                                    {{ m.text }}
                                  </div>
                                </div>
                              </div>
                              <div
                                class="avatar-circle bg-success text-white d-flex align-items-center justify-content-center ms-2"
                                style="
                                  width: 36px;
                                  height: 36px;
                                  min-width: 36px;
                                  border-radius: 50%;
                                  font-size: 14px;
                                  font-weight: bold;
                                ">
                                {{ (m.senderName || "Y").charAt(0).toUpperCase() }}
                              </div>
                            </div>
                          </div>
                        </template>

                        <!-- Admin controls - di chuyển xuống dưới để dễ thao tác -->
                        <div v-if="isAdmin" class="admin-controls mb-3 p-2 bg-light rounded">
                          <div class="d-flex align-items-center gap-2 mb-2">
                            <label class="form-label mb-0 small">Reply to:</label>
                            <select v-model="selectedUserId" class="form-select form-select-sm" style="width: auto">
                              <option value="">Broadcast to All</option>
                              <option v-for="user in uniqueUsers" :key="user.id" :value="user.id">
                                {{ user.name }} ({{ user.role }})
                              </option>
                            </select>
                            <button v-if="selectedUserId" class="btn btn-sm btn-outline-secondary"
                              @click="selectedUserId = null" title="Switch to broadcast">
                              Broadcast
                            </button>
                          </div>
                          <div class="small text-muted">
                            Target:
                            {{
                              selectedUserId
                                ? getUserName(selectedUserId) + " (direct)"
                                : "All users (broadcast)"
                            }}
                          </div>
                        </div>
                      </div>
                      <div class="card-footer bg-white border-top p-3">
                        <div class="input-group">
                          <input v-model="text" @keyup.enter="sendMsg" type="text" class="form-control" :placeholder="isAdmin
                              ? selectedUserId
                                ? `Reply to ${getUserName(selectedUserId)}`
                                : 'Broadcast to all users...'
                              : 'Type your message...'
                            " />
                          <button @click="sendMsg" class="btn btn-success" :disabled="!text || !text.trim()">
                            <i class="fa-solid fa-paper-plane me-2"></i>Send
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Tab 3: Members - chỉ hiển thị khi user trong room (status === 1) -->
              <div v-if="userCheckInRoomStatus === 1" class="tab-pane fade members-tab-pane" id="members" role="tabpanel" aria-labelledby="members-tab">
                <div class="row m-0 px-2">
                  <div class="col-lg-12 p-0 mb-3">
                    <div class="card p-0 d-flex flex-column border border-2 border-success">
                      <div class="card-body d-flex justify-content-between align-items-center" style="overflow-y: auto">
                        <div class="d-flex align-items-center gap-2">
                          <i class="fa-solid fa-users fa-lg"></i>
                          <h5 class="mb-0">Members</h5>
                          <span class="badge border border-2 border-success text-success">
                            {{ members.length }} joined
                          </span>
                        </div>
                        <button class="btn btn-outline-success btn-sm px-3 py-2 d-flex align-items-center gap-2"
                          :disabled="membersLoading" @click="loadMembers">
                          <i v-if="membersLoading" class="fas fa-spinner fa-spin"></i>
                          <i v-else class="fa-solid fa-rotate"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="col-12 p-0">
                    <div class="card p-0">
                      <div class="card-body">
                        <div class="p-4 text-center text-muted" v-if="membersLoading">
                          <i class="fas fa-spinner fa-spin fa-2x text-success mb-2"></i>
                          <p class="m-0">Loading members...</p>
                        </div>
                        <div v-else-if="membersError" class="alert alert-danger m-3">
                          {{ membersError }}
                        </div>
                        <div v-else-if="!members.length" class="p-4 text-center text-muted">
                          <i class="fa-solid fa-user-slash fa-2x mb-2"></i>
                          <p class="m-0">No participants have joined yet.</p>
                        </div>
                        <ul v-else class="list-group list-group-flush px-2">
                          <li v-for="member in members" :key="member.id || member.userId || member.email"
                            class="list-group-item d-flex justify-content-between align-items-center gap-2 flex-wrap px-0">
                            <div class="me-auto">
                              <p class="m-0 fw-semibold">{{ getMemberDisplayName(member) }}</p>
                              <small class="text-muted">{{
                                member.role || member.type || "Participant"
                                }}</small>
                            </div>
                            <div class="d-flex align-items-center gap-2">
                              <span class="badge bg-success" v-if="member.status">
                                {{ member.status }}
                              </span>
                              <button class="btn btn-outline-danger btn-sm px-3" @click="openReportModal(member)">
                                <i class="fa-solid fa-flag"></i>
                              </button>
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tabs Navigation (Right Side) -->
            <div class="tabs-sidebar px-3">
              <!-- Logo -->
              <div class="logo-container text-center mb-3">
                <img
                  src="@/assets/img/Logo_AA.png"
                  alt="ArtAuction Logo"
                  @click="goToHome"
                  style="width: 45px; cursor: pointer; transition: transform 0.2s;"
                  @mouseover="$event.target.style.transform = 'scale(1.1)'"
                  @mouseleave="$event.target.style.transform = 'scale(1)'"
                  title="Về trang chủ"
                />
              </div>

              <ul class="nav nav-tabs flex-column" id="auctionTabs" role="tablist">
                <li class="nav-item" role="presentation">
                  <button class="nav-link active" id="bidding-tab" data-bs-toggle="tab" data-bs-target="#bidding"
                    type="button" role="tab" aria-controls="bidding" aria-selected="true" title="Đặt giá">
                    <i class="fa-solid fa-gavel"></i>
                  </button>
                </li>
                <li v-if="userCheckInRoomStatus === 1" class="nav-item" role="presentation">
                  <button class="nav-link" id="chat-tab" data-bs-toggle="tab" data-bs-target="#chat" type="button"
                    role="tab" aria-controls="chat" aria-selected="false" title="Chat">
                    <i class="fa-solid fa-comments"></i>
                  </button>
                </li>
                <li v-if="userCheckInRoomStatus === 1" class="nav-item" role="presentation">
                  <button class="nav-link" id="members-tab" data-bs-toggle="tab" data-bs-target="#members" type="button"
                    role="tab" aria-controls="members" aria-selected="false" title="Members list">
                    <i class="fa-solid fa-users"></i>
                  </button>
                </li>
              </ul>
            </div>
            <!-- End Tabs Navigation -->
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- </div> -->
  <!-- Report Member Modal (Custom) -->
  <div v-if="showReportModal" class="custom-report-modal">
    <div class="modal-backdrop fade show" @click="closeReportModal()"></div>
    <div class="modal fade show d-block" tabindex="-1" role="dialog" @click.self="closeReportModal()">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-success fw-bold">
              Report {{ getMemberDisplayName(reportForm.member) }}
            </h5>
            <button type="button" class="btn-close" @click="closeReportModal" :disabled="reportSubmitting"
              aria-label="Close"></button>
          </div>
          <form @submit.prevent="submitMemberReport">
            <div class="modal-body">
              <div class="mb-4">
                <p class="form-label mb-2">Report Type <span class="text-danger">*</span></p>
                <select class="form-select" v-model="reportForm.reportType" :disabled="reportSubmitting" required>
                  <option v-for="type in reportTypes" :key="type" :value="type">{{ type }}</option>
                </select>
              </div>
              <div class="mb-4">
                <p class="form-label mb-2">Reason <span class="text-danger">*</span></p>
                <textarea class="form-control" v-model.trim="reportForm.reason" rows="4" :class="{
                  'is-invalid':
                    showReportErrors && (!reportForm.reason || !reportForm.reason.trim()),
                }" :disabled="reportSubmitting" placeholder="Describe the issue in detail" required></textarea>
                <div class="invalid-feedback">Please describe the issue.</div>
              </div>
              <div class="mb-4">
                <p class="form-label mb-2">Evidence (optional)</p>
                <input type="file" class="form-control" accept="image/*" @change="handleReportFileChange"
                  :disabled="reportSubmitting" ref="reportEvidenceInput" />
                <small class="text-muted" v-if="reportForm.evidence">
                  Selected: {{ reportForm.evidence.name }}
                </small>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-outline-secondary" @click="closeReportModal"
                :disabled="reportSubmitting">
                Cancel
              </button>
              <button type="submit" class="btn btn-danger" :disabled="reportSubmitting || !isReportFormValid">
                <i v-if="reportSubmitting" class="fas fa-spinner fa-spin me-2"></i>
                Submit Report
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
      <div class="modal-content">
        <!-- <div class="modal-header">
          <h1 class="modal-title fs-4 fw-bold text-success text-center" id="exampleModalLabel">Artwork Information</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div> -->
        <div class="modal-header position-relative">
          <h1 class="modal-title fs-4 text-success text-center fw-bold w-100 m-0" id="postModalLabel">
            Artwork Information
          </h1>
          <button type="button" class="btn-close position-absolute end-0 me-3" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <!-- Cột hình ảnh -->
            <div class="col-lg-6 d-flex justify-content-center align-items-center">
              <img :src="artworkDetail.avtArtwork ||
                'https://i.pinimg.com/736x/8b/a0/d6/8ba0d6ee7608f8caa427a819de41638a.jpg'
                " class="img-thumbnail" style="max-height: 450px; object-fit: cover" alt="Artwork" />
            </div>

            <!-- Cột thông tin -->
            <div class="col-lg-6 d-flex flex-column gap-3">
              <div class="alert alert-success mt-3 py-2" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                  <p class="m-0">Starting Price</p>
                  <p class="m-0 fw-bold">{{ formatUSD(artworkDetail.startedPrice || 0) }}</p>
                </div>
              </div>

              <h4 class="fw-bold text-success m-0">
                {{ artworkDetail.title || "Untitled Artwork" }}
              </h4>

              <div class="d-flex justify-content-between align-items-center">
                <p class="m-0 text-success fw-bold">Artist</p>
                <p class="m-0">{{ artworkDetail.ownerId || "Unknown" }}</p>
              </div>

              <div class="d-flex justify-content-between align-items-center">
                <p class="m-0 text-success fw-bold">Category</p>
                <p class="m-0">{{ artworkDetail.paintingGenre || "N/A" }}</p>
              </div>

              <div class="d-flex justify-content-between align-items-center">
                <p class="m-0 text-success fw-bold">Year Created</p>
                <p class="m-0">{{ artworkDetail.yearOfCreation || "N/A" }}</p>
              </div>

              <!-- Material (optional) -->
              <div class="d-flex justify-content-between align-items-center" v-if="artworkDetail.material">
                <p class="m-0 text-success fw-bold">Material</p>
                <p class="m-0">{{ artworkDetail.material }}</p>
              </div>

              <!-- Size (optional) -->
              <div class="d-flex justify-content-between align-items-center" v-if="artworkDetail.size">
                <p class="m-0 text-success fw-bold">Size</p>
                <p class="m-0">{{ artworkDetail.size }}</p>
              </div>

              <div class="d-flex flex-column gap-2">
                <p class="m-0 text-success fw-bold">Description</p>

                <p class="m-0" style="text-align: justify">
                  {{ artworkDetail.description || "No description available." }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import ChatSocket from "../../../socket";
import { ZegoUIKitPrebuilt } from "@zegocloud/zego-uikit-prebuilt";
// const auctionId = ref('auction-001');

export default {
  name: "AuctionRoom",
  inheritAttrs: false,
  // props: ["id"],
  data() {
    return {
      // roomId: "support:auction-001-userA",
      roomID: this.$route.params.id,
      roomId: null, // Room ID cho chat (sẽ được set = roomID)

      detail_auction: {},
      artworkSession: {}, // Thông tin artwork từ session
      artworkDetail: {}, // Thông tin chi tiết artwork từ API /artwork/by-session

      roomStatusInterval: null, // Interval để check trạng thái phòng
      refreshInterval: 5000, // Thời gian refresh (ms) - có thể chỉnh: 3000 = 3 giây

      // === COUNTDOWN CONFIG ===
      COUNTDOWN_DURATION_MINUTES: 3, // Thời gian countdown ban đầu (phút) - Có thể đổi: 15, 20, 30, v.v.
      TIME_EXTENSION_THRESHOLD_MINUTES: 2, // Ngưỡng thời gian để kéo dài (phút) - Nếu còn dưới giá trị này thì kéo dài
      TIME_EXTENSION_AMOUNT_MINUTES: 1, // Thời gian kéo dài mỗi lần (phút)

      role: "audience", // or "host"
      loading: false,
      error: null,
      inviteLink: "",

      client: null,
      connected: false,
      messages: [],
      text: "",

      // === USER INFO ===
      currentUserId: null,
      currentUserEmail: null,
      currentUsername: null,

      joined: false,
      snapshot: null,

      // === ADMIN CONFIG ===
      adminId: "U-4019812134200", // Admin ID từ database
      adminEmail: "connchonam@example.com", // Admin email để nhận diện
      adminUsername: "john_sins", // Admin username để nhận diện

      // === CHAT STATE ===
      isAdmin: false, // User hiện tại có phải admin không
      selectedUserId: null, // User được admin chọn để reply (null = broadcast)

      // === MEMBERS STATE ===
      members: [],
      membersLoading: false,
      membersError: null,
      reportingMemberId: null,
      showReportModal: false,
      reportSubmitting: false,
      showReportErrors: false,
      reportForm: {
        member: null,
        reportType: "",
        reason: "",
        evidence: null,
      },
      reportTypes: [
        "Fake Identity",
        "Suspicious Activity",
        "Scam / Fraud",
        "Harassment / Abusive Behavior",
        "Policy Violation",
        "Spam / Unwanted Ads",
        "Unauthorized Access",
        "Other",
      ],

      // === BID STATE ===
      bidAmount: "", // Giá trị bid người dùng nhập
      isPlacingBid: false, // Trạng thái đang đặt giá
      selectedQuickBid: null, // Nút đặt giá nhanh được chọn

      // === COUNTDOWN TIMER ===
      countdownSeconds: 0, // Số giây còn lại (từ WebSocket)
      countdownInterval: null, // Interval cho countdown
      lastBidPrice: 0, // Giá bid cuối cùng để detect bid mới

      sessionEndTime: null, // Thời gian kết thúc session từ WebSocket

      // === AUCTION WEBSOCKET ===
      auctionSocket: null,
      auctionRoomSubscription: null,
      auctionBidsSubscription: null,

      // === USER CHECK IN ROOM ===
      userCheckInRoomStatus: null, // null = chưa check, 0 = không trong room, 1 = trong room
    };
  },

  async mounted() {
    // === INITIALIZATION ===
    // Đảm bảo roomID được set từ route params trước
    this.roomID = this.$route.params.id;
    // Đảm bảo roomId cũng được set ngay từ đầu
    this.roomId = this.roomID;

    console.log("🚀 User Auction Room mounted with roomID:", this.roomID, "roomId:", this.roomId);

    this.initializeUser();
    this.loadFromCache();
    await this.loadHistory();
    this.connectSocket();

    this.loadArtworkBySession();

    // Kết nối WebSocket cho auction countdown
    this.connectAuctionWebSocket();

    const url = new URL(window.location.href);
    const params = Object.fromEntries(url.searchParams.entries());
    // Ép Zego dùng đúng id phòng theo route thay vì random/query
    this.role = params.role ?? "audience";
    this.loadAuctionRoom();
    this.loadMembers();
    this.startLiveStream();

    // Check user trong room
    this.checkUserInRoom();

    // Bắt đầu check trạng thái phòng liên tục
    this.startRoomStatusCheck();

    // Scroll to bottom sau khi load xong
    this.$nextTick(() => {
      setTimeout(() => {
        this.scrollToBottom();
      }, 500);
    });
  },
  beforeUnmount() {
    // Clear interval check status phòng
    if (this.roomStatusInterval) {
      clearInterval(this.roomStatusInterval);
      this.roomStatusInterval = null;
    }

    // Clear countdown interval
    this.stopCountdownInterval();

    // Cleanup socket
    if (this.socket) {
      this.socket.deactivate();
    }

    // Cleanup auction WebSocket
    this.disconnectAuctionWebSocket();
  },
  watch: {
    // Tự động scroll xuống khi có tin nhắn mới
    messages: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      deep: true,
    },

    // Detect bid mới để hiển thị thông báo

    "artworkSession.currentPrice": function (newPrice, oldPrice) {
      // Kiểm tra nếu giá thay đổi và lớn hơn giá cũ (có bid mới)
      if (newPrice && oldPrice && newPrice > oldPrice) {
        console.log(
          "🔥 Bid mới! Giá tăng từ",
          this.formatUSD(oldPrice),
          "lên",
          this.formatUSD(newPrice)
        );
      }
    },
  },
  methods: {
    formatUSD(number) {
      // Đổi sang format tiền Việt (VND)
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(number || 0);
    },

    // Navigate to home page
    goToHome() {
      this.$router.push('/');
    },

    // === COUNTDOWN METHODS ===

    // Khởi tạo countdown từ WebSocket hoặc session data
    initializeCountdown() {
      // ⚠️ CHỈ khởi tạo countdown nếu session đang LIVE (status = 1)
      if (!this.artworkSession || this.artworkSession.status !== 1) {
        console.log("⏸️ Session chưa bắt đầu (status !== 1), không khởi tạo countdown");
        console.log("Session status:", this.artworkSession?.status);
        // Dừng countdown nếu đang chạy
        this.stopCountdownInterval();
        this.countdownSeconds = 0;
        this.sessionEndTime = null;
        return;
      }

      console.log("🚀 Session đang LIVE (status = 1), khởi tạo countdown...");

      // Ưu tiên dùng endedAt từ session (nếu có)
      if (this.artworkSession.endedAt) {
        this.sessionEndTime = new Date(this.artworkSession.endedAt);
        this.updateCountdownFromEndTime();

        this.startCountdownInterval();
        console.log("✅ Countdown initialized from endedAt:", this.countdownSeconds, "seconds");
        return;
      }

      // Fallback: Dùng startTime + durationSeconds
      const timeField =
        this.artworkSession.startTime ||
        this.artworkSession.start_time ||
        this.artworkSession.createdAt ||
        this.artworkSession.created_at;

      if (!timeField) {
        console.warn("⚠️ Không tìm thấy trường startTime hoặc endedAt trong session!");
        console.log("Session object:", this.artworkSession);
        // Không khởi tạo countdown, đợi WebSocket
        return;
      }

      // Tính endTime từ startTime + durationSeconds
      const durationSeconds =
        this.artworkSession.durationSeconds || this.COUNTDOWN_DURATION_MINUTES * 60;
      const startTime = new Date(timeField).getTime();
      const endTime = startTime + durationSeconds * 1000; // milliseconds

      this.sessionEndTime = new Date(endTime);
      this.updateCountdownFromEndTime();
      this.lastBidPrice = this.artworkSession.currentPrice || 0;

      console.log("✅ Countdown initialized:", this.countdownSeconds, "seconds");
      console.log("Start time:", new Date(timeField).toLocaleString("vi-VN"));
      console.log(`End time:`, this.sessionEndTime.toLocaleString("vi-VN"));

      // Bắt đầu countdown interval
      this.startCountdownInterval();
    },

    updateCountdownFromEndTime() {
      if (!this.sessionEndTime) return;

      const now = new Date();
      const endTime = new Date(this.sessionEndTime);
      const remainingMs = endTime.getTime() - now.getTime();
      this.countdownSeconds = Math.max(0, Math.floor(remainingMs / 1000));
    },

    // Kéo dài countdown - Giờ được xử lý bởi WebSocket từ server
    extendCountdown() {
      // Method này giữ lại để tương thích, nhưng logic extend được xử lý bởi WebSocket
      console.log("⏱️ Countdown extension handled by WebSocket");
    },

    // Tính lại countdown theo thời gian thực từ server
    recalculateCountdown() {
      // Không làm gì cả - để countdown tự đếm ngược
      // Chỉ extendCountdown() sẽ can thiệp khi còn dưới TIME_EXTENSION_THRESHOLD_MINUTES và có bid mới
      return;
    },

    // Bắt đầu countdown interval (cập nhật mỗi giây)
    startCountdownInterval() {
      // Clear interval cũ nếu có
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
      }

      console.log("🚀 Starting countdown interval...");

      // Tạo interval mới - cập nhật từ sessionEndTime
      this.countdownInterval = setInterval(() => {
        if (this.sessionEndTime) {
          this.updateCountdownFromEndTime();

          // Log mỗi 10 giây để theo dõi

          if (this.countdownSeconds > 0 && this.countdownSeconds % 10 === 0) {
            console.log("⏱️ Countdown:", this.countdownSeconds, "seconds remaining");
          }

          // Hết thời gian
          if (this.countdownSeconds <= 0) {
            this.stopCountdownInterval();
            console.log("⏰ Hết thời gian đấu giá!");
            this.$toast?.warning?.("⏰ Hết thời gian đấu giá!");
          }
        } else {
          // Không có sessionEndTime, dừng interval
          this.stopCountdownInterval();
        }
      }, 1000); // Cập nhật mỗi giây
    },

    // Dừng countdown interval
    stopCountdownInterval() {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
      }
    },

    // Gọi API dừng session
    stopSession() {
      // Lấy sessionId từ artworkSession
      const sessionId = this.artworkSession?.sessionId || this.artworkSession?.id;

      if (!sessionId) {
        console.error("❌ Không tìm thấy sessionId để dừng session");
        this.$toast?.error?.("Không thể dừng session: Thiếu sessionId");
        return;
      }

      console.log("🛑 Đang dừng session:", sessionId);

      axios
        .post(
          `http://localhost:8081/api/stream/stop-session/${sessionId}`,
          {},
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        )
        .then((res) => {
          console.log("✅ Session đã dừng thành công:", res.data);
          this.$toast?.success?.("Session đấu giá đã kết thúc!");

          // Có thể redirect về trang kết quả hoặc làm gì đó khác
          // setTimeout(() => {
          //   this.$router.push('/');
          // }, 2000);
        })
        .catch((err) => {
          console.error("❌ Lỗi khi dừng session:", err);
          this.$toast?.error?.(
            "Lỗi khi dừng session: " + (err.response?.data?.message || err.message)
          );
        });
    },

    loadAuctionRoom() {
      axios
        .get("http://localhost:8081/api/stream/room/" + this.roomID, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.detail_auction = res.data;
          console.log("Room details loaded:", this.detail_auction);
          // Load artwork nếu có sessionId trong detail_auction
          if (res.data.sessionId) {
            console.log("Session ID:", res.data.sessionId);
            this.loadArtworkBySession("Artwork session loaded:", res.data.sessionId);
          }
        })
        .catch((err) => {
          console.error("Error loading room details:", err);
          if (err.response?.status === 404) {
            this.$toast?.error?.("Không tìm thấy phòng đấu giá");
            this.$router?.push?.("/");
          } else {
            this.$toast?.error?.(err.response?.data?.message || "Lỗi khi tải thông tin phòng");
          }
        });
    },
    loadArtworkBySession() {
      axios
        .get("http://localhost:8081/api/stream/room/" + this.roomID + "/sessions/current-or-next", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.artworkSession = res.data;
          console.log("📦 Artwork session loaded:", this.artworkSession);

          // Lấy thông tin chi tiết artwork từ API mới
          if (res.data.id) {
            this.loadArtworkDetailBySessionId(res.data.id);
          }

          // Khởi tạo countdown sau khi load session thành công
          this.$nextTick(() => {
            this.initializeCountdown();

            // Subscribe to bids cho session này nếu WebSocket đã kết nối
            if (this.auctionSocket && this.auctionSocket.connected && res.data.id) {
              this.subscribeToSessionBids(res.data.id);
            }
          });
        })
        .catch((err) => {
          console.error("Error loading artwork session:", err);
          if (err.response?.status !== 404) {
            this.$toast?.error?.(err.response?.data?.message || "Lỗi khi tải thông tin artwork");
          }
        });
    },

    // === LOAD CHI TIẾT ARTWORK TỪ API MỚI ===
    loadArtworkDetailBySessionId(sessionId) {
      console.log("🎨 Loading artwork detail for session:", sessionId);

      axios
        .get(`http://localhost:8081/api/artwork/by-session/${sessionId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.artworkDetail = res.data;
          console.log("✅ Artwork detail loaded:", this.artworkDetail);
          console.log("📝 Title:", this.artworkDetail.title);
          console.log("🖼️ Image URL:", this.artworkDetail.artworkUrl);
          console.log("💰 Started Price:", this.artworkDetail.startedPrice);
          console.log("🎨 Genre:", this.artworkDetail.paintingGenre);
          console.log("📅 Year:", this.artworkDetail.yearOfCreation);
          console.log("🧑‍🎨 Owner ID:", this.artworkDetail.ownerId);
          console.log(this.artworkDetail, "sdvsdv");
        })
        .catch((err) => {
          console.error("❌ Error loading artwork detail:", err);
          if (err.response?.status !== 404) {
            this.$toast?.error?.("Không thể tải thông tin chi tiết tác phẩm");
          }
        });
    },

    async loadMembers() {
      if (!this.roomID) return;

      this.membersLoading = true;
      this.membersError = null;

      try {
        const response = await axios.post(
          `http://localhost:8081/api/auctionroom/members`,
          {
            roomId: this.roomID
          },
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        );

        console.log('📦 Raw API response:', response.data);

        // API trả về array trực tiếp: [{ id, username, avt }]
        const payload = response.data;
        let membersList = [];

        if (Array.isArray(payload)) {
          // Response là array trực tiếp
          membersList = payload;
        } else if (Array.isArray(payload?.data)) {
          // Response có data wrapper
          membersList = payload.data;
        } else if (Array.isArray(payload?.members)) {
          // Response có members property
          membersList = payload.members;
        } else {
          membersList = [];
        }

        // Map và normalize member data để đảm bảo có đầy đủ thông tin
        this.members = membersList.map(member => ({
          id: member.id || member.userId || member.user_id || null,
          userId: member.id || member.userId || member.user_id || null,
          username: member.username || member.userName || null,
          name: member.name || member.fullName || member.displayName || member.username || null,
          displayName: member.displayName || member.name || member.fullName || member.username || null,
          fullName: member.fullName || member.name || member.displayName || member.username || null,
          email: member.email || null,
          avt: member.avt || member.avatar || member.avatarUrl || null,
          role: member.role || member.type || "Participant",
          status: member.status || null,
        }));

        console.log('✅ Members loaded:', this.members.length, this.members);
      } catch (error) {
        console.error("❌ Error loading members:", error);
        this.membersError = error.response?.data?.message || "Could not load member list";
        this.members = [];
      } finally {
        this.membersLoading = false;
      }
    },

    async checkUserInRoom() {
      if (!this.roomID) return;

      try {
        const response = await axios.get(
          `http://localhost:8081/api/user/check-in-room/${this.roomID}`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        );

        const data = response.data;
        this.userCheckInRoomStatus = data.status || 0;
        console.log("✅ User check in room status:", this.userCheckInRoomStatus, data.message);
      } catch (error) {
        console.error("❌ Error checking user in room:", error);
        // Nếu lỗi, mặc định là không trong room (status = 0)
        this.userCheckInRoomStatus = 0;
      }
    },

    getMemberDisplayName(member) {
      if (!member) return "Unknown user";

      return (
        member.displayName ||
        member.username ||
        member.fullName ||
        member.name ||
        member.email ||
        member.userId ||
        "Unknown user"
      );
    },

    openReportModal(member) {
      this.reportForm.member = member;
      this.reportForm.reportType = this.reportTypes[0] || "Other";
      this.reportForm.reason = "";
      this.reportForm.evidence = null;
      this.reportingMemberId = member?.id || member?.userId || member?.email || null;
      this.showReportErrors = false;
      this.showReportModal = true;
    },

    closeReportModal(force = false) {
      if (!force && this.reportSubmitting) return;
      this.resetReportModalState();
    },

    handleReportFileChange(event) {
      const file = event.target?.files?.[0] || null;
      this.reportForm.evidence = file;
    },

    async submitMemberReport() {
      if (!this.reportForm.member || !this.roomID) return;

      const memberIdentifier =
        this.reportForm.member.id || this.reportForm.member.userId || this.reportForm.member.email;

      if (!memberIdentifier) {
        this.$toast?.error?.("Không xác định được người cần báo cáo");
        return;
      }

      if (!this.isReportFormValid) {
        this.showReportErrors = true;
        this.$toast?.warning?.("Vui lòng điền đầy đủ thông tin báo cáo");
        return;
      }

      const formData = new FormData();
      formData.append("reportType", this.reportForm.reportType || "Other");
      formData.append("reportedEntityId", memberIdentifier);
      formData.append("reason", this.reportForm.reason.trim());
      formData.append("entityType", "USER");
      if (this.reportForm.evidence) {
        formData.append("image", this.reportForm.evidence);
      }

      this.reportSubmitting = true;

      try {
        await axios.post("http://localhost:8081/api/reports/user", formData, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
            "Content-Type": "multipart/form-data",
          },
        });

        this.$toast?.success?.("Đã gửi báo cáo người dùng");
        this.closeReportModal(true);
      } catch (error) {
        console.error("Error reporting member:", error);
        this.$toast?.error?.(error.response?.data?.message || "Không thể báo cáo người dùng");
      } finally {
        this.reportSubmitting = false;
      }
    },

    resetReportModalState() {
      this.showReportModal = false;
      this.reportingMemberId = null;
      this.reportForm.member = null;
      this.reportForm.reportType = this.reportTypes[0] || "Other";
      this.reportForm.reason = "";
      this.reportForm.evidence = null;
      this.showReportErrors = false;
      if (this.$refs.reportEvidenceInput) {
        this.$refs.reportEvidenceInput.value = "";
      }
    },

    // === BID METHODS ===

    // Đặt giá nhanh - Giá hiện tại + giá trị nút
    setQuickBid(amount) {
      const currentPrice = this.artworkSession.currentPrice || 0;
      const newBidAmount = currentPrice + amount;
      this.bidAmount = newBidAmount;
      this.selectedQuickBid = amount; // Lưu nút được chọn để highlight

      console.log(
        `🚀 Quick bid: ${this.formatUSD(currentPrice)} + ${this.formatUSD(
          amount
        )} = ${this.formatUSD(newBidAmount)}`
      );
    },

    datGia() {
      if (this.isPlacingBid) return;

      // Kiểm tra có nhập giá không
      if (!this.bidAmount || this.bidAmount <= 0) {
        this.$toast.error("Vui lòng nhập giá đấu giá hợp lệ!");
        return;
      }

      // Kiểm tra có room ID không
      if (!this.roomID) {
        this.$toast.error("Chưa có phòng đấu giá. Vui lòng kiểm tra lại.");
        return;
      }

      this.isPlacingBid = true;

      axios
        .post(
          "http://localhost:8081/api/bids/" + this.roomID + "/place",
          {
            amount: Number(this.bidAmount),
          },
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        )
        .then((res) => {
          if (res.data.result) {
            console.log("Bid placed successfully", res.data);
            this.$toast.success(res.data.message);
            this.bidAmount = ""; // Reset giá sau khi đặt thành công
            this.selectedQuickBid = null; // Reset nút được chọn

            // Kéo dài countdown nếu còn dưới 2 phút
            this.extendCountdown();
          } else {
            this.$toast.error(res.data.message);
          }
        })
        .catch((err) => {
          console.error(err);
          this.$toast.error("Lỗi đặt giá: " + (err.response?.data?.message || err.message));
        })
        .finally(() => {
          this.isPlacingBid = false;
        });
    },

    // === ROOM STATUS CHECK ===
    startRoomStatusCheck() {
      // Check ngay lần đầu
      this.checkRoomStatus();
      this.refreshArtworkSession();

      // Sau đó check theo thời gian đã config (có thể chỉnh trong data)
      this.roomStatusInterval = setInterval(() => {
        this.checkRoomStatus();
        this.refreshArtworkSession();
      }, this.refreshInterval); // Thời gian refresh được config trong data()
    },

    checkRoomStatus() {
      // Không log để tránh spam console
      axios
        .get("http://localhost:8081/api/stream/room/" + this.roomID, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          // Cập nhật detail_auction với data mới
          this.detail_auction = res.data;

          // Check status của phòng
          if (res.data && res.data.status === 0) {
            console.log("Phòng đã kết thúc (status = 0)");
            // Clear interval để không check nữa
            if (this.roomStatusInterval) {
              clearInterval(this.roomStatusInterval);
              this.roomStatusInterval = null;
            }
            // Hiển thị thông báo và redirect
            this.$toast?.warning?.("Phòng đấu giá đã kết thúc. Đang chuyển về trang chủ...");
            setTimeout(() => {
              this.$router.push("/");
            }, 2000); // Delay 2 giây để user đọc thông báo
          }
        })
        .catch((err) => {
          // Nếu API lỗi 404, phòng có thể đã bị xóa
          if (err.response?.status === 404) {
            console.log("Không tìm thấy phòng (404)");
            // Clear interval
            if (this.roomStatusInterval) {
              clearInterval(this.roomStatusInterval);
              this.roomStatusInterval = null;
            }
            // Redirect về home
            this.$toast?.error?.("Không tìm thấy phòng đấu giá. Đang chuyển về trang chủ...");
            setTimeout(() => {
              this.$router.push("/");
            }, 2000);
          }
          // Các lỗi khác không làm gì (có thể là lỗi mạng tạm thời)
        });
    },

    refreshArtworkSession() {
      // Load lại artwork session mỗi 2 giây để cập nhật currentPrice và winnerId
      axios
        .get("http://localhost:8081/api/stream/room/" + this.roomID + "/sessions/current-or-next")
        .then((res) => {
          // Cập nhật dữ liệu mới
          this.artworkSession = res.data;

          console.log(
            "🔄 Data refreshed - Current Price:",
            this.formatUSD(res.data.currentPrice),
            "- Winner:",
            res.data.winnerId
          );
        })
        .catch((err) => {
          // Không log lỗi 404 vì có thể chưa có session
          if (err.response?.status !== 404) {
            console.error("Error refreshing artwork session:", err);
          }
        });
    },

    //livestream
    copyInvite() {
      if (!this.inviteLink) return;
      navigator.clipboard?.writeText(this.inviteLink);
    },

    async startLiveStream() {
      const user = this.$page?.props?.auth?.user ?? null;
      const userName = user?.name ?? `Guest-${Math.floor(Math.random() * 100000)}`;
      const userID = String(user?.id ?? `g${Date.now()}`);

      let appID = this.$page?.props?.chatRoom?.appID;
      let serverSecret = this.$page?.props?.chatRoom?.serverSecret;
      let zegoRole = "audience"; // Default role

      // Fallback: fetch from backend REST API if props are missing
      if (!appID || !serverSecret) {
        try {
          const res = await axios.get(`http://localhost:8081/api/stream/token`, {
            params: { roomId: this.roomID },
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          });
          appID = res.data?.appID;
          serverSecret = res.data?.token; // Use token as serverSecret for generateKitTokenForTest
          zegoRole = res.data?.role || "audience"; // Get role from API response
        } catch (e) {
          console.error("Fetch credentials failed", e);
        }
      }

      if (!appID || !serverSecret) {
        this.error =
          "Thiếu Zego appID/serverSecret từ backend. Vui lòng cấu hình .env hoặc VITE_API_URL.";
        return;
      }

      const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(
        appID,
        serverSecret,
        this.roomID,
        userID,
        userName
      );

      // Client luôn là Audience - chỉ xem livestream
      const role = ZegoUIKitPrebuilt.Audience;

      // Cấu hình cho Client (Audience) - chỉ xem, không livestream
      let config = {
        showPreJoinView: false,
        turnOnCameraWhenJoining: false, // Client không bật camera
        showMyCameraToggleButton: false, // Client không thể tắt/bật camera
        showAudioVideoSettingsButton: false, // Client không thể cài đặt audio/video
        showScreenSharingButton: false, // Client không thể share screen
        showTextChat: false, // ẩn chat của Zego (dùng chat riêng)
        showUserList: false, // Client không xem được danh sách user
        showLeaveButton: true, // Client có thể leave
        showTurnOnRemoteCameraButton: false, // Client không thể bật camera cho user khác
        showTurnOnRemoteMicrophoneButton: false, // Client không thể bật mic cho user khác
        showRemoveUserButton: false, // Client không thể remove user

        videoResolutionList: [
          ZegoUIKitPrebuilt.VideoResolution_360P,
          ZegoUIKitPrebuilt.VideoResolution_180P,
          ZegoUIKitPrebuilt.VideoResolution_480P,
          ZegoUIKitPrebuilt.VideoResolution_720P,
        ],
        videoResolutionDefault: ZegoUIKitPrebuilt.VideoResolution_720P, // Client dùng chất lượng thấp hơn
      };

      const zp = ZegoUIKitPrebuilt.create(kitToken);
      zp.joinRoom({
        container: this.$refs.chatRoomElement,
        scenario: {
          mode: ZegoUIKitPrebuilt.LiveStreaming,
          config: {
            role,
          },
        },
        sharedLinks: [
          {
            name: "Join as Audience",
            url: window.location.origin + "/client/auction-room/" + this.roomID + "?role=Audience",
          },
        ],
        ...config,
      });

      this.inviteLink =
        window.location.origin + "/client/auction-room/" + this.roomID + "?role=Audience";

      // this.loading = true;
      // setTimeout(() => {
      //     this.initLiveStream();
      //     this.loading = false;
      // }, 3000);
    },

    // === INITIALIZATION ===
    initializeUser() {
      // Đảm bảo roomId = roomID từ route params
      this.roomId = this.roomID || this.$route?.params?.id;

      // Extract user info từ JWT và localStorage
      const info = this.extractUserInfoFromToken();
      this.currentUserId = info.id;
      this.currentUserEmail = info.email;
      this.currentUsername = info.username;
      this.isAdmin = this.checkIfAdmin(info);
    },

    // === MESSAGE LOADING ===
    async loadHistory() {
      // Đảm bảo roomId được set trước khi load
      if (!this.roomId) {
        this.roomId = this.roomID || this.$route?.params?.id;
      }

      console.log("📚 Loading chat history for roomId:", this.roomId);
      try {
        const res = await axios.get(
          `http://localhost:8081/api/chats/rooms/${this.roomId}/messages`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        );

        console.log("📚 Chat history response:", res.data);

        let list = this.extractListFromResponse(res.data);
        list = this.sortMessages(list);

        console.log("📚 Extracted and sorted messages:", list);

        // Lọc tin nhắn theo role: Admin xem tất cả, User chỉ xem thread với admin
        const filtered = this.isAdmin ? list : this.filterMessagesForUser(list);

        console.log("📚 Filtered messages for user:", filtered);

        this.messages = filtered.map((m) => this.normalizeMessage(m));
        console.log("📚 Final messages after normalization:", this.messages);
        this.saveToCache();
        this.$nextTick(() => this.scrollToBottom());
      } catch (e) {
        console.error("❌ Load history error:", e);
      }
    },

    // === SOCKET CONNECTION ===
    connectSocket() {
      // Đảm bảo roomId được set trước khi connect
      if (!this.roomId) {
        this.roomId = this.roomID || this.$route?.params?.id;
      }

      console.log("🔌 Connecting chat socket with roomId:", this.roomId);
      this.socket = new ChatSocket("http://localhost:8081", localStorage.getItem("token"));
      this.socket.connect(
        () => {
          this.connected = true;
          console.log("✅ Chat socket connected, subscribing to room:", this.roomId);
          this.subscription = this.socket.subscribeRoom(this.roomId, (body) => {
            console.log("📨 Received message:", body);
            // Với user: chỉ nhận thread của mình với admin
            if (!this.isAdmin && !this.shouldShowMessage(body)) {
              console.log("🚫 Message filtered out for user");
              return;
            }

            console.log("✅ Adding message to chat");
            this.messages.push(this.normalizeIncoming(body));
            this.saveToCache();
            this.$nextTick(() => this.scrollToBottom());
          });
        },
        (err) => {
          console.error("STOMP error:", err);
        }
      );
    },

    // === AUCTION WEBSOCKET FOR COUNTDOWN ===
    connectAuctionWebSocket() {
      console.log("🔌 Connecting to auction WebSocket for countdown...");
      this.auctionSocket = new ChatSocket("http://localhost:8081", localStorage.getItem("token"));

      this.auctionSocket.connect(
        () => {
          console.log("✅ Auction WebSocket connected");

          // Subscribe to auction room events
          this.auctionRoomSubscription = this.auctionSocket.subscribeAuctionRoom(
            this.roomID,
            (message) => {
              this.handleAuctionRoomEvent(message);
            }
          );

          // Load current session để lấy countdown ban đầu
          this.loadCurrentSessionForCountdown();
        },
        (err) => {
          console.error("❌ Auction WebSocket error:", err);
        }
      );
    },

    disconnectAuctionWebSocket() {
      if (this.auctionRoomSubscription) {
        this.auctionRoomSubscription.unsubscribe();
        this.auctionRoomSubscription = null;
      }
      if (this.auctionBidsSubscription) {
        this.auctionBidsSubscription.unsubscribe();
        this.auctionBidsSubscription = null;
      }
      if (this.auctionSocket) {
        this.auctionSocket.deactivate();
        this.auctionSocket = null;
      }
    },

    handleAuctionRoomEvent(message) {
      console.log("📨 Auction room event received:", message);

      if (message.eventType === "SESSION_STARTED") {
        console.log("✅ Session started:", message);

        // Cập nhật artworkSession
        if (message.sessionId) {
          this.loadArtworkBySession();
        }

        // Cập nhật countdown từ endTime
        if (message.endTime) {
          this.sessionEndTime = new Date(message.endTime);
          this.updateCountdownFromEndTime();
          this.startCountdownInterval();
        }

        // Subscribe to bids for this session
        if (message.sessionId) {
          this.subscribeToSessionBids(message.sessionId);
        }
      } else if (message.eventType === "SESSION_ENDED") {
        console.log("⏰ Session ended:", message);
        this.stopCountdownInterval();
        this.countdownSeconds = 0;
        this.sessionEndTime = null;

        // Unsubscribe from bids
        if (this.auctionBidsSubscription) {
          this.auctionBidsSubscription.unsubscribe();
          this.auctionBidsSubscription = null;
        }

        // Show notification that session ended
        this.$toast?.warning?.("Session đấu giá đã kết thúc!");

        // DON'T auto-load next session - let admin start new session manually
        // User will see countdown at 0:00 and can wait for admin to start next session
      } else if (message.eventType === "ROOM_STOPPED") {
        console.log("🛑 Room stopped by admin:", message);

        // Cleanup countdown
        this.stopCountdownInterval();
        this.countdownSeconds = 0;
        this.sessionEndTime = null;

        // Unsubscribe from bids
        if (this.auctionBidsSubscription) {
          this.auctionBidsSubscription.unsubscribe();
          this.auctionBidsSubscription = null;
        }

        // Stop room status check interval
        if (this.roomStatusInterval) {
          clearInterval(this.roomStatusInterval);
          this.roomStatusInterval = null;
        }

        // Hiển thị thông báo và redirect
        this.$toast?.warning?.("Phòng đấu giá đã bị dừng bởi admin. Đang chuyển về trang chủ...");

        setTimeout(() => {
          this.$router.push("/");
        }, 2000); // Delay 2 giây để user đọc thông báo
      }
    },

    subscribeToSessionBids(sessionId) {
      // Unsubscribe old subscription if exists
      if (this.auctionBidsSubscription) {
        this.auctionBidsSubscription.unsubscribe();
      }

      // Subscribe to new session bids
      this.auctionBidsSubscription = this.auctionSocket.subscribeAuctionBids(
        sessionId,
        (message) => {
          this.handleBidEvent(message);
        }
      );
    },

    handleBidEvent(message) {
      console.log("💰 Bid event received:", message);

      if (message.eventType === "BID_ACCEPTED") {
        // Cập nhật countdown từ remainingSeconds hoặc endTime
        if (message.remainingSeconds !== undefined) {
          this.countdownSeconds = message.remainingSeconds;
          // Cập nhật sessionEndTime từ remainingSeconds
          const now = new Date();
          this.sessionEndTime = new Date(now.getTime() + message.remainingSeconds * 1000);
        } else if (message.endTime) {
          this.sessionEndTime = new Date(message.endTime);
          this.updateCountdownFromEndTime();
        }

        // Cập nhật currentPrice nếu có
        if (message.price !== undefined && this.artworkSession) {
          this.artworkSession.currentPrice = message.price;
        }

        // Cập nhật leader nếu có
        if (message.leader && this.artworkSession) {
          this.artworkSession.winnerId = message.leader;
        }

        // Hiển thị thông báo nếu được gia hạn
        if (message.extended) {
          this.$toast?.info?.("⏱️ Thời gian đã được gia hạn thêm 120 giây!");
        }
      }
    },

    loadCurrentSessionForCountdown() {
      axios
        .get(`http://localhost:8081/api/stream/room/${this.roomID}/sessions/current-or-next`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          if (res.data && res.data.status === 1) {
            // Session đang LIVE
            // Cập nhật countdown từ endedAt
            if (res.data.endedAt) {
              this.sessionEndTime = new Date(res.data.endedAt);
              this.updateCountdownFromEndTime();
              this.startCountdownInterval();
            }

            // Subscribe to bids cho session này
            if (res.data.id) {
              this.subscribeToSessionBids(res.data.id);
            }
          }
        })
        .catch((err) => {
          if (err.response?.status !== 404) {
            console.error("Error loading current session for countdown:", err);
          }
        });
    },

    // === MESSAGE SENDING ===

    // --- Gửi tin ---
    sendMsg() {
      if (!this.text.trim() || !this.connected) return;

      let payload;
      if (this.isAdmin) {
        // Admin có thể gửi cho tất cả hoặc user cụ thể
        payload = {
          content: this.text,
          type: "SUPPORT",
          receiverId: this.selectedUserId || null, // null = broadcast đến tất cả
          auctionId: this.roomId,
        };
      } else {
        // User gửi cho admin
        payload = {
          content: this.text,
          type: "SUPPORT",
          receiverId: this.adminId, // gửi trực tiếp tới admin
          auctionId: this.roomId,
        };
      }

      this.socket && this.socket.sendRoom(this.roomId, payload);
      this.text = "";
      this.$nextTick(() => this.scrollToBottom());
    },

    // === HELPER METHODS ===

    // Sắp xếp tin nhắn theo thời gian (cũ -> mới)
    sortMessages(list) {
      const canCompare = list.some((m) => this.getComparableValue(m) != null);
      if (canCompare) {
        return list.slice().sort((a, b) => {
          const va = this.getComparableValue(a) ?? Number.NEGATIVE_INFINITY;
          const vb = this.getComparableValue(b) ?? Number.NEGATIVE_INFINITY;
          return va < vb ? -1 : 1; // cũ -> mới
        });
      }
      return list.slice().reverse(); // API trả newest-first
    },

    // Lọc tin nhắn cho user (chỉ xem thread với admin)
    filterMessagesForUser(list) {
      console.log("🔍 filterMessagesForUser - input list:", list);
      const filtered = list.filter((m) => {
        const sId = this.extractSenderId(m);
        const rId = this.extractReceiverId(m);

        // Truyền message object vào để check role
        const isSenderAdmin = this.isAdminUser(sId, m);
        const isReceiverAdmin = this.isAdminUser(rId, m);

        // User -> Admin (direct)
        const userToAdmin = String(sId) === String(this.currentUserId) && isReceiverAdmin;
        // Admin -> User (direct reply)
        const adminToUser = isSenderAdmin && String(rId) === String(this.currentUserId);
        // Admin broadcast (receiverId = null hoặc empty)
        const adminBroadcast = isSenderAdmin && (rId == null || rId === "" || rId === undefined);

        const shouldInclude = userToAdmin || adminToUser || adminBroadcast;

        if (!shouldInclude) {
          console.log("🚫 Message filtered out:", { sId, rId, currentUserId: this.currentUserId, isSenderAdmin, isReceiverAdmin });
        }

        return shouldInclude;
      });
      console.log("🔍 filterMessagesForUser - filtered result:", filtered);
      return filtered;
    },

    // Kiểm tra tin nhắn có nên hiển thị cho user không (cho socket)
    shouldShowMessage(message) {
      const sId = this.extractSenderId(message);
      const rId = this.extractReceiverId(message);

      // Truyền message object vào để check role
      const isSenderAdmin = this.isAdminUser(sId, message);
      const isReceiverAdmin = this.isAdminUser(rId, message);

      // User -> Admin (direct)
      const userToAdmin = String(sId) === String(this.currentUserId) && isReceiverAdmin;
      // Admin -> User (direct reply)
      const adminToUser = isSenderAdmin && String(rId) === String(this.currentUserId);
      // Admin broadcast (receiverId = null hoặc empty)
      const adminBroadcast = isSenderAdmin && (rId == null || rId === "" || rId === undefined);

      const shouldShow = userToAdmin || adminToUser || adminBroadcast;
      console.log("🔍 shouldShowMessage check:", {
        message,
        sId,
        rId,
        currentUserId: this.currentUserId,
        isSenderAdmin,
        isReceiverAdmin,
        userToAdmin,
        adminToUser,
        adminBroadcast,
        shouldShow
      });

      return shouldShow;
    },

    // Extract sender ID từ message object
    extractSenderId(m) {
      return (
        m.senderId ||
        m.sender_id ||
        (m.sender && (m.sender.id || m.sender.userId || m.sender.user_id)) ||
        m.userId ||
        m.user_id ||
        null
      );
    },

    // Extract receiver ID từ message object
    extractReceiverId(m) {
      return (
        m.receiverId ||
        m.receiver_id ||
        (m.receiver && (m.receiver.id || m.receiver.userId || m.receiver.user_id)) ||
        null
      );
    },

    // Kiểm tra user có phải admin không (by ID pattern, role, hoặc email)
    isAdminUser(userId, message = null) {
      if (!userId) return false;

      // Check theo pattern: Admin ID thực tế bắt đầu bằng "Ad-"
      const isAdminByPattern = String(userId).startsWith("Ad-");

      // Check theo role từ message nếu có
      let isAdminByRole = false;
      if (message) {
        const senderRole = message.senderRole || message.sender_role || (message.sender && message.sender.role) || null;
        isAdminByRole = senderRole === 1;
      }

      // Check theo adminId/adminEmail cũ (fallback)
      const isAdminByOldCheck = String(userId) === String(this.adminId) || userId === this.adminEmail;

      const isAdmin = isAdminByPattern || isAdminByRole || isAdminByOldCheck;
      console.log("🔍 isAdminUser check:", {
        userId,
        adminId: this.adminId,
        adminEmail: this.adminEmail,
        isAdminByPattern,
        isAdminByRole,
        isAdminByOldCheck,
        isAdmin
      });
      return isAdmin;
    },

    // === USER MANAGEMENT ===
    extractUserIdFromToken() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return null;
        const parts = token.split(".");
        if (parts.length < 2) return null;
        const payloadJson = JSON.parse(decodeURIComponent(escape(window.atob(parts[1]))));
        return payloadJson.userId || payloadJson.id || payloadJson._id || payloadJson.sub || null;
      } catch (e) {
        return null;
      }
    },

    // Trích xuất đầy đủ info từ JWT
    extractUserInfoFromToken() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return { id: null, email: null, username: null, role: null };
        const parts = token.split(".");
        if (parts.length < 2) return { id: null, email: null, username: null, role: null };
        const p = JSON.parse(decodeURIComponent(escape(window.atob(parts[1]))));
        return {
          id: p.userId || p.id || p._id || p.sub || null,
          email: p.email || null,
          username: p.username || p.name || null,
          role: p.role ?? null,
        };
      } catch (_) {
        return { id: null, email: null, username: null, role: null };
      }
    },

    // Kiểm tra user hiện tại có phải admin không
    checkIfAdmin(info) {
      try {
        // Check localStorage trước (có thể admin được set ở đây)
        const localEmail = localStorage.getItem("email_kh");
        const localName = localStorage.getItem("name_kh");
        const byLocalEmail = localEmail === this.adminEmail;
        const byLocalName = localName === this.adminUsername;

        // Check JWT token
        const tokenUserId = info && info.id;
        const byRole = info && info.role === 1;
        const byId = tokenUserId && String(tokenUserId) === String(this.adminId);
        const byUsername = info && info.username === this.adminUsername;
        const byEmail = info && info.email === this.adminEmail;

        return Boolean(byLocalEmail || byLocalName || byRole || byId || byUsername || byEmail);
      } catch (e) {
        return false;
      }
    },

    // --- Cuộn về cuối khung chat ---
    scrollToBottom() {
      const el = this.$refs.chatMessages;
      if (el) {
        setTimeout(() => {
          el.scrollTop = el.scrollHeight;
        }, 100);
      }
    },

    // --- Cache message theo phòng trong sessionStorage ---
    saveToCache() {
      try {
        const key = `chat:${this.roomId || this.roomID}`;
        sessionStorage.setItem(key, JSON.stringify(this.messages));
      } catch (_) { }
    },
    loadFromCache() {
      try {
        const key = `chat:${this.roomId || this.roomID}`;
        const raw = sessionStorage.getItem(key);
        if (raw) {
          const cached = JSON.parse(raw);
          if (Array.isArray(cached)) {
            this.messages = cached;
          }
        }
      } catch (_) { }
    },

    // Chuẩn hoá dữ liệu tin nhắn từ API
    normalizeMessage(m) {
      const senderId =
        m.senderId ||
        m.sender_id ||
        (m.sender && (m.sender.id || m.sender.userId || m.sender.user_id)) ||
        m.userId ||
        m.user_id ||
        null;
      const receiverId =
        m.receiverId ||
        m.receiver_id ||
        (m.receiver && (m.receiver.id || m.receiver.userId || m.receiver.user_id)) ||
        null;
      const text = m.content ?? m.message ?? m.text ?? "";
      const senderNameRaw =
        m.senderName || m.sender_name || (m.sender && (m.sender.name || m.sender.username)) || null;
      const senderEmail = m.senderEmail || m.sender_email || (m.sender && m.sender.email) || null;

      const senderRole = m.senderRole || m.sender_role || (m.sender && m.sender.role) || null;

      // Check admin theo pattern "Ad-" hoặc role
      const isAdminSender = String(senderId).startsWith("Ad-") || senderRole === 1 || String(senderId) === String(this.adminId) || senderId === this.adminEmail;

      let senderName;
      if (isAdminSender) {
        // Admin: ưu tiên senderNameRaw, nếu không có thì dùng senderEmail, cuối cùng mới dùng name từ localStorage
        if (senderNameRaw) {
          senderName = senderNameRaw; // Dùng tên thực tế từ database
        } else if (senderEmail) {
          senderName = senderEmail;
        } else {
          // Nếu không có tên, lấy từ localStorage admin hoặc dùng "Admin"
          senderName = localStorage.getItem("name_admin") || "Admin";
        }
      } else if (senderNameRaw) {
        senderName = senderNameRaw;
      } else if (senderEmail) {
        // Hiển thị email thay vì senderId
        senderName = senderEmail;
      } else {
        // Fallback về senderId nếu không có email
        senderName = senderId || "Unknown";
      }
      const time = this.formatTime(m.sentAt || m.createdAt || m.created_at || m.timestamp);

      // Xác định role và tên hiển thị
      let displayName = senderName || "Unknown";
      // Dùng isAdminSender để xác định role (đã check pattern "Ad-" và senderRole)
      let role = isAdminSender ? "admin" : "user";

      return {
        text,
        mine:
          senderId != null && this.currentUserId != null
            ? String(senderId) === String(this.currentUserId)
            : false,
        senderName: `${displayName} (${role})`,
        time: time,
        senderId: senderId,
        receiverId: receiverId,
      };
    },
    // --- Chuẩn hoá tin từ socket ---
    normalizeIncoming(body) {
      return this.normalizeMessage(body);
    },
    // --- Lấy mảng tin nhắn từ response ---
    extractListFromResponse(data) {
      if (Array.isArray(data)) return data;
      if (data && Array.isArray(data.data)) return data.data;
      if (data && Array.isArray(data.result)) return data.result;
      if (data && data.page && Array.isArray(data.page.content)) return data.page.content;
      return [];
    },
    // --- Giá trị so sánh (thời gian hoặc id) ---
    getComparableValue(m) {
      const tRaw =
        m.createdAt || m.created_at || m.timestamp || m.createdDate || m.created_date || null;
      const t = tRaw ? Date.parse(tRaw) : NaN;
      if (!Number.isNaN(t)) return t;
      const idRaw = m.id || m.messageId || m.message_id || null;
      const idNum = idRaw != null && !Number.isNaN(Number(idRaw)) ? Number(idRaw) : NaN;
      if (!Number.isNaN(idNum)) return idNum;
      return null;
    },

    // Format thời gian
    formatTime(timestamp) {
      if (!timestamp) return "";
      try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString("vi-VN", {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false, // 24h format như Zalo
        });
      } catch (e) {
        return "";
      }
    },

    // Lấy tên user từ ID
    getUserName(userId) {
      const user = this.uniqueUsers.find((u) => u.id === userId);
      return user ? user.name : "Unknown";
    },

    // Reply to user (từ Reply button)
    replyToUser(userId) {
      this.selectedUserId = userId;
      // Auto-focus vào input để admin có thể gõ ngay
      this.$nextTick(() => {
        const input = this.$el.querySelector(".chat-input input");
        if (input) input.focus();
      });
    },
  },

  computed: {
    // Lấy danh sách user duy nhất từ messages
    uniqueUsers() {
      const users = new Map();
      this.messages.forEach((msg) => {
        if (
          msg.senderId &&
          msg.senderId !== this.currentUserId &&
          msg.senderId !== this.adminId &&
          msg.senderId !== this.adminEmail
        ) {
          const role =
            msg.senderId === this.adminId || msg.senderId === this.adminEmail ? "admin" : "user";
          const name = msg.senderName ? msg.senderName.split(" (")[0] : msg.senderId; // Dùng senderId (email) làm tên
          users.set(msg.senderId, {
            id: msg.senderId,
            name: name,
            role: role,
          });
        }
      });
      return Array.from(users.values());
    },

    // Hiển thị countdown dạng MM:SS
    countdownDisplay() {
      if (this.countdownSeconds <= 0) return "0:00";
      const minutes = Math.floor(this.countdownSeconds / 60);
      const seconds = this.countdownSeconds % 60;
      return `${minutes}:${seconds.toString().padStart(2, "0")}`;
    },

    isReportFormValid() {
      return Boolean(
        this.reportForm.member &&
        this.reportForm.reportType &&
        this.reportForm.reportType.trim() &&
        this.reportForm.reason &&
        this.reportForm.reason.trim()
      );
    },

    // Tính toán các nút đặt giá nhanh dựa trên bước giá
    quickBidButtons() {
      const bidStep = this.artworkSession.bidStep || 100; // Mặc định 100 nếu không có bidStep
      return [bidStep * 1, bidStep * 2, bidStep * 3, bidStep * 4, bidStep * 5, bidStep * 6];
    },
  },
};
</script>
<style scoped>
/* Tabs Wrapper */
.tabs-wrapper {
  display: flex;
  align-items: stretch;
  gap: 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  height: 100%;
  min-height: 600px;
}

/* Content Box */
.content-box {
  border: none;
  background-color: #fff;
  padding: 0;
  height: 100%;
  overflow-y: auto;
}

/* Tabs Sidebar */
.tabs-sidebar {
  /* background-color: #ffffff; */
  padding: 15px 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* min-width: 65px; */
  /* border-left: 2px solid #e0e0e0; */
}

/* Vertical Tabs Styling */
.nav-tabs.flex-column {
  border-bottom: none;
  border-left: none;
  padding-left: 0;
  gap: 15px;
  background-color: transparent;
}

.nav-tabs.flex-column .nav-item {
  width: auto;
}

.nav-tabs.flex-column .nav-link {
  border: none;
  color: #6c757d;
  font-weight: 600;
  padding: 0;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border-radius: 10px;
  background-color: transparent;
  position: relative;
  opacity: 0.4;
}

.nav-tabs.flex-column .nav-link:hover {
  opacity: 0.7;
  transform: scale(1.1);
}

.nav-tabs.flex-column .nav-link.active {
  color: #044a42;
  background-color: transparent;
  transform: scale(1.05);
  opacity: 1;
}

.nav-tabs.flex-column .nav-link i {
  font-size: 22px;
}

.tab-content {
  animation: fadeIn 0.3s ease-in-out;
  height: 100%;
}

.tab-pane {
  height: 100%;
}

.chat-tab-pane {
  height: 100%;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Chat Bubbles */
.chat-bubble-left {
  background: #ffffff;
  border-radius: 12px 12px 12px 4px;
  padding: 10px 14px;
  max-width: 70%;
  display: inline-block;
  text-align: left;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  word-wrap: break-word;
  line-height: 1.5;
}

.chat-bubble-right {
  background: linear-gradient(135deg, #044a42 0%, #066a5e 100%);
  color: white;
  border-radius: 12px 12px 4px 12px;
  padding: 10px 14px;
  max-width: 70%;
  display: inline-block;
  text-align: left;
  box-shadow: 0 2px 4px rgba(4, 74, 66, 0.2);
  word-wrap: break-word;
  line-height: 1.5;
}

/* Avatar Circle */
.avatar-circle {
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

/* Chat Content Container */
.chat-content {
  display: flex;
  flex-direction: column;
}

/* Scrollbar Styling */
.chat-content::-webkit-scrollbar {
  width: 6px;
}

.chat-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.chat-content::-webkit-scrollbar-thumb {
  background: #044a42;
  border-radius: 10px;
}

.chat-content::-webkit-scrollbar-thumb:hover {
  background: #033831;
}

/* Smooth scroll behavior */
.chat-content {
  scroll-behavior: smooth;
}

/* Admin Controls */
.admin-controls {
  border: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

/* Input Styling */
/* .form-control:focus {
  box-shadow: none;
  border-color: #044a42;
} */

/* Card Header Badge */
.card-header .badge {
  font-weight: 500;
}

/* Message animations handled by global fadeIn */

/* Quick Bid Buttons */
.quick-bid-btn {
  cursor: pointer;
  border: 2px solid transparent !important;
  box-sizing: border-box;
}

.quick-bid-btn:hover {
  border-color: #044a42;
}

.quick-bid-btn:active {
  box-sizing: border-box;
}

.quick-bid-btn .card-body {
  font-weight: 600;
  color: #044a42;
}

.quick-bid-btn:hover .card-body p {
  color: #066a5e;
}

/* Quick Bid Active State */
.quick-bid-active {
  border: 2px solid #044a42 !important;
  background-color: rgba(4, 74, 66, 0.05);
}

.quick-bid-active .card-body p {
  color: #044a42;
  font-weight: 700;
}

.custom-report-modal {
  position: fixed;
  inset: 0;
  z-index: 1055;
  pointer-events: none;
}

.custom-report-modal .modal-backdrop {
  pointer-events: auto;
}

.custom-report-modal .modal {
  pointer-events: auto;
}

/* Responsive */
@media (max-width: 768px) {

  .chat-bubble-left,
  .chat-bubble-right {
    max-width: 85%;
  }

  .chat-content {
    height: 300px !important;
  }
}
</style>
