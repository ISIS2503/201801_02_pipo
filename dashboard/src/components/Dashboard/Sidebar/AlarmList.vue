<template>
  <div class="md-scrollbar">
    <div v-for="(alarm, index) in alarms" :key="index">
      <alarm :alarm="alarm"/>
    </div>
  </div>
</template>

<script>
import Alarm from "./Alarm";
export default {
  name: "AlarmList",
  components: {
    Alarm
  },
  props: ["alarms", "filters"],
  data() {
    return {
      revisedAlarms: []
    };
  },
  computed: {
    filteredAlarms() {
      let filtered = [];

      filtered = this.alarms
        .filter(alarm => (this.filters.revised ? !alarm.revised : true))
        .filter(alarm => (this.filters.notRevised ? alarm.revised : true))
        .filter(alarm => {
          if (alarm.type === "emergency") {
            return !this.filters.emergencies.includes(parseInt(alarm.emergencia)) //Si lo incluye, está dentro de los filtros, es decir, debe retornar falso
          } else if (alarm.type === "failure") {
            return !this.filters.faliures.includes(parseInt(alarm.falla)) //Si lo incluye, está dentro de los filtros, es decir, debe retornar falso
          } else {
            return true; //nunca filtrar errores desconocidos
          }
        });

      return filtered;
    }
  }
};
</script>

<style scoped>

</style>
