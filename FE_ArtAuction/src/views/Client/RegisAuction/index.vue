<template>
  <div class="container-fluid mb-5">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading auction room information...</p>
    </div>

    <!-- Main Content -->
    <div v-else class="container">

      <!-- Progress Steps -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card p-0">
            <div class="card-body">
              <div class="d-flex justify-content-center align-items-center gap-3">
                <div class="text-center">
                  <div class="rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2"
                    :class="currentStep >= 1 ? 'bg-success text-white' : 'bg-secondary text-white'"
                    style="width: 40px; height: 40px;">
                    <strong>1</strong>
                  </div>
                  <small :class="currentStep >= 1 ? 'text-success fw-bold' : 'text-muted'">Information</small>
                </div>
                <div class="border-top flex-grow-1" :class="currentStep > 1 ? 'border-success' : 'border-secondary'"
                  style="width: 100px; max-width: 150px; border-width: 3px !important;"></div>
                <div class="text-center">
                  <div class="rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2"
                    :class="currentStep >= 2 ? 'bg-success text-white' : 'bg-secondary text-white'"
                    style="width: 40px; height: 40px;">
                    <strong>2</strong>
                  </div>
                  <small :class="currentStep >= 2 ? 'text-success fw-bold' : 'text-muted'">Confirmation</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 1: Auction Information -->
      <div v-show="currentStep === 1">
        <div class="row">
          <!-- Room Details -->
          <div class="col-lg-8">
            <div class="card shadow-md p-0">
              <div class="card-header bg-success text-white">
                <h5 class="m-1"><i class="fa-solid fa-info-circle me-3"></i>Room Details</h5>
              </div>
              <div class="card-body">
                <div class="row d-flex">
                  <div class="col-lg-6">
                    <div class="row gap-3">
                      <div class="col-12">
                        <div class="position-relative overflow-hidden">
                          <img :src="auctionRoom.imageAuctionRoom" class="w-100 rounded-3"
                            style="max-height: 50vh; object-fit: cover;" alt="Auction Room">
                          <span class="position-absolute top-0 start-0 m-3 badge bg-danger">
                            {{ getStatusText(auctionRoom.status) }}
                          </span>
                        </div>
                      </div>
                      <div class="col-12">
                        <div class=" d-flex justify-content-between alert alert-success py-2 m-0">
                          <p class="m-0 text-muted small">Registered Users</p>
                          <p class="m-0"><strong class="text-success">{{ auctionRoom.viewCount || 0 }}</strong>
                          </p>
                        </div>

                      </div>
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="row gap-3">
                      <div class="col-12 d-flex justify-content-between">
                        <p class="m-0  small">Room ID</p>
                        <p class="m-0 fw-semibold">{{ auctionRoom.id }}</p>
                      </div>
                      <div class="col-12 d-flex justify-content-between">
                        <p class="m-0  small">Room Name</p>
                        <p class="m-0 fw-bold">{{ auctionRoom.roomName }}</p>
                      </div>
                      <div class="col-12 d-flex justify-content-between">
                        <p class="m-0  small">Type</p>
                        <p class="m-0"><span class="badge bg-success">{{ auctionRoom.type }}</span></p>
                      </div>
                      <div class="col-12 d-flex justify-content-between">
                        <p class="m-0  small">Start</p>
                        <p class="m-0">{{ formatTime(auctionRoom.startedAt) }}</p>
                      </div>
                      <div class="col-12 d-flex justify-content-between">
                        <p class="m-0  small">End</p>
                        <p class="m-0">{{ formatTime(auctionRoom.stoppedAt) }}</p>
                      </div>
                      <div class="col-12">
                        <p class="m-0  small">Description</p>
                        <p class="m-0 ">{{ auctionRoom.description || 'N/A' }}</p>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- Artworks List -->
          <div class="col-lg-4" v-if="sessions.length > 0">
            <div class="card shadow-md border-0 p-0">
              <div class="card-header bg-success text-white">
                <h5 class="m-1"><i class="fa-solid fa-palette me-3"></i>Auction Items ({{ sessions.length }})</h5>
              </div>
              <div class="card-body p-2" style="max-height: 500px; overflow-y: auto;">
                <div class="list-group list-group-flush">
                  <a v-for="(session, index) in sessions" :key="session.id" href="#"
                    class="list-group-item list-group-item-action p-2 mb-2 rounded" data-bs-toggle="modal"
                    data-bs-target="#sessionModal" @click="selectedSession = session">
                    <div class="d-flex gap-3 align-items-center">
                      <!-- Artwork Image -->
                      <div class="flex-shrink-0 position-relative">
                        <img :src="session.imageUrl || 'https://via.placeholder.com/80x80?text=No+Image'"
                          class="rounded" style="width: 80px; height: 80px; object-fit: cover;" alt="Artwork">
                        <span
                          class="position-absolute top-0 start-0 badge bg-light text-success border border-2 border-success rounded-circle m-1"
                          style="width: 25px; height: 25px; font-size: 0.8rem; padding: 0; display: flex; align-items: center; justify-content: center;">
                          {{ index + 1 }}
                        </span>
                      </div>

                      <!-- Artwork Info -->
                      <div class="flex-grow-1 min-w-0">
                        <h6 class="mb-1 fw-bold text-truncate">{{ session.artworkTitle || session.artworkId }}</h6>
                        <div class="small">
                          <div class="d-flex justify-content-between mb-1">
                            <span class="text-muted">Starting Price:</span>
                            <strong class="text-success">{{ formatUSD(session.startingPrice) }}</strong>
                          </div>
                          <div class="d-flex justify-content-between">
                            <span class="text-muted">Bid Step:</span>
                            <strong class="text-success">{{ formatUSD(session.bidStep) }}</strong>
                          </div>
                        </div>
                      </div>

                      <!-- View Icon -->
                      <div class="flex-shrink-0">
                        <i class="fa-solid fa-chevron-right text-muted"></i>
                      </div>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Next Button -->
          <div class="col-12">
            <div class="text-center mt-4">
              <button class="btn btn-success fs-6 px-5" @click="currentStep = 2">
                Continue <i class="fa-solid fa-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Session Detail Modal -->
      <div class="modal fade" id="sessionModal" tabindex="-1" aria-labelledby="sessionModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
          <div class="modal-content" v-if="selectedSession">
            <div class="modal-header bg-success text-white">
              <h5 class="modal-title" id="sessionModalLabel">
                <i class="fa-solid fa-image me-2"></i>Artwork Information
              </h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row g-4 align-items-stretch">
                <!-- Left: Artwork preview card -->
                <div class="col-lg-6 d-flex">
                  <!-- <div class="card p-0"> -->
                  <div class="d-flex align-items-center justify-content-center w-100">
                    <div class="position-relative ">
                      <img
                        :src="selectedSession.artwork?.avtArtwork || selectedSession.imageUrl || selectedSession.artwork?.imageUrls?.[0] || 'https://via.placeholder.com/600x400?text=No+Image'"
                        class="w-100 rounded-3" style="object-fit: cover; cursor: zoom-in; max-height: 55vh;"
                        alt="Artwork preview" @click="openArtworkZoom">
                      <div class="position-absolute top-0 start-0">
                        <div class="px-3 py-2 text-muted">
                          <span class="badge px-3 py-1" :class="getSessionStatusClass(selectedSession.status)">
                            {{ getSessionStatusText(selectedSession.status) }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- </div> -->
                </div>

                <!-- Middle: Artwork detail info -->
                <div class="col-lg-6 d-flex">
                  <div class="row">
                    <div class="col-lg-12 mb-3">
                      <div class="card">
                        <div class="card-body">
                          <h5 class="fw-bold mb-3 text-success">
                            {{ selectedSession.artwork?.title || selectedSession.artworkTitle ||
                              selectedSession.artworkId
                            }}
                          </h5>
                          <p class="text-muted small mb-0">
                            {{ selectedSession.artwork?.description || 'No description available.' }}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="col-lg-6 d-flex">
                      <div class="card p-0">
                        <div class="card-body">
                          <h6 class="text-success fw-bold mb-3">Artwork Details</h6>
                          <div class=" d-flex flex-column gap-3">
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Owner</span>
                              <strong class="small">
                                {{ selectedSession.ownerName || 'N/A' }}
                              </strong>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Genre</span>
                              <strong class="small text-end">
                                {{ selectedSession.artwork?.paintingGenre || 'N/A' }}
                              </strong>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Year</span>
                              <strong class="small text-end">
                                {{ selectedSession.artwork?.yearOfCreation || 'N/A' }}
                              </strong>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Material</span>
                              <strong class="small text-end">
                                {{ selectedSession.artwork?.material || 'N/A' }}
                              </strong>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Size</span>
                              <strong class="small text-end">
                                {{ selectedSession.artwork?.size || 'N/A' }}
                              </strong>
                            </div>
                            <div v-if="selectedSession.artwork?.certificateId"
                              class="d-flex justify-content-between align-items-center">
                              <span class="text-muted small">Certificate</span>
                              <strong class="small text-end">
                                {{ selectedSession.artwork.certificateId }}
                              </strong>
                            </div>
                          </div>



                        </div>
                      </div>
                    </div>

                    <!-- Right: Price information -->
                    <div class="col-lg-6 d-flex">
                      <div class="card p-0">
                        <div class="card-body d-flex flex-column justify-content-between">
                          <div class="">
                            <h6 class="text-success fw-bold mb-3 ">Time Information</h6>
                            <div class="d-flex flex-column gap-3">
                              <div class="d-flex justify-content-between align-items-center">
                                <span class="text-muted small">Start</span>
                                <span class="small">
                                  {{ formatTime(selectedSession.startTime) }}
                                </span>
                              </div>
                              <div class="d-flex justify-content-between align-items-center">
                                <span class="text-muted small">End</span>
                                <span class="small">
                                  {{ formatTime(selectedSession.endedAt) }}
                                </span>
                              </div>
                            </div>
                          </div>

                          <hr>
                          <div class="">
                            <h6 class="text-success fw-bold mb-3">Price Information</h6>
                            <div class=" d-flex flex-column gap-2">
                              <div class="d-flex justify-content-between align-items-center">
                                <span class="text-muted small d-block">Starting Price</span>
                                <span class="fw-bold text-success">
                                  {{ formatUSD(selectedSession.startingPrice) }}
                                </span>
                              </div>
                              <div class="d-flex justify-content-between align-items-center">
                                <span class="text-muted small d-block">Bid Step</span>
                                <span class="fw-bold text-warning">
                                  {{ formatUSD(selectedSession.bidStep) }}
                                </span>
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
          </div>
        </div>
      </div>

      <!-- Zoomed Artwork Modal -->
      <div v-if="showZoomImage && selectedSession" class="modal fade show d-block" tabindex="-1" role="dialog"
        aria-modal="true" @click.self="closeArtworkZoom">
        <div class="modal-backdrop fade show"></div>
        <div class="modal-dialog modal-dialog-centered modal-fullscreen">
          <div class="modal-content bg-dark border-0">
            <div class="modal-header bg-transparent border-0 justify-content-center">
              <h5 class="modal-title text-white text-center w-100">
                {{ selectedSession.artwork?.title || selectedSession.artworkTitle || selectedSession.artworkId }}
              </h5>
              <button type="button" class="btn-close btn-close-white" @click="closeArtworkZoom"></button>
            </div>
            <div class="modal-body text-center">
              <img
                :src="selectedSession.artwork?.avtArtwork || selectedSession.imageUrl || selectedSession.artwork?.imageUrls?.[0] || 'https://via.placeholder.com/1200x800?text=No+Image'"
                class="img-fluid w-100 h-100" style="max-height: 90vh; object-fit: contain;" alt="Artwork zoomed">
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Registration Form -->
      <div v-show="currentStep === 2">
        <div class="row ">
          <div class="col-lg-6">
            <!-- Profile Summary -->
            <div class="card shadow-md border-4 border-success border-top mb-4 p-0">
              <!-- <div class="card-header">
                <h5 class="m-1"><i class="fa-solid fa-clipboard-check me-3"></i>Registration Profile</h5>
              </div> -->
              <div class="card-body">
                <h5 class="m-1 fw-bold text-success"><i class="fa-solid fa-clipboard-check me-3 fa-lg"></i>Registration
                  Profile</h5>
                <hr>
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="d-flex align-items-center gap-3">
                      <div class="border border-2 border-success rounded p-2">
                        <i class="text-success fa-solid fa-user"></i>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <small class="text-muted d-block">User ID</small>
                        <strong>{{ userId }}</strong>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-flex align-items-center gap-3">
                      <div class="border border-2 border-success rounded p-2">
                        <i class="text-success fa-solid fa-door-open"></i>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <small class="text-muted d-block">Auction Room</small>
                        <strong>{{ auctionRoom.roomName }}</strong>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-flex align-items-center gap-3">
                      <div class="border border-2 border-success rounded p-2">
                        <i class="text-success fa-solid fa-images"></i>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <small class="text-muted d-block">Number of Items</small>
                        <strong>{{ sessions.length }} items</strong>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-flex align-items-center gap-3">
                      <div class="border border-2 border-success rounded p-2">
                        <i class="text-success fa-solid fa-calendar-check"></i>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <small class="text-muted d-block">Payment Deadline</small>
                        <strong>{{ auctionRoom.paymentDeadlineDays }} days</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Deposit Card -->
            <div class="card shadow-md  border-4 border-success border-top mb-4 p-0">

              <div class="card-body">
                <div class="d-flex align-items-center">
                  <i class="fa-solid fa-money-bill-wave fa-xl text-success me-3"></i>
                  <div class="m-1 ">
                    <h5 class="fw-bold m-0 text-success">Participation Deposit</h5>
                    <small>Amount required for registration</small>
                  </div>
                </div>
                <hr>
                <div class="text-center my-3">
                  <h2 class="fw-bold text-success mb-0">{{ formatUSD(auctionRoom.depositAmount) }}</h2>
                </div>
                <hr>
                <div class="mb-2">
                  <i class="fa-solid fa-check-circle text-success me-2"></i>
                  <small>100% refund if not winning</small>
                </div>
                <div>
                  <i class="fa-solid fa-calculator text-success me-2"></i>
                  <small>Deducted from total if winning</small>
                </div>
              </div>
            </div>


          </div>
          <div class="col-lg-6">
            <!-- Registration Form -->
            <form @submit.prevent="handleRegister">
              <div class="card shadow-md border-0 mb-4 p-0">
                <div class="card-header bg-success text-white">
                  <h5 class="m-1 fw-bold"><i class="fa-solid fa-credit-card me-3 fa-lg"></i>Payment Information</h5>
                </div>
                <div class="card-body">
                  <!-- Payment Breakdown -->
                  <div class="mb-3">
                    <div class="alert alert-success">
                      <h6 class="fw-bold mb-3 text-success">
                        <i class="fa-solid fa-file-invoice-dollar me-2"></i>Payment Breakdown
                      </h6>
                      <div class="d-flex justify-content-between mb-2">
                        <span class="text-muted">Registration Fee:</span>
                        <strong>{{ formatUSD(registrationFee) }}</strong>
                      </div>
                      <div class="d-flex justify-content-between mb-2">
                        <span class="text-muted">Participation Deposit:</span>
                        <strong>{{ formatUSD(auctionRoom.depositAmount) }}</strong>
                      </div>
                      <hr class="my-2 text-">
                      <div class="d-flex justify-content-between mb-1">
                        <span class="fw-bold text-dark">Total Registration:</span>
                        <h6 class="mb-0 text-success fw-bold">{{ formatUSD(totalRegistration) }}</h6>
                      </div>

                    </div>
                  </div>


                  <div class="form-check">
                    <input v-model="formData.agreedToTerms" class="form-check-input" type="checkbox" id="termsCheck"
                      @change="onOuterTermsChange" required>
                    <label class="form-check-label" for="termsCheck">
                      I have read and agree to the
                      <a href="#" class="text-success fw-semibold" @click.prevent="openTermsModal">
                        Terms &amp; Conditions
                      </a>
                    </label>
                  </div>

                  <!-- Action Buttons -->
                  <div class="d-grid gap-2 d-md-flex justify-content-center mt-4">
                    <button type="button" class="btn btn-outline-secondary btn-lg flex-md-fill" @click="currentStep = 1"
                      :disabled="isSubmitting">
                      <i class="fa-solid fa-arrow-left me-2"></i>Back
                    </button>
                    <button type="button" class="btn btn-success btn-lg flex-md-fill" @click="fetchPaymentInfo"
                      data-bs-toggle="modal" data-bs-target="#exampleModal"
                      :disabled="isSubmitting || !formData.agreedToTerms">
                      <span v-if="isSubmitting">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Processing...
                      </span>
                      <span v-else>
                        <i class="fa-solid fa-check-circle me-2"></i>
                        mở qr
                      </span>
                    </button>
                  </div>
                </div>
              </div>


            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms & Conditions Modal -->
    <div v-if="showTermsModal">
      <div class="modal-backdrop fade show"></div>
      <div class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true" @click.self="closeTermsModal">
        <div class="modal-dialog modal-lg modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Terms &amp; Conditions</h5>
              <button type="button" class="btn-close" @click="closeTermsModal"></button>
            </div>
            <div class="modal-body p-0">
              <div class="px-3 py-3" style="height: 70vh; overflow-y: auto;" @scroll="handleTermsScroll"
                ref="termsScroll">
                <div v-if="termsHtml" v-html="termsHtml"></div>
                <p v-else class="text-center text-muted my-4">
                  Loading terms &amp; conditions...
                </p>
              </div>
            </div>
            <div class="modal-footer flex-column align-items-start align-items-md-center">
              <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="modalAgreeCheck" v-model="modalAgree"
                  :disabled="!canAgreeInModal" @change="onModalAgreeChange">
                <label class="form-check-label" for="modalAgreeCheck">
                  I have read and agree to the Terms &amp; Conditions
                  <span v-if="!canAgreeInModal" class="text-muted small ms-1">
                    (Scroll to the bottom to enable)
                  </span>
                </label>
              </div>
              <button type="button" class="btn btn-secondary ms-md-auto" @click="closeTermsModal">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment QR Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h1 class="modal-title fs-6" id="exampleModalLabel">
              <i class="fa-solid fa-qrcode me-2"></i>Scan the QR code to pay the registration fee &amp; deposit.
            </h1>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <template v-if="paymentInfo.qrUrl">
              <img :src="paymentInfo.qrUrl" alt="Payment QR" class="img-fluid rounded mb-3" style="max-width:320px;" />
              <div class="small text-muted mb-1">
                Nội dung chuyển khoản:
                <strong>{{ paymentInfo.note || '—' }}</strong>
              </div>
              <div class="small text-muted mb-2">
                {{ paymentInfo.message }}
              </div>
              <span class="badge" :class="paymentInfo.paid ? 'bg-success' : 'bg-warning text-dark'">
                {{ paymentInfo.paid ? 'Đã thanh toán' : 'Chưa thanh toán' }}
              </span>
            </template>
            <template v-else>
              <div class="d-flex justify-content-center py-5">
                <div class="spinner-border text-success" role="status"></div>
              </div>
              <div class="small text-muted">Generating payment QR…</div>
            </template>
          </div>
          <div class="modal-footer">
            <!-- <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Đóng</button> -->
            <button type="button" class="btn btn-success w-100 btn-lg fw-bold" @click="checkPaymentStatus" :disabled="isCheckingPayment">
              <i v-if="isCheckingPayment" class="fas fa-spinner fa-spin me-2"></i>
              <i v-else class="fas fa-check-circle me-2"></i>
              {{ isCheckingPayment ? 'Checking...' : 'Check Payment' }}
            </button>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      loading: true,
      isSubmitting: false,
      isCheckingPayment: false,
      currentStep: 1,
      auctionRoomId: null,
      userId: null,
      selectedSession: null,
      auctionRoom: {
        id: '',
        roomName: '',
        description: '',
        type: '',
        imageAuctionRoom: '',
        depositAmount: 0,
        startedAt: null,
        stoppedAt: null,
        viewCount: 0,
        status: 0,
        paymentDeadlineDays: 7
      },
      sessions: [],
      formData: {
        paymentMethod: '',
        notes: '',
        agreedToTerms: false
      },
      showTermsModal: false,
      termsHtml: '',
      canAgreeInModal: false,
      modalAgree: false,
      // Payment
      showPaymentModal: false,
      paymentInfo: {
        qrUrl: '',
        transactionId: '',
        note: '',
        paid: false,
        message: ''
      },
      showZoomImage: false
    };
  },

  computed: {
    registrationFee() {
      // Phí hồ sơ đăng ký cố định (VNĐ)
      return 100000;
    },
    totalRegistration() {
      return (this.registrationFee || 0) + (this.auctionRoom.depositAmount || 0);
    }
  },

  mounted() {
    this.auctionRoomId = this.$route.params.id;
    this.getUserId();
    this.loadAuctionRoomDetails();
  },

  methods: {
    openTermsModal() {
      this.showTermsModal = true;
      this.canAgreeInModal = false;
      this.modalAgree = false;

      if (!this.termsHtml) {
        // Load terms content once from public HTML
        fetch('/QuyChe_ArtAuction.html')
          .then((res) => res.text())
          .then((html) => {
            this.termsHtml = html;
          })
          .catch((err) => {
            console.error('Failed to load terms:', err);
          });
      }
    },
    closeTermsModal() {
      this.showTermsModal = false;
    },
    handleTermsScroll(event) {
      const el = event.target;
      if (!el) return;
      const bottomReached = el.scrollTop + el.clientHeight >= el.scrollHeight - 10;
      if (bottomReached) {
        this.canAgreeInModal = true;
      }
    },
    onModalAgreeChange() {
      // Khi tick trong modal -> tự tick checkbox bên ngoài
      this.formData.agreedToTerms = !!this.modalAgree;
      // Không tự đóng modal, để người dùng tự quyết định
    },
    onOuterTermsChange() {
      // Nếu user cố tick khi chưa scroll hết trong modal thì không cho
      if (this.formData.agreedToTerms && !this.canAgreeInModal) {
        this.formData.agreedToTerms = false;
        this.openTermsModal();
      }
    },
    getUserId() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          this.userId = payload.userId || payload.sub || 'Unknown';
        } catch (err) {
          console.error('Error parsing token:', err);
          this.userId = 'Unknown';
        }
      }
    },

    loadAuctionRoomDetails() {
      this.loading = true;
      const token = localStorage.getItem('token');

      axios
        .get(`http://localhost:8081/api/auctionroom/complete/${this.auctionRoomId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        .then((res) => {
          console.log('API Response:', res.data);
          if (res.data) {
            if (res.data.room) {
              this.auctionRoom = res.data.room;
            }
            if (res.data.sessions) {
              // Transform nested structure to flat structure for template compatibility
              this.sessions = res.data.sessions.map(item => ({
                ...item.session,
                artwork: item.artwork,
                // Use artwork's image if session imageUrl is null
                imageUrl: item.session.imageUrl || item.artwork?.avtArtwork,
                // Add artwork title for display
                artworkTitle: item.artwork?.title,
                // Owner display name
                ownerName: item.ownerName
              }));
            }
          }
        })
        .catch((err) => {
          console.error('Error loading auction room:', err);
          this.$toast.error('Unable to load auction room information!');
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // handleRegister() {
    //   if (!this.formData.agreedToTerms) {
    //     this.$toast.warning('Please agree to the terms!');
    //     return;
    //   }

    //   this.isSubmitting = true;
    //   const token = localStorage.getItem('token');

    //   const requestData = {
    //     auctionRoomId: this.auctionRoomId,
    //     userId: this.userId,
    //     paymentMethod: this.formData.paymentMethod,
    //     notes: this.formData.notes,
    //     depositAmount: this.auctionRoom.depositAmount
    //   };

    //   console.log('Registering with data:', requestData);

    //   axios
    //     .post('http://localhost:8081/api/auctionroom/register', requestData, {
    //       headers: {
    //         'Authorization': `Bearer ${token}`,
    //         'Content-Type': 'application/json'
    //       }
    //     })
    //     .then((res) => {
    //       console.log('Registration success:', res.data);
    //       this.$toast.success('Successfully registered for auction!');
    //       // After register, fetch payment QR
    //       this.fetchPaymentInfo();
    //     })
    //     .catch((err) => {
    //       console.error('Registration error:', err);
    //       const errorMsg = err.response?.data?.message || 'Registration failed!';
    //       this.$toast.error(errorMsg);
    //     })
    //     .finally(() => {
    //       this.isSubmitting = false;
    //     });
    // },

    fetchPaymentInfo() {
      const token = localStorage.getItem('token');
      if (!this.auctionRoomId) {
        this.$toast.error('Missing auction room ID');
        return;
      }

      this.isSubmitting = true;

      // Mở modal ngay, hiển thị trạng thái loading QR
      this.showPaymentModal = true;
      this.paymentInfo = {
        qrUrl: '',
        transactionId: '',
        note: '',
        paid: false,
        message: 'Generating payment QR…'
      };

      console.log('🔄 Fetching payment QR for room:', this.auctionRoomId);

      axios
        .post(
          `http://localhost:8081/api/payment/${this.auctionRoomId}/registration/payment`,
          {},
          {
            headers: {
              Authorization: token ? `Bearer ${token}` : ''
            }
          }
        )
        .then((res) => {
          console.log('✅ Payment QR generated:', res.data);
          this.paymentInfo = {
            qrUrl: res.data.qrUrl,
            transactionId: res.data.transactionId || '',
            note: res.data.note,
            paid: res.data.paid,
            message: res.data.message
          };
        })
        .catch((err) => {
          console.error('❌ Payment info error:', err);
          const errorMsg = err.response?.data?.message || 'Không thể tải QR thanh toán';
          this.$toast.error(errorMsg);
          // Nếu lỗi, đóng modal lại
          this.showPaymentModal = false;
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },

    closePaymentModal() {
      this.showPaymentModal = false;
    },

    cleanupModalBackdrop() {
      // Remove all backdrops
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());

      // Reset body
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    },

    checkPaymentStatus() {
      const token = localStorage.getItem('token');
      if (!this.auctionRoomId) {
        this.$toast.error('Missing auction room ID');
        return;
      }

      if (!this.paymentInfo.note) {
        this.$toast.error('Payment note is missing');
        return;
      }

      this.isCheckingPayment = true;
      console.log('🔍 Checking payment status for room:', this.auctionRoomId);
      console.log('📝 Payment note:', this.paymentInfo.note);

      axios
        .post(
          `http://localhost:8081/api/payment/${this.auctionRoomId}/registration/verify`,
          {
            note: this.paymentInfo.note // ✅ Gửi nội dung chuyển khoản lên BE
          },
          {
            headers: {
              Authorization: token ? `Bearer ${token}` : ''
            }
          }
        )
        .then((res) => {
          console.log('✅ Payment verification response:', res.data);

          const data = res.data;

          // Update payment info from response
          if (data.qrUrl) {
            this.paymentInfo.qrUrl = data.qrUrl;
          }
          if (data.note) {
            this.paymentInfo.note = data.note;
          }

          // Update payment status
          if (data.paid === true) {
            this.$toast.success(data.message || 'Payment confirmed! Your registration is complete.');
            this.paymentInfo.paid = true;
            this.paymentInfo.message = data.message || 'Payment successful';

            // Close modal and redirect after 2 seconds
            setTimeout(() => {
              const modalElement = document.getElementById('exampleModal');
              if (modalElement) {
                const modal = bootstrap.Modal.getInstance(modalElement);
                if (modal) {
                  modal.hide();
                }
              }

              // Cleanup backdrop before redirect
              setTimeout(() => {
                this.cleanupModalBackdrop();
                // Redirect after cleanup
                this.$router.push('/client/auction');
              }, 200);
            }, 2000);
          } else {
            this.$toast.warning(data.message || 'Payment not found. Please complete the transfer.');
            this.paymentInfo.message = data.message;
          }
        })
        .catch((err) => {
          console.error('❌ Payment verification error:', err);
          const errorMsg = err.response?.data?.message || 'Unable to verify payment';
          this.$toast.error(errorMsg);
        })
        .finally(() => {
          this.isCheckingPayment = false;
        });
    },

    openArtworkZoom() {
      this.showZoomImage = true;
    },

    closeArtworkZoom() {
      this.showZoomImage = false;
    },

    goBack() {
      this.$router.go(-1);
    },

    getStatusText(status) {
      const statusMap = {
        0: 'Not Started',
        1: 'In Progress',
        2: 'Coming Soon'
      };
      return statusMap[status] || 'Unknown';
    },

    getSessionStatusText(status) {
      const statusMap = {
        0: 'Not Started',
        1: 'In Auction',
        2: 'Ended'
      };
      return statusMap[status] || 'Unknown';
    },

    getSessionStatusClass(status) {
      const classMap = {
        0: 'bg-secondary',
        1: 'bg-success',
        2: 'bg-danger'
      };
      return classMap[status] || 'bg-secondary';
    },

    formatUSD(amount) {
      // Giữ lại để tránh lỗi nếu còn chỗ cũ dùng, nhưng chuyển sang định dạng VNĐ
      return this.formatVND(amount);
    },

    formatVND(amount) {
      if (!amount && amount !== 0) return '0 ₫';
      return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount);
    },

    formatTime(dateString) {
      if (!dateString) return 'Not specified';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  }
};
</script>

<style scoped>
/* Minimal custom styles - mostly using Bootstrap */
.hover-shadow {
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.hover-shadow:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-5px);
}
</style>
