<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">Email settings</h5>
      <p>Configure email server and email templates</p>
    </div>
    <div class="card-body">
      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">SMTP Host</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">SMTP Port</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">SMTP Username</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">SMTP Password</lable>
        <div class="input-group">
          <input
            type="password"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Email sent</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>
      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Sender's name</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
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
