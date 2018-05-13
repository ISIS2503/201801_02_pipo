<template>
<div class="principal">
    <div class="md-layout">
        <div class="md-layout-item md-size-15">
            <div class="lateral">
                <div class="md-layout-item md-size-100">
                    <tower-Grid class="towers select"></tower-Grid>
                </div>
                <div class="md-layout-item md-size-100">
                    <floor-grid class="floors select"></floor-grid>
                </div>
            </div>
        </div>
        <div class="md-layout-item">
            <map-grid></map-grid>
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
  }
};
</script>


<style scoped>
.principal {
  height: 100vh;
}

.select {
  margin: auto 0;
}

.lateral {
  position: fixed;
  left: 10px;
  bottom: 20%;
}

.md-layout {
  min-height: 100vh;
}

.floors {
  margin-top: 100px;
}

.towers {
  margin-bottom: 50px;
}

.md-layout-item {
  margin: auto 0;
}
</style>
