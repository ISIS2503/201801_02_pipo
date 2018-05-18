<template>
<div>
  <md-card>
    <div class="name-container">
      <p class="name">{{ur.torres.length > 1 ? 'TORRES' : 'TORRE'}}</p>
    </div>
    <div class="container">
      <div class="towerContainer" v-for="(torre, index) in ur.torres" :key="index">
        <div @click="selectTower(torre.numero)" :class="{ activeTower: towerIndex == parseInt(torre.numero) }">
          <md-button class="md-raised" :key="index">{{torre.numero}}</md-button>
        </div>
      </div>
    </div>
  </md-card>
</div>
</template>

<script>
export default {
    name: "TowerGrid",
   props: ["ur", 'tower-index'],
   methods: {
       selectTower(numero){
          this.$emit("select-tower", numero);
       }
   }
};
</script>
<style scoped>
.name-container {
    font-weight: bold;
    font-size: 1.5rem;
    padding: 1rem 0;
    margin: none;
    background: rgb(77, 77, 77);
    color: white;
}

.name {
    margin: 0 0;
}

.md-card {
    display: inline-block;
    overflow: auto;
    border: 3px rgb(77, 77, 77) solid;
}

.container {
    display: inline-block;
}

.md-button {
    display: block;
    margin: 0;   
    border-bottom: 3px rgb(77, 77, 77) solid;
}

.active-tower{
    background-color: aqua;
}

.md-button:last-child {
    border-bottom: none;
}
</style>
