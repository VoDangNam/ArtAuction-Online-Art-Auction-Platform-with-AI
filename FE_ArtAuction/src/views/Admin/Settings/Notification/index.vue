<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title fw-bold">Notification settings</h5>
      <p>Manage notifications to users</p>
    </div>
    <div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex flex-column gap-1">
          <lable class="fw-bold">Bidding Notice</lable>
          <small>Send notifications when new bids are placed</small>
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
          <lable class="fw-bold">Auction start notice</lable>
          <small>Send auction information to users 1 day in advance</small>
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
          <lable class="fw-bold">Auction End Notice</lable>
          <small>Auction results announcement</small>
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
          <lable class="fw-bold">Payment reminder</lable>
          <small>Remind the winner to pay</small>
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
          <lable class="fw-bold">System announcement</lable>
          <small>Thông báo bảo trì, truy cập</small>
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
