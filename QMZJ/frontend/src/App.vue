<template>
  <div id="app">
    <!-- img src="./assets/logo.png" -->
    <router-view />
    <PetComponent v-if="isLoggedIn" />
  </div>
</template>

<script>
import PetComponent from "@/components/PetComponent.vue";

export default {
  name: "App",
  components: {
    PetComponent,
  },
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = (localStorage.getItem("isLoggedIn") === "true");
      if(localStorage.getItem("isChat") === "true"){
        this.isLoggedIn = false;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: "hongleixingshu", "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
}

@font-face {
  font-family: "hongleixingshu";
  src: url("~@/assets/HongLeiXingShuJianTi-2.otf") format("opentype");
}
</style>
