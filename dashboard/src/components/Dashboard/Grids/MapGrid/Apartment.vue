<template>
<div class="apto md-layout-item glow">
    <div v-if="aptoIcono(apartamento)"  class="md-layout-item">
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

    <div  v-if="aptoNoIcono(apartamento)"  :class="assignIcon(apartamento)"> 
        <!-- <div class="apartment-number" >
            {{apartamento.numero}}
        </div> 
        <div class="apartmentBackground">
            <div class="apartmentImage">
                                
            </div>
         </div>       -->                     
    </div>  
    <md-tooltip md-direction="top">Puerta abierta</md-tooltip>
</div>
</template>

<script>
import "../../../../styles/apartment-icon.scss";
export default {
  name: "Apartment",
  props: ["apartamento"],
  data() {
    return {};
  },
  methods: {
    scrollToAlarm(alarm) {
      //Colorar el grid
      let apto = document.getElementById(alarm.apartamento);
      apto.scrollIntoView({ behavior: "smooth" });
      apto.classList.add("brillo");

      const returnToNormal = () => {
        let apto1 = document.getElementById(alarm.apartamento);
        apto1.classList.remove("brillo");
      };

      const stop = setTimeout(returnToNormal, 1000);

      //this.$scrollTo(apto, 1000);
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
    }
  }
};
</script>

<style scoped lang="scss">
$gris: rgb(189, 195, 199);
$negrito: rgb(77, 77, 77);
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

.md-tooltip {
  background: rgb(77, 77, 77);
  color: white;
}

</style>
