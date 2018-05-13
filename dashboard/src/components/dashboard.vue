<template>
<div class="dashboard">
    <div class="md-layout">
        <div class="md-layout-item md-size-75">
            <grids></grids>
        </div>
        <div class="md-layout-item sidebar-container">
            <sidebar class="sidebar"></sidebar>
        </div>
    </div>
</div>
</template>



<script>
import Grids from './Dashboard/Grids/Grids.vue'
import Sidebar from './Dashboard/Sidebar/Sidebar.vue'
export default {
    name: "dashboard",
    components: {
        Grids,
        Sidebar
    },
    data() {
        return {
            msg: "Welcome to Your Vue.js App"
        };
    }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.sidebar-container{
    position: fixed;
    right:0;
    top:0;
    width:25%;
}
</style>
