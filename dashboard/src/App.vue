<template>
<div id="app">
    <router-view/>
</div>
</template>


<script>
export default {
    name: "App"
};
</script>


<style>
@import url("https://fonts.googleapis.com/css?family=Roboto");
#app {
    font-family: "Roboto", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    max-width: 100%;
    overflow-x: hidden;
}

.md-list{
  background: whitesmoke;
  padding: 0px;
}
</style>
