<template>
<div class="md-layout-item" v-on:click="selectProperty(apartamento.numero, apartamento.owner)">
    <div v-if="aptoIcono(apartamento)" class="md-layout-item apto" :class="{'glow':mustGlow}">
       <!-- <div class="apartment-number" >
            {{apartamento.numero}}
        </div> 
        <div class="apartment-icon md-layout-item">
            <div :id="index"  class="apartment-door">
                <div class="apartment-doorbell"/>
                <div class="apartment-lock"/>
            </div>
        </div>  -->
    </div>

    <div  v-if="aptoNoIcono(apartamento)" class="md-layout-item apto-alarma" :class="{'glow':mustGlow}"> 
        <!-- <div class="apartment-number" >
            {{apartamento.numero}}
        </div> 
        <div class="apartmentBackground">
            <div class="apartmentImage">
                                
            </div>
         </div>       -->                     
    </div>  
    <md-tooltip md-direction="top">{{apartamento.numero}}</md-tooltip>
</div>
</template>

<script>
import "../../../../styles/apartment-icon.scss";
export default {
  name: "Apartment",
  props: ["apartamento"],
  data() {
    return {
      mustGlow: false
    };
  },
  methods: {
    selectProperty: function(number, auth0_owner) {
      let selectedAlarm = undefined;
      console.log(this.apartamento);
      if(this.apartamento.alarmas.length>0)
      {
        selectedAlarm= this.apartamento.alarmas[0];
      }
      this.$emit("select-detail", number, auth0_owner, selectedAlarm);
    },
    alarmRevised(alarm) {
      alarm.revised = true;
    },
    aptoIcono(apto) {
      if (apto === undefined) {
        return false;
      }
      if (apto.alarmas.length > 0) {
        return false;
      }
      return true;
    },
    aptoNoIcono(apto) {
      if (apto === undefined) {
        return false;
      }
      if (apto.alarmas.length > 0) {
        return true;
      }
      return false;
    },
    glow(){
      this.mustGlow=true;
      setTimeout(function(){
      console.log('se quita');
      this.mustGlow=false;
      }, 1000);
    }
  }
};
</script>

<style scoped lang="scss">
$gris: rgb(189, 195, 199);
$negrito: rgb(77, 77, 77);
$with-alarm: rgb(230,0,2);
.md-scrollbar {
  width: calc(100% + 9px);
  max-height: 81%;
  overflow: scroll;
}

.apto {
  cursor: pointer;
  height: 20px;
  background-color: $gris;
  border: 1px solid $negrito;
}

.apto-alarma{
  cursor: pointer;
  height: 20px;
  background-color: $with-alarm;
  border: 1px solid $negrito;
}

.md-tooltip {
  background: rgb(77, 77, 77);
  color: white;
}

.apto:hover{
border: 1px solid rgb(86, 180, 239);
box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05) inset, 0px 0px 8px rgba(82, 168, 236, 0.6);
}

.glow{
border: 1px solid rgb(86, 180, 239);
box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05) inset, 0px 0px 8px rgba(82, 168, 236, 0.6);
}
</style>
