<template>

<div>
        <div v-for="(piso, index) in tower.pisos" :key="index">
            <div class="md-layout">
                <!-- <b-row> -->
                    <div class="floor-number md-layout-item md-size-5">{{piso.numero}}</div>

                    <apartment 
                    v-for="(apartamento, index) in piso.apartamentos" 
                    :apartamento="apartamento" 
                    :key="index" 
                    :id="'apartment'+piso.numero+'-'+apartamento.numero"
                    v-on:select-detail="passSelectDetail(piso.numero,...arguments)" ></apartment>               

                <!-- </b-row> -->
            </div>
        </div>
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
    scrollToAlarm(alarm){
      console.log('towr ', this.tower);
      let apto = document.getElementById('apartment'+alarm.apartamento.split("-")[1]+'-'+alarm.apartamento.split("-")[2]);  
      apto.scrollIntoView({ behavior: "smooth" });
      apto.classList.add("glow");
      setTimeout(function(){
        apto.classList.remove("glow");
      }, 1000);
    },
    passSelectDetail(floorNumber, aptoNumber, auth0_owner, selectedAlarm){
      let localID= this.tower.numero+ '-'+ floorNumber + '-' + aptoNumber;
      this.$emit("select-detail", localID, auth0_owner, selectedAlarm);
    }
  },
};
</script>

<style scoped>
.md-scrollbar {
  width: calc(100% + 9px);
  max-height: 81%;
  overflow: scroll;
}

.floor-number {
  vertical-align: middle;
  display: inline-block;
  padding: 0;
  overflow: hidden;
  box-shadow: 1px 0px 1px 1px black;
  font-weight: bold;
  font-size: 0.5rem;
  height: unset !important;
  border-radius: 15% 0 0 15%;
}

.glow{
/*border: 1px solid rgb(86, 180, 239);*/
box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05) inset, 0px 0px 8px rgba(82, 168, 236, 0.6);
}
</style>
