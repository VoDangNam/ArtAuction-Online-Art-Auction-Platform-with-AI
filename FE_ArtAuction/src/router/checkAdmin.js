import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "bottom-right" });

export default function (from, to, next) {
  axios
    .get("http://localhost:8081/api/admin/auth/me", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
    .then((res) => {
      if (res.data) {
        next();

        console.log("test check:", res.data);

        localStorage.setItem("name_admin", res.data.name);
        localStorage.setItem("email_admin", res.data.email);
        localStorage.setItem("check_admin", res.data.status);
        localStorage.setItem("avatar_admin", res.data.avatar);
      } else {
        next("/admin/login");
        toaster.error("You need to log in first!");
      }
    })
    .catch((error) => {
      console.error("Admin auth check failed:", error);
      localStorage.removeItem("token");
      localStorage.removeItem("name_admin");
      localStorage.removeItem("email_admin");
      localStorage.removeItem("check_admin");
      localStorage.removeItem("avatar_admin");
      next("/admin/login");
      toaster.error("You need to log in first!");
    });
}
