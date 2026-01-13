<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">Payment settings</h5>
      <p>Configure system security features</p>
    </div>
    <div class="card-body">
      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Service fee (%)</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            placeholder="fee"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
        <small class="text-body-secondary">Service fee based on auction value</small>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Minimum deposit amount</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Bank transfer</lable>
          <small>Allow bank transfers</small>
        </div>
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            id="switchCheckChecked"
            checked
          />
        </div>
      </div>
      <hr class="mb-3" />

      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">E-wallet</lable>
          <small>Allow payment via e-wallet</small>
        </div>
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            id="switchCheckChecked"
            checked
          />
        </div>
      </div>
      <hr class="mb-3" />

      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Credit card</lable>
          <small>Allow card payments</small>
        </div>
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            id="switchCheckChecked"
            checked
          />
        </div>
      </div>
      <hr class="mb-3" />

      <div class="d-flex justify-content-end">
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PaymentSettings",
};
</script>

<style></style>
