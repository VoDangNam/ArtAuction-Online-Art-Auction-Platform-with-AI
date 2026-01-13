import { ref, computed, onUnmounted } from 'vue';
import axios from 'axios';
import ChatSocket from '../socket';

/**
 * Composable để quản lý countdown và WebSocket cho phiên đấu giá
 * @param {string} roomId - ID của phòng đấu giá
 * @param {object} options - Các tùy chọn
 * @param {function} options.onSessionStarted - Callback khi session bắt đầu
 * @param {function} options.onSessionEnded - Callback khi session kết thúc
 * @param {function} options.onBidAccepted - Callback khi có bid được chấp nhận
 * @param {function} options.onCountdownEnd - Callback khi countdown kết thúc
 * @param {function} options.onRoomStopped - Callback khi phòng đấu giá bị dừng
 * @param {object} options.toast - Toast instance để hiển thị thông báo
 */
export function useAuctionCountdown(roomId, options = {}) {
    // ============ STATE ============
    const auctionSocket = ref(null);
    const auctionRoomSubscription = ref(null);
    const auctionBidsSubscription = ref(null);

    const currentSession = ref(null);
    const countdownSeconds = ref(0);
    const countdownInterval = ref(null);
    const sessionStartTime = ref(null);
    const sessionDurationSeconds = ref(0);
    const sessionMaxDurationSeconds = ref(0);

    // ============ COMPUTED ============
    const countdownDisplay = computed(() => {
        if (countdownSeconds.value <= 0) return '0:00';
        const minutes = Math.floor(countdownSeconds.value / 60);
        const seconds = countdownSeconds.value % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    });

    const isSessionActive = computed(() => {
        return currentSession.value !== null && countdownSeconds.value > 0;
    });

    // ============ WEBSOCKET METHODS ============

    /**
     * Kết nối WebSocket
     */
    function connectWebSocket() {
        console.log('🔌 [useAuctionCountdown] Connecting to auction WebSocket...');

        const token = localStorage.getItem('token');
        auctionSocket.value = new ChatSocket("http://localhost:8081", token);

        auctionSocket.value.connect(() => {
            console.log('✅ [useAuctionCountdown] Auction WebSocket connected');

            // Subscribe to auction room events
            auctionRoomSubscription.value = auctionSocket.value.subscribeAuctionRoom(
                roomId,
                handleAuctionRoomEvent
            );
        }, (err) => {
            console.error('❌ [useAuctionCountdown] Auction WebSocket error:', err);
        });
    }

    /**
     * Ngắt kết nối WebSocket
     */
    function disconnectWebSocket() {
        if (auctionRoomSubscription.value) {
            auctionRoomSubscription.value.unsubscribe();
            auctionRoomSubscription.value = null;
        }
        if (auctionBidsSubscription.value) {
            auctionBidsSubscription.value.unsubscribe();
            auctionBidsSubscription.value = null;
        }
        if (auctionSocket.value) {
            auctionSocket.value.deactivate();
            auctionSocket.value = null;
        }
        stopCountdownInterval();
    }

    /**
     * Xử lý event từ auction room (SESSION_STARTED, SESSION_ENDED, ROOM_STOPPED)
     */
    function handleAuctionRoomEvent(message) {
        console.log('📨 [useAuctionCountdown] Auction room event received:', message);

        if (message.eventType === 'SESSION_STARTED') {
            console.log('✅ [useAuctionCountdown] Session started:', message);

            currentSession.value = {
                sessionId: message.sessionId,
                orderIndex: message.orderIndex,
                startedAt: message.startTime,
                currentPrice: message.currentPrice || 0
            };

            // Lưu thông tin thời gian để tính countdown
            if (message.startTime) {
                sessionStartTime.value = new Date(message.startTime);
            }

            // Lưu durationSeconds từ message hoặc tính từ endTime - startTime
            if (message.durationSeconds !== undefined) {
                sessionDurationSeconds.value = message.durationSeconds;
            } else if (message.endTime && message.startTime) {
                const start = new Date(message.startTime);
                const end = new Date(message.endTime);
                sessionDurationSeconds.value = Math.floor((end - start) / 1000);
            }

            // Lưu maxDurationSeconds nếu có
            if (message.maxDurationSeconds !== undefined) {
                sessionMaxDurationSeconds.value = message.maxDurationSeconds;
            }

            // Bắt đầu countdown
            updateCountdownFromStartTime();
            startCountdownInterval();

            // Subscribe to bids for this session
            if (message.sessionId) {
                subscribeToSessionBids(message.sessionId);
            }

            // Callback
            if (options.onSessionStarted) {
                options.onSessionStarted(currentSession.value);
            }

        } else if (message.eventType === 'SESSION_ENDED') {
            console.log('⏰ [useAuctionCountdown] Session ended:', message);

            stopCountdownInterval();
            countdownSeconds.value = 0;
            sessionStartTime.value = null;
            sessionDurationSeconds.value = 0;
            sessionMaxDurationSeconds.value = 0;

            // Unsubscribe from bids
            if (auctionBidsSubscription.value) {
                auctionBidsSubscription.value.unsubscribe();
                auctionBidsSubscription.value = null;
            }

            // Callback
            if (options.onSessionEnded) {
                options.onSessionEnded(message);
            }

            currentSession.value = null;

        } else if (message.eventType === 'ROOM_STOPPED') {
            console.log('🛑 [useAuctionCountdown] Room stopped:', message);

            // Cleanup all state
            stopCountdownInterval();
            countdownSeconds.value = 0;
            sessionStartTime.value = null;
            sessionDurationSeconds.value = 0;
            sessionMaxDurationSeconds.value = 0;
            currentSession.value = null;

            // Unsubscribe from bids
            if (auctionBidsSubscription.value) {
                auctionBidsSubscription.value.unsubscribe();
                auctionBidsSubscription.value = null;
            }

            // Callback
            if (options.onRoomStopped) {
                options.onRoomStopped(message);
            }
        }
    }

    /**
     * Subscribe to session bids
     */
    function subscribeToSessionBids(sessionId) {
        // Unsubscribe old subscription if exists
        if (auctionBidsSubscription.value) {
            auctionBidsSubscription.value.unsubscribe();
        }

        // Subscribe to new session bids
        auctionBidsSubscription.value = auctionSocket.value.subscribeAuctionBids(
            sessionId,
            handleBidEvent
        );
    }

    /**
     * Xử lý bid event (BID_ACCEPTED)
     */
    function handleBidEvent(message) {
        console.log('💰 [useAuctionCountdown] Bid event received:', message);

        if (message.eventType === 'BID_ACCEPTED') {
            // Cập nhật countdown từ remainingSeconds (ưu tiên)
            if (message.remainingSeconds !== undefined) {
                countdownSeconds.value = message.remainingSeconds;
            }
            // Hoặc tính lại từ endTime nếu có
            else if (message.endTime && sessionStartTime.value) {
                const endTime = new Date(message.endTime);
                const startTime = new Date(sessionStartTime.value);
                sessionDurationSeconds.value = Math.floor((endTime - startTime) / 1000);
                updateCountdownFromStartTime();
            }

            // Cập nhật currentPrice nếu có
            if (message.price !== undefined && currentSession.value) {
                currentSession.value.currentPrice = message.price;
            }

            // Hiển thị thông báo nếu được gia hạn
            if (message.extended) {
                if (options.toast?.info) {
                    options.toast.info('⏱️ Thời gian đã được gia hạn thêm 120 giây!');
                }

                // Cập nhật lại durationSeconds khi được extend
                if (message.endTime && sessionStartTime.value) {
                    const endTime = new Date(message.endTime);
                    const startTime = new Date(sessionStartTime.value);
                    sessionDurationSeconds.value = Math.floor((endTime - startTime) / 1000);
                }
            }

            // Callback
            if (options.onBidAccepted) {
                options.onBidAccepted(message);
            }
        }
    }

    // ============ COUNTDOWN METHODS ============

    /**
     * Cập nhật countdown từ startTime và durationSeconds
     */
    function updateCountdownFromStartTime() {
        if (!sessionStartTime.value || !sessionDurationSeconds.value) return;

        const now = new Date();
        const startTime = new Date(sessionStartTime.value);
        const elapsedSeconds = Math.floor((now - startTime) / 1000);
        const remainingSeconds = sessionDurationSeconds.value - elapsedSeconds;

        countdownSeconds.value = Math.max(0, remainingSeconds);
    }

    /**
     * Bắt đầu interval countdown
     */
    function startCountdownInterval() {
        // Clear existing interval
        if (countdownInterval.value) {
            clearInterval(countdownInterval.value);
        }

        // Update countdown every second
        countdownInterval.value = setInterval(() => {
            if (sessionStartTime.value && sessionDurationSeconds.value) {
                updateCountdownFromStartTime();

                // Nếu hết thời gian, dừng interval
                if (countdownSeconds.value <= 0) {
                    stopCountdownInterval();

                    if (options.toast?.warning) {
                        options.toast.warning('⏰ Hết thời gian đấu giá!');
                    }

                    // Callback
                    if (options.onCountdownEnd) {
                        options.onCountdownEnd(currentSession.value);
                    }
                }
            } else {
                stopCountdownInterval();
            }
        }, 1000);
    }

    /**
     * Dừng interval countdown
     */
    function stopCountdownInterval() {
        if (countdownInterval.value) {
            clearInterval(countdownInterval.value);
            countdownInterval.value = null;
        }
    }

    // ============ API METHODS ============

    /**
     * Load session hiện tại từ API
     */
    async function loadCurrentSession() {
        try {
            const response = await axios.get(
                `http://localhost:8081/api/stream/room/${roomId}/sessions/current-or-next`,
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem("token")
                    }
                }
            );

            if (response.data && response.data.status === 1) {
                // Session đang LIVE
                currentSession.value = {
                    sessionId: response.data.id,
                    orderIndex: response.data.orderIndex,
                    startedAt: response.data.startTime,
                    currentPrice: response.data.currentPrice
                };

                // Lưu thông tin thời gian
                if (response.data.startTime) {
                    sessionStartTime.value = new Date(response.data.startTime);
                }

                // Lưu durationSeconds
                if (response.data.durationSeconds !== undefined) {
                    sessionDurationSeconds.value = response.data.durationSeconds;
                } else if (response.data.endedAt && response.data.startTime) {
                    // Fallback: tính từ endedAt - startTime
                    const start = new Date(response.data.startTime);
                    const end = new Date(response.data.endedAt);
                    sessionDurationSeconds.value = Math.floor((end - start) / 1000);
                }

                // Lưu maxDurationSeconds
                if (response.data.maxDurationSeconds !== undefined) {
                    sessionMaxDurationSeconds.value = response.data.maxDurationSeconds;
                }

                // Bắt đầu countdown
                updateCountdownFromStartTime();
                startCountdownInterval();

                // Subscribe to bids cho session này
                if (response.data.id) {
                    subscribeToSessionBids(response.data.id);
                }
            }
        } catch (err) {
            if (err.response?.status !== 404) {
                console.error('[useAuctionCountdown] Error loading current session:', err);
            }
        }
    }

    /**
     * Khởi tạo: Kết nối WebSocket và load session hiện tại
     */
    function initialize() {
        connectWebSocket();
        loadCurrentSession();
    }

    /**
     * Cleanup khi component unmount
     */
    function cleanup() {
        disconnectWebSocket();
    }

    // Auto cleanup on unmount
    onUnmounted(() => {
        cleanup();
    });

    // ============ RETURN ============
    return {
        // State
        currentSession,
        countdownSeconds,
        sessionStartTime,
        sessionDurationSeconds,
        sessionMaxDurationSeconds,

        // Computed
        countdownDisplay,
        isSessionActive,

        // Methods
        initialize,
        cleanup,
        connectWebSocket,
        disconnectWebSocket,
        loadCurrentSession,
        updateCountdownFromStartTime,
    };
}

export default useAuctionCountdown;
