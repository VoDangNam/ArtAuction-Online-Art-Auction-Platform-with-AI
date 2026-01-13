<template>
  <div class="row">
    <h4 class="text-primary fw-bold">System Settings</h4>
    <p class="text-body-secondary">System Configuration Management and Customization</p>
    <div class="col-12 col-lg-3 mb-3 mb-lg-0">
      <SubMenuSettingAdmin />
    </div>
    <div class="col-12 col-lg-9">
      <RouterView />
    </div>
  </div>
</template>

<script>
import SubMenuSettingAdmin from "@/components/SubMenuSettingAdmin.vue";

export default {
  components: {
    SubMenuSettingAdmin,
  },
};
</script>

<style lang="scss" scoped></style>
