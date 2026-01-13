import { createRouter, createWebHistory } from "vue-router"; // cài vue-router: npm install vue-router@next --save

import checkAdmin from "./checkAdmin";
import checkUser from "./checkUser";

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Khachhang/Login/index.vue"),
    meta: { layout: "blank" },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Khachhang/Register/index.vue"),
    meta: { layout: "blank" },
  },

  // trước login - ko cần checkUser
  {
    path: "/",
    component: () => import("../views/Khachhang/Home/index.vue"),
    meta: { layout: "client" },
  },
  {
    path: "/about-us",
    name: "about_us",
    component: () => import("../views/Khachhang/AboutUs/index.vue"),
    meta: { layout: "client" },
  },
  // {
  //   path: "/help",
  //   name: "help",
  //   component: () => import("../views/Khachhang/Help/index.vue"),
  //   meta: { layout: "client" },
  // },

  // sau login - phải checkUser
  {
    path: "/client/home",

    component: () => import("../views/Client/Home/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },
  {
    path: "/client/auction",
    name: "auction",
    component: () => import("../views/Client/Auction/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },
  {
    path: "/client/profile",
    // name: "profile",
    component: () => import("../views/Client/Profile/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
    children: [
      {
        path: "",
        redirect: "/client/profile/art-management",
      },
      {
        path: "art-management",
        name: "profile-art-management",
        component: () => import("../views/Client/Profile/Management/index.vue"),
      },
      {
        path: "history",
        name: "profile-history",
        component: () => import("../views/Client/Profile/History/index.vue"),
      },
      {
        path: "invoices",
        name: "profile-invoices",
        component: () => import("../views/Client/Profile/Invoices/index.vue"),
      },
      {
        path: "e-wallet",
        name: "profile-e-wallet",
        component: () => import("../views/Client/Profile/EWallet/index.vue"),
      },
    ],
  },
  {
    path: "/client/payment/:roomId/:invoiceId",
    name: "payment",
    component: () => import("../views/Client/Payment/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },
  {
    path: "/client/register-artwork",
    name: "invoice",
    component: () => import("../views/Client/RegisArtwork/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },
  {
    path: "/client/auction-room/:id",
    name: "auction-room",
    component: () => import("../views/Client/AuctionRoom/index.vue"),
    meta: { layout: "blank" },
    // meta: { layout: "client" },
    props: true,
    beforeEnter: checkUser,
  },
  {
    path: "/client/Regis-auct-room/:id",
    name: "Regis-auct-room",
    component: () => import("../views/Client/RegisAuction/index.vue"),
    meta: { layout: "client" },
    props: true,
    beforeEnter: checkUser,
  },

  //test
  {
    path: "/client/live-test",
    // name: 'auction-room',
    component: () => import("../views/Client/testLiveClient/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },

  {
    path: "/client/edit-profile",
    // name: 'auction-room',
    component: () => import("../views/Client/EditProfile/index.vue"),
    meta: { layout: "client" },
    beforeEnter: checkUser,
  },

  {
    path: "/client/forgot-password",
    // name: 'auction-room',
    component: () => import("../views/Client/ForgotPassword/index.vue"),
    meta: { layout: "blank" },
    // beforeEnter: checkUser,
  },




  // ADMIN
  {
    path: "/admin/dashboard",
    name: "ad-dashboard",
    component: () => import("../views/Admin/Dashboard/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-employees",
    // name: 'auction-room',
    component: () => import("../views/Admin/Employees/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,

  },
  {
    path: "/admin/management-users",
    // name: 'auction-room',
    component: () => import("../views/Admin/Users/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-schedule",
    // name: 'auction-room',
    component: () => import("../views/Admin/Schedules/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-invoice",
    // name: 'auction-room',
    component: () => import("../views/Admin/Invoices/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  // {
  //   path: '/admin/live',
  //   name: 'admin-live',
  //   component: () => import('../views/Admin/testLiveStream/index.vue'),
  //   meta: { layout: "default" },
  // },
  {
    path: "/admin/testlivestream/:id",
    name: "admin-test-livestream",
    component: () => import("../views/Admin/testLiveStream/index.vue"),
    meta: { layout: "blank" },
    beforeEnter: checkAdmin,

  },
  {
    path: "/admin/livestream",
    // name: 'admin-livestream',
    component: () => import("../views/Admin/LiveStream/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/chat/:id",
    name: "admin-chat",
    component: () => import("../views/Admin/Chat/index.vue"),
    meta: { layout: "default" },
    props: true,
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-artwork",
    // name: 'auction-room',
    component: () => import("../views/Admin/Artworks/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-auction",

    component: () => import("../views/Admin/AuctionRoom/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/login",
    // name: "login",
    component: () => import("../views/Admin/LoginAdmin/index.vue"),
    meta: { layout: "blank" },
  },
  {
    path: "/admin/management-report",
    // name: 'auction-room',
    component: () => import("../views/Admin/Reports/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-notification",
    // name: 'auction-room',
    component: () => import("../views/Admin/Notification/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/management-statistical",

    component: () => import("../views/Admin/Statistical/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  // {
  //   path: "/admin/management-admin",

  //   component: () => import("../views/Admin/Admin-Management/index.vue"),
  //   meta: { layout: "default" },
  // },
  {
    path: "/admin/management-setting",
    // name: "admin-settings",
    component: () => import("../views/Admin/Settings/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
    children: [
      {
        path: "",
        redirect: "general-setting",
      },
      {
        path: "general-setting",
        name: "admin-general-setting",
        component: () => import("../views/Admin/Settings/General/index.vue"),
      },
      {
        path: "payment-setting",
        name: "admin-payment",
        component: () => import("../views/Admin/Settings/Payment/index.vue"),
      },
      {
        path: "notification-setting",
        name: "admin-notifications",
        component: () => import("../views/Admin/Settings/Notification/index.vue"),
      },
      {
        path: "email-setting",
        name: "admin-email",
        component: () => import("../views/Admin/Settings/Email/index.vue"),
      },
      {
        path: "security-setting",
        name: "admin-security",
        component: () => import("../views/Admin/Settings/Security/index.vue"),
      },
      {
        path: "database-setting",
        name: "admin-database",
        component: () => import("../views/Admin/Settings/Database/index.vue"),
      },
    ],
  },
  {
    path: "/admin/management-statistical",
    // name: "admin-settings",
    component: () => import("../views/Admin/Statistical/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
    children: [
      {
        path: "",
        redirect: "revenues",
      },
      {
        path: "revenues",
        // name: "admin-general-setting",
        component: () => import("../views/Admin/Statistical/Revenue/index.vue"),
      },
      {
        path: "users",
        // name: "admin-payment",
        component: () => import("../views/Admin/Statistical/User/index.vue"),
      },
      {
        path: "auctions",
        // name: "admin-notifications",
        component: () => import("../views/Admin/Statistical/AUction/index.vue"),
      },
      {
        path: "bids",
        // name: "admin-email",
        component: () => import("../views/Admin/Statistical/Bid/index.vue"),
      },
      {
        path: "artworks",
        // name: "admin-security",
        component: () => import("../views/Admin/Statistical/Artwork/index.vue"),
      },
      {
        path: "reports",
        // name: "admin-database",
        component: () => import("../views/Admin/Statistical/Report/index.vue"),
      },
    ],
  },
  {
    path: "/admin/add-auction-room",
    name: "add-auction-room",
    component: () => import("../views/Admin/AddAuctionRoom/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/artwork-detail/:id",
    name: "artwork-detail",
    component: () => import("../views/Admin/ArtworkDetail/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/sent-notification",
    // name: "artwork-detail",
    component: () => import("../views/Admin/SentNotification/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/seller-requests",
    // name: "artwork-detail",
    component: () => import("../views/Admin/SellerRequest/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/auction-detail/:id",
    component: () => import("../views/Admin/AuctionDetail/index.vue"),
    meta: { layout: "default" },
    props: true,
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/edit-auction-room/:id",
    // name: "artwork-detail",
    component: () => import("../views/Admin/EditAuctionRoom/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/edit-artwork/:id",
    // name: "artwork-detail",
    component: () => import("../views/Admin/EditArtwork/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/add-admin",
    // name: "artwork-detail",
    component: () => import("../views/Admin/AddAdmin/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/add-user",
    // name: "artwork-detail",
    component: () => import("../views/Admin/AddUser/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin/profile",
    // name: "artwork-detail",
    component: () => import("../views/Admin/Profile/index.vue"),
    meta: { layout: "default" },
    beforeEnter: checkAdmin,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

// Chuyển hướng người dùng đã đăng nhập khỏi các trang dành cho khách
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isGuestPage = to.path === "/" || to.path === "/login" || to.path === "/register";

  if (token && isGuestPage) {
    return next("/client/home");
  }

  return next();
});
export default router;
