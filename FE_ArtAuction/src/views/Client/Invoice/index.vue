<template>
  <div class="container mt-3">
    <div class="row mb-4">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">
            <div class="checkout-steps mb-4">
              <div class="step completed">
                <div class="circle">1</div>
                <div class="label me-5 pe-5">Review</div>
                <div class="connector right"></div>
              </div>
              <div class="step current">
                <div class="connector left"></div>
                <div class="circle">2</div>
                <div class="label">Payment</div>
                <div class="connector right"></div>
              </div>
              <div class="step upcoming after-current">
                <div class="connector left"></div>
                <div class="circle">3</div>
                <div class="label">Shipping</div>
                <div class="connector right"></div>
              </div>
              <div class="step upcoming">
                <div class="connector left"></div>
                <div class="circle">4</div>
                <div class="label ms-4 ps-4">Complete</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-7 col-md-6 col-sm-12">
        <div class="row">
          <div class="col-12 mb-4">
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <div class="col-12">
                    <p class="fs-5 fw-bold text-success text-center">Personal Information</p>
                  </div>
                  <div class="col-lg-12 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Receiver</label>
                    <input type="text" class="form-control">
                  </div>
                  <!-- <div class="col-lg-6 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Last Name</label>
                    <input type="text" class="form-control">
                  </div> -->
                  <div class="col-lg-12 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Email Address</label>
                    <input type="text" class="form-control">
                  </div>
                  <!-- quốc gia -->
                  <div class="col-lg-4 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Country</label>
                    <!-- <input type="text" class="form-control"> -->
                    <input type="text" class="form-control" value="Việt Nam" readonly>
                  </div>
                  <!-- tỉnh/thành phố -->
                  <div class="col-lg-4 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Province/City</label>
                    <!-- <input type="text" class="form-control"> -->
                    <select class="form-select" v-model="form.cityCode">
                      <option value="" disabled>Select City</option>
                      <option v-for="p in provinces" :key="p.code" :value="p.code">
                        {{ p.name }}
                      </option>
                    </select>
                  </div>
                  <!-- phường/xã -->
                  <div class="col-lg-4 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Ward/Commune</label>
                    <!-- <input type="text" class="form-control"> -->
                    <select class="form-select" v-model="form.wardCode" :disabled="wards.length === 0">
                      <option value="" disabled>Select Ward</option>
                      <option v-for="w in wards" :key="w.code" :value="w.code">
                        {{ w.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-lg-12 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Street Address</label>
                    <input type="text" class="form-control">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <div class="col-12">
                    <p class="fs-5 fw-bold text-success text-center">Payment Information</p>
                  </div>
                  <div class="col-12">
                    <img src="https://qrcode-gen.com/images/qrcode-default.png" class="img-fluid" alt="">
                  </div>
                  <!-- <div class="col-lg-12 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Card Number</label>
                    <input type="text" class="form-control">
                  </div>
                  <div class="col-lg-6 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Expiry Date</label>
                    <input type="text" class="form-control">
                  </div>
                  <div class="col-lg-6 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">CVV</label>
                    <input type="text" class="form-control">
                  </div>
                  <div class="col-lg-12 col-md-12 col-sm-12 mb-3">
                    <label for="" class="mb-1">Cardholder Name</label>
                    <input type="text" class="form-control">
                  </div> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-5 col-md-6 col-sm-12">
        <div class="row">
          <!-- >Order Summary -->
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <div class="col-12">
                    <p class="fs-5 fw-bold text-success text-center">Order Summary</p>
                  </div>
                  <!-- contenr Order -->
                  <div class="col-lg-12">
                    <div class="row">
                      <div class="col-lg-6">
                        <img src="https://i.pinimg.com/1200x/1b/08/af/1b08af4eab12bd921dc3541ccf6a10b1.jpg" alt="..."
                          class="img-thumbnail w-100 h-100">
                      </div>
                      <div class="col-lg-6 d-flex flex-column gap-2 ps-lg-0">
                        <p class="fw-bold fs-6 text-success m-0">Sunset Over the Valley</p>
                        <p class=" m-0">by Maria Rodriguez</p>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Type</p>
                          <p class=" m-0">Oil on Canvas</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">size</p>
                          <p class=" m-0">24 x 36</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Auction</p>
                          <p class=" m-0">#A-2024-0123</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Winning Bid</p>
                          <p class=" m-0">$8,500.00</p>
                        </div>
                      </div>
                    </div>
                    <hr class="border-2 border-success">
                    <div class="row">
                      <div class="col-lg-12 d-flex flex-column gap-2">
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Artwork Price</p>
                          <p class=" m-0">$8,500.00</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Buyer's Premium (15%) </p>
                          <p class=" m-0">$1,275.00</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Insurance</p>
                          <p class=" m-0">$125.00</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Shipping & Handling</p>
                          <p class=" m-0">$75.00</p>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <p class=" m-0">Sales Tax (8.5%)</p>
                          <p class=" m-0">$680.00</p>
                        </div>
                      </div>
                    </div>
                    <hr class="border-2 border-success">
                    <div class="row">
                      <div class="col-lg-12 d-flex flex-column gap-2">
                        <div class="d-flex justify-content-between align-items-center">
                          <p class="text-success fw-bold m-0">Total Amount</p>
                          <p class="text-success fw-bold m-0">$10,655.00</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- chọn bank - radio -->
                  <div class="col-12 my-3">
                    <div class="card border border-2 border-success">
                      <div class="card-body d-flex flex-column gap-3">
                        <p class="m-0 fw-bold text-success">Payment Method</p>
                        <div class="form-check d-flex align-items-center gap-3">
                          <input class="form-check-input text-success" type="radio" name="exampleRadios" id="radio1"
                            value="option1" checked>
                          <div class="d-flex align-items-center gap-2">
                            <img src="../../../assets/img/MBBank_logo.png" class="img-bank" alt="">
                            <label class="form-check-label" for="radio1"> MB Bank </label>

                          </div>
                        </div>
                        <!-- <div class="form-check d-flex align-items-center gap-3">
                          <input class="form-check-input text-success" type="radio" name="exampleRadios" id="radio2"
                            value="option2">
                          <div class=" d-flex align-items-center gap-2">
                            <img src="../../../assets/img/PayPal_logo.png" class="img-bank" alt="">
                            <label class="form-check-label " for="radio2">Paypal </label>
                          </div>
                        </div> -->
                      </div>
                    </div>

                  </div>
                  <!-- btn thanh toán -->
                  <div class="col-12 my-3">
                    <button class="btn btn-lg fw-bold fs-6 btn-success w-100">Confirm & Pay</button>
                  </div>
                  <!-- card đảm bảo -->
                  <div class="col-12 mt-4">
                    <div class="card border border-2 border-success">
                      <div class="card-body d-flex flex-column gap-3">
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-shield-halved fs-5 text-success"></i>
                          <p class="m-0">256-bit SSL Encryption</p>
                        </div>
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-lock fs-5 text-success"></i>
                          <p class="m-0">PCI DSS Compliant</p>
                        </div>
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-certificate fs-5 text-success"></i>
                          <p class="m-0">Certificate of Authenticity</p>
                        </div>
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-rotate-left fs-5 text-success"></i>
                          <p class="m-0">30-Day Return Policy</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Need Help -->
                  <div class="col-12 mt-4">
                    <div class="card border border-2 border-success">
                      <div class="card-body d-flex flex-column gap-3">
                        <div class="d-flex align-items-center gap-4 text-success ">
                          <i class="fa-solid fa-headset fs-5 text-success"></i>
                          <p class="m-0 fw-bold fs-5">Need Help?</p>
                        </div>
                        <p class="m-0">Our auction specialists are available to assist you.</p>
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-phone fs-5 text-success"></i>
                          <p class="m-0">+84 12 345 678</p>
                        </div>
                        <div class="d-flex align-items-center gap-4">
                          <i class="fa-solid fa-envelope fs-5 text-success"></i>
                          <p class="m-0">nckhc1se11@gmail.com</p>
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
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      baseV2: 'https://provinces.open-api.vn/api/v2',
      baseV1: 'https://provinces.open-api.vn/api/v1',
      provinces: [],
      wards: [],
      form: {
        cityCode: '',  // giữ dạng string
        wardCode: ''
      },
      loading: {
        provinces: false,
        wards: false
      },
      errMsg: ''
    }
  },

  watch: {
    'form.cityCode': {
      handler(newCode) {
        this.form.wardCode = '';
        this.wards = [];
        if (!newCode) return;
        this.loadWardsByProvince(newCode);
      }
    }
  },

  mounted() {
    this.loadProvinces();
  },
  methods: {
    loadProvinces() {
      this.loading.provinces = true;
      this.errMsg = '';

      // TRẢ VỀ promise để chain .finally CHỈ CHẠY SAU KHI Fallback (nếu có) xong
      return axios.get(`${this.baseV2}/`, { params: { depth: 1 } })
        .then(res => {
          const list = Array.isArray(res.data) ? res.data : (res.data.results || res.data);
          this.provinces = list.map(p => ({ code: String(p.code), name: p.name }));
        })
        .catch(eV2 => {
          // Return inner promise để .finally đợi
          return axios.get(`${this.baseV1}/`, { params: { depth: 1 } })
            .then(res => {
              const list = Array.isArray(res.data) ? res.data : (res.data.results || res.data);
              this.provinces = list.map(p => ({ code: String(p.code), name: p.name }));
            })
            .catch(eV1 => {
              this.errMsg = 'Không tải được danh sách tỉnh/thành.';
              console.error('Load provinces failed:', eV2?.message, eV1?.message);
              // đẩy lỗi ra ngoài nếu muốn bắt tiếp ở nơi khác
              throw eV1;
            });
        })
        .finally(() => {
          this.loading.provinces = false;
        });
    },

    loadWardsByProvince(provinceCode) {
      this.loading.wards = true;
      this.errMsg = '';

      return axios.get(`${this.baseV2}/p/${provinceCode}`, { params: { depth: 2 } })
        .then(res => {
          const pv2 = res.data;

          // Case v2 đã có wards trực tiếp (sau sáp nhập)
          if (pv2 && Array.isArray(pv2.wards)) {
            this.wards = pv2.wards.map(w => ({ code: String(w.code), name: w.name }));
            return;
          }

          // Case vẫn còn districts → flatten wards
          if (pv2 && Array.isArray(pv2.districts)) {
            const flat = [];
            pv2.districts.forEach(d => {
              if (Array.isArray(d.wards)) {
                d.wards.forEach(w => flat.push({ code: String(w.code), name: w.name }));
              }
            });
            if (flat.length) {
              this.wards = flat;
              return;
            }
          }

          // Không lấy được từ v2 → RETURN fallback v1 để .finally đợi
          return this.loadWardsByProvinceV1(provinceCode);
        })
        .catch(eV2 => {
          // RETURN fallback v1 để .finally đợi
          return this.loadWardsByProvinceV1(provinceCode)
            .catch(eV1 => {
              this.errMsg = 'Không tải được danh sách phường/xã.';
              console.error('Load wards failed:', eV2?.message, eV1?.message);
              throw eV1;
            });
        })
        .finally(() => {
          this.loading.wards = false;
        });
    },

    loadWardsByProvinceV1(provinceCode) {
      // HÀM NÀY PHẢI RETURN promise để nơi gọi có thể chain tiếp
      return axios.get(`${this.baseV1}/p/${provinceCode}`, { params: { depth: 2 } })
        .then(res => {
          const p = res.data;
          const flat = [];
          if (p && Array.isArray(p.districts)) {
            p.districts.forEach(d => {
              if (Array.isArray(d.wards)) {
                d.wards.forEach(w => flat.push({ code: String(w.code), name: w.name }));
              }
            });
          }
          this.wards = flat;
        });
    }
  },
}
</script>
<style></style>
