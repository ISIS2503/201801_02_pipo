<template>
  <div class="md-scrollbar">
    <alarm 
      v-for="(emergency, index) in filteredEmergencies" :key="index"
      tower="emergency.torre"
      apartment="emergency.apartment"
      alarm="emergency.alarm"
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
  props: ["emergencies", 'filters'],
  data() {
    return {
      revisedEmergencies: []
    }
  },
  computed:{
    filteredEmergencies(){
      return emergencies
    }
  }
};
</script>

<style scoped>

</style>
