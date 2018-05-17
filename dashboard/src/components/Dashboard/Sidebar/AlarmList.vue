<template>
  <div class="md-scrollbar">
    <div v-for="(alarm, index) in alarms" :key="index">
      <alarm @scroll-to-alarm="scrollToAlarm(...arguments)" :alarm="alarm"/>
    </div>
  </div>
</template>

<script>

const defaultAlarm = {sensetime: 1526576385325, id:"Arduino 007", emergencia: "3", apartamento: "2-5-3", conjunto: "Toscana" , zona: "Centro"}


import Alarm from "./Alarm";
export default {
  name: "AlarmList",
  components: {
    Alarm
  },
  props: ["alarms", "filters"],
  data() {
    return {
      
    };
  },
  methods:{
    scrollToAlarm(alarm){
      //Pass event
      this.$emit('scroll-to-alarm', alarm)
    }
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

      return filtered.reverse();
    }
  },
  mounted(){
    setInterval(()=> this.alarms.push(defaultAlarm), 30000)
  }
};
</script>

<style scoped>

</style>
