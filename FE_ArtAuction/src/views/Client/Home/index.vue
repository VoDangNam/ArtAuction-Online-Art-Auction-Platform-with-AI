<template>
  <!-- ========== Carousel ========== -->
  <div class="row bg-success py-5 mb-4">
    <div class="col-lg-12">
      <div class="container">
        <div class="row">
          <div data-aos="fade-right" data-aos-duration="800"
            class="col-lg-6 text-light d-flex flex-column justify-content-center gap-5">
            <div class="">
              <h1 class=" fw-bold">Welcome back, <span class="text-success-light-home fs-1 fw-bold"> {{ user.name
              }}</span> !</h1>
              <p>Discover extraordinary artworks and place your bids on masterpieces</p>
            </div>
            <div class="d-flex align-items-center gap-5">
              <div class="stat">
                <div class="d-flex align-items-center gap-3 fs-4 mb-2">
                  <i class="fa-solid fa-gavel"></i>
                  <p class="fw-bold number m-0">247</p>
                </div>
                <div class="label">Live Auctions</div>
              </div>
              <div class="stat">
                <div class="d-flex align-items-center gap-3 fs-4 mb-2">
                  <i class="fa-solid fa-image"></i>
                  <p class="fw-bold number m-0">1.2K</p>
                </div>
                <div class="label">Available Artworks</div>
              </div>
              <div class="stat">
                <div class="d-flex align-items-center gap-3 fs-4 mb-2">
                  <i class="fa-solid fa-users"></i>
                  <p class="fw-bold number m-0">5.8K</p>
                </div>
                <div class="label">Active Bidders</div>
              </div>
            </div>
          </div>
          <div data-aos="fade-left" data-aos-duration="800" class="col-lg-6">
            <div id="carouselExampleIndicators"
              class="carousel slide carousel-fade border border-4 border-light shadow-lg rounded-4 overflow-hidden"
              data-bs-ride="carousel" data-bs-interval="2000">
              <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"
                  aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"
                  aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"
                  aria-label="Slide 3"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="3"
                  aria-label="Slide 3"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="4"
                  aria-label="Slide 3"></button>
              </div>
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <img src="https://i.pinimg.com/736x/88/cd/21/88cd216810a2be6669f35bea9c98293c.jpg"
                    class="d-block w-100" style="height: 350px;" alt="...">
                </div>
                <div class="carousel-item">
                  <img src="https://i.pinimg.com/1200x/36/19/09/36190987c6cd3c29ec4f1ac202decbf1.jpg"
                    class="d-block w-100" style="height: 350px;" alt="...">
                </div>
                <div class="carousel-item">
                  <img src="https://i.pinimg.com/736x/c5/8d/17/c58d170aa6f5dd02eae800c604e94c69.jpg"
                    class="d-block w-100" style="height: 350px;" alt="...">
                </div>
                <div class="carousel-item">
                  <img src="https://i.pinimg.com/1200x/77/e5/c5/77e5c5b3543c4312a06d8279aa0add6a.jpg"
                    class="d-block w-100" style="height: 350px;" alt="...">
                </div>
                <div class="carousel-item">
                  <img src="https://i.pinimg.com/1200x/ca/b4/30/cab4302b07b4c54695c3affacfcf63e3.jpg"
                    class="d-block w-100" style="height: 350px;" alt="...">
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- ========== Các cuộc đấu đang diễn ra ========== -->
  <div class="container py-5">
    <div class="row">
      <div class="col-12 text-center mb-4" data-aos="fade-up" data-aos-duration="800">
        <h3 class="fw-bold mb-2 text-success">Featured Auctions</h3>
        <p>Join the most exciting live auctions happening right now</p>
      </div>
      <div class="col-12">
        <div class="row">
          <template v-for="(auction, index) in ongoingAuctions" :key="auction.id">
            <!-- Card đấu giá -->
            <div class="col-lg-3 col-md-6 col-12 mb-4 d-flex" data-aos="fade-up" :data-aos-delay="index * 100" data-aos-duration="600">
              <div class="card p-0 overflow-hidden auction-card">
                <div class="p-0 position-relative">
                  <img :src="auction.imageAuctionRoom" class="img-auction" alt="" loading="lazy">
                  <div class="">
                    <span class="badge position-absolute top-0 start-0 m-3 bg-danger px-3">LIVE</span>
                  </div>
                  <span class="badge position-absolute top-0 end-0 m-3 bg-success px-3">12:35</span>
                  <span class="badge position-absolute bottom-0 end-0 m-3 bg-success">{{ auction.viewCount }}
                    bidders</span>
                </div>
                <!-- Nội dung card -->
                <div class="card-body d-flex flex-column gap-3">
                  <div class="d-flex flex-column gap-2">
                    <p class="fw-bold m-0 text-success fs-5"> {{ auction.roomName }} </p>
                    <p class="m-0 text-muted small"> {{ auction.id }} </p>
                    <div class="d-flex gap-2 align-items-center justify-content-between">
                      <span class="m-0">Category</span>
                      <span class="m-0"> {{ auction.type }} </span>
                    </div>
                    <p class="m-0 small description-clamp"> {{ auction.description }} </p>
                  </div>
                  <div class="mt-auto">
                    <div class="">
                      <router-link :to="`/client/auction-room/${auction.id}`" class="w-100">
                        <button class="btn btn-success w-100">Join AuctAuction</button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
      <div class="col-12 text-center mt-3">
        <button class="btn btn-outline-success px-5 fs-5">Discover</button>
      </div>
    </div>
  </div>

  <!-- ========== Browse by Category ========== -->
  <div class="row bg-success-light-home py-5">
    <div class="col-lg-12">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center mb-4" data-aos="fade-up" data-aos-duration="800">
            <h3 class="fw-bold mb-2 text-success">Browse by Category</h3>
            <p>Explore diverse art collections</p>
          </div>
          <div class="col-lg-12">
            <div class="row">
              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="0" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-palette text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Paintings</p>
                    <span class="text-muted small m-0">342 items</span>
                  </div>
                </div>
              </div>

              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-brush text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Sculptures</p>
                    <span class="text-muted small m-0">156 items</span>
                  </div>
                </div>
              </div>

              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-camera text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Photography</p>
                    <span class="text-muted small m-0">289 items</span>
                  </div>
                </div>
              </div>

              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="300" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-laptop text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Digital Art</p>
                    <span class="text-muted small m-0">421 items</span>
                  </div>
                </div>
              </div>

              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="400" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-layer-group text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Mixed Media</p>
                    <span class="text-muted small m-0">198 items</span>
                  </div>
                </div>
              </div>

              <div class="col-lg-2 col-md-4 col-6" data-aos="fade-up" data-aos-delay="500" data-aos-duration="600">
                <div class="card auction-card">
                  <div class="card-body text-center">
                    <div class="d-flex mb-3">
                      <div class="mx-auto p-3 bg-light rounded-circle">
                        <i class="fa-solid fa-print text-success fs-2"></i>
                      </div>
                    </div>
                    <p class="fw-bold fs-6 mb-1">Prints</p>
                    <span class="text-muted small m-0">267 items</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========== Tác phẩm nổi bật ========== -->
  <div class="container">
    <div class="row my-5">
      <div class="col-12 text-center mb-4" data-aos="fade-up" data-aos-duration="800">
        <h3 class="fw-bold mb-2 text-success">Featured Artwork</h3>
        <p>Explore standout creations handpicked from our curated collection</p>
      </div>

      <!-- Loading state -->
      <!-- <div v-if="loading" class="col-12 text-center py-5">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Đang tải tác phẩm...</p>
      </div> -->

      <!-- Error state -->
      <!-- <div v-else-if="error" class="col-12 text-center py-5">
        <div class="alert alert-warning" role="alert">
          <i class="fa-solid fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
      </div> -->
      <!-- bg-opacity-75 -->
      <!-- style="background: rgba(0, 0, 0, 0.5); border-bottom-left-radius: 0.5rem; border-bottom-right-radius: 0.5rem;" -->
      <!-- Content -->
      <div class="col-lg-12">
        <div class="row">
          <template v-for="(item, index) in featuredList.slice(0, 4)" :key="item.id">
            <div class="col-12 col-md-6 col-lg-3 mb-4 d-flex" data-aos="fade-up" :data-aos-delay="index * 100" data-aos-duration="600">
              <div class="card auction-card w-100">
                <div class="card-body p-2 position-relative featured-art-card">
                  <div class="featured-art-image-wrapper position-relative ">
                    <img :src="item.avtArtwork" alt="thumb" class="w-100 rounded-2 featured-art-image" loading="lazy" />
                    <div class="position-absolute top-0 start-0 w-100 p-2 artwork-overlay overlay-top">
                      <div class="bg-dark bg-opacity-75 text-white rounded-3 p-2">
                        <p class="m-0 fw-bold">
                          {{ item.title }}
                        </p>
                      </div>
                    </div>
                    <div class="position-absolute bottom-0 start-0 w-100 p-2 artwork-overlay overlay-bottom">
                      <div class="bg-dark bg-opacity-75 text-white rounded-3 p-2">
                        <div class="d-flex justify-content-between align-items-center">
                          <p class="m-0 small fw-bold text-white">
                            {{ item.ownerName }}
                          </p>
                          <span class="m-0 small bg-success text-white p-1 px-3 rounded-2">
                            {{ item.paintingGenre }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="artwork-info d-flex">
                    <p class="m-0 small text-muted">
                      {{ item.description }}
                    </p>
                  </div>
                </div>

              </div>
            </div>
          </template>
        </div>
      </div>
      <!-- <template v-for="item in featuredList" :key="item.id">
        <div class="col-12 col-md-6 col-lg-4 mb-4 d-flex">
          <div class="card w-100 p-0">
            <div class="card-body">
              <div class="row">
                <div class="col-4 d-flex align-items-center pe-lg-0">
                  <img :src="item.avtArtwork" alt="thumb" class="w-100 img-thumbnail img-art" loading="lazy" />
                </div>

                <div class="col-8 d-flex flex-column gap-2">
                  <p class="m-0 fw-bold title-clamp">
                    {{ item.title }}
                  </p>
                  <div class="d-flex small justify-content-between align-items-center">
                    <p class="m-0">Author</p>
                    <p class="m-0">
                      {{ item.ownerName }}
                    </p>
                  </div>
                  <div class="d-flex small justify-content-between align-items-center">
                    <p class="m-0">Category</p>
                    <p class="m-0">
                      {{ item.paintingGenre }}
                    </p>
                  </div>

                  <p class="m-0 small description-clamp">
                    {{ item.description }}
                  </p>

                </div>
              </div>
            </div>

          </div>
        </div>
      </template> -->

    </div>
  </div>

  <!-- ========== Các cuộc đấu giá sắp tới ========== -->
  <!-- <div class="row">
    <div class="col-12">
      <div class="container">
        <div class="row pt-4 mb-5">

          <div class="col-12 text-center mb-4" data-aos="fade-up" data-aos-duration="800">
            <h3 class="fw-bold mb-2 text-success">Upcoming Auctions</h3>
            <p>Mark your calendar for these exciting events</p>
          </div>
          <template v-for="(auction, index) in upcomingAuctions" :key="auction.id">
            <div class="col-lg-3 col-md-6 col-12 mb-4 d-flex" data-aos="fade-up" :data-aos-delay="index * 100" data-aos-duration="600">
              <div class="card p-0 overflow-hidden auction-card">
                <div class="p-0 position-relative">
                  <img :src="auction.imageAuctionRoom" class="img-auction" alt="" loading="lazy">
                  <div class="">
                    <span class="badge position-absolute top-0 start-0 m-3 bg-warning px-3 text-dark">Upcoming</span>
                  </div>
                </div>
                <div class="card-body d-flex flex-column gap-3">
                  <div class="d-flex flex-column gap-2">
                    <p class="fw-bold m-0 text-success fs-5"> {{ auction.roomName }} </p>
                    <p class="m-0 text-muted small"> {{ auction.id }} </p>
                    <div class="d-flex gap-2 align-items-center justify-content-between">
                      <span class="m-0">Category</span>
                      <span class="m-0"> {{ auction.type }} </span>
                    </div>
                    <p class="m-0 small description-clamp"> {{ auction.description }} </p>
                  </div>
                  <div class="mt-auto">
                    <div class="">
                      <router-link :to="`/client/Regis-auct-room/${auction.id}`" class="w-100">
                        <button class="btn btn-outline-warning w-100">Reserve Spot</button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <div class="col-12 text-center mt-3">
            <button class="btn btn-outline-success px-5 fs-5">Discover</button>
          </div>
        </div>
      </div>
    </div>
  </div> -->
</template>

<script>
import axios from "axios";

export default {
  // name: "ClientHome",
  data() {
    return {
      user: {},
      featuredList: [],
      loading: false,
      error: null,
      ongoingAuctions: [],
      upcomingAuctions: [],
    };
  },

  mounted() {
    this.user = {
      name: localStorage.getItem("name_kh"),
    };
    this.fetchFeatured();
    this.fetchSixRoomFeatured();
  },

  methods: {
    goToRoom(id) {
      if (!id) return;
      this.$router.push({
        name: 'auction-room',
        params: { id }
      });
    },

    fetchFeatured() {
      this.loading = true;
      axios
        .get("http://localhost:8081/api/artwork/top-4-highest-price")
        .then((res) => {
          this.featuredList = res.data;
          console.log("✅ Top 4 highest price artworks:", this.featuredList);
        })
        .catch((err) => {
          this.error = err.message;
          console.error("❌ Error fetching featured artworks:", err);
        });
    },

    async fetchSixRoomFeatured() {
      this.loading = true;
      try {
        // Fetch top 4 ongoing auctions (status = 1)
        const ongoingResponse = await axios.get("http://localhost:8081/api/auctionroom/top-4-ongoing");
        this.ongoingAuctions = ongoingResponse.data || [];
        console.log("✅ Top 4 ongoing auctions:", this.ongoingAuctions);

        // Fetch top 4 upcoming auctions with highest price (status = 0)
        const upcomingResponse = await axios.get("http://localhost:8081/api/auctionroom/top-4-upcoming-highest-price");
        this.upcomingAuctions = upcomingResponse.data || [];
        console.log("✅ Top 4 upcoming auctions:", this.upcomingAuctions);
      } catch (err) {
        this.error = err.message;
        console.error("❌ Error fetching auction rooms:", err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style></style>
