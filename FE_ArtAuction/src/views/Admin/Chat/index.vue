<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h4 class="mb-0">
              <i class="fa-solid fa-comments me-2"></i>
              Admin Chat Support
            </h4>
            <div class="d-flex align-items-center gap-2">
              <span class="badge bg-success">Admin Mode</span>
              <span class="badge bg-info">{{ roomId }}</span>
              <span class="badge bg-warning">{{ adminUsername }}</span>
            </div>
          </div>
          <div class="card-body p-0">
            <div class="row g-0">
              <!-- Danh sách phòng chat -->
              <div class="col-md-3 border-end">
                <div class="p-3 border-bottom">
                  <h6 class="mb-2">Auction Rooms</h6>
                  <select v-model="selectedRoomId" @change="switchRoom" class="form-select form-select-sm">
                    <option value="">Select a room...</option>
                    <option v-for="room in availableRooms" :key="room.id" :value="room.id">
                      {{ room.name }} ({{ room.id }})
                    </option>
                  </select>
                </div>
                <div class="p-3">
                  <h6 class="mb-2">Active Users</h6>
                  <div class="list-group list-group-flush">
                    <div v-for="user in uniqueUsers" :key="user.id"
                         class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                         :class="{ 'active': selectedUserId === user.id }"
                         @click="selectUser(user.id)">
                      <div>
                        <div class="fw-bold">{{ user.name }}</div>
                        <small class="text-muted">{{ user.role }}</small>
                      </div>
                      <span v-if="user.unreadCount > 0" class="badge bg-danger">{{ user.unreadCount }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Khu vực chat chính -->
              <div class="col-md-9">
                <div class="d-flex flex-column" style="height: 70vh;">
                  <!-- Header chat -->
                  <div class="p-3 border-bottom bg-light">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="mb-0">
                          {{ selectedUserId ? `Chat with ${getUserName(selectedUserId)}` : 'Broadcast to All Users' }}
                        </h6>
                        <small class="text-muted">Room: {{ roomId }}</small>
                      </div>
                      <div class="d-flex gap-2">
                        <button v-if="selectedUserId" @click="selectedUserId = null"
                                class="btn btn-sm btn-outline-primary">
                          <i class="fa-solid fa-broadcast-tower me-1"></i>
                          Broadcast
                        </button>
                        <button @click="refreshMessages" class="btn btn-sm btn-outline-secondary">
                          <i class="fa-solid fa-refresh me-1"></i>
                          Refresh
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Nội dung chat -->
                  <div class="flex-grow-1 p-3 chat-content" ref="chatContainer">
                    <div v-if="messages.length === 0" class="text-center text-muted py-5">
                      <i class="fa-solid fa-comments fa-3x mb-3"></i>
                      <p>No messages yet. Start a conversation!</p>
                    </div>

                    <template v-for="(m, idx) in messages" :key="idx">
                      <div v-if="!m.mine" class="chat-content-leftside">
                        <div class="d-flex">
                          <img src="../../../assets/img/avt.png" width="32" height="32" class="rounded-circle me-2" alt="">
                          <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                              <small class="text-muted fw-bold">{{ m.senderName || 'User' }}</small>
                              <button v-if="m.senderId && m.senderId !== adminId && m.senderId !== adminEmail"
                                class="btn btn-link btn-sm ms-2 p-0" @click="replyToUser(m.senderId)"
                                title="Reply this user">Reply</button>
                            </div>
                            <div class="chat-left-msg bg-secondary bg-opacity-10 text-dark mb-1">
                              <p class="mb-0">{{ m.text }}</p>
                              <small class="text-muted">{{ m.time }}</small>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div v-else class="chat-content-rightside">
                        <div class="d-flex">
                          <div class="flex-grow-1 me-2">
                            <div class="d-flex align-items-center justify-content-end mb-1">
                              <small class="text-muted fw-bold">{{ m.senderName || 'Admin' }}</small>
                            </div>
                            <div class="d-flex gap-3 align-items-center justify-content-end">
                              <div class="chat-right-msg bg-success bg-opacity-25 text-dark mb-1">
                                <p class="mb-0">{{ m.text }}</p>
                                <small class="text-muted">{{ m.time }}</small>
                              </div>
                            </div>
                          </div>
                          <img src="../../../assets/img/user_test.jpg" width="32" height="32" class="rounded-circle ms-2" alt="">
                        </div>
                      </div>
                    </template>
                  </div>

                  <!-- Input chat -->
                  <div class="p-3 border-top">
                    <div class="chat-input">
                      <input v-model="text" @keyup.enter="sendMsg"
                        :placeholder="selectedUserId ? `Reply to ${getUserName(selectedUserId)}` : 'Broadcast to all users...'" />
                      <button @click="sendMsg">Gửi</button>
                    </div>
                    <div class="mt-2">
                      <small class="text-muted">
                        Target: {{ selectedUserId ? getUserName(selectedUserId) + ' (direct)' : 'All users (broadcast)' }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ChatSocket from '../../../socket';

export default {
  name: 'AdminChat',
  props: ["id"],
  data() {
    return {
      baseUrl: "http://localhost:8081",
      roomId: this.$route.params.id || "ACR-33101829954600", // Lấy từ params
      selectedRoomId: this.$route.params.id || "ACR-33101829954600",

      // Socket & Messages
      socket: null,
      connected: false,
      messages: [],
      text: "",

      // User Info
      currentUserId: null,
      currentUserEmail: null,
      currentUsername: null,

      // Admin Config (giả định admin)
      adminId: "U-4019812134200",
      adminEmail: "connchonam@example.com",
      adminUsername: "john_sins",

      // Chat State
      selectedUserId: null, // null = broadcast

      // Available rooms for testing
      availableRooms: [
        { id: "ACR-33101829954600", name: "Auction Room 1" },
        { id: "auction-002", name: "Auction Room 2" },
        { id: "auction-003", name: "Auction Room 3" }
      ]
    }
  },

  async mounted() {
    this.initializeUser();
    this.loadFromCache();
    await this.loadHistory();
    this.connectSocket();
  },

  beforeUnmount() {
    if (this.socket) this.socket.deactivate();
  },

  methods: {
    // === INITIALIZATION ===
    initializeUser() {
      // Set admin user info - giả định admin
      this.currentUserId = this.adminId;
      this.currentUserEmail = this.adminEmail;
      this.currentUsername = this.adminUsername;

      // Set admin info in localStorage để backend nhận diện
      localStorage.setItem('email_kh', this.adminEmail);
      localStorage.setItem('name_kh', this.adminUsername);
    },

    // === ROOM MANAGEMENT ===
    switchRoom() {
      if (this.selectedRoomId && this.selectedRoomId !== this.roomId) {
        // Disconnect old socket
        if (this.socket) this.socket.deactivate();

        this.roomId = this.selectedRoomId;
        this.selectedUserId = null; // Reset user selection
        this.messages = [];

        // Load new room data
        this.loadFromCache();
        this.loadHistory();
        this.connectSocket();

        // Update URL
        this.$router.push(`/admin/chat/${this.roomId}`);
      }
    },

    // === MESSAGE LOADING ===
    async loadHistory() {
      try {
        console.log(`Loading messages for room: ${this.roomId}`);
        const res = await axios.get(
          `${this.baseUrl}/api/chats/rooms/${this.roomId}/messages`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        );

        console.log("API Response:", res.data);
        let list = this.extractListFromResponse(res.data);
        console.log("Extracted list:", list);
        list = this.sortMessages(list);

        // Admin xem tất cả tin nhắn trong phòng
        this.messages = list.map((m) => this.normalizeMessage(m));
        console.log("Normalized messages:", this.messages);
        this.saveToCache();
        this.$nextTick(() => this.scrollToBottom());
      } catch (e) {
        console.error("Load history error:", e);
        // Fallback: thử load từ cache nếu API lỗi
        this.loadFromCache();
      }
    },

    // === SOCKET CONNECTION ===
    connectSocket() {
      if (this.socket) this.socket.deactivate();

      console.log(`Connecting socket to room: ${this.roomId}`);
      this.socket = new ChatSocket(this.baseUrl, localStorage.getItem('token'));
      this.socket.connect(() => {
        this.connected = true;
        console.log("Socket connected successfully");
        this.subscription = this.socket.subscribeRoom(this.roomId, (body) => {
          console.log("Received message:", body);
          // Admin nhận tất cả tin nhắn trong phòng
          this.messages.push(this.normalizeIncoming(body));
          this.saveToCache();
          this.$nextTick(() => this.scrollToBottom());
        });
      }, (err) => {
        console.error('STOMP error:', err);
        this.connected = false;
      });
    },

    // === MESSAGE SENDING ===
    sendMsg() {
      if (!this.text.trim() || !this.connected) return;

      const payload = {
        content: this.text,
        type: "SUPPORT",
        receiverId: this.selectedUserId || null, // null = broadcast
        auctionId: this.roomId
      };

      this.socket && this.socket.sendRoom(this.roomId, payload);
      this.text = "";
      this.$nextTick(() => this.scrollToBottom());
    },

    // === USER MANAGEMENT ===
    selectUser(userId) {
      this.selectedUserId = userId;
    },

    replyToUser(userId) {
      this.selectedUserId = userId;
      this.$nextTick(() => {
        const input = this.$el.querySelector('.form-control');
        if (input) input.focus();
      });
    },

    // === HELPER METHODS ===
    sortMessages(list) {
      const canCompare = list.some((m) => this.getComparableValue(m) != null);
      if (canCompare) {
        return list.slice().sort((a, b) => {
          const va = this.getComparableValue(a) ?? Number.NEGATIVE_INFINITY;
          const vb = this.getComparableValue(b) ?? Number.NEGATIVE_INFINITY;
          return va < vb ? -1 : 1;
        });
      }
      return list.slice().reverse();
    },

    extractSenderId(m) {
      return m.senderId || m.sender_id || (m.sender && (m.sender.id || m.sender.userId || m.sender.user_id)) || m.userId || m.user_id || null;
    },

    extractReceiverId(m) {
      return m.receiverId || m.receiver_id || (m.receiver && (m.receiver.id || m.receiver.userId || m.receiver.user_id)) || null;
    },

    isAdminUser(userId) {
      return String(userId) === String(this.adminId) || userId === this.adminEmail;
    },

    normalizeMessage(m) {
      const senderId = this.extractSenderId(m);
      const receiverId = this.extractReceiverId(m);
      const text = m.content ?? m.message ?? m.text ?? '';
      const senderNameRaw = m.senderName || m.sender_name || (m.sender && (m.sender.name || m.sender.username)) || null;
      const senderEmail = m.senderEmail || m.sender_email || (m.sender && m.sender.email) || null;

      let senderName;
      if (this.isAdminUser(senderId)) {
        senderName = 'john_sins (admin)';
      } else if (senderNameRaw) {
        senderName = senderNameRaw;
      } else if (senderEmail) {
        senderName = senderEmail;
      } else {
        senderName = senderId || 'Unknown';
      }

      const time = this.formatTime(m.sentAt || m.createdAt || m.created_at || m.timestamp);

      return {
        text,
        mine: senderId != null && this.currentUserId != null ? String(senderId) === String(this.currentUserId) : false,
        senderName: senderName,
        time: time,
        senderId: senderId,
        receiverId: receiverId
      };
    },

    normalizeIncoming(body) {
      return this.normalizeMessage(body);
    },

    extractListFromResponse(data) {
      if (Array.isArray(data)) return data;
      if (data && Array.isArray(data.data)) return data.data;
      if (data && Array.isArray(data.result)) return data.result;
      if (data && data.page && Array.isArray(data.page.content)) return data.page.content;
      return [];
    },

    getComparableValue(m) {
      const tRaw = m.createdAt || m.created_at || m.timestamp || m.createdDate || m.created_date || null;
      const t = tRaw ? Date.parse(tRaw) : NaN;
      if (!Number.isNaN(t)) return t;
      const idRaw = m.id || m.messageId || m.message_id || null;
      const idNum = idRaw != null && !Number.isNaN(Number(idRaw)) ? Number(idRaw) : NaN;
      if (!Number.isNaN(idNum)) return idNum;
      return null;
    },

    formatTime(timestamp) {
      if (!timestamp) return '';
      try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('vi-VN', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        });
      } catch (e) {
        return '';
      }
    },

    getUserName(userId) {
      const user = this.uniqueUsers.find(u => u.id === userId);
      return user ? user.name : 'Unknown';
    },

    scrollToBottom() {
      const el = this.$refs.chatContainer;
      if (el) {
        el.scrollTop = el.scrollHeight;
      }
    },

    saveToCache() {
      try {
        const key = `admin-chat:${this.roomId}`;
        sessionStorage.setItem(key, JSON.stringify(this.messages));
      } catch (_) { }
    },

    loadFromCache() {
      try {
        const key = `admin-chat:${this.roomId}`;
        const raw = sessionStorage.getItem(key);
        if (raw) {
          const cached = JSON.parse(raw);
          if (Array.isArray(cached)) {
            this.messages = cached;
          }
        }
      } catch (_) { }
    },

    refreshMessages() {
      this.messages = [];
      this.loadHistory();
    }
  },

  computed: {
    uniqueUsers() {
      const users = new Map();
      this.messages.forEach(msg => {
        if (msg.senderId && !this.isAdminUser(msg.senderId)) {
          const name = msg.senderName ? msg.senderName.split(' (')[0] : msg.senderId;
          users.set(msg.senderId, {
            id: msg.senderId,
            name: name,
            role: 'user',
            unreadCount: 0 // TODO: implement unread count
          });
        }
      });
      return Array.from(users.values());
    }
  }
}
</script>

<style scoped>
.chat-content {
  height: 100%;
  overflow-y: auto;
  background-color: #f8f9fa;
}

.chat-left-msg,
.chat-right-msg {
  padding: 8px 12px;
  border-radius: 12px;
  max-width: 70%;
  word-wrap: break-word;
  position: relative;
}

.chat-left-msg small,
.chat-right-msg small {
  display: block;
  margin-top: 4px;
  font-size: 0.75rem;
  opacity: 0.7;
}

.chat-content-leftside {
  margin-bottom: 15px;
}

.chat-content-rightside {
  margin-bottom: 15px;
}

.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.list-group-item.active:hover {
  background-color: #0b5ed7;
}

/* Chat input giống AuctionRoom */
.chat-input {
  display: flex;
  gap: 8px;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input input:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.chat-input button {
  padding: 8px 16px;
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #0b5ed7;
}

.chat-input button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

</style>
