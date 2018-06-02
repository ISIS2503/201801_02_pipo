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

    <div class="container" v-if="ur.torres[towerIndex]">
        <div class="roof">
            <div class="middle-roof"/>            
            <div class="bottom-roof"/>            
        </div>

        <div v-for="(piso, index) in ur.torres[towerIndex].pisos" :key="index">
            <div class="md-layout">
                <!-- <b-row> -->
                    <div class="floor-number md-layout-item md-size-5">{{piso.numero}}</div>

                        <div
                          v-for="(apartamento, index) in piso.apartamentos" 
                          :key="index"                          
                          v-on:click="selectProperty('' + ur.torres[towerIndex].numero + '-' + piso.numero + '-' + apartamento.numero, apartamento.owner)"
                          :id="ur.torres[towerIndex].numero + '-' + piso.numero + '-' + apartamento.numero"
                          :v-scroll-to="ur.torres[towerIndex].numero + '-' + piso.numero + '-' + apartamento.numero"
                          class="md-layout-item"
                        >

                        <div v-if="aptoIcono(apartamento)"  class="apto md-layout-item">
                            <div class="apartment-number" >
                                {{apartamento.numero}}
                            </div>
                            <div class="apartment-icon md-layout-item">
                                <div :id="index"  class="apartment-door">
                                    <div class="apartment-doorbell"/>
                                    <div class="apartment-lock"/>
                                </div>
                            </div>
                        </div>

                        <div  v-if="aptoNoIcono(apartamento)"  :class="assignIcon(apartamento)"> 
                          <div class="apartment-number" >
                                {{apartamento.numero}}
                          </div>
                            <div class="apartmentBackground">
                                <div class="apartmentImage">
                                
                                </div>
                            </div>
                            
                          </div>
                    </div>                  

                <!-- </b-row> -->
            </div>
        </div>
            <div class="middle-floor" />
            <div class="bottom-floor" />
    </div>


</div>
</template>

<script>
import "../../../styles/tower.css";
import "../../../styles/apartment-icon.css";
import data from "./ProvisionalData"; //Importar datos para probar front

export default {
  name: "MapGrid",
  props: ["urPP", "alarms", "towerIndex"], //Cambiar urPP a ur para despliegue real
  data: function() {
    return {
      ur: null, //El despliegue real no tiene este atributo en el data
      boolean: true
    };
  },
  computed: {},
  methods: {
    selectProperty: function(localID, auth0_owner) {
      let selectedAlarm = undefined;
      for (var alarm of this.alarms) {
        if (alarm.apartamento === localID) {
          selectedAlarm = alarm;
        }
      }

      this.$emit("select-detail", localID, auth0_owner, selectedAlarm);
    },
    previousTower() {
      this.towerIndex =
        (this.towerIndex - 1 + this.ur.torres.length) % this.ur.torres.length;
      this.$emit("tower-selected", this.towerIndex);
    },
    nextTower() {
      this.towerIndex = (this.towerIndex + 1) % this.ur.torres.length;
      this.$emit("tower-selected", this.towerIndex);
    },
    scrollToAlarm(alarm) {
      //Colorar el grid
      let apto = document.getElementById(alarm.apartamento);
      console.log("apto", apto);
      apto.scrollIntoView({ behavior: "smooth" });
      apto.classList.add("brillo");

      const returnToNormal = () => {
        let apto1 = document.getElementById(alarm.apartamento);
        apto1.classList.remove("brillo");
      };

      const stop = setTimeout(returnToNormal, 1000);

      //this.$scrollTo(apto, 1000);
    },
    pushAlarm(dir, alarm) {
      //console.log('llega1');
      this.ur.torres[dir[0] - 1].pisos[
        this.ur.torres[dir[0] - 1].pisos.length - dir[1]
      ].apartamentos[dir[2] - 1].alarmas.push(alarm);
      //console.log('llega6');
      console.log(this.towerIndex);
    },
    assignIcon(apartamento) {
      if (apartamento.alarmas.length > 0) {
      }
      let classObject = {};
      classObject["md-layout-item"] = true;
      if (apartamento.alarmas.length > 0) {
        classObject[apartamento.alarmas[0].normalType] = true;
        classObject["with-alarm"] = true;
        return classObject;
      } else {
        classObject["apto"] = true;
      }
      console.log("al menos?");
      return classObject;
    },
    aptoIcono(apto) {
      if (apto === undefined) {
        console.log("undefined");
        return false;
      }
      if (apto.alarmas.length > 0) {
        console.log("lista");
        return false;
      }
      return true;
    },
    aptoNoIcono(apto) {
      if (apto === undefined) {
        console.log("undefined2");
        return false;
      }
      if (apto.alarmas.length > 0) {
        console.log("lista2");
        return true;
      }
      return false;
    }
  },
  mounted() {
    this.torres = this.ur; //set unidad to prop
    console.log(data);
    this.ur = data; //Reemplazar el prop 'ur' por una propiedad en el data, usando los datos importados
  }
};
</script>

<style scoped>
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
  font-size: 3rem;
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

.floor-number {
  vertical-align: middle;
  display: inline-block;
  line-height: 140px;
  padding: 0;
  overflow: hidden;
  box-shadow: 1px 0px 1px 1px black;
  font-weight: bold;
  font-size: 2rem;
  height: unset !important;
  border-radius: 15% 0 0 15%;
}

/* Puerta abierta */
.e-1 .apartmentImage {
  background: url("../../../assets/puertaAbierta.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Apertura sospechosa */
.e-2 .apartmentImage {
  background: url("../../../assets/aperturaSospechosa.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Apertura no permitida */
.e-3 .apartmentImage {
  background: url("../../../assets/aperturaNoPermitida.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Batería baja */
.e-4 .apartmentImage {
  background: url("../../../assets/bateriaCritica.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Cerradura fuera de linea */
.f-1 .apartmentImage {
  background: url("../../../assets/cerraduraFueraLinea.png");
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

/* Hub fuer de linea */
.f-2 .apartmentImage {
  background: url("../../../assets/hubFueraLinea.png");
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
  width:100%;
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

.container {
  text-align: center;
  width: 102%;
  position: relative;
  left: -10px;
}

.brillo {
  box-shadow: 10px 10px 20px red;
  transition: box-shadow 0.3s ease-in-out repeat;
}
</style>
