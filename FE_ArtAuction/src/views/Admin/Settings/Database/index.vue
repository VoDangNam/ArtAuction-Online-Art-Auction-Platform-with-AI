<template>
  <!-- <div class="border border-3 border-primary rounded-3"> -->
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">Database settings</h5>
      <p>Database backup and optimization management</p>
    </div>
    <div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Automatic backup</lable>
          <small>Automatic database backup</small>
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
        <lable class="fw-bold">Backup time</lable>
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
        <lable class="fw-bold">Backup storage (days)</lable>
        <div class="input-group">
          <input
            type="number"
            class="form-control"
            aria-label="Username"
            aria-describedby="basic-addon1"
          />
        </div>
      </div>

      <div class="d-flex justify-content-center mb-3">
        <div class="backup d-flex align-items-center flex-column gap-2">
          <!-- sửa viền -->
          <button type="button" class="btn btn-outline-light border border-primary w-100 py-1">
            <i class="fa-solid fa-database me-2"></i>
            Backup now
          </button>
          <button type="button" class="btn btn-outline-light border border-primary w-100 py-1">
            Database optimization
          </button>
          <button
            type="button"
            class="btn btn-outline-light border border-primary w-100 py-1 text-danger"
          >
            Delete old data
          </button>
        </div>
      </div>

      <div class="d-flex justify-content-end">
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
  <!-- </div> -->
</template>

<script>
export default {
  name: "PaymentSettings",
};
</script>

<style></style>
