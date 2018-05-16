<template>
  <div class="md-scrollbar">
    <alarm 
      v-for="(alarm, index) in filteredAlarms" :key="index"
      alarm="alarm"
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
  props: ['alarms', 'filters'],
  data() {
    return {
      revisedEmergencies: []
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
