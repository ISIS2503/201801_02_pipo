<template>
<div class="principal">
  <div class="md-layout">
    <div class="md-layout-item md-size-15">
      <div class="lateral">
        <div class="logo"></div>
          <div class="md-layout-item md-size-100">
              <tower-Grid :ur="ur" 
              v-on:select-tower="selectTower(...arguments)" 
              class="towers select"></tower-Grid>
          </div>
          <div class="md-layout-item md-size-100">
              <floor-grid :ur="ur"
               :tower-index="towerIndex"
               class="floors select"></floor-grid>
          </div>
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
import TowerGrid from "./TowerGrid.vue";
import FloorGrid from "./FloorGrid.vue";
import MapGrid from "./MapGrid.vue";
export default {
  name: "Grids",
  components: {
    TowerGrid,
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
      console.log(localID, " /// ", owner, " /// ", alarm);
      this.$emit("select-detail", localID, owner, alarm);
    },
    scrollToAlarm(alarm) {
      this.towerIndex = parseInt(alarm.localID.split("-")[0]);
      this.$refs.mapgrid.scrollToAlarm(alarm);
    },
    selectTower(number){
       this.towerIndex = parseInt(number);
    },
    towerSelected(number){
      this.towerIndex=parseInt(number);
    }
  }
};
</script>


<style scoped>
.principal {
  height: 100vh;
  margin-right: 5%;
}

.select {
  margin: auto 0;
}

.lateral {
  position: fixed;
  left: 25px;
  bottom: 22%;
}

.logo {
  background: url("../../../assets/yale.png");
  background-size: contain;
  width: 150px;
  height: 150px;
  position: fixed;
  left: 0;
  top: 0;
}

.floors {
  margin-top: 100px;
}

.towers {
  margin-bottom: 50px;
}

.md-layout {
  min-height: 100vh;
}

.md-layout-item {
  margin: auto 0;
}
</style>
