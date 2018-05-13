<template>
<div class="dashboard">
    <div class="md-layout ">
        <div class="md-layout-item md-size-75">
          <grids></grids>
        </div>
        <div class="md-layout-item"></div>
    </div>
</div>
</template>


<script>
import Grids from './Dashboard/Grids/Grids.vue'
export default {
  name: "dashboard",
  components: { Grids },
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  }
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
