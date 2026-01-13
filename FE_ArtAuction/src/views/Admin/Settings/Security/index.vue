<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">Security settings</h5>
      <p>Configure system security features</p>
    </div>
    <div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Two-factor authentication</lable>
          <small>2FA required</small>
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
          <lable class="fw-bold">Email authentication</lable>
          <small>Email verification required upon registration</small>
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
          <lable class="fw-bold">Gender verification</lable>
          <small>Required to participate in the auction</small>
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

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Session timeout (minutes)</lable>
        <div class="input-group">
          <input
            type="number"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Maximum number of logins</lable>
        <div class="input-group">
          <input
            type="number"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
        <small class="text-secondary">Lock account after number of failed login attempts</small>
      </div>

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
