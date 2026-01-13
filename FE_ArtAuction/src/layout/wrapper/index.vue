<template>
  <div class="wrapper admin-theme">
    <!-- Sidebar  -->
    <MenuAdmin></MenuAdmin>

    <!-- Page Content  -->

    <div id="content-page" class="content-page">
      <div class="container-fluid">
        <router-view></router-view>
      </div>
    </div>
    <BotAdmin></BotAdmin>
    <ScrollToTop></ScrollToTop>
  </div>
</template>
<script>
import BotAdmin from "../components/admin/BotAdmin.vue";
import MenuAdmin from "../components/admin/MenuAdmin.vue";
import ScrollToTop from "../../components/ScrollToTop.vue";

import $ from "jquery";
window.jQuery = window.$ = $;

import "../../assets/js/jquery.min.js";
import "../../assets/js/customizer.js";
import "../../assets/js/popper.min.js";
import "../../assets/js/bootstrap.min.js";
import "../../assets/js/custom.js";
import "../../assets/js/menu-demo.js";

export default {
  name: "default-layout",
  components: {
    MenuAdmin,
    BotAdmin,
    ScrollToTop,
  },
};
</script>
<style>
@import "../../assets/css/custom-purple-theme.css";

@import "../../assets/css/responsive.css";
@import "../../assets/css/remixicon.css";
@import "../../assets/css/style.css";
@import "../../assets/css/floatingbutton.css";
@import "../../assets/css/fixes.css";
@import "../../assets/css/style-admin.css";

/* @import "../../assets/css/bootstrap.min.css"; */
</style>
