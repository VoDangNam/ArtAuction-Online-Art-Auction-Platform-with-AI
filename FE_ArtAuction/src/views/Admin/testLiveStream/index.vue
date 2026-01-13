<template>
  <div class="container-fluid px-5 mt-3">
    <!-- Header với thông tin phòng và controls -->
    <div class="row mb-3">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h4 class="mb-1">
                  <i class="fas fa-broadcast-tower text-danger me-2"></i>
                  Admin Live Stream Control
                </h4>
                <small class="text-muted">
                  Mã phòng: <strong>{{ roomID }}</strong>
                </small>
              </div>
              <div class="d-flex gap-2">
                <button @click="batDauPhongDauGia" class="btn btn-success btn-sm" :disabled="isStartingRoom || isRoomStarted">
                  <i v-if="isStartingRoom" class="fas fa-spinner fa-spin me-1"></i>
                  <i v-else-if="isRoomStarted" class="fas fa-check-circle me-1"></i>
                  <i v-else class="fas fa-play me-1"></i>
                  {{ isStartingRoom ? 'Đang bắt đầu...' : (isRoomStarted ? 'Phòng đã bắt đầu' : 'Bắt đầu phòng đấu giá') }}
                </button>
                <button @click="dungPhongDauGia" class="btn btn-outline-danger btn-sm" :disabled="isStoppingRoom">
                  <i v-if="isStoppingRoom" class="fas fa-spinner fa-spin me-1"></i>
                  <i v-else class="fas fa-power-off me-1"></i>
                  {{ isStoppingRoom ? 'Đang dừng...' : 'Dừng phòng đấu giá' }}
                </button>
                <button @click="copyInvite" class="btn btn-outline-primary btn-sm">
                  <i class="fas fa-copy me-1"></i>Copy Link
                </button>
              </div>
            </div>

            <!-- Link mời khán giả -->
            <div class="mt-3">
              <label class="form-label fw-bold">Link mời khán giả:</label>
              <div class="input-group">
                <input type="text" class="form-control" :value="inviteLink" readonly>
                <button @click="copyInvite" class="btn btn-outline-secondary" type="button">
                  <i class="fas fa-copy"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Livestream Container -->
    <div class="row" style="height: calc(100vh - 200px)">
      <div class="col-8">
        <div class="card p-0">
          <div class="card-body p-0">
            <div v-show="error" class="alert alert-danger m-3">...</div>
            <div ref="container" style="height:70vh;width:100%;background:#000;"></div>
          </div>
        </div>
      </div>
      <div class="col-4 d-flex ps-0">
        <div class="card p-0 w-100">
          <div class="card-body ps-1 pe-0 d-flex flex-column" style="height: 100%;">
            <div class="tabs-wrapper d-flex gap-0 flex-grow-1" style="min-height: 0;">
              <div class="tab-content flex-grow-1 content-box" id="auctionTabsContent" style="overflow-y: auto;">
                <!-- Tab 1: Bidding -->
                <div class="tab-pane fade show active" id="bidding" role="tabpanel" aria-labelledby="bidding-tab">
                  <div class="row px-2" style="height: 100%; overflow-y: auto;">
                    <!-- Thống kê -->
                    <div class="col-lg-12 mb-3 mt-2">
                      <div class="card">
                        <div class="card-body py-2">
                          <h6 class="card-title mb-2">
                            <i class="fas fa-users text-primary me-2"></i>
                            Thống kê
                          </h6>
                          <div class="row text-center">
                            <div class="col-6">
                              <div class="border-end">
                                <h5 class="text-success mb-1">
                                  <i class="fas fa-clock me-1"></i>{{ duration || '00:00' }}
                                </h5>
                                <small class="text-muted">Livestream</small>
                              </div>
                            </div>
                            <div class="col-6">
                              <h5 class="text-info mb-1">{{ auctionCountdown.currentSession.value?.sessionId || '-' }}
                              </h5>
                              <small class="text-muted">Session ID</small>
                            </div>
                          </div>

                          <!-- Countdown Timer -->
                          <div
                            v-if="auctionCountdown.currentSession.value && auctionCountdown.countdownSeconds.value > 0"
                            class="mt-2">
                            <div class="alert alert-warning py-2 text-center mb-0">
                              <small class="d-block mb-1">
                                <i class="fas fa-hourglass-half me-1"></i>
                                <strong>Thời gian còn lại:</strong>
                              </small>
                              <h5 class="text-danger mb-0 fw-bold">{{ auctionCountdown.countdownDisplay.value }}</h5>
                            </div>
                          </div>
                          <div v-else-if="auctionCountdown.currentSession.value" class="mt-2">
                            <div class="alert alert-secondary py-2 text-center mb-0">
                              <small class="text-muted">Chưa có phiên đấu giá đang chạy</small>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- start-current -->
                    <div class="col-lg-12 mb-3">
                      <div class="card border border-2 border-success shadow-sm p-0">
                        <div class="card-body py-2">
                          <div class="alert alert-success mb-2 py-2 text-center" role="alert">
                            <strong>{{ roomID }}</strong>
                          </div>
                          <div class="row text-center">
                            <div class="col-6 p-0">
                              <div class="border-end">
                                <p class="m-1">Start</p>
                                <p class="fw-bold m-0">
                                  {{ formatUSD(artworkSession.startingPrice || 0) }}
                                </p>
                              </div>
                            </div>
                            <div class="col-6 p-0">
                              <p class="m-1">Current</p>
                              <p class="fw-bold text-success m-0">
                                {{ formatUSD(artworkSession.currentPrice || 0) }}
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
                            <p class="m-0">{{ artworkSession.winnerId || '-' }}</p>
                            <p class="m-0 fw-bold text-success">
                              {{ formatUSD(artworkSession.currentPrice || 0) }}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Control buttons -->
                    <div class="col-lg-12 mb-3">
                      <div class="row">
                        <div class="col-6">
                          <button @click="ketThucSection" class="w-100 btn btn-outline-danger"
                            :disabled="isStoppingSection">
                            <i v-if="isStoppingSection" class="fas fa-spinner fa-spin me-2"></i>
                            <i v-else class="fas fa-stop me-2"></i>
                            {{ isStoppingSection ? 'Đang kết thúc...' : 'Kết thúc section' }}
                          </button>
                        </div>
                        <div class="col-6">
                          <button
                            @click="batDauSectionMoi"
                            class="w-100 btn btn-success"
                            :disabled="isStartingSection || auctionCountdown.isSessionActive.value">
                            <i v-if="isStartingSection" class="fas fa-spinner fa-spin me-2"></i>
                            <i v-else-if="auctionCountdown.isSessionActive.value" class="fas fa-circle-notch fa-spin me-2"></i>
                            <i v-else class="fas fa-play me-2"></i>
                            <span v-if="auctionCountdown.isSessionActive.value">Session đang chạy</span>
                            <span v-else>{{ isStartingSection ? 'Đang bắt đầu...' : 'Bắt đầu section' }}</span>
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- detail-artwork -->
                    <div class="col-lg-12 mt-2">
                      <div class="card bg-transparent border border-2 border-success shadow-sm p-0">
                        <div class="card-body d-flex justify-content-center align-items-center gap-2 p-2">
                          <img :src="artworkSession.imageUrl ||
                            'https://i.pinimg.com/736x/8b/a0/d6/8ba0d6ee7608f8caa427a819de41638a.jpg'
                            " class="img-thumbnail" style="max-height: 150px; width: 100%; object-fit: contain;"
                            alt="" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Tab 2: Chat -->
                <div class="tab-pane fade chat-tab-pane" id="chat" role="tabpanel" aria-labelledby="chat-tab">
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
                                      m.senderName || "User"
                                    }}</small>
                                    <button v-if="
                                      m.senderId &&
                                      m.senderId !== currentUserId
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

                            <!-- My message (Admin) -->
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
                        </div>
                        <div class="card-footer bg-white border-top p-3">

                          <!-- Reply Preview Bar (Messenger-style) -->
                          <div v-if="selectedUserId"
                            class="reply-preview-bar d-flex align-items-center justify-content-between mb-2 p-2 bg-light rounded">
                            <div class="d-flex align-items-center gap-2">
                              <i class="fa-solid fa-reply text-primary"></i>
                              <div>
                                <small class="text-muted d-block" style="font-size: 0.75rem;">Replying to</small>
                                <strong class="text-dark" style="font-size: 0.875rem;">{{ getUserName(selectedUserId)
                                  }}</strong>
                              </div>
                            </div>
                            <button @click="selectedUserId = ''" class="btn btn-sm btn-link text-muted p-0"
                              title="Cancel reply">
                              <i class="fa-solid fa-times fa-lg"></i>
                            </button>
                          </div>
                          <div class="input-group">
                            <input v-model="text" @keyup.enter="sendMsg" type="text" class="form-control"
                              :placeholder="selectedUserId ? `Reply to ${getUserName(selectedUserId)}...` : 'Type message to all users...'" />
                            <button @click.prevent="sendMsg" class="btn btn-success" type="button"
                              :disabled="!text || !text.trim()">
                              <i class="fa-solid fa-paper-plane me-2"></i>Send
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Tab 3: Members -->
                <div class="tab-pane fade members-tab-pane" id="members" role="tabpanel" aria-labelledby="members-tab">
                  <div class="row m-0 px-2">
                    <div class="col-lg-12 p-0 mb-3">
                      <div class="card p-0 d-flex flex-column border border-2 border-success">
                        <div class="card-body d-flex justify-content-between align-items-center">
                          <div class="d-flex align-items-center gap-2">
                            <i class="fa-solid fa-users fa-lg"></i>
                            <h5 class="mb-0">Members</h5>
                            <span class="badge border border-2 border-success text-success">
                              {{ members.length }} joined
                            </span>
                          </div>
                          <button @click="loadMembers" class="btn btn-sm btn-outline-success" title="Refresh members">
                            <i class="fas fa-sync-alt"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="col-12 p-0">
                      <div class="card p-0">
                        <div class="card-body" style="max-height: 60vh; overflow-y: auto;">
                          <!-- Loading state -->
                          <div v-if="members.length === 0" class="p-4 text-center text-muted">
                            <i class="fa-solid fa-users fa-2x mb-2"></i>
                            <p class="m-0">Chưa có thành viên nào tham gia</p>
                          </div>

                          <!-- Members list -->
                          <div v-else>
                            <div v-for="(member, index) in members" :key="member.id || index"
                              class="member-item d-flex align-items-center justify-content-between p-2 border-bottom">
                              <div class="d-flex align-items-center gap-2">
                                <div class="avatar-circle bg-primary text-white d-flex align-items-center justify-content-center"
                                  style="width: 36px; height: 36px; border-radius: 50%; font-size: 14px; font-weight: bold;">
                                  {{ (member.username || member.email || 'U').charAt(0).toUpperCase() }}
                        </div>
                                <div>
                                  <div class="fw-semibold">{{ member.username || member.email || 'Unknown' }}</div>
                                  <small class="text-muted" v-if="member.email && member.username">{{ member.email }}</small>
                                </div>
                              </div>
                              <span class="badge bg-success">Online</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Tabs Navigation (Right Side) -->
              <div class="tabs-sidebar px-3">
                <ul class="nav nav-tabs flex-column" id="auctionTabs" role="tablist">
                  <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="bidding-tab" data-bs-toggle="tab" data-bs-target="#bidding"
                      type="button" role="tab" aria-controls="bidding" aria-selected="true" title="Đặt giá">
                      <i class="fa-solid fa-gavel"></i>
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button class="nav-link" id="chat-tab" data-bs-toggle="tab" data-bs-target="#chat" type="button"
                      role="tab" aria-controls="chat" aria-selected="false" title="Chat">
                      <i class="fa-solid fa-comments"></i>
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button class="nav-link" id="members-tab" data-bs-toggle="tab" data-bs-target="#members"
                      type="button" role="tab" aria-controls="members" aria-selected="false" title="Members list">
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

    <!-- Thông tin bổ sung -->
    <div class="row mt-3">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h6 class="card-title">
              <i class="fas fa-info-circle text-info me-2"></i>
              Hướng dẫn sử dụng
            </h6>
            <ul class="list-unstyled mb-0">
              <li><i class="fas fa-check text-success me-2"></i>Bật camera và microphone để bắt đầu livestream</li>
              <li><i class="fas fa-check text-success me-2"></i>Chia sẻ link cho khán giả để họ có thể xem</li>
              <li><i class="fas fa-check text-success me-2"></i>Sử dụng các nút điều khiển để quản lý buổi đấu giá</li>
              <li><i class="fas fa-exclamation-triangle text-warning me-2"></i>Sử dụng nút "Stop broadcast" của
                ZEGOCLOUD để dừng</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import { ZegoUIKitPrebuilt } from "@zegocloud/zego-uikit-prebuilt";
import useAuctionCountdown from '../../../composables/useAuctionCountdown';
import ChatSocket from '../../../socket';

export default {
  props: ["id"],
  data() {
    return {
      // id: this.$route.params.id,
      roomID: this.$route.params.id || this.id, // Lấy từ route params

      user: {},

      error: null,
      inviteLink: "",
      zp: null,
      viewerCount: 0,
      duration: "00:00",
      status: "Đang khởi tạo...",
      startTime: null,
      durationInterval: null,
      isStartingSection: false,
      isStoppingSection: false,
      isStartingRoom: false,
      isStoppingRoom: false,
      isRoomStarted: false, // Track if room has been started

      // Interval để refresh session data
      sessionRefreshInterval: null,

      // === ARTWORK SESSION ===
      artworkSession: {},

      // === CHAT STATE ===
      socket: null,
      connected: false,
      messages: [],
      text: "",
      currentUserId: null,
      currentUserEmail: null,
      currentUsername: null,
      selectedUserId: "", // User được admin chọn để reply (empty = broadcast)
      subscription: null,

      // === MEMBERS STATE ===
      members: [],
    }
  },
  setup(props, { expose }) {
    // Sử dụng composable cho auction countdown
    const roomID = props.id || window.location.pathname.split('/').pop();

    // Tạo ref để lưu instance của component (để gọi methods)
    let componentInstance = null;

    const auctionCountdown = useAuctionCountdown(roomID, {
      onSessionStarted: (session) => {
        console.log('✅ Session started callback:', session);
      },
      onSessionEnded: (message) => {
        console.log('⏰ Session ended callback:', message);
      },
      onBidAccepted: (message) => {
        console.log('💰 Bid accepted callback:', message);
      },
      onCountdownEnd: (session) => {
        console.log('⏰ Countdown ended callback:', session);
        // Gọi autoStopSession từ component methods
        if (componentInstance && componentInstance.autoStopSession) {
          componentInstance.autoStopSession();
        }
      },
      onRoomStopped: (message) => {
        console.log('🛑 Room stopped callback:', message);
        // Redirect về dashboard khi phòng bị dừng
        if (componentInstance && componentInstance.$toast) {
          componentInstance.$toast.warning('Phòng đấu giá đã bị dừng.');
        }
        if (componentInstance && componentInstance.$router) {
          setTimeout(() => {
            componentInstance.$router.push('/admin/dashboard');
          }, 1000);
        }
      },
      toast: null, // Toast sẽ được xử lý trong component
    });

    return {
      auctionCountdown,
      setComponentInstance: (instance) => {
        componentInstance = instance;
      }
    };
  },
  mounted() {

    // Initialize user info with fallback
    const storedName = localStorage.getItem("name_admin");
    const storedEmail = localStorage.getItem("email_admin");
    const tokenInfo = this.extractUserInfoFromToken();

    this.user = {
      name: storedName || tokenInfo.username || storedEmail || `Admin_${Date.now()}`,
    };

    console.log("👤 User initialized:", this.user);

    // Đảm bảo roomID được set từ route params
    if (this.$route.params.id) {
      this.roomID = this.$route.params.id;
    }

    // Initialize user info
    this.initializeUser();

    // Load chat history and connect socket
    this.loadFromCache();
    this.loadHistory();
    this.connectSocket();

    // Load artwork session
    this.loadArtworkBySession();
    this.startSessionRefresh();

    // Load members list
    this.loadMembers();

    this.startAsHost();

    // Set component instance để composable có thể gọi methods
    if (this.setComponentInstance) {
      this.setComponentInstance(this);
    }

    // Khởi tạo auction countdown composable
    this.auctionCountdown.initialize();

    // Scroll to bottom sau khi load xong
    this.$nextTick(() => {
      setTimeout(() => {
        this.scrollToBottom();
      }, 500);
    });
  },

  beforeRouteLeave(to, from, next) {
    // Chặn hoàn toàn nếu phòng đang chạy - chỉ cho phép thoát qua nút "Dừng phòng"
    if (this.isRoomStarted) {
      this.$toast.warning('⚠️ Phòng đấu giá đang chạy! Bạn phải bấm "Dừng phòng đấu giá" trước khi rời khỏi trang.');
      next(false); // Chặn tất cả navigation
    } else {
      next(); // Cho phép thoát bình thường
    }
  },

  beforeUnmount() {
    if (this.durationInterval) {
      clearInterval(this.durationInterval);
    }
    if (this.sessionRefreshInterval) {
      clearInterval(this.sessionRefreshInterval);
    }
    if (this.zp) {
      this.zp.destroy();
    }
    // Cleanup socket
    if (this.socket) {
      this.socket.deactivate();
    }
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
    // Composable tự động cleanup qua onUnmounted
  },

  methods: {
    copyInvite() {
      if (this.inviteLink) navigator.clipboard?.writeText(this.inviteLink);
    },

    // Bắt đầu phòng đấu giá
    batDauPhongDauGia() {
      if (this.isStartingRoom || this.isRoomStarted) return;

      // Xác nhận trước khi bắt đầu
      if (!confirm('Bạn có chắc chắn muốn bắt đầu phòng đấu giá?')) {
        return;
      }

      this.isStartingRoom = true;

      axios
        .post(`http://localhost:8081/api/stream/start/${this.roomID}`, {}, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          console.log("✅ Room started successfully", res.data);
          this.$toast.success('Phòng đấu giá đã được bắt đầu thành công!');

          // Set flag để không cho bấm nữa
          this.isRoomStarted = true;

          // Reload lại session để cập nhật trạng thái
          this.loadCurrentSession();
        })
        .catch((err) => {
          console.error('❌ Error starting room:', err);
          const errorMessage = err.response?.data?.message || err.message;
          this.$toast.error('Lỗi bắt đầu phòng đấu giá: ' + errorMessage);
        })
        .finally(() => {
          this.isStartingRoom = false;
        });
    },

    formatDateTime(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },

    // Load session data để cập nhật currentPrice
    loadCurrentSession() {
      axios
        .get(`http://localhost:8081/api/stream/room/${this.roomID}/sessions/current-or-next`, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          if (res.data) {
            // Cập nhật artworkSession với data mới (bao gồm currentPrice)
            this.artworkSession = res.data;
          }
        })
        .catch((err) => {
          // Không log lỗi 404 vì có thể chưa có session
          if (err.response?.status !== 404) {
            console.error('Error loading session:', err);
          }
        });
    },

    startSessionRefresh() {
      // Load ngay lần đầu
      this.loadCurrentSession();

      // Sau đó load mỗi 2 giây để cập nhật currentPrice
      this.sessionRefreshInterval = setInterval(() => {
        this.loadCurrentSession();
      }, 2000);
    },

    stopSessionRefresh() {
      if (this.sessionRefreshInterval) {
        clearInterval(this.sessionRefreshInterval);
        this.sessionRefreshInterval = null;
      }
    },

    // Load members list
    async loadMembers() {
      if (!this.roomID) return;

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

        const payload = response.data;

        if (Array.isArray(payload)) {
          this.members = payload;
        } else if (Array.isArray(payload?.data)) {
          this.members = payload.data;
        } else if (Array.isArray(payload?.members)) {
          this.members = payload.members;
        } else {
          this.members = [];
        }

        console.log('✅ Admin - Members loaded:', this.members.length);
      } catch (error) {
        console.error("Error loading members:", error);
        this.$toast?.error?.("Không thể tải danh sách thành viên");
      }
    },

    startAsHost() {
      this.status = "Đang khởi tạo...";

      // Ensure userName is valid
      const userName = this.user?.name || `Admin_${Date.now()}`;
      const userID = String(this.$page?.props?.auth?.user?.id ?? `h${Date.now()}`);

      console.log("🚀 Starting as host with:", { userName, userID, roomID: this.roomID });

      let appID = this.$page?.props?.chatRoom?.appID;
      let serverSecret = this.$page?.props?.chatRoom?.serverSecret;

      if (!appID || !serverSecret) {
        const apiBase = `${window.location.protocol}//${window.location.hostname}:8081`;
        axios.get(`${apiBase}/api/stream/token`, {
          params: { roomId: this.roomID },
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
          .then((res) => {
            appID = res.data?.appID;
            serverSecret = res.data?.token;

            if (!appID || !serverSecret) {
              throw new Error('Invalid credentials from backend');
            }

            this.continueStartAsHost(appID, serverSecret, userID, userName);
          })
          .catch((e) => {
            console.error('Error fetching credentials:', e);
            this.error = 'Thiếu Zego appID/serverSecret từ backend. Vui lòng kiểm tra cấu hình.';
            this.status = "Lỗi khởi tạo";
          });
        return;
      }

      this.continueStartAsHost(appID, serverSecret, userID, userName);
    },

    continueStartAsHost(appID, serverSecret, userID, userName) {
      console.log("🔧 continueStartAsHost called with:", { appID, serverSecret: '***', userID, userName });

      if (!appID || !serverSecret) {
        this.error = 'Thiếu Zego appID/serverSecret từ backend. Vui lòng kiểm tra cấu hình.';
        this.status = "Lỗi khởi tạo";
        console.error("❌ Missing appID or serverSecret");
        return;
      }

      if (!userName || userName === 'null' || userName === 'undefined') {
        this.error = 'Thiếu tên người dùng. Vui lòng đăng nhập lại.';
        this.status = "Lỗi khởi tạo";
        console.error("❌ Invalid userName:", userName);
        return;
      }

      try {
        this.status = "Đang tạo token...";
        console.log("🔑 Generating token for:", { roomID: this.roomID, userID, userName });

        const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(
          parseInt(appID),
          serverSecret,
          this.roomID,
          userID,
          userName
        );

        this.status = "Đang kết nối...";
        console.log("✅ Token generated, creating ZegoUIKit instance...");
        this.zp = ZegoUIKitPrebuilt.create(kitToken);

        // Lắng nghe event khi livestream bắt đầu
        const zegoEngine = this.zp.expressEngine;
        if (zegoEngine) {
          zegoEngine.on('publisherStateUpdate', (result) => {
            console.log('Publisher state update:', result);
            if (result.state === 'PUBLISHING') {
              console.log('Livestream started - Starting timer...');
              if (!this.startTime) {
                this.startTime = new Date();
                this.startDurationTimer();
                this.status = "Đang livestream";
              }
            }
          });
        }

        // Cấu hình tối giản - để ZEGOCLOUD hoạt động theo mặc định
        this.zp.joinRoom({
          container: this.$refs.container,
          scenario: { mode: ZegoUIKitPrebuilt.LiveStreaming, config: { role: ZegoUIKitPrebuilt.Host } },
          sharedLinks: [{
            name: 'Join as Audience',
            url: `${window.location.origin}/client/auction-room/${this.roomID}?role=audience`,
          }],
          // Cấu hình cho Admin Host
          turnOnCameraWhenJoining: true,
          showMyCameraToggleButton: true,
          showAudioVideoSettingsButton: true,
          showScreenSharingButton: true,
          showTextChat: true,
          showUserList: true,
          showLeaveButton: false,
          showLeaveRoomConfirmDialog: false,
        });





        this.inviteLink = `${window.location.origin}/client/auction-room/${this.roomID}?role=audience`;
        this.status = "Đã sẵn sàng - Nhấn Go Live";

      } catch (error) {
        console.error('Error starting livestream:', error);
        this.error = 'Lỗi khởi tạo livestream: ' + error.message;
        this.status = "Lỗi";
      }
    },

    startDurationTimer() {
      this.durationInterval = setInterval(() => {
        if (this.startTime) {
          const now = new Date();
          const diff = Math.floor((now - this.startTime) / 1000);
          const hours = Math.floor(diff / 3600);
          const minutes = Math.floor((diff % 3600) / 60);
          const seconds = diff % 60;

          // Hiển thị theo định dạng: HH:MM:SS
          if (hours > 0) {
            this.duration = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
          } else {
            this.duration = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
          }
        }
      }, 1000);
    },

    batDauSectionMoi() {
      if (this.isStartingSection) return;

      this.isStartingSection = true;

      axios
        .post(`http://localhost:8081/api/stream/room/${this.roomID}/start-next`, {}, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          this.currentSession = res.data;
          console.log("Session started successfully", this.currentSession);
          this.$toast.success(`Đã bắt đầu section mới: ${res.data.sessionId}`);

          // Bắt đầu refresh session data để cập nhật currentPrice
          this.startSessionRefresh();
        })
        .catch((err) => {
          console.error(err);

          // Xử lý lỗi "session already running"
          const errorMessage = err.response?.data?.message || err.message;
          if (errorMessage.includes('session is already running')) {
            this.$toast.error('Đã có session đang chạy! Vui lòng kết thúc session hiện tại trước khi bắt đầu session mới.');
          } else {
            this.$toast.error('Lỗi bắt đầu section: ' + errorMessage);
          }
        })
        .finally(() => {
          this.isStartingSection = false;
        });
    },

    ketThucSection() {
      if (this.isStoppingSection) return;

      // ✅ Sửa: Sử dụng auctionCountdown.currentSession.value thay vì this.currentSession
      const currentSession = this.auctionCountdown.currentSession.value;
      if (!currentSession || !currentSession.sessionId) {
        this.$toast.error('Không có session nào đang chạy để kết thúc');
        return;
      }

      this.isStoppingSection = true;

      axios
        .post(`http://localhost:8081/api/stream/stop-session/${currentSession.sessionId}`, {}, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          console.log("Session stopped successfully", res.data);
          this.$toast.success(`Đã kết thúc section: ${currentSession.sessionId}`);
          // ✅ Không cần set this.currentSession = null vì composable sẽ tự động cập nhật
        })
        .catch((err) => {
          console.error(err);
          this.$toast.error('Lỗi kết thúc section: ' + (err.response?.data?.message || err.message));
        })
        .finally(() => {
          this.isStoppingSection = false;
        });
    },

    formatDateTime(dateString) {
      if (!dateString) return '-';
      try {
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
      } catch (error) {
        return dateString;
      }
    },

    dungPhongDauGia() {
      if (this.isStoppingRoom) return;

      // Xác nhận trước khi dừng
      if (!confirm('Bạn có chắc chắn muốn dừng phòng đấu giá? Hành động này không thể hoàn tác!')) {
        return;
      }

      this.isStoppingRoom = true;

      axios
        .post(`http://localhost:8081/api/stream/stop/${this.roomID}`, {}, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          console.log("Room stopped successfully", res.data);
          this.$toast.success('Đã dừng phòng đấu giá thành công!');

          // Reset flag để cho phép navigation
          this.isRoomStarted = false;

          // Redirect về trang chủ hoặc trang quản lý
          setTimeout(() => {
            this.$router.push('/admin/management-auction');
          }, 500);
        })
        .catch((err) => {
          console.error(err);
          this.$toast.error('Lỗi dừng phòng đấu giá: ' + (err.response?.data?.message || err.message));
        })
        .finally(() => {
          this.isStoppingRoom = false;
        });
    },

    // Tự động dừng session khi hết thời gian countdown
    autoStopSession() {
      // Kiểm tra có session hiện tại không (từ composable)
      if (!this.auctionCountdown.currentSession.value || !this.auctionCountdown.currentSession.value.sessionId) {
        console.warn('⚠️ No active session to auto-stop');
        return;
      }

      // Tránh gọi API nếu đang trong quá trình dừng
      if (this.isStoppingSection) {
        console.warn('⚠️ Session is already being stopped');
        return;
      }

      console.log('⏰ Auto-stopping session due to countdown reaching 0:', this.auctionCountdown.currentSession.value.sessionId);

      this.isStoppingSection = true;

      axios
        .post(`http://localhost:8081/api/stream/stop-session/${this.auctionCountdown.currentSession.value.sessionId}`, {}, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          console.log("✅ Session auto-stopped successfully", res.data);
          this.$toast?.success?.('✅ Session đã tự động kết thúc do hết thời gian!');

          // Composable sẽ tự động reset khi nhận SESSION_ENDED từ WebSocket
        })
        .catch((err) => {
          console.error('❌ Error auto-stopping session:', err);

          // Chỉ hiển thị lỗi nếu không phải 404 (session đã kết thúc)
          if (err.response?.status !== 404) {
            this.$toast?.error?.('Lỗi tự động kết thúc session: ' + (err.response?.data?.message || err.message));
          } else {
            console.log('ℹ️ Session already ended on server side');
          }
        })
        .finally(() => {
          this.isStoppingSection = false;
        });
    },

    // === ARTWORK SESSION METHODS ===
    loadArtworkBySession() {
      axios
        .get(`http://localhost:8081/api/stream/room/${this.roomID}/sessions/current-or-next`, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          this.artworkSession = res.data;
          console.log("📦 Artwork session loaded:", this.artworkSession);
        })
        .catch((err) => {
          console.error("Error loading artwork session:", err);
          if (err.response?.status !== 404) {
            this.$toast?.error?.(err.response?.data?.message || "Lỗi khi tải thông tin artwork");
          }
        });
    },

    formatUSD(number) {
      // Đổi sang format tiền Việt (VND)
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(number || 0);
    },

    // === CHAT METHODS ===
    initializeUser() {
      const info = this.extractUserInfoFromToken();
      this.currentUserId = info.id;
      this.currentUserEmail = info.email;
      this.currentUsername = info.username;
    },

    extractUserInfoFromToken() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return { id: null, email: null, username: null };
        const parts = token.split(".");
        if (parts.length < 2) return { id: null, email: null, username: null };
        const p = JSON.parse(decodeURIComponent(escape(window.atob(parts[1]))));
        return {
          id: p.userId || p.id || p._id || p.sub || null,
          email: p.email || null,
          username: p.username || p.name || null,
        };
      } catch (_) {
        return { id: null, email: null, username: null };
      }
    },

    async loadHistory() {
      try {
        const res = await axios.get(
          `http://localhost:8081/api/chats/rooms/${this.roomID}/messages`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        );

        let list = this.extractListFromResponse(res.data);
        list = this.sortMessages(list);

        // Admin xem tất cả tin nhắn trong phòng
        this.messages = list.map((m) => this.normalizeMessage(m));
        this.saveToCache();
        this.$nextTick(() => this.scrollToBottom());
      } catch (e) {
        console.error("Load history error:", e);
      }
    },

    connectSocket() {
      console.log("🔌 Admin connecting chat socket with roomID:", this.roomID);
      this.socket = new ChatSocket("http://localhost:8081", localStorage.getItem("token"));
      this.socket.connect(
        () => {
          this.connected = true;
          console.log("✅ Admin chat socket connected, subscribing to room:", this.roomID);
          this.subscription = this.socket.subscribeRoom(this.roomID, (body) => {
            console.log("📨 Admin received message:", body);
            // Admin nhận tất cả tin nhắn trong phòng
            const normalized = this.normalizeIncoming(body);
            console.log("📝 Normalized message:", normalized);
            this.messages.push(normalized);
            this.saveToCache();
            this.$nextTick(() => this.scrollToBottom());
          });
        },
        (err) => {
          console.error("STOMP error:", err);
        }
      );
    },

    sendMsg() {
      if (!this.text.trim() || !this.connected) {
        console.log("❌ Cannot send message - text empty or not connected");
        return;
      }

      // Admin có thể gửi cho tất cả hoặc user cụ thể
      const payload = {
        content: this.text,
        type: "SUPPORT",
        receiverId: this.selectedUserId || null, // null = broadcast đến tất cả
        auctionId: this.roomID,
      };

      console.log("📤 Admin sending message:", payload);
      this.socket && this.socket.sendRoom(this.roomID, payload);
      this.text = "";

      // Clear reply selection after sending
      this.selectedUserId = "";

      this.$nextTick(() => this.scrollToBottom());
    },

    // === CHAT HELPER METHODS ===
    sortMessages(list) {
      const canCompare = list.some((m) => this.getComparableValue(m) != null);
      if (canCompare) {
        return list.slice().sort((a, b) => {
          const va = this.getComparableValue(a) ?? Number.NEGATIVE_INFINITY;
          const vb = this.getComparableValue(b) ?? Number.NEGATIVE_INFINITY;
          return va < vb ? -1 : 1; // cũ -> mới
        });
      }
      return list.slice().reverse();
    },

    extractListFromResponse(data) {
      if (Array.isArray(data)) return data;
      if (data && Array.isArray(data.data)) return data.data;
      if (data && Array.isArray(data.result)) return data.result;
      if (data && data.page && Array.isArray(data.page.content)) return data.page.content;
      return [];
    },

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

      let senderName;
      if (senderNameRaw) {
        senderName = senderNameRaw;
      } else if (senderEmail) {
        senderName = senderEmail;
      } else {
        senderName = senderId || "Unknown";
      }

      const time = this.formatTime(m.sentAt || m.createdAt || m.created_at || m.timestamp);

      // Check if this message is from current user (admin)
      const isMine = senderId != null && this.currentUserId != null
        ? String(senderId) === String(this.currentUserId)
        : false;

      console.log("🔍 Admin normalizeMessage:", {
        senderId,
        currentUserId: this.currentUserId,
        isMine,
        receiverId
      });

      return {
        text,
        mine: isMine,
        senderName: senderName,
        time: time,
        senderId: senderId,
        receiverId: receiverId,
      };
    },

    normalizeIncoming(body) {
      return this.normalizeMessage(body);
    },

    formatTime(timestamp) {
      if (!timestamp) return "";
      try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString("vi-VN", {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        });
      } catch (e) {
        return "";
      }
    },

    scrollToBottom() {
      const el = this.$refs.chatMessages;
      if (el) {
        setTimeout(() => {
          el.scrollTop = el.scrollHeight;
        }, 100);
      }
    },

    saveToCache() {
      try {
        const key = `chat:${this.roomID}`;
        sessionStorage.setItem(key, JSON.stringify(this.messages));
      } catch (_) { }
    },

    loadFromCache() {
      try {
        const key = `chat:${this.roomID}`;
        const raw = sessionStorage.getItem(key);
        if (raw) {
          const cached = JSON.parse(raw);
          if (Array.isArray(cached)) {
            this.messages = cached;
          }
        }
      } catch (_) { }
    },

    getUserName(userId) {
      const user = this.uniqueUsers.find((u) => u.id === userId);
      return user ? user.name : "Unknown";
    },

    replyToUser(userId) {
      this.selectedUserId = userId;
      this.$nextTick(() => {
        const input = this.$el.querySelector(".card-footer input");
        if (input) input.focus();
      });
    },

  },

  watch: {
    messages: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      deep: true,
    },
  },

  computed: {
    uniqueUsers() {
      const users = new Map();
      this.messages.forEach((msg) => {
        if (
          msg.senderId &&
          msg.senderId !== this.currentUserId
        ) {
          const name = msg.senderName || msg.senderId;
          users.set(msg.senderId, {
            id: msg.senderId,
            name: name,
          });
        }
      });
      return Array.from(users.values());
    },

    countdownDisplay() {
      if (this.countdownSeconds <= 0) return '0:00';
      const minutes = Math.floor(this.countdownSeconds / 60);
      const seconds = this.countdownSeconds % 60;
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
  }
}
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
  min-height: 0;
}

/* Content Box */
.content-box {
  border: none;
  background-color: #fff;
  padding: 0;
  height: 100%;
  overflow-y: auto;
  min-height: 0;
}

/* Tabs Sidebar */
.tabs-sidebar {
  padding: 15px 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-width: 60px;
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
  position: relative;
}

.nav-tabs.flex-column .nav-link {
  border: none;
  color: #9d7bd5;
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
  opacity: 1;
}

.nav-tabs.flex-column .nav-link:hover {
  opacity: 0.8;
  transform: scale(1.1);
}

.nav-tabs.flex-column .nav-link.active {
  color: #9d7bd5;
  background-color: #673ab7;
  transform: scale(1.05);
  opacity: 1;
}

.nav-tabs.flex-column .nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background-color: #044a42;
  border-radius: 2px;
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

/* Reply Preview Bar (Messenger-style) */
.reply-preview-bar {
  border-left: 3px solid #0084ff;
  background: linear-gradient(90deg, rgba(0, 132, 255, 0.05) 0%, rgba(0, 132, 255, 0.02) 100%);
  animation: slideDown 0.2s ease-out;
  transition: all 0.2s ease;
}

.reply-preview-bar:hover {
  background: linear-gradient(90deg, rgba(0, 132, 255, 0.08) 0%, rgba(0, 132, 255, 0.04) 100%);
}

.reply-preview-bar i.fa-reply {
  font-size: 1rem;
  color: #0084ff;
}

.reply-preview-bar button {
  transition: all 0.2s ease;
}

.reply-preview-bar button:hover {
  transform: scale(1.1);
  color: #dc3545 !important;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Admin Controls */
.admin-controls {
  border: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

/* Member Item */
.member-item {
  transition: background-color 0.2s ease;
}

.member-item:hover {
  background-color: #f8f9fa;
}

.member-item:last-child {
  border-bottom: none !important;
}

.member-item .avatar-circle {
  flex-shrink: 0;
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
