<template>
  <div class="wrapper ">
    <div class="page-wrapper">
      <div class="page-content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>
<script>
import "../../assets/js/jquery.min.js";
import "../../assets/js/customizer.js";
import "../../assets/js/popper.min.js";
import "../../assets/js/bootstrap.min.js";
import "../../assets/js/custom.js";
import "../../assets/js/menu-demo.js";

export default {
  name: "default-layout",
  components: {
    // MenuClient,
    // BotClient
  }
}

</script>
<style>
@import "../../assets/css/custom-purple-theme.css";
@import "../../assets/css/triangles.css";
@import "../../assets/css/responsive.css";
@import "../../assets/css/remixicon.css";
@import "../../assets/css/style.css";
@import "../../assets/css/floatingbutton.css";
@import "../../assets/css/fixes.css";
@import "../../assets/css/style-admin.css";

@import 'bootstrap/dist/css/bootstrap.min.css';
@import 'bootstrap';
</style>
