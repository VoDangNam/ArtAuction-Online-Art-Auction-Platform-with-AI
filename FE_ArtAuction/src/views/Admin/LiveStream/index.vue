<template>
  <div id="root" style="width: 100%; height: 100vh;"></div>
</template>
<script>
import axios from 'axios';
import { ZegoUIKitPrebuilt } from "@zegocloud/zego-uikit-prebuilt";

export default {
  data() {
    return {
      roomID: "ACR-349213179032200",
      zp: null,
    }
  },
  mounted() {
    this.initZegoCloud();
    // Ngăn chặn các event listener có thể đóng modal ZegoCloud
    this.preventZegoModalAutoClose();
  },
  methods: {
    preventZegoModalAutoClose() {
      // Đợi DOM render xong
      this.$nextTick(() => {
        // Ngăn chặn backdrop click đóng modal ZegoCloud
        document.addEventListener('click', (e) => {
          const target = e.target;
          // Kiểm tra nếu click vào backdrop của ZegoCloud modal
          if (target && (
            target.closest('[id*="zego"]') ||
            target.closest('[class*="zego"]') ||
            target.closest('[id*="Zego"]') ||
            target.closest('[class*="Zego"]')
          )) {
            // Kiểm tra nếu là backdrop của modal ZegoCloud
            const isZegoBackdrop = target.classList && (
              target.classList.toString().includes('backdrop') ||
              target.classList.toString().includes('Backdrop') ||
              target.classList.toString().includes('overlay') ||
              target.classList.toString().includes('Overlay')
            );

            if (isZegoBackdrop && target.closest('[id*="zego"], [class*="zego"], [id*="Zego"], [class*="Zego"]')) {
              // Ngăn chặn event propagation để modal không tự đóng
              e.stopPropagation();
              e.stopImmediatePropagation();
            }
          }
        }, true); // Use capture phase
      });
    },

    getUrlParams(url) {
      let urlStr = url.split('?')[1];
      if (!urlStr) return {};
      const urlSearchParams = new URLSearchParams(urlStr);
      return Object.fromEntries(urlSearchParams.entries());
    },

    async initZegoCloud() {
      const params = this.getUrlParams(window.location.href);
      // Sử dụng roomID từ data, hoặc từ URL params nếu có, hoặc random
      const roomID = params['roomID'] || this.roomID || (Math.floor(Math.random() * 10000) + "");
      const userID = String(this.$page?.props?.auth?.user?.id ?? Math.floor(Math.random() * 10000));
      const userName = this.$page?.props?.auth?.user?.name ?? ("userName" + userID);

      // Get role from URL params, default to Host
      let role = params['role'] || 'Host';
      role = role === 'Host' ? ZegoUIKitPrebuilt.Host : ZegoUIKitPrebuilt.Audience;

      // Config for Host role
      let config = {};
      if (role === ZegoUIKitPrebuilt.Host) {
        config = {
          turnOnCameraWhenJoining: true,
          showMyCameraToggleButton: true,
          showAudioVideoSettingsButton: true,
          showScreenSharingButton: true,
          showTextChat: true,
          showUserList: true,
        };
      }

      // Get appID and serverSecret from API
      let appID = this.$page?.props?.chatRoom?.appID;
      let serverSecret = this.$page?.props?.chatRoom?.serverSecret;

      if (!appID || !serverSecret) {
        try {
          const apiBase = `${window.location.protocol}//${window.location.hostname}:8081`;
          const res = await axios.get(`${apiBase}/api/stream/token`, {
            params: { roomId: roomID },
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          });
          appID = res.data?.appID;
          serverSecret = res.data?.token;
        } catch (e) {
          console.error('Error fetching credentials:', e);
          return;
        }
      }

      if (!appID || !serverSecret) {
        console.error('Missing appID or serverSecret');
        return;
      }

      try {
        const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, roomID, userID, userName);
        this.zp = ZegoUIKitPrebuilt.create(kitToken);

        this.zp.joinRoom({
          container: document.querySelector("#root"),
          scenario: {
            mode: ZegoUIKitPrebuilt.LiveStreaming,
            config: {
              role,
            },
          },
          sharedLinks: [{
            name: 'Join as an audience',
            url:
              window.location.protocol + '//' +
              window.location.host +
              window.location.pathname +
              '?roomID=' +
              roomID +
              '&role=Audience',
          }],
          ...config
        });
      } catch (error) {
        console.error('Error starting livestream:', error);
      }
    },
  },
  beforeUnmount() {
    if (this.zp) {
      this.zp.destroy();
    }
  }
}
</script>
<style>
#root {
  width: 100vw;
  height: 100vh;
}
</style>
