<template>
    <div class="arrow-container" @click="handleClick">
      <a class="arrow">
        <div class="chevron"></div>
        <div class="chevron"></div>
        <div class="chevron"></div>
      </a>
    </div>
</template>
  
<script>
export default {
  name: 'ArrowAnimation',
  props: {
    onClick: {
      type: Function,
      required: true,
    },
  },
  methods: {
    handleClick() {
      this.onClick();
    },
  },
};
</script>
  
 
<style scoped>
  .arrow-container {
    display: flex;
    justify-content: center;
    align-items: center;
    /* width: 100%; */
    margin: 0 auto;
  }
  
  .arrow {
    position: relative;
    width: 24px;
    height: 24px;
    margin-top: 5vh;
    margin-bottom: 10vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .chevron {
    position: absolute;
    width: 28px;
    height: 8px;
    opacity: 0;
    transform: scale3d(0.5, 0.5, 0.5);
    animation: move 3s ease-out infinite;
  }
  
  .chevron:nth-child(1) {
    animation-delay: 0s;
  }
  
  .chevron:nth-child(2) {
    animation-delay: 1s;
  }
  
  .chevron:nth-child(3) {
    animation-delay: 2s;
  }
  
  .chevron:before,
  .chevron:after {
    content: " ";
    position: absolute;
    top: 0;
    height: 100%;
    background: #fff;
  }
  
  .chevron:before {
    left: 0;
    width: 51%;
    transform: skew(0deg, 30deg);
  }
  
  .chevron:after {
    right: 0;
    width: 50%;
    transform: skew(0deg, -30deg);
  }
  
  @keyframes move {
    25% {
      opacity: 1;
    }
    33% {
      opacity: 1;
      transform: translateY(30px);
    }
    67% {
      opacity: 1;
      transform: translateY(40px);
    }
    100% {
      opacity: 0;
      transform: translateY(55px) scale3d(0.5, 0.5, 0.5);
    }
  }
  </style>
  
