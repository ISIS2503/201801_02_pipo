<template>
<div class="principal">
  <div class="md-layout">
    <div class="md-layout-item md-size-15">
      <div class="lateral">
        <div class="logo"></div>
          <div class="md-size-100">
              <tower-selector
                :ur="ur" 
                v-on:select-tower="selectTower(...arguments)" 
                class="towers-select"
              />
          </div>
     <!--<div class="md-layout-item md-size-100">
              <floor-grid :ur="ur"
               :tower-index="towerIndex"
               class="floors select"></floor-grid>
          </div> -->
      </div>
    </div>
    <div class="md-layout-item">
      <map-grid
        v-on:select-detail="passSelectDetail(...arguments)" 
        v-on:select-tower="towerSelected(...arguments)" 
        :ur="ur"
        :alarms="alarms" 
        :tower-index="towerIndex"
        ref="mapgrid"
      />
    </div>
  </div>
</div>
</template>


<script>
import TowerSelector from "./TowerSelector.vue";
import FloorGrid from "./FloorGrid.vue";
import MapGrid from "./MapGrid/MapGrid.vue";
export default {
  name: "Grids",
  components: {
    TowerSelector,
    FloorGrid,
    MapGrid
  },
  props: ["ur", "alarms"],
  data() {
    return {
      towerIndex: 0
    };
  },
  methods: {
    passSelectDetail(localID, owner, alarm) {
      this.$emit("select-detail", localID, owner, alarm);
    },
    scrollToAlarm(alarm) {
      this.towerIndex = parseInt(alarm.apartamento.split("-")[0])-1;
      this.$refs.mapgrid.scrollToAlarm(alarm);
    },
    selectTower(number){
      this.$refs.mapgrid.scrollToTower(number);
    },
    towerSelected(number){
      this.towerIndex=parseInt(number);
    },
    pushAlarm(dir,alarm){
      this.$refs.mapgrid.pushAlarm(dir,alarm);
    }
  }
};
</script>


<style scoped>
.principal {
  height: 100vh;
  margin-right: 5%;
}

.towers-select{
  height: calc(100vh - 150px);
  position: relative;
}

.lateral {
  position: fixed;
  top:0;
  display: flex;
  flex-direction: column;
}

.logo {
  background: url("../../../assets/yale.png");
  background-size: contain;
  width: 150px;
  height: 150px;
}


.md-layout {
  min-height: 100vh;
}

.md-layout-item {
  margin: auto 0;
}
</style>
