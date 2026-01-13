<template>
  <div class="wrapper">
    <div class="header-wrapper">
      <MenuClient></MenuClient>
    </div>
    <div class="page-wrapper">
      <div class="page-content">
        <router-view></router-view>
      </div>
    </div>
    <BotClient></BotClient>
    <ScrollToTop></ScrollToTop>
  </div>
</template>
<script>
import BotClient from "../components/client/BotClient.vue";
import MenuClient from "../components/client/MenuClient.vue";
import ScrollToTop from "../../components/ScrollToTop.vue";

export default {
  name: "app",
  components: {
    MenuClient,
    BotClient,
    ScrollToTop
  }
}
</script>
<style>
@import "../../assets/css/bootstrap-override.css";
@import "../../assets/css/base.css";
@import "../../assets/css/pages.css";
@import "../../assets/css/bootstrap.min.css";


@import 'bootstrap/dist/css/bootstrap.min.css';
@import 'bootstrap';
/* @import '@fortawesome/fontawesome-free/css/all.min.css'; */
</style>
