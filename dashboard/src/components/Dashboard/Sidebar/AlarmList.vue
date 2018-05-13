<template>
  <div class="md-scrollbar">
    <alarm 
      v-for="alarm, index in filteredAlarms"
      :key="alarm.timestamp"
      tower="alarm.torre"
      apartment="alarm.apartment"
      alarm="alarm.alarm"
    />
  </div>
</template>

<script>
import Alarm from './Alarm'
export default {
  name: "AlarmList",
  components:{
    Alarm
  },
  props: ["alarms"],
  data() {
    return {
      filters: []
    }
  },
  computed:{
    filteredAlarms(){
      return alarms
    }
  }
};
</script>

<style scoped>

</style>
