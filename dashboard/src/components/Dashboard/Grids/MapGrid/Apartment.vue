<template>
<div class="md-layout-item">
    <div v-if="aptoIcono(apartamento)"  class="apto md-layout-item">
       <!-- <div class="apartment-number" >
            {{apartamento.numero}}
        </div> -->
        <div class="apartment-icon md-layout-item">
            <div :id="index"  class="apartment-door">
                <div class="apartment-doorbell"/>
                <div class="apartment-lock"/>
            </div>
        </div>
    </div>

    <div  v-if="aptoNoIcono(apartamento)"  :class="assignIcon(apartamento)"> 
        <!-- <div class="apartment-number" >
            {{apartamento.numero}}
        </div> -->
        <div class="apartmentBackground">
            <div class="apartmentImage">
                                
            </div>
         </div>                            
    </div>  
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
      //Pass event
      this.$emit("scroll-to-alarm", alarm);
    },
    alarmRevised(alarm) {
      alarm.revised = true;
    },
    aptoIcono(apto) {
        console.log('apt ', apto)
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
         console.log('apt ', apto)
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
};
</script>

<style scoped>
.md-scrollbar {
  width: calc(100% + 9px);
  max-height: 81%;
  overflow: scroll;
}
</style>
