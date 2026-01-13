<template>
  <div class="container mb-5">
    <!-- Role 0: User bình thường (chỉ xem) -->
    <div v-if="userRole === '0'" class="row justify-content-center mt-3">
      <div class="col-lg-8 col-md-10">
        <div class="card border-0 shadow-lg" data-aos="zoom-in" data-aos-duration="800">
          <div class="card-body text-center py-5">
            <div class="mb-3">
              <i class="fas fa-eye text-success" style="font-size: 60px;"></i>
            </div>
            <h3 class="fw-bold text-success mb-3">Viewer Account</h3>
            <p class="text-muted fs-6 mb-4">
              You're currently a viewer. To register artwork for auction, you’ll need to upgrade your account.
            </p>
            <div class="alert alert-danger d-inline-block px-5 py-3 mb-4">
              <i class="fas fa-info-circle me-2"></i>
              <strong>Upgrade Required:</strong> Please update your profile to become a seller
            </div>
            <!-- <div class="mb-3">
              <p class="text-muted">
                <i class="fas fa-clock me-2"></i>
                Redirecting to profile page in <strong>5 seconds</strong>...
              </p>
            </div> -->
            <button class="btn btn-success btn-lg fs-6 px-5 mt-3" @click="$router.push('/client/edit-profile')">
              <i class="fas fa-arrow-right me-2"></i>
              Upgrade to Seller
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Role 1: Buyer (người mua) -->
    <div v-else-if="userRole === '1'" class="row mt-3">
      <div :class="showSellerRequestForm ? 'col-lg-8' : 'col-lg-8 col-md-10 mx-auto'"
        :data-aos="showSellerRequestForm ? 'fade-right' : 'fade-right'" data-aos-duration="800"
        :key="'buyer-card-' + showSellerRequestForm" style="transition: all 0.5s ease;">
        <div class="card border-0 shadow-lg">
          <div class="card-body text-center py-5">
            <div class="mb-3">
              <i class="fas fa-shopping-cart text-info" style="font-size: 60px;"></i>
            </div>
            <h3 class="fw-bold text-dark mb-3">You're Currently a Buyer</h3>
            <p class="text-muted fs-6 mb-4">
              To register and sell artwork, you need to upgrade your account to become a seller.
            </p>
            <div class="alert alert-info d-inline-block px-5 py-3 mb-4">
              <i class="fas fa-info-circle me-2"></i>
              <strong>Upgrade Required:</strong> Submit a request to become a seller
            </div>
            <div class="mb-4">
              <div class="d-flex justify-content-center gap-3 align-items-center mb-3">
                <div class="text-center">
                  <i class="fas fa-shopping-cart text-info" style="font-size: 40px;"></i>
                  <p class="mb-0 mt-2 fw-bold">Buyer</p>
                  <small class="text-success">Current Role</small>
                </div>
                <div>
                  <i class="fas fa-arrow-right text-muted" style="font-size: 30px;"></i>
                </div>
                <div class="text-center">
                  <i class="fas fa-palette text-success" style="font-size: 40px;"></i>
                  <p class="mb-0 mt-2 fw-bold">Seller</p>
                  <small class="text-muted">Required Role</small>
                </div>
              </div>
            </div>
            <button class="btn btn-success btn-lg px-5" @click="toggleSellerRequestForm"
              :disabled="isSubmittingSellerRequest">
              <!-- <i class="fas fa-paper-plane me-2"></i> -->
              {{ showSellerRequestForm ? 'Cancel Request' : 'Request Seller Upgrade' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Form yêu cầu trở thành seller -->
      <div v-if="showSellerRequestForm" class="col-lg-4" data-aos="fade-left" data-aos-duration="800">
        <div class="card border-0 shadow-lg border-top border-4 border-success">
          <div class="card-body">
            <h5 class="fw-bold text-success mb-3">
              <i class="fas fa-store me-2"></i>Seller Request
            </h5>
            <p class="text-muted small mb-4">Please provide your verification image and description</p>

            <!-- Upload ảnh xác minh -->
            <div class="mb-4">
              <label class="form-label fw-bold">
                Verification Image <span class="text-danger">*</span>
              </label>
              <input type="file" class="form-control" accept="image/*" @change="handleSellerImageUpload"
                :disabled="isSubmittingSellerRequest" />
              <small class="text-muted">Upload ID card or business license</small>

              <!-- Preview ảnh -->
              <div v-if="sellerRequestForm.imagePreview" class="mt-3">
                <img :src="sellerRequestForm.imagePreview" class="img-thumbnail" style="max-height: 200px;"
                  alt="Preview">
                <button type="button" class="btn btn-sm btn-danger mt-2 w-100" @click="removeSellerImage"
                  :disabled="isSubmittingSellerRequest">
                  <i class="fas fa-times me-1"></i>Remove Image
                </button>
              </div>
            </div>

            <!-- Mô tả -->
            <div class="mb-4">
              <label class="form-label fw-bold">
                Description <span class="text-danger">*</span>
              </label>
              <textarea v-model="sellerRequestForm.description" class="form-control" rows="5"
                placeholder="Tell us why you want to become a seller..." :disabled="isSubmittingSellerRequest"
                maxlength="500"></textarea>
              <small class="text-muted">{{ sellerRequestForm.description.length }}/500 characters</small>
            </div>

            <!-- Nút submit -->
            <button class="btn btn-success w-100 fw-bold" @click="submitSellerRequest"
              :disabled="!canSubmitSellerRequest || isSubmittingSellerRequest">
              <span v-if="isSubmittingSellerRequest">
                <span class="spinner-border spinner-border-sm me-2"></span>Submitting...
              </span>
              <span v-else>
                <i class="fas fa-paper-plane me-2"></i>Submit Request
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Form đăng ký artwork - chỉ hiển thị khi role = 2 -->
    <div v-else-if="userRole === '2'">
      <!-- Success View -->
      <div v-if="showSuccessView" class="row justify-content-center mt-4">
        <div class="col-lg-8">
          <div class="card border-0 shadow-lg" data-aos="zoom-in" data-aos-duration="800">
            <div class="card-body text-center py-5">
              <!-- Success Icon -->
              <div class="mb-4">
                <div class="rounded-circle bg-success d-inline-flex align-items-center justify-content-center"
                     style="width: 70px; aspect-ratio: 1/1;">
                  <i class="fas fa-check text-white" style="font-size: 35px;"></i>
                </div>
              </div>

              <!-- Success Message -->
              <h3 class="fw-bold text-success mb-3">
                Artwork Registered Successfully!
              </h3>

              <p class="text-muted fs-6 mb-3">
                {{ successData?.message || 'Your artwork has been submitted and is awaiting approval.' }}
              </p>

              <!-- Artwork Info -->
              <div class="alert alert-light border d-inline-block px-5 mb-3">
                <p class="m-0">
                  <strong>Artwork Title:</strong> {{ successData?.artworkTitle }}
                </p>
                <p class="mb-0" v-if="successData?.artworkId">
                  <strong>Artwork ID:</strong> {{ successData?.artworkId }}
                </p>
              </div>

              <!-- Information -->
              <div class="alert alert-info d-inline-block px-5 py-3 mb-4">
                <i class="fas fa-info-circle me-2"></i>
                Your artwork will be reviewed by our team. You will be notified once it's approved.
              </div>

              <!-- Action Buttons -->
              <div class="d-flex justify-content-center gap-3 mt-2">
                <button class="btn btn-outline-success btn-lg px-5 w-100" @click="registerAnother">
                  <i class="fas fa-plus me-2"></i>
                  Register Another Artwork
                </button>
                <button class="btn btn-success btn-lg px-5 w-100" @click="goToHome">
                  <i class="fas fa-home me-2"></i>
                  Back to Home
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Check Upload (hiển thị nếu chưa check AI) -->
      <div v-if="!aiChecked && !showAIDetectionResult && !showSuccessView" class="row justify-content-center mt-4">
        <div class="col-lg-8">
          <div class="card border-0 p-0 shadow-lg" data-aos="zoom-in" data-aos-duration="800">
            <div class="card-body text-center py-5">
              <div class="mb-4">
                <i class="fas fa-robot text-success" style="font-size: 60px;"></i>
              </div>
              <h3 class="fw-bold text-success mb-3">AI Image Detection</h3>
              <p class="text-muted fs-6 mb-4">
                Please upload your artwork image to verify it's not AI-generated before registering.
              </p>

              <div class="alert alert-info d-inline-block px-5 py-3 mb-4">
                <i class="fas fa-info-circle me-2"></i>
                <strong>Required:</strong> Only human-created artworks are allowed
              </div>

              <!-- Upload area -->
              <div class="mb-4">
                <input type="file" ref="aiCheckFile" class="form-control mx-auto" style="max-width: 400px;"
                  accept="image/*" @change="handleAICheckUpload" :disabled="checkingAI" />
                <small class="text-muted d-block mt-2">Format: JPG, PNG, WEBP (Max 5MB)</small>
              </div>

              <!-- Preview -->
              <div v-if="aiCheckImagePreview" class="mb-4">
                <img :src="aiCheckImagePreview" class="img-thumbnail" style="max-height: 300px;" alt="Preview">
              </div>

              <!-- Button -->
              <button class="btn btn-success btn-lg px-5" @click="checkAIImage"
                :disabled="!aiCheckImageFile || checkingAI || classifyingArtwork">
                <span v-if="checkingAI">
                  <span class="spinner-border spinner-border-sm me-2"></span>Checking AI...
                </span>
                <span v-else-if="classifyingArtwork">
                  <span class="spinner-border spinner-border-sm me-2"></span>Classifying...
                </span>
                <span v-else>
                  <i class="fas fa-search me-2"></i>Check Image
                </span>
              </button>

              <!-- Loading message -->
              <div v-if="classifyingArtwork" class="mt-3">
                <div class="alert alert-info d-inline-block">
                  <i class="fas fa-spinner fa-spin me-2"></i>
                  Analyzing artwork style with AI...
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Detection Result (hiển thị nếu phát hiện AI) -->
      <div v-if="showAIDetectionResult" class="row justify-content-center mt-4">
        <div class="col-lg-10">
          <div class="card border-danger p-0 shadow-lg" data-aos="zoom-in" data-aos-duration="800">
            <div class="card-header bg-danger text-white">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  AI Image Detection
                </h5>
                <button type="button" class="btn-close btn-close-white" @click="closeAIDetectionResult"></button>
              </div>
            </div>
            <div class="card-body">
              <div class="text-center mb-3">
                <div class="alert alert-danger mb-3">
                  <i class="fas fa-robot fa-3x mb-3"></i>
                  <h5>{{ aiDetectionResult?.message || 'Image detected as AI' }}</h5>
                  <h4 class="mt-2 mb-0">
                    <span class="badge bg-danger fs-5">
                      AI: {{ formatProbability(aiDetectionResult?.aiProbability) }}%
                    </span>
                  </h4>
                </div>

                <div class="row text-center mb-3">
                  <div class="col-6">
                    <div class="card bg-light">
                      <div class="card-body py-3">
                        <h6 class="text-muted mb-1">AI Probability</h6>
                        <h3 class="text-danger mb-0">
                          {{ formatProbability(aiDetectionResult?.aiProbability) }}%
                        </h3>
                      </div>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="card bg-light">
                      <div class="card-body py-3">
                        <h6 class="text-muted mb-1">Human Probability</h6>
                        <h3 class="text-success mb-0">
                          {{ formatProbability(aiDetectionResult?.humanProbability) }}%
                        </h3>
                      </div>
                    </div>
                  </div>
                </div>

                <p class="text-muted mb-3">
                  Your image has a high probability of being AI-generated.
                  If you believe this is an error, please report it for our review.
                </p>

                <div class="d-flex justify-content-center gap-2">
                  <button type="button" class="btn btn-secondary" @click="closeAIDetectionResult">
                    <i class="fas fa-upload me-2"></i>Upload Different Image
                  </button>
                  <button type="button" class="btn btn-warning" @click="handleReportAI">
                    <i class="fas fa-flag me-2"></i>Report Error
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Form đăng ký (hiển thị sau khi check AI pass) -->
      <div v-if="aiChecked && !showAIDetectionResult && !showSuccessView">
        <div class="row">
          <div class="col-lg-12 d-flex justify-content-between align-items-center mt-4 mb-3">
            <div class="" data-aos="fade-right" data-aos-duration="800">
              <h3 class="fw-bold">
                <i class="fas fa-check-circle text-success me-2"></i>
                Register Artwork for Auction
              </h3>
              <p class="text-muted">
                Please fill in all information below to register your artwork for auction.
                All fields marked with <span class="text-danger">*</span> are required.
              </p>
            </div>
            <div class=" d-flex gap-3" data-aos="fade-left" data-aos-duration="800">
              <button type="button" class="btn btn-secondary" @click="resetForm" :disabled="isSubmitting">
                <i class="fas fa-redo me-2"></i>Reset
              </button>
              <button type="button" class="btn btn-success btn-lg px-5" :disabled="isSubmitting || !formData.agreedToTerms" @click="submitArtwork">
                <i v-if="isSubmitting" class="fas fa-spinner fa-spin me-2"></i>
                <i v-else class="fas fa-paper-plane me-2"></i>
                {{ isSubmitting ? 'Submitting...' : 'Register Artwork' }}
              </button>
            </div>
          </div>
        </div>
        <div class="row" data-aos="fade-up" data-aos-duration="800">
          <div class="col-lg-8 d-flex">
            <div class="card border-top border-4 border-success">
              <div class="card-body">
                <div class="row">
                  <!-- name artwork -->
                  <div class="col-lg-12 mb-4">
                    <label class="form-label fw-bold">
                      Artwork Title <span class="text-danger">*</span>
                    </label>
                    <input v-model="formData.title" type="text" class="form-control"
                      :class="{ 'is-invalid': errors.title }" placeholder="Enter artwork title" required />
                    <div v-if="errors.title" class="invalid-feedback">{{ errors.title }}</div>
                  </div>
                  <!-- Painting Genre -->
                  <div class="col-lg-6 d-flex flex-column gap-1 mb-4">
                    <div class="p-3 rounded" style="border: 2px dashed #044A424D;">
                      <div class="form-label fw-bold mb-3 d-flex justify-content-between align-items-center">
                        <div class="">
                          <i class="fas fa-palette me-2"></i>Genre <span class="text-danger">*</span>
                        </div>
                        <span v-if="classificationResult" class="badge bg-success ms-2">
                          <i class="fas fa-magic"></i> AI Suggested
                        </span>
                      </div>

                      <input v-model="formData.paintingGenre" type="text" class="form-control"
                        placeholder="Select or type artwork genre..." :class="{ 'is-invalid': errors.paintingGenre }"
                        list="genreList" required />

                      <datalist id="genreList">
                        <!-- AI Suggestions nếu có -->
                        <option v-for="genre in suggestedGenres" :key="'ai-' + genre.label" :value="genre.label">
                        </option>

                        <!-- Default genres -->
                        <option value="Landscape"></option>
                        <option value="Portrait"></option>
                        <option value="Abstract"></option>
                        <option value="Still Life"></option>
                        <option value="Contemporary"></option>
                        <option value="Traditional"></option>
                        <option value="Modern"></option>
                        <option value="Impressionism"></option>
                        <option value="Romanticism"></option>
                        <option value="Realism"></option>
                        <option value="Symbolism"></option>
                        <option value="Expressionism"></option>
                        <option value="Abstract_Expressionism"></option>
                        <option value="Cubism"></option>
                        <option value="Surrealism"></option>
                        <option value="Pop_Art"></option>
                      </datalist>

                      <div v-if="errors.paintingGenre" class="invalid-feedback">{{ errors.paintingGenre }}</div>

                      <!-- Đề xuất thể loại từ AI -->
                      <div v-if="suggestedGenres.length > 0" class="mt-2">
                        <small class="text-muted d-block mb-2 mt-2">
                          Đề xuất thể loại:
                        </small>
                        <div class="d-flex flex-wrap gap-2">
                          <button v-for="genre in suggestedGenres.slice(0, 4)" :key="'btn-' + genre.label" type="button"
                            class="btn btn-sm w-100 d-flex justify-content-between align-items-center"
                            :class="formData.paintingGenre === genre.label ? 'btn-success' : 'btn-outline-success'"
                            @click="formData.paintingGenre = genre.label">
                            <span>{{ genre.label }}</span>
                            <span class="badge bg-white text-success">{{ genre.probability }}%</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="row d-flex align-content-between gap-2">
                      <!-- Material -->
                      <div class="col-lg-12 ">
                        <label class="form-label fw-bold">
                          Material <span class="text-danger">*</span>
                        </label>
                        <input v-model="formData.material"
                               type="text"
                               class="form-control"
                               :class="{ 'is-invalid': errors.material }"
                               placeholder="Select or type material..."
                               list="materialList"
                               required />

                        <datalist id="materialList">
                          <option value="Oil"></option>
                          <option value="Acrylic"></option>
                          <option value="Watercolor"></option>
                          <option value="Gouache"></option>
                          <option value="Tempera"></option>
                          <option value="Ink"></option>
                          <option value="Charcoal"></option>
                          <option value="Pencil"></option>
                          <option value="Pastel"></option>
                          <option value="Oil Pastel"></option>
                          <option value="Crayon"></option>
                          <option value="Mixed Media"></option>
                          <option value="Collage"></option>
                          <option value="Digital"></option>
                          <option value="Photography"></option>
                          <option value="Spray Paint"></option>
                          <option value="Canvas"></option>
                          <option value="Paper"></option>
                          <option value="Wood"></option>
                          <option value="Metal"></option>
                          <option value="Glass"></option>
                          <option value="Fabric"></option>
                        </datalist>

                        <div v-if="errors.material" class="invalid-feedback">{{ errors.material }}</div>
                        <small class="text-muted">
                          <i class="fas fa-info-circle me-1"></i>
                          Common materials available or enter custom
                        </small>
                      </div>

                      <!-- Size -->
                      <div class="col-lg-12 ">
                        <label class="form-label fw-bold">
                          Size <span class="text-danger">*</span>
                        </label>
                        <input v-model="formData.size"
                               type="text"
                               class="form-control"
                               :class="{ 'is-invalid': errors.size }"
                               placeholder="Select or type size..."
                               list="sizeList"
                               required />

                        <datalist id="sizeList">
                          <!-- Common canvas sizes -->
                          <option value="20x25cm"></option>
                          <option value="30x40cm"></option>
                          <option value="40x50cm"></option>
                          <option value="50x60cm"></option>
                          <option value="50x70cm"></option>
                          <option value="60x80cm"></option>
                          <option value="70x100cm"></option>
                          <option value="80x100cm"></option>
                          <option value="100x120cm"></option>
                          <option value="100x150cm"></option>
                          <!-- Common square sizes -->
                          <option value="20x20cm"></option>
                          <option value="30x30cm"></option>
                          <option value="40x40cm"></option>
                          <option value="50x50cm"></option>
                          <option value="60x60cm"></option>
                          <option value="80x80cm"></option>
                          <option value="100x100cm"></option>
                          <!-- 3D sizes -->
                          <option value="30x40x5cm"></option>
                          <option value="50x70x5cm"></option>
                          <option value="60x80x10cm"></option>
                        </datalist>

                        <div v-if="errors.size" class="invalid-feedback">{{ errors.size }}</div>
                        <small class="text-muted">
                          <i class="fas fa-info-circle me-1"></i>
                          Common sizes available or enter custom (e.g: 70x50cm or 100x80x5cm)
                        </small>
                      </div>

                      <!-- Year of Creation -->
                      <div class="col-lg-12 ">
                        <label class="form-label fw-bold">
                          Year of Creation <span class="text-danger">*</span>
                        </label>
                        <input v-model.number="formData.yearOfCreation" type="number" class="form-control"
                          :class="{ 'is-invalid': errors.yearOfCreation }" placeholder="Enter year of creation"
                          :min="1900" :max="currentYear" required />
                        <div v-if="errors.yearOfCreation" class="invalid-feedback">{{ errors.yearOfCreation }}</div>
                      </div>
                    </div>
                  </div>



                  <!-- Description -->
                  <div class="col-lg-12">
                    <label class="form-label fw-bold">
                      Description <span class="text-danger">*</span>
                    </label>
                    <textarea v-model="formData.description" class="form-control"
                      :class="{ 'is-invalid': errors.description }" rows="4"
                      placeholder="Detailed description of the artwork" required></textarea>
                    <div v-if="errors.description" class="invalid-feedback">{{ errors.description }}</div>
                  </div>
                </div>

              </div>



            </div>
          </div>
          <div class="col-lg-4 d-flex">
            <div class="card border-top border-4 border-success">
              <div class="card-body">
                <div class="row">
                  <!-- Starting Price -->
                  <div class="col-lg-12 mb-3">
                    <div class="d-flex justify-content-between align-items-center">
                      <label class="form-label fw-bold">
                        Starting Price (VND) <span class="text-danger">*</span>
                      </label>
                      <small class="text-muted">
                        Price: {{ formatCurrency(formData.startedPrice) }}
                      </small>
                    </div>

                    <input v-model.number="formData.startedPrice" type="number" class="form-control"
                      :class="{ 'is-invalid': errors.startedPrice }" placeholder="Enter starting price" min="1000"
                      step="1000" required />
                    <small v-if="!errors.startedPrice" class="form-text text-muted">
                      Minimum 1,000 VND
                    </small>
                    <div v-if="errors.startedPrice" class="invalid-feedback d-block">
                      {{ errors.startedPrice }}
                    </div>

                  </div>
                  <!-- Certificate File -->
                  <div class="mb-3">
                    <label class="form-label fw-bold">
                      Certificate File <span class="text-danger">*</span>
                    </label>
                    <input ref="certificateInput" type="file" class="form-control" @change="handleCertificateUpload"
                      accept=".pdf,.jpg,.jpeg,.png" required />
                    <small class="text-muted">Format: PDF, JPG, PNG (Max 5MB)</small>

                    <!-- Certificate file name display -->
                    <div v-if="certificateFile" class="mt-2">
                      <div class="alert alert-success py-2 mb-0 d-flex align-items-center justify-content-between">
                        <div>
                          <i class="fas fa-file-check me-2"></i>
                          <span>{{ certificateFile.name }}</span>
                        </div>
                        <button type="button" class="btn btn-sm btn-danger" @click="removeCertificate">
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </div>
                    <div v-if="errors.certificateId" class="invalid-feedback d-block">{{ errors.certificateId }}</div>
                  </div>

                  <!-- Image Upload (Required) -->
                  <div class="">
                    <div class="form-label fw-bold d-flex justify-content-between align-items-center mb-3">
                      Artwork Image
                      <span class="badge bg-success ms-2">
                        <i class="fas fa-check-circle me-1"></i>AI Verified
                      </span>
                    </div>

                    <!-- Verified Image Display -->
                    <div v-if="imagePreview" class="position-relative">
                      <div class="border rounded p-2 bg-light">
                        <img :src="imagePreview" class="img-fluid rounded"
                          style="max-height: 250px; width: 100%; object-fit: contain;" alt="Verified Artwork">
                      </div>
                      <div class="alert alert-success mt-2 py-2 mb-0 d-flex align-items-center">
                        <i class="fas fa-shield-alt me-2"></i>
                        <small>This image has been verified as human-created artwork</small>
                      </div>
                    </div>

                    <!-- Fallback nếu không có ảnh -->
                    <div v-else class="alert alert-warning">
                      <i class="fas fa-exclamation-triangle me-2"></i>
                      Please complete AI image verification first
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-lg-12">
            <div class="card border-top border-4 border-success">
              <div class="card-body">
                <div class="form-check">
                  <input v-model="formData.agreedToTerms" class="form-check-input" type="checkbox" id="termsCheck"
                    @change="onOuterTermsChange" required>
                  <label class="form-check-label" for="termsCheck">
                    I have read and agree to the
                    <a href="#" class="text-success fw-semibold" @click.prevent="openTermsModal">
                      Service Contract
                    </a>
                  </label>
                </div>
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
                  <h5 class="modal-title">Service Contract</h5>
                  <button type="button" class="btn-close" @click="closeTermsModal"></button>
                </div>
                <div class="modal-body p-0">
                  <div class="px-3 py-3" style="height: 70vh; overflow-y: auto;" @scroll="handleTermsScroll"
                    ref="termsScroll">
                    <div v-if="termsHtml" v-html="termsHtml"></div>
                    <p v-else class="text-center text-muted my-4">
                      Loading contract...
                    </p>
                  </div>
                </div>
                <div class="modal-footer flex-column align-items-start align-items-md-center">
                  <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" id="modalAgreeCheck" v-model="modalAgree"
                      :disabled="!canAgreeInModal" @change="onModalAgreeChange">
                    <label class="form-check-label" for="modalAgreeCheck">
                      I have read and agree to the Service Contract
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

        <!-- Report AI Modal -->
        <div v-if="showReportModal" class="modal-backdrop fade show"></div>
        <div v-if="showReportModal" class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true"
          @click.self="closeReportModal">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title text-danger fw-bold">Report AI Result</h5>
                <button type="button" class="btn-close" @click="closeReportModal" :disabled="reportSubmitting"></button>
              </div>
              <form @submit.prevent="submitReportAI">
                <div class="modal-body">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Report Type</label>
                    <select class="form-select" v-model="reportForm.reportType" :disabled="reportSubmitting" required>
                      <option value="Inaccurate AI Result">Inaccurate AI Result</option>
                      <option value="Wrong Classification">Wrong Classification</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Reason <span class="text-danger">*</span></label>
                    <textarea class="form-control" rows="4" v-model.trim="reportForm.reason"
                      :class="{ 'is-invalid': showReportErrors && !reportForm.reason.trim() }"
                      :disabled="reportSubmitting" placeholder="Describe the issue" required></textarea>
                    <div class="invalid-feedback">Please enter a detailed reason.</div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Attached Image</label>
                    <div class="alert alert-info py-2 mb-0" v-if="imageFile">
                      <i class="fas fa-image me-2"></i>{{ imageFile.name }}
                      <span class="badge bg-secondary ms-2">Using uploaded image</span>
                    </div>
                    <div class="alert alert-warning py-2 mb-0" v-else>
                      No image found. Please upload artwork image before reporting.
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="closeReportModal"
                    :disabled="reportSubmitting">Cancel</button>
                  <button type="submit" class="btn btn-danger" :disabled="reportSubmitting || !canSubmitReport">
                    <i v-if="reportSubmitting" class="fas fa-spinner fa-spin me-2"></i>
                    Submit Report
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        <!-- Loading Modal -->
        <div v-if="isSubmitting" class="modal-backdrop fade show"></div>
        <div v-if="isSubmitting" class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg">
              <div class="modal-body text-center py-5">
                <div class="mb-3">
                  <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <h5 class="fw-bold text-success mb-2">Registering Artwork</h5>
                <p class="text-muted mb-1">Please wait while we process your submission...</p>
                <small class="text-muted">Do not close this window.</small>
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

export default {
  data() {
    return {
      formData: {
        title: '',
        description: '',
        startedPrice: 0,
        yearOfCreation: new Date().getFullYear(),
        paintingGenre: '',
        material: '',
        size: '',
        certificateId: '',
        status: 0, // 0 = Pending approval
        agreedToTerms: false
      },
      errors: {},
      isSubmitting: false,
      imageFile: null,
      imagePreview: null,
      certificateFile: null,
      currentYear: new Date().getFullYear(),
      // AI Detection Result
      showAIDetectionResult: false,
      aiDetectionResult: null,

      // Success view
      showSuccessView: false,
      successData: null,

      // Report AI modal
      showReportModal: false,
      reportSubmitting: false,
      // Terms & Conditions modal
      showTermsModal: false,
      termsHtml: '',
      canAgreeInModal: false,
      modalAgree: false,
      reportForm: {
        reportType: 'Inaccurate AI Result',
        reason: ''
      },
      showReportErrors: false,

      // Role check
      userRole: null,

      // Seller request form (for role 0)
      showSellerRequestForm: false,
      isSubmittingSellerRequest: false,
      sellerRequestForm: {
        imageFile: null,
        imagePreview: null,
        description: ''
      },
      redirectTimeout: null,

      // AI Check states (for role 2)
      aiChecked: false,
      checkingAI: false,
      aiCheckImageFile: null,
      aiCheckImagePreview: null,

      // Classification states
      classifyingArtwork: false,
      classificationResult: null,
      suggestedGenres: []
    }
  },

  computed: {
    canSubmitSellerRequest() {
      return this.sellerRequestForm.imageFile !== null &&
        this.sellerRequestForm.description.trim().length >= 10;
    },

    canSubmitReport() {
      return this.reportForm.reason.trim().length >= 10 && this.imageFile !== null;
    }
  },

  mounted() {
    // Check role từ localStorage
    // Role 0: User bình thường (chỉ xem)
    // Role 1: Buyer (người mua)
    // Role 2: Seller (người bán/artist)
    this.userRole = localStorage.getItem("role_kh");

    // Role = 0: User bình thường (viewer) → Redirect sau 5 giây (nếu không mở form)
    if (this.userRole === "0") {
      this.redirectTimeout = setTimeout(() => {
        if (!this.showSellerRequestForm) {
       //   this.$router.push("/client/edit-profile");
        }
      }, 5000);
    }
    // Role = 1: Buyer → Hiển thị giao diện yêu cầu upgrade, KHÔNG redirect tự động
    else if (this.userRole === "1") {
      // Chỉ hiển thị giao diện, user tự quyết định khi nào upgrade
      console.log("User is a buyer, showing seller upgrade request page");
    }
    // Role khác (không phải 0, 1, 2) → Redirect với thông báo
    else if (this.userRole !== "2") {
      this.$toast.error("Invalid role. Please update your profile.");
      setTimeout(() => {
        this.$router.push("/client/edit-profile");
      }, 1500);
    }
    // Role = 2: Seller → Cho phép đăng ký artwork
  },

  beforeUnmount() {
    // Clear timeout khi component unmount
    if (this.redirectTimeout) {
      clearTimeout(this.redirectTimeout);
    }
  },

  methods: {
    // AI Check Methods (for role 2)
    handleAICheckUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
          this.$toast.error("Image size must be less than 5MB");
          event.target.value = '';
          return;
        }

        // Validate file type
        if (!file.type.startsWith('image/')) {
          this.$toast.error("Please upload an image file");
          event.target.value = '';
          return;
        }

        this.aiCheckImageFile = file;

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          this.aiCheckImagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    checkAIImage() {
      if (!this.aiCheckImageFile || this.checkingAI) return;

      this.checkingAI = true;

      const formData = new FormData();
      formData.append("image", this.aiCheckImageFile);

      axios.post("http://localhost:5000/predict", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then((res) => {
          const data = res.data;
          console.log("AI Check result:", data);

          // Nếu result = "Human" hoặc prediction = "Human"
          if (data.result === "Human" || data.prediction === "Human") {
            this.$toast.success("✓ Image verified as human-created artwork!");

            // Set ảnh đã check làm ảnh preview cho form
            this.imageFile = this.aiCheckImageFile;
            this.imagePreview = this.aiCheckImagePreview;

            // Tự động gọi API phân loại artwork
            this.classifyArtwork(this.aiCheckImageFile);
          }
          // Nếu là AI
          else {
            this.$toast.error("⚠ Image detected as AI-generated!");
            this.aiDetectionResult = {
              message: "Image detected as AI-generated",
              aiProbability: data.ai_probability || 0,
              humanProbability: data.human_probability || 0,
              prediction: data.prediction,
              confidence: data.confidence
            };
            this.showAIDetectionResult = true;
          }
        })
        .catch((err) => {
          console.error("AI Check error:", err);
          const errorMessage = err.response?.data?.message || "Failed to check image. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.checkingAI = false;
        });
    },

    classifyArtwork(imageFile) {
      if (!imageFile || this.classifyingArtwork) return;

      this.classifyingArtwork = true;
      this.$toast.info("🎨 Classifying artwork style...");

      const formData = new FormData();
      formData.append("file", imageFile);

      axios.post("http://localhost:5000/classify", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then((res) => {
          const data = res.data;
          console.log("Classification result:", data);

          this.classificationResult = data;

          // Set top1 (phân loại chính xác nhất) vào formData
          if (data.top1) {
            this.formData.paintingGenre = data.top1.label;
            this.$toast.success(`✓ Artwork classified as: ${data.top1.label}`);
          }

          // Lưu topk suggestions để hiển thị trong dropdown
          if (data.topk && Array.isArray(data.topk)) {
            this.suggestedGenres = data.topk.map(item => ({
              label: item.label,
              probability: (item.probability * 100).toFixed(2)
            }));
          }

          // Set aiChecked = true để hiển thị form
          this.aiChecked = true;
        })
        .catch((err) => {
          console.error("Classification error:", err);
          const errorMessage = err.response?.data?.message || "Failed to classify artwork. You can select genre manually.";
          this.$toast.warning(errorMessage);

          // Vẫn cho phép user tiếp tục ngay cả khi classify fail
          this.aiChecked = true;
        })
        .finally(() => {
          this.classifyingArtwork = false;
        });
    },

    // Seller Request Methods (for role 0 and 1)
    toggleSellerRequestForm() {
      this.showSellerRequestForm = !this.showSellerRequestForm;

      // Refresh AOS animation khi toggle
      this.$nextTick(() => {
        if (typeof AOS !== 'undefined') {
          AOS.refresh();
        }
      });

      // Nếu mở form, clear redirect timeout (chỉ cho role 0)
      if (this.showSellerRequestForm && this.redirectTimeout) {
        clearTimeout(this.redirectTimeout);
        this.redirectTimeout = null;
      } else if (!this.showSellerRequestForm && this.userRole === "0") {
        // Nếu đóng form, set lại timeout (chỉ cho role 0)
        this.redirectTimeout = setTimeout(() => {
          this.$router.push("/client/edit-profile");
        }, 5000);
      }
    },

    handleSellerImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
          this.$toast.error("Image size must be less than 5MB");
          event.target.value = '';
          return;
        }

        // Validate file type
        if (!file.type.startsWith('image/')) {
          this.$toast.error("Please upload an image file");
          event.target.value = '';
          return;
        }

        this.sellerRequestForm.imageFile = file;

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          this.sellerRequestForm.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    removeSellerImage() {
      this.sellerRequestForm.imageFile = null;
      this.sellerRequestForm.imagePreview = null;
    },

    submitSellerRequest() {
      if (!this.canSubmitSellerRequest || this.isSubmittingSellerRequest) return;

      this.isSubmittingSellerRequest = true;

      const formData = new FormData();
      formData.append("verificationImage", this.sellerRequestForm.imageFile);
      formData.append("description", this.sellerRequestForm.description);

      axios.post("http://localhost:8081/api/seller-request", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: "Bearer " + localStorage.getItem("token")
        }
      })
        .then((res) => {
          this.$toast.success(res.data?.message || "Seller request submitted successfully. Please wait for admin approval.");

          // Reset form
          this.sellerRequestForm = {
            imageFile: null,
            imagePreview: null,
            description: ''
          };
          this.showSellerRequestForm = false;

          // Có thể redirect hoặc reload
          // setTimeout(() => {
          //   this.$router.push('/client/home');
          // }, 2000);
        })
        .catch((err) => {
          console.error("Seller request error:", err);
          const errorMessage = err.response?.data?.message || "Failed to submit seller request. Please try again.";
          this.$toast.error(errorMessage);
        })
        .finally(() => {
          this.isSubmittingSellerRequest = false;
        });
    },

    // Validate form
    validateForm() {
      this.errors = {};
      let isValid = true;

      // Title
      if (!this.formData.title || this.formData.title.trim().length < 3) {
        this.errors.title = 'Artwork title must be at least 3 characters';
        isValid = false;
      }

      // Description
      if (!this.formData.description || this.formData.description.trim().length < 10) {
        this.errors.description = 'Description must be at least 10 characters';
        isValid = false;
      }

      // Starting Price
      if (!this.formData.startedPrice || this.formData.startedPrice < 1000) {
        this.errors.startedPrice = 'Starting price must be at least 1,000 VND';
        isValid = false;
      }

      // Year of Creation
      if (!this.formData.yearOfCreation ||
        this.formData.yearOfCreation < 1900 ||
        this.formData.yearOfCreation > this.currentYear) {
        this.errors.yearOfCreation = `Year of creation must be from 1900 to ${this.currentYear}`;
        isValid = false;
      }

      // Painting Genre
      if (!this.formData.paintingGenre) {
        this.errors.paintingGenre = 'Please select a genre';
        isValid = false;
      }

      // Material
      if (!this.formData.material) {
        this.errors.material = 'Please select a material';
        isValid = false;
      }

      // Size
      if (!this.formData.size || this.formData.size.trim().length < 3) {
        this.errors.size = 'Please enter the size';
        isValid = false;
      }

      // Certificate File
      if (!this.certificateFile) {
        this.errors.certificateId = 'Please select a certificate file';
        isValid = false;
      }

      return isValid;
    },

    // Handle file upload
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
          this.$toast?.error?.('File size must not exceed 5MB');
          event.target.value = '';
          return;
        }

        // Validate file type
        if (!file.type.startsWith('image/')) {
          this.$toast?.error?.('Please select an image file');
          event.target.value = '';
          return;
        }

        this.imageFile = file;

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    // Remove image
    removeImage() {
      this.imageFile = null;
      this.imagePreview = null;
    },

    // Handle certificate file upload
    handleCertificateUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
          this.$toast?.error?.('File size must not exceed 5MB');
          event.target.value = '';
          return;
        }

        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
          this.$toast?.error?.('Please select a PDF file or image (JPG, PNG)');
          event.target.value = '';
          return;
        }

        this.certificateFile = file;
      }
    },

    // Remove certificate
    removeCertificate() {
      this.certificateFile = null;
    },

    // Format currency
    formatCurrency(value) {
      if (!value) return '0 ₫';
      return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    },

    // Format probability percentage
    formatProbability(value) {
      if (value === null || value === undefined || isNaN(value)) return '0.00';
      return Number(value).toFixed(2);
    },

    // Terms & Conditions methods
    openTermsModal() {
      this.showTermsModal = true;
      this.canAgreeInModal = false;
      this.modalAgree = false;

      if (!this.termsHtml) {
        // Load contract content once from public HTML
        fetch('/HopDong_ArtAuction.html')
          .then((res) => res.text())
          .then((html) => {
            this.termsHtml = html;
          })
          .catch((err) => {
            console.error('Failed to load contract:', err);
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
    },
    onOuterTermsChange() {
      // Nếu user cố tick khi chưa scroll hết trong modal thì không cho
      if (this.formData.agreedToTerms && !this.canAgreeInModal) {
        this.formData.agreedToTerms = false;
        this.openTermsModal();
      }
    },

    // Submit form
    submitArtwork() {
      console.log('Register Artwork');
      // Validate
      if (!this.validateForm()) {
        this.$toast?.error?.('Please check the information you entered');
        return;
      }

      // Check if image is required
      if (!this.imageFile) {
        this.$toast?.error?.('Please select an artwork image');
        return;
      }

      // Check Terms & Conditions
      if (!this.formData.agreedToTerms) {
        this.$toast?.error?.('Please agree to the Service Contract');
        return;
      }

      this.isSubmitting = true;

      // Prepare form data for multipart/form-data
      const formData = new FormData();

      // Tạo metadata object theo yêu cầu của backend
      const metadata = {
        title: this.formData.title,
        description: this.formData.description,
        startedPrice: this.formData.startedPrice,
        yearOfCreation: this.formData.yearOfCreation,
        paintingGenre: this.formData.paintingGenre,
        material: this.formData.material,
        size: this.formData.size,
        certificateId: this.formData.certificateId,
        status: this.formData.status
      };

      // Append metadata as JSON string
      formData.append('metadata', JSON.stringify(metadata));

      // Append image if exists
      if (this.imageFile) {
        formData.append('image', this.imageFile);
      }

      // Append certificate file if exists
      if (this.certificateFile) {
        formData.append('certificate', this.certificateFile);
      }

      // Debug: log formData
      console.log('Sending metadata:', metadata);
      console.log('Sending image:', this.imageFile?.name);
      console.log('Sending certificate:', this.certificateFile?.name);

      // Send to API
      axios
        .post('http://localhost:8081/api/artworks/ingest', formData, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
            // Không set Content-Type, để browser tự động set boundary cho multipart/form-data
          }
        })
        .then((res) => {
          console.log('Artwork registered:', res.data);

          // Kiểm tra AI detection result
          const prediction = res.data.prediction;
          const aiProbability = parseFloat(res.data.aiProbability) || 0;
          const humanProbability = parseFloat(res.data.humanProbability) || 0;
          const status = res.data.status;

          console.log('AI Probability:', res.data.aiProbability);
          console.log('Human Probability:', res.data.humanProbability);

          // Nếu phát hiện là AI hoặc status = false
          if (prediction === 'AI' || status === false) {
            // Lưu thông tin AI detection
            this.aiDetectionResult = {
              prediction: prediction,
              aiProbability: aiProbability,
              humanProbability: humanProbability,
              message: res.data.message
            };

            console.log('Setting aiDetectionResult:', this.aiDetectionResult);

            // Hiển thị kết quả AI detection
            this.showAIDetectionResult = true;
            this.isSubmitting = false;

            // Scroll đến vị trí kết quả AI detection
            this.$nextTick(() => {
              const resultCard = document.querySelector('.border-danger');
              if (resultCard) {
                resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }
            });
          } else {
            // If Human - success
            this.successData = {
              message: res.data.message || 'Artwork registered successfully!',
              artworkTitle: this.formData.title,
              artworkId: res.data.artworkId || res.data.id
            };

            // Show success view
            this.showSuccessView = true;

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        })
        .catch((err) => {
          console.error('Error submitting artwork:', err);

          if (err.response?.data?.message) {
            this.$toast?.error?.('Error: ' + err.response.data.message);
          } else {
            this.$toast?.error?.('An error occurred while registering the artwork. Please try again.');
          }
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },

    // Reset form
    resetForm() {
      this.formData = {
        title: '',
        description: '',
        startedPrice: 0,
        yearOfCreation: new Date().getFullYear(),
        paintingGenre: '',
        material: '',
        size: '',
        certificateId: '',
        status: 0
      };
      this.errors = {};

      // ❌ KHÔNG reset ảnh artwork (đã qua AI check)
      // this.imageFile = null;
      // this.imagePreview = null;

      // ✅ Reset Certificate File
      this.certificateFile = null;
      // Reset input file element
      if (this.$refs.certificateInput) {
        this.$refs.certificateInput.value = '';
      }
    },

    // Navigate to home
    goToHome() {
      this.$router.push('/client/home');
    },

    // Register another artwork
    registerAnother() {
      this.showSuccessView = false;
      this.successData = null;
      this.aiChecked = false;
      this.aiCheckImageFile = null;
      this.aiCheckImagePreview = null;
      this.classificationResult = null;
      this.suggestedGenres = [];
      this.resetForm();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    // Close AI Detection Result
    closeAIDetectionResult() {
      this.showAIDetectionResult = false;
      this.aiDetectionResult = null;

      // Reset AI check để cho phép upload lại (cho role 2)
      if (this.userRole === "2") {
        this.aiChecked = false;
        this.aiCheckImageFile = null;
        this.aiCheckImagePreview = null;

        // Reset classification data
        this.classificationResult = null;
        this.suggestedGenres = [];
        this.formData.paintingGenre = '';

        // Reset file input
        if (this.$refs.aiCheckFile) {
          this.$refs.aiCheckFile.value = '';
        }
      }
    },

    // Handle Report AI Image
    handleReportAI() {
      this.showReportErrors = false;
      this.reportForm.reportType = 'Inaccurate AI Result';
      this.reportForm.reason = '';
      this.showReportModal = true;
    },

    closeReportModal() {
      if (this.reportSubmitting) return;
      this.showReportModal = false;
      this.reportForm.reason = '';
      this.showReportErrors = false;
    },

    async submitReportAI() {
      if (!this.imageFile) {
        this.$toast?.error?.('Không tìm thấy ảnh đã tải lên để gửi báo cáo.');
        return;
      }

      if (!this.reportForm.reason.trim()) {
        this.showReportErrors = true;
        return;
      }

      this.reportSubmitting = true;

      const formData = new FormData();
      formData.append('reportType', this.reportForm.reportType || 'Inaccurate AI Result');
      formData.append('reason', this.reportForm.reason.trim());
      formData.append('image', this.imageFile);

      try {
        console.log('AI report payload:', {
          reportType: this.reportForm.reportType,
          reason: this.reportForm.reason.trim(),
          image: this.imageFile?.name
        });

        const res = await axios.post('http://localhost:8081/api/reports/ai-artwork', formData, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });

        console.log('AI report response:', res.data);
        this.$toast?.success?.('Đã gửi báo cáo AI thành công.');
        this.closeReportModal();
        this.closeAIDetectionResult();
      } catch (error) {
        console.error('Error reporting AI artwork:', error);
        this.$toast?.error?.(error.response?.data?.message || 'Không thể gửi báo cáo AI.');
      } finally {
        this.reportSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 15px;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #044a42 0%, #066a5e 100%);
}

.form-label {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.form-control:focus,
.form-select:focus {
  border-color: #044a42;
  box-shadow: 0 0 0 0.2rem rgba(4, 74, 66, 0.25);
}

.btn-success {
  background: linear-gradient(135deg, #044a42 0%, #066a5e 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-success:hover {
  background: linear-gradient(135deg, #033831 0%, #055548 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(4, 74, 66, 0.3);
}

.btn-success:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.img-thumbnail {
  border: 2px solid #044a42;
  border-radius: 8px;
}

.invalid-feedback {
  display: block;
}

/* Responsive */
@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem !important;
  }

  .btn-lg {
    width: 100%;
    margin-top: 1rem;
  }

  .d-flex.justify-content-between {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-secondary {
    width: 100%;
  }

  /* AI Detection buttons on mobile */
  .card.border-danger .d-flex.gap-2 {
    flex-direction: column;
    width: 100%;
  }

  .card.border-danger .d-flex.gap-2 button {
    width: 100%;
  }
}

/* AI Detection Result Card */
.fa-robot {
  color: #dc3545;
  animation: pulse 2s infinite;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

.card.border-danger {
  border-width: 3px;
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header.bg-danger {
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(4, 74, 66, 0.95);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-out;
}

.loading-content {
  text-align: center;
  color: white;
}

.logo-spinner {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
  animation: float 3s ease-in-out infinite;
}

.logo-circle i {
  font-size: 2.5rem;
  color: #044a42;
  animation: rotate 5s linear infinite;
}

.ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  animation: ripple 2s ease-out infinite;
}

.delay-1 {
  animation-delay: 1s;
}

.loading-title {
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.loading-text {
  font-size: 1.1rem;
  opacity: 0.8;
  margin-bottom: 1.5rem;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.loading-dots span {
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes ripple {
  0% {
    width: 80px;
    height: 80px;
    opacity: 0.8;
  }

  100% {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
  }

  40% {
    transform: scale(1);
  }
}

/* Smooth transitions for card animation */
[data-aos] {
  transition-property: transform, opacity, margin, padding;
}

.row {
  transition: all 0.3s ease;
}

.col-lg-8,
.col-lg-4,
.col-md-10 {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
