<template>
  <div class="container">
    <div class="row">
      <!-- infor -->
      <div class="col-lg-7 col-md-12 mb-4 d-flex">
        <div class="card">
          <div class="card-body p-4">
            <div class="row">
              <div
                class="col-lg-4 col-md-12 d-flex flex-column justify-content-center align-items-center mb-lg-0 mb-xs-4">
                <!-- <img src="../../../assets/img/user_test.jpg" class="avatar mb-4" alt="" /> -->
                <img :src="userData.avt || '/src/assets/img/avt.png'" class="avatar m-0 mb-4 " alt="" />



                <router-link to="/client/edit-profile">
                  <button class="btn btn-outline-success w-100 text-nowrap mt-auto">
                    Edit Profile
                  </button>

                </router-link>

              </div>

              <div class="col-lg-8 col-md-12 d-flex flex-column">
                <h4 class="fw-bold text-success mt-auto pb-3">{{ userData.username }}</h4>
                <div class="mt-auto d-flex flex-column gap-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="m-0 fw-bold">Phone</p>
                    <p class="m-0 text-success">{{ userData.phonenumber }}</p>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="m-0 fw-bold">Email</p>
                    <p class="m-0 text-success">{{ userData.email }}</p>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="m-0 fw-bold">Citizen identification</p>
                    <p class="m-0 text-success">{{ userData.cccd }}</p>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="m-0 fw-bold">Date of birth</p>
                    <p class="m-0 text-success">{{ userData.dateOfBirth }}</p>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <p class="m-0 fw-bold">Address</p>
                    <p class="m-0 text-success">{{ userData.address }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 4 khối -->
      <div class="col-lg-5 col-md-12 mb-4 d-flex ">
        <div class="row d-flex">
          <div class="col-lg-12 mb-3">
            <div class="card">
              <div class="card-body p-2">
                <h5 class="fw-bold m-0 text-success text-center">Auction Statistics</h5>
              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-12 mb-md-2 mb-3">
            <div class="card bg-success text-white">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div class="">
                  <p class="fw-bold">Monthly Auctions</p>
                  <p class="fw-bold m-0">10 works</p>
                </div>
                <div class="bg-custom px-3 py-4 rounded-circle hide-on-small">
                  <i class="fa-solid fa-gavel text-success flip-x fa-2xl"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-12 mb-md-2 mb-3">
            <div class="card bg-success text-white">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div class="">
                  <p class="fw-bold">Works Auctioned</p>
                  <p class="fw-bold m-0">5 works</p>
                </div>
                <div class="bg-custom px-3 py-4 rounded-circle hide-on-small">
                  <i class="fa-solid fa-panorama text-success flip-x fa-2xl"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-12 mb-md-0 mb-3">
            <div class="card bg-success text-white">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div class="">
                  <p class="fw-bold">Total Spending</p>
                  <p class="fw-bold m-0">$ 80M</p>
                </div>
                <div class="bg-custom px-3 py-4 rounded-circle hide-on-small">
                  <i class="fa-solid fa-sack-dollar text-success fa-2xl"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6 col-md-6 col-sm-12  mb-md-0 mb-3">

            <div class="card bg-success text-white">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div class="">
                  <p class="fw-bold">Auction Revenue</p>
                  <p class="fw-bold m-0">$ 100M</p>
                </div>
                <div class="bg-custom px-3 py-4 rounded-circle hide-on-small">
                  <i class="fa-solid fa-hand-holding-dollar text-success fa-2xl"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <SubMenuProfile />
    </div>
  </div>
  <!-- menu phụ + vùng gắn trang con -->
</template>
<script>

import SubMenuProfile from '@/components/SubMenuProfile.vue'
import axios from 'axios';
export default {
  components: { SubMenuProfile },

  data() {
    return {
      userData: {},

    }
  },

  mounted() {
    this.loadUserData();

    window.addEventListener('avatar-updated', this.handleAvatarUpdate);
  },

  beforeUnmount() {
    window.removeEventListener('avatar-updated', this.handleAvatarUpdate);
  },

  methods: {
    handleAvatarUpdate(event) {
      const newAvatar = event.detail.avatar;
      console.log('Profile - Avatar updated:', newAvatar);

      // Cập nhật avatar trong userData
      this.userData.avt = newAvatar;
    },

    loadUserData() {
      axios
        .get('http://localhost:8081/api/user/info', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem("token")
          }
        })
        .then((res) => {
          this.userData = res.data;
          console.log(this.userData);

        })
        .catch((err) => {
          console.error(err);
        });
    },
  }
}

</script>
<style></style>
