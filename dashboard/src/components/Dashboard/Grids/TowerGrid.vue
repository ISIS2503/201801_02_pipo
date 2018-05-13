<template>
<div>
   <md-card>
    <p>Torre</p>
    <div class="contenedor">
        <md-button class="md-raised">1</md-button>
        <md-button class="md-raised">2</md-button>
        <md-button class="md-raised">3</md-button>
    </div>
    </md-card>
</div>
</template>




<script>
export default {
    name: "TowerGrid"
};
</script>




<style scoped>
.md-card{
  display: inline-block;
}
.contenedor{
  display: inline-block;
}
 .md-button {
    display: block;
    margin: 0;
}
</style>
