import { Client } from "@stomp/stompjs";
import SockJS from "sockjs-client";

export class ChatSocket {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl;
    this.token = token;
    this.client = null;
    this.connected = false;
  }

  connect(onConnected, onError) {
    console.log('=== SOCKET CONNECT DEBUG ===');
    console.log('Base URL:', this.baseUrl);
    console.log('Token:', this.token);
    console.log('WebSocket URL:', this.baseUrl + "/ws");

    const socket = new SockJS(this.baseUrl + "/ws", null, {
      transports: ['websocket', 'xhr-streaming', 'xhr-polling'],
      withCredentials: true // ✅ SỬA: Bật credentials để match với backend
    });
    console.log('SockJS created:', !!socket);

    this.client = new Client({
      webSocketFactory: () => socket,
      connectHeaders: {
        Authorization: this.token ? "Bearer " + this.token : undefined,
      },
      reconnectDelay: 5000,
      debug: (str) => {
        console.log('STOMP Debug:', str);
      },
      onConnect: (frame) => {
        console.log('✅ STOMP client connected successfully!');
        console.log('Connection frame:', frame);
        this.connected = true;
        if (typeof onConnected === "function") onConnected();
      },
      onStompError: (frame) => {
        console.error('❌ STOMP error:', frame);
        this.connected = false;
        if (typeof onError === "function") onError(frame);
      },
      onWebSocketError: (error) => {
        console.error('❌ WebSocket error:', error);
        this.connected = false;
        if (typeof onError === "function") onError(error);
      },
    });

    console.log('STOMP client created:', !!this.client);
    console.log('Activating STOMP client...');
    this.client.activate();
  }

  subscribeRoom(roomId, handler) {
    console.log('=== SUBSCRIBE ROOM DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Room ID:', roomId);
    console.log('Topic:', `/topic/room.${roomId}`);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot subscribe - client or connection not ready');
      return null;
    }

    const subscription = this.client.subscribe(`/topic/room.${roomId}`, (msg) => {
      console.log('📨 Received message on room topic:', msg);
      try {
        const body = JSON.parse(msg.body);
        console.log('📨 Parsed message body:', body);
        if (typeof handler === "function") handler(body);
      } catch (e) {
        console.error('❌ Error parsing message:', e);
      }
    });

    console.log('✅ Subscribed to room topic successfully');
    return subscription;
  }

  sendRoom(roomId, payload) {
    console.log('=== SEND ROOM DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Room ID:', roomId);
    console.log('Payload:', payload);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot send - client or connection not ready');
      return;
    }

    const destination = `/app/room.send.${roomId}`;
    console.log('📡 Publishing to destination:', destination);

    this.client.publish({
      destination: destination,
      body: JSON.stringify(payload),
    });

    console.log('✅ Message published successfully');
  }

  subscribeGlobal(roomId, handler) {
    console.log('=== SUBSCRIBE GLOBAL DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Room ID:', roomId);
    console.log('Topic:', `/topic/global.${roomId}`);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot subscribe - client or connection not ready');
      return null;
    }

    const subscription = this.client.subscribe(`/topic/global.${roomId}`, (msg) => {
      console.log('📨 Received message on global topic:', msg);
      try {
        const body = JSON.parse(msg.body);
        console.log('📨 Parsed message body:', body);
        if (typeof handler === "function") handler(body);
      } catch (e) {
        console.error('❌ Error parsing message:', e);
      }
    });

    console.log('✅ Subscribed to global topic successfully');
    return subscription;
  }

  sendGlobal(roomId, payload) {
    console.log('=== SEND GLOBAL DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Room ID:', roomId);
    console.log('Payload:', payload);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot send - client or connection not ready');
      return;
    }

    const destination = `/app/global.send.${roomId}`;
    console.log('📡 Publishing to destination:', destination);

    this.client.publish({
      destination: destination,
      body: JSON.stringify(payload),
    });

    console.log('✅ Message published successfully');
  }

  deactivate() {
    console.log('🔌 Deactivating socket...');
    if (this.client) this.client.deactivate();
    this.connected = false;
  }

  // === AUCTION WEBSOCKET METHODS ===

  /**
   * Subscribe to auction room events (SESSION_STARTED, SESSION_ENDED)
   * @param {string} roomId - Auction room ID
   * @param {function} handler - Callback function to handle messages
   * @returns {object|null} Subscription object or null if failed
   */
  subscribeAuctionRoom(roomId, handler) {
    console.log('=== SUBSCRIBE AUCTION ROOM DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Room ID:', roomId);
    console.log('Topic:', `/topic/auction-room/${roomId}`);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot subscribe - client or connection not ready');
      return null;
    }

    const subscription = this.client.subscribe(`/topic/auction-room/${roomId}`, (msg) => {
      console.log('📨 Received auction room event:', msg);
      try {
        const body = JSON.parse(msg.body);
        console.log('📨 Parsed auction room event:', body);
        if (typeof handler === "function") handler(body);
      } catch (e) {
        console.error('❌ Error parsing auction room message:', e);
      }
    });

    console.log('✅ Subscribed to auction room topic successfully');
    return subscription;
  }

  /**
   * Subscribe to auction session bid events (BID_ACCEPTED)
   * @param {string} sessionId - Auction session ID
   * @param {function} handler - Callback function to handle messages
   * @returns {object|null} Subscription object or null if failed
   */
  subscribeAuctionBids(sessionId, handler) {
    console.log('=== SUBSCRIBE AUCTION BIDS DEBUG ===');
    console.log('Client exists:', !!this.client);
    console.log('Connected:', this.connected);
    console.log('Session ID:', sessionId);
    console.log('Topic:', `/topic/auction.${sessionId}.bids`);

    if (!this.client || !this.connected) {
      console.log('❌ Cannot subscribe - client or connection not ready');
      return null;
    }

    const subscription = this.client.subscribe(`/topic/auction.${sessionId}.bids`, (msg) => {
      console.log('📨 Received auction bid event:', msg);
      try {
        const body = JSON.parse(msg.body);
        console.log('📨 Parsed auction bid event:', body);
        if (typeof handler === "function") handler(body);
      } catch (e) {
        console.error('❌ Error parsing auction bid message:', e);
      }
    });

    console.log('✅ Subscribed to auction bids topic successfully');
    return subscription;
  }
}

export default ChatSocket;
