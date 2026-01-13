<template>
  <transition name="fade">
    <button
      v-show="isVisible"
      @click="scrollToTop"
      class="scroll-to-top-btn"
      title="Back to top"
      aria-label="Scroll to top">
      <i class="fa-solid fa-chevron-up"></i>
    </button>
  </transition>
</template>

<script>
export default {
  name: 'ScrollToTop',
  data() {
    return {
      isVisible: false,
      scrollThreshold: 300 // Hiện nút khi scroll xuống 300px
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    handleScroll() {
      // Hiện nút khi scroll xuống quá scrollThreshold
      this.isVisible = window.pageYOffset > this.scrollThreshold;
    },
    scrollToTop() {
      // Scroll smooth về đầu trang
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }
};
</script>

<style scoped>
.scroll-to-top-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 50px;
  height: 50px;
  background: #ffffff;
  color: #044a42;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 9999;
}

.scroll-to-top-btn:hover {
  background: #ffffff;
  color: #066b5e;
  border-color: #044a42;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(4, 74, 66, 0.2);
}

.scroll-to-top-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(4, 74, 66, 0.3);
}

.scroll-to-top-btn i {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-3px);
  }
}

/* Fade transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* Responsive */
@media (max-width: 768px) {
  .scroll-to-top-btn {
    width: 45px;
    height: 45px;
    bottom: 20px;
    right: 20px;
    font-size: 18px;
  }
}
</style>

