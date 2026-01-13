<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">General Settings</h5>
      <p>Configure basic system information</p>
    </div>
    <div class="card-body">
      <div class="d-flex flex-column gap-1">
        <lable class="fw-bold">Website name</lable>
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Website name"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1">
        <lable class="fw-bold">Describe</lable>
        <div class="input-group mb-3">
          <textarea class="form-control" aria-label="With textarea"></textarea>
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Contact Email</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            placeholder="Email"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex flex-column gap-1 mb-3">
        <lable class="fw-bold">Support phone number</lable>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            placeholder="Number phone"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Maintenance mode</lable>
          <small>Temporarily block website access</small>
        </div>
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" role="switch" id="switchCheckDefault" />
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
  name: "GeneralSettings",
};
</script>

<style></style>
