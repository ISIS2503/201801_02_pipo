<template>

<div class="tower-container">
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

    <div v-for="(tower, index) in ur.torres" :key="index" :id="'tower'+tower.numero">

      <div class="above">
         <h1 class="next tower-name">TORRE {{tower.numero}}</h1>
      </div> 

      <div class="roof">
        <div class="middle-roof"/>            
        <div class="bottom-roof"/>            
      </div>           

      <towerGrid 
      :tower="tower" 
      :ref="'tower'+tower.numero"
      v-on:select-detail="passSelectDetail(...arguments)" ></towerGrid>

       <div class="floor">
            <div class="middle-floor"/>            
            <div class="bottom-floor"/>            
        </div> 
    </div>

</div>
</template>

<script>
import data from "../Provisionaldata"; //Importar datos para probar front
import TowerGrid from "./TowerGrid.vue";
export default {
  name: "MapGrid",
  props: ["urPP", "alarms", "towerIndex"], //Cambiar urPP a ur para despliegue real
  components: {
    TowerGrid
  },
  data: function() {
    return {
      ur: null, //El despliegue real no tiene este atributo en el data
      boolean: true
    };
  },
  methods: {
    passSelectDetail: function(localID, auth0_owner, selectedAlarm) {
      this.$emit("select-detail", localID, auth0_owner, selectedAlarm);
    },
    scrollToAlarm(alarm) {
      this.$refs['tower'+ alarm.apartamento.split("-")[0]].scrollToAlarm(alarm);
    },
    scrollToTower(number){
      let tower = document.getElementById('tower'+number);
      tower.scrollIntoView({ behavior: "smooth" });
      tower.classList.remove("tower-shine");
      setTimeout(function(){
        tower.classList.add("tower-shine");
      }, 500);
    },
    pushAlarm(dir, alarm) {
      this.ur.torres[dir[0] - 1].pisos[
        this.ur.torres[dir[0] - 1].pisos.length - dir[1]
      ].apartamentos[dir[2] - 1].alarmas.push(alarm);
    }
  },
  mounted() {
    this.torres = this.ur; //set unidad to prop
    console.log(data);
    this.ur = data; //Reemplazar el prop 'ur' por una propiedad en el data, usando los datos importados
  }
};
</script>

<style scoped lang="scss">
.above {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.next {
  display: inline-block;
  vertical-align: middle;
}

.tower-name {
  font-weight: bold;
  font-size: 1rem;
}

.tower-shine{
  position:relative;
  overflow: hidden;
}

.tower-shine::after {
  pointer-events: none;
  animation: shine 5s ease-in-out;
  animation-fill-mode: forwards;  
  content: "";
  position: absolute;
  top: -110%;
  left: -210%;
  width: 200%;
  height: 200%;
  opacity: 0;
  transform: rotate(30deg);
  
  background: rgba(255, 255, 255, 0.13);
  background: linear-gradient(
    to right, 
    rgba(255, 255, 255, 0.13) 0%,
    rgba(255, 255, 255, 0.13) 77%,
    rgba(255, 255, 255, 0.5) 92%,
    rgba(255, 255, 255, 0.0) 100%
  );
}

.tower-shine:active:after {
 // opacity: 0;
  pointer-events: none;
}

@keyframes shine{
  10% {
    opacity: 1;
    top: -30%;
    left: -30%;
    transition-property: left, top, opacity;
    transition-duration: 0.7s, 0.7s, 0.15s;
    transition-timing-function: ease;
  }
  100% {
    opacity: 0;
    top: -30%;
    left: -30%;
    transition-property: left, top, opacity;
  }
}

.icon-container {
  display: flex;
}

.cursor {
  width: 55px;
  height: 55px;
  background: rgb(77, 77, 77);
  color: white;
  border-radius: 50%;
  line-height: 55px;
  text-align: center;
}

.cursor:hover {
  cursor: pointer;
}

.cursor-left {
  position: relative;
  padding-left: 11px;
}

.floor-container {
  position: relative;
  display: flex;
  width: 90%;
}

.roof {
  position: relative;
  z-index: 2;
  height: 70px;
}

.apartment-number {
  height: 50px;
  width: 100%;
  border: 1px rgb(77, 77, 77) solid;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  line-height: 50px;
  font-weight: bold;
  font-size: 2rem;
  position: relative;
}

/* Puerta abierta */
.e-1 .apartmentImage {
  //background: url("../../../assets/puertaAbierta.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Apertura sospechosa */
.e-2 .apartmentImage {
  //background: url("../../../assets/aperturaSospechosa.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Apertura no permitida */
.e-3 .apartmentImage {
  // background: url("../../../assets/aperturaNoPermitida.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Batería baja */
.e-4 .apartmentImage {
  // background: url("../../../assets/bateriaCritica.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Cerradura fuera de linea */
.f-1 .apartmentImage {
  // background: url("../../../assets/cerraduraFueraLinea.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Hub fuer de linea */
.f-2 .apartmentImage {
  // background: url("../../../assets/hubFueraLinea.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

.with-alarm .apartment-number {
  background: white;
  color: rgb(223, 0, 22);
}

.apartmentBackground {
  width: 100%;
  height: 100px;
  background: rgb(77, 77, 77);
}

.apartmentBackground:hover,
.apartmentBackground:active {
  cursor: pointer;
}

.col-1 {
  display: inline-block;
  height: 118px;
  position: relative;
  top: 1px;
}

.apto {
  display: inline-block;
  padding: 0;
  vertical-align: middle;
  width: 100%;
}

.apto:hover,
.apto:active {
  cursor: pointer;
}

.cuerpo {
  position: relative;
  z-index: 1;
  width: 100%;
  top: -5px;
  height: 600px;
  background: rgb(132, 96, 75);
  border-top: rgb(77, 77, 77) 1px solid;
}

.tower-container {
  margin: 2rem 0;
  display: grid;
  grid-template-columns: repeat(5, 20%);
  justify-content: center;
  grid-row-gap: 1.5rem;
  grid-column-gap: 1.5rem;
  text-align: center;
  position: relative;
}

.brillo {
  box-shadow: 10px 10px 20px red;
  transition: box-shadow 0.3s ease-in-out repeat;
}
</style>
