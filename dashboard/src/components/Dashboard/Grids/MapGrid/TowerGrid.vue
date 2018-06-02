<template>

<div>
    <!-- Header del edificio (eliminado)
    <div class="above">
      <div @click="previousTower" class="icon-container">
        <md-icon class="md-size-2x next cursor cursor-left">arrow_back_ios</md-icon>
      </div>
        <h1 class="next tower-name">TORRE {{ur.torres[towerIndex].numero}}</h1>
      <div @click="nextTower" class="icon-container">
        <md-icon class="md-size-2x next cursor">arrow_forward_ios</md-icon>
      </div>
    </div> -->
        <div v-for="(piso, index) in tower.pisos" :key="index">
            <div class="md-layout">
                <!-- <b-row> -->
                    <div class="floor-number md-layout-item md-size-5">{{piso.numero}}</div>

                    <apartment v-for="(apartamento, index) in piso.apartamentos" :apartamento="apartamento" :key="index"></apartment>               

                <!-- </b-row> -->
            </div>
        </div>
            <div class="middle-floor" />
            <div class="bottom-floor" />
</div>
</template>

<script>
import "../../../../styles/tower.scss";
import Apartment from "./Apartment";
export default {
  name: "TowerGrid",
  components: {
    Apartment
  },
  props: ["tower"],
  data() {
    return {};
  },
  methods: {
  },
};
</script>

<style scoped>
.md-scrollbar {
  width: calc(100% + 9px);
  max-height: 81%;
  overflow: scroll;
}
</style>
