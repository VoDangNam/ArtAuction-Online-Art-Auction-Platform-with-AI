<template>
    <div class="container">
        <div style="margin: 8px 0;" v-if="!error">
            <small>
                Mã phòng: <strong>{{ roomID }}</strong>
                — Link mời:
                <a :href="inviteLink" target="_blank">Mở link Audience</a>
                <button @click="copyInvite" style="margin-left:8px">Copy</button>
            </small>
        </div>
        <div v-if="error" class="">
            <p>{{ error }}</p>
        </div>
        <div v-else class="" ref="chatRoomElement" style="height: 100vh; width: 100%; border: 2px solid #000;">
            <!-- <p v-if="loading">Loading live stream...</p> -->
            <!-- <div v-else id="live-stream-container" style="height: 80vh; width: 100%; background-color: #000;"></div> -->

        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { ZegoUIKitPrebuilt } from "@zegocloud/zego-uikit-prebuilt";

export default {
    data() {
        return {
            chatData: null,
            roomID: "default-room",
            role: "host", // or "audience"
            loading: false,
            error: null,
            inviteLink: "",
        }
    },
    mounted() {
        const url = new URL(window.location.href);
        const params = Object.fromEntries(url.searchParams.entries());
        this.roomID = params.roomID ?? (Math.floor(Math.random() * 100000) + "");
        this.role = params.role ?? "host";
        this.startLiveStream();
    },
    methods: {
        copyInvite() {
            if (!this.inviteLink) return;
            navigator.clipboard?.writeText(this.inviteLink);
        },

        async startLiveStream() {
            const user = this.$page?.props?.auth?.user ?? null;
            const userName = user?.name ?? `Guest-${Math.floor(Math.random()*100000)}`;
            const userID = String(user?.id ?? `g${Date.now()}`);

            let appID = this.$page?.props?.chatRoom?.appID;
            let serverSecret = this.$page?.props?.chatRoom?.serverSecret;
            let zegoRole = "audience"; // Default role

            // Fallback: fetch from backend REST API if props are missing
            if (!appID || !serverSecret) {
                try {
                    const apiBase = `${window.location.protocol}//${window.location.hostname}:8081`;
                    const res = await axios.get(`${apiBase}/api/stream/token`, {
                        params: { roomId: this.roomID },
                        headers: {
                            Authorization: "Bearer " + localStorage.getItem("token"),
                        },
                    });
                    appID = res.data?.appID;
                    serverSecret = res.data?.token; // Use token as serverSecret for generateKitTokenForTest
                    zegoRole = res.data?.role || "audience"; // Get role from API response
                } catch (e) {
                    console.error('Fetch credentials failed', e);
                }
            }

            if (!appID || !serverSecret) {
                this.error = "Thiếu Zego appID/serverSecret từ backend. Vui lòng cấu hình .env hoặc VITE_API_URL.";
                return;
            }

            const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(
                appID,
                serverSecret,
                this.roomID,
                userID,
                userName
            );

            // Use role from API response, default to Audience for client
            const role = zegoRole === "host" ? ZegoUIKitPrebuilt.Host : ZegoUIKitPrebuilt.Audience;

            let config = {};





            // Client view: no host controls
            if (false) {
                config = {
                    turnOnCameraWhenJoining: true,
                    showMyCameraToggleButton: true,
                    showAudioVideoSettingsButton: true,
                    showScreenSharingButton: true,
                    showTextChat: true,
                    showUserList: true,
                };
            }


            const zp = ZegoUIKitPrebuilt.create(kitToken);
            zp.joinRoom({
                container: this.$refs.chatRoomElement,
                scenario: {
                    mode: ZegoUIKitPrebuilt.LiveStreaming,
                    config: {
                        role,
                    }
                },
                sharedLinks: [
                    {
                        name: 'Join as Audience',
                        url: `${window.location.origin}${window.location.pathname}?roomID=${this.roomID}&role=Audience`,
                    }],
                ...config,
            });

            this.inviteLink = `${window.location.origin}${window.location.pathname}?roomID=${this.roomID}&role=Audience`;

            // this.loading = true;
            // setTimeout(() => {
            //     this.initLiveStream();
            //     this.loading = false;
            // }, 3000);
        },

        // async initLiveStream() {
        //     const appID = 123456789; // Replace with your App ID
        //     const serverSecret = "your_server_secret"; // Replace with your Server Secret
        //     const userID = "user123"; // Replace with the user ID
        //     const userName = "User 123"; // Replace with the user name
        //     const roomID = "room123"; // Replace with the room ID

        //     const kitToken = ZegoUIKitPreBuilt.generateKitTokenForTest(appID, serverSecret, roomID, userID, userName);
        //     const zp = ZegoUIKitPreBuilt.create(kitToken);

        //     zp.joinRoom({
        //         container: document.getElementById('live-stream-container'),
        //         scenario: {
        //             mode: ZegoUIKitPreBuilt.LiveStreamingMode.Host,
        //         },
        //         sharedLinks: [
        //             {
        //                 name: 'Join as Audience',
        //                 url: window.location.href,
        //             },
        //         ],
        //     });
        // }
    },
}
</script>
<style></style>
