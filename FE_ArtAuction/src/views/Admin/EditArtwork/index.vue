<template>
  <div class="container-fluid py-4 bg-light-subtle min-vh-100">
    <div
      v-if="isLoading"
      class="d-flex flex-column align-items-center justify-content-center py-5"
      style="min-height: 400px"
    >
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3 text-secondary fw-medium">Loading artwork data...</p>
    </div>

    <div v-else class="container-xl">
      <div
        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4"
      >
        <div class="mb-3 mb-md-0">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb mb-1">
              <li class="breadcrumb-item">
                <router-link to="/admin/management-artwork" class="text-decoration-none"
                  >Artwork Management</router-link
                >
              </li>
              <li class="breadcrumb-item active text-muted" aria-current="page">Edit Artwork</li>
            </ol>
          </nav>
          <div class="d-flex align-items-center gap-3">
            <h4 class="fw-bold text-primary mb-0">Edit: {{ artworkForm.title }}</h4>
            <span
              class="badge rounded-pill px-3 py-2 border"
              :class="getStatusClass(artworkForm.status)"
            >
              {{ convertStatus(artworkForm.status) }}
            </span>
          </div>
        </div>

        <div class="d-flex gap-2">
          <button
            class="btn btn-white border shadow-sm fw-medium text-secondary"
            @click="$router.back()"
          >
            <i class="fa-solid fa-xmark me-2"></i>Cancel
          </button>
          <button
            class="btn btn-primary shadow-sm fw-bold px-4"
            @click="saveChanges"
            :disabled="isSaving"
          >
            <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fa-solid fa-floppy-disk me-2"></i>Save Changes
          </button>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-lg-8">
          <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
              <div class="d-flex align-items-center gap-3">
                <div
                  class="bg-secondary bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-solid fa-pen-nib"></i>
                </div>
                <h6 class="fw-bold mb-0 text-uppercase text-secondary">General Information</h6>
              </div>
            </div>
            <div class="card-body p-4">
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">ARTWORK TITLE</label>
                <input
                  type="text"
                  class="form-control bg-light border-0 fw-bold"
                  v-model="artworkForm.title"
                  placeholder="Enter artwork title..."
                />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">AUTHOR / ARTIST</label>
                <input
                  type="text"
                  class="form-control bg-light border-0"
                  v-model="artworkForm.author"
                  placeholder="Artist name..."
                />
              </div>
              <div class="mb-0">
                <label class="form-label small fw-bold text-secondary">DESCRIPTION</label>
                <textarea
                  class="form-control bg-light border-0"
                  rows="5"
                  v-model="artworkForm.description"
                  placeholder="Write a description regarding the artwork..."
                ></textarea>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
              <div class="d-flex align-items-center gap-3">
                <div
                  class="bg-info bg-opacity-10 text-info rounded-circle d-flex align-items-center justify-content-center"
                  style="width: 40px; height: 40px"
                >
                  <i class="fa-solid fa-sliders"></i>
                </div>
                <h6 class="fw-bold mb-0 text-uppercase text-secondary">Specifications</h6>
              </div>
            </div>
            <div class="card-body p-4">
              <div class="row g-3">
                <div class="col-12 col-md-6">
                  <label class="form-label small fw-bold text-secondary">Painting Genre</label>
                  <input
                    type="text"
                    class="form-control bg-light border-0"
                    v-model="artworkForm.paintingGenre"
                    placeholder="e.g. Oil on Canvas"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <label class="form-label small fw-bold text-secondary">YEAR OF CREATION</label>
                  <input
                    type="number"
                    class="form-control bg-light border-0"
                    v-model="artworkForm.yearOfCreation"
                    placeholder="YYYY"
                    :max="new Date().getFullYear()"
                  />
                  <!-- <small v-if="errors.yearOfCreation" class="text-danger">{{
                    errors.yearOfCreation
                  }}</small> -->
                </div>
                <div class="col-12 col-md-6">
                  <label class="form-label small fw-bold text-secondary">SIZE (Dimensions)</label>
                  <input
                    type="text"
                    class="form-control bg-light border-0"
                    v-model="artworkForm.size"
                    placeholder="e.g. 100x80 cm"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 col-lg-4">
          <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
            <div class="card-body p-0 position-relative bg-dark">
              <div class="position-absolute top-0 end-0 p-3 z-1">
                <span
                  class="badge bg-dark bg-opacity-75 backdrop-blur border border-secondary text-white"
                >
                  <i class="fa-solid fa-lock me-1"></i> Image Locked
                </span>
              </div>

              <div class="ratio ratio-1x1">
                <img
                  :src="artworkForm.avtArtwork"
                  alt="Artwork Preview"
                  class="object-fit-cover w-100 h-100 opacity-90"
                />
              </div>

              <div class="p-3 bg-light border-top">
                <small class="text-muted d-flex align-items-center">
                  <i class="fa-solid fa-circle-info text-warning me-2"></i>
                  <span
                    >The artwork image cannot be modified once uploaded to ensure
                    authenticity.</span
                  >
                </small>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
              <h6 class="fw-bold mb-0 text-uppercase text-secondary">
                <i class="fa-solid fa-tag me-2"></i>Sales & Status
              </h6>
            </div>
            <div class="card-body p-4">
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">STARTING PRICE</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-0 text-success fw-bold">₫</span>
                  <input
                    type="number"
                    class="form-control bg-light border-0 fw-bold fs-5 text-end"
                    v-model.number="priceVND"
                    min="0"
                    step="1000"
                    placeholder="0"
                  />
                </div>
              </div>

              <hr class="border-secondary opacity-10 my-3" />

              <div class="alert alert-light border d-flex align-items-center mb-0" role="alert">
                <i class="fa-regular fa-clock me-2 text-secondary"></i>
                <div class="small text-secondary">
                  Created at: <strong>{{ artworkForm.createdAt }}</strong>
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
import axios from "axios";

export default {
  name: "EditArtwork",
  data() {
    return {
      artworkId: null,
      isLoading: false,
      isSaving: false,
      errors: {},
      artworkForm: {
        title: "",
        paintingGenre: "",
        author: "",
        yearOfCreation: "",
        material: "",
        size: "",
        priceVND: 0,
        status: 0,
        description: "",
        avtArtwork: "",
        createdAt: "",
      },
      priceVND: 0,
    };
  },
  mounted() {
    this.artworkId = this.$route.params.id;
    if (this.artworkId) {
      this.loadArtworkDetail();
    }
  },
  methods: {
    formatCurrencyVND(value) {
      if (!value) return "0 ₫";
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
      }).format(value);
    },
    // Load dữ liệu chi tiết
    loadArtworkDetail() {
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/artworks/${this.artworkId}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then((res) => {
          const data = res.data;
          console.log("API Response:", data);

          const artworkData = Array.isArray(data) ? data[0] : data;

          if (artworkData) {
            this.artworkForm = {
              title: artworkData.title || "",
              paintingGenre: artworkData.paintingGenre || "",
              author: artworkData.author || "",
              yearOfCreation: artworkData.yearOfCreation || "",
              material: artworkData.material || "",
              size: artworkData.size || "",
              priceVND: artworkData.startedPrice || 0,

              status: artworkData.status !== undefined ? artworkData.status : 0,
              description: artworkData.description || "",

              avtArtwork: artworkData.avtArtwork || "",
              createdAt: artworkData.createdAt || "",
            };

            this.priceVND = artworkData.startedPrice || 0;
          }
        })
        .catch((err) => {
          console.error(err);
          alert("Unable to load work information.");
        })
        .finally(() => (this.isLoading = false));
    },

    saveChanges() {
      this.errors = {};
      const currentYear = new Date().getFullYear();

      // Validate Năm sáng tác
      if (this.artworkForm.yearOfCreation > currentYear) {
        this.errors.yearOfCreation = `Year cannot be in the future (Max: ${currentYear})`;
        alert("Invalid Year of Creation!");
        return;
      }

      // Validate Giá VND
      if (this.priceVND <= 0) {
        this.errors.price = "Starting price must be greater than 0 ₫.";
        return;
      }

      if (this.artworkForm.yearOfCreation < 0) {
        this.errors.yearOfCreation = "Year cannot be negative";
        return;
      }

      this.isSaving = true;
      const payload = {
        title: this.artworkForm.title,
        author: this.artworkForm.author,
        paintingGenre: this.artworkForm.paintingGenre,
        yearOfCreation: this.artworkForm.yearOfCreation,
        material: this.artworkForm.material,
        size: this.artworkForm.size,
        startedPrice: Math.round(Number(this.priceVND)),
        status: this.artworkForm.status,
        description: this.artworkForm.description,
      };

      axios
        .put(
          `http://localhost:8081/api/admin/artworks/cap-nhat-tac-pham/${this.artworkId}`,
          payload,
          {
            headers: { Authorization: "Bearer " + localStorage.getItem("token") },
          }
        )
        .then(() => {
          alert("Artwork updated successfully!");
          this.$router.push("/admin/management-artwork");
        })
        .catch((err) => {
          console.error(err);
          alert("Failed to update artwork.");
        })
        .finally(() => (this.isSaving = false));
    },

    convertStatus(status) {
      switch (status) {
        case 0:
          return "Not approved";
        case 1:
          return "Approved";
        case 2:
          return "Up for auction";
        case 3:
          return "Refused";
        default:
          return "Unknown";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 0:
          return "bg-secondary-subtle border-secondary-subtle text-secondary";
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 2:
          return "bg-warning-subtle border-warning-subtle text-warning-emphasis";
        case 3:
          return "bg-danger-subtle border-danger-subtle text-danger";
        default:
          return "bg-light text-dark";
      }
    },
    getStatusBackground(status) {
      switch (status) {
        case 0:
          return "bg-secondary-subtle text-secondary";
        case 1:
          return "bg-success-subtle text-success";
        case 2:
          return "bg-warning-subtle text-dark";
        case 3:
          return "bg-danger-subtle text-danger";
        default:
          return "bg-light text-dark";
      }
    },
  },
};
</script>

<style scoped>
.backdrop-blur {
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* Custom cho input */
.form-control:focus,
.form-select:focus {
  background-color: #fff;
  border: 1px solid #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}
</style>
