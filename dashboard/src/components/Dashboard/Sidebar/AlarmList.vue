<template>
  <div class="md-scrollbar">
    <div v-for="(alarm, index) in filteredAlarms" :key="index">
      <alarm 
        @scroll-to-alarm="scrollToAlarm(...arguments)" 
        :alarm="alarm"
       />
    </div>
  </div>
</template>

<script>

const defaultAlarm = {sensetime: 1526576385325, id:"Arduino 007", timestamp: new Date().getTime(), emergencia: "3", apartamento: "1-1-2", conjunto: "Toscana" , zona: "Centro", normalType: "e-4"}


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
    },
    alarmRevised(alarm){
      alarm.revised = true
    }
  },
  computed: {
    filteredAlarms() {
      let filtered = [];

      filtered = this.alarms
        .filter(alarm => (this.filters.revised ? !alarm.revised : true))
        .filter(alarm => (this.filters.notRevised ? alarm.revised : true))
        .filter(alarm => {
          if (alarm.emergencia) {
            return !this.filters.emergencies.includes(parseInt(alarm.emergencia)) //Si lo incluye, está dentro de los filtros, es decir, debe retornar falso
          } else if (alarm.fallo) {
            return !this.filters.failures.includes(parseInt(alarm.fallo)) //Si lo incluye, está dentro de los filtros, es decir, debe retornar falso
          } else {
            return true; //nunca filtrar errores desconocidos
          }
        });

        let test = []
        for(var alarmm of filtered){
          test.push(alarmm.timestamp)
        }
      return filtered.slice().reverse();
    }
  },
  mounted(){

    const meterAlarma = () => {
      this.alarms.push(Object.assign({}, defaultAlarm))
    };
/* 
    meterAlarma();
    meterAlarma();
    //setInterval(meterAlarma, 4000); */
  }
};
</script>

<style scoped>

.md-scrollbar{
  width:calc(100% + 9px);
  max-height:81%;
 overflow: scroll;
}
</style>
