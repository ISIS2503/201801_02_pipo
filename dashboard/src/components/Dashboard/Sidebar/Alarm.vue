<template>
  <div class="container md-layout" @click="scrollToAlarm">
    <div class="md-layout-item md-size-15">
      <md-icon class="md-size-2x">lock_open</md-icon>
    </div>
    <div class="md-layout-item md-size-85">
      <h2>Torre {{tower}}</h2>
      <h3>Apto {{apartment}}</h3>
      <p>{{alarmMessage}}</p>
    </div>
    <md-button v-if="!alarm.revised" class="md-icon-button" @click="alarmRevised">
      <md-icon>
        done_outline
      </md-icon>
    </md-button>
    <p class="time">{{timeMessage}}</p>
  </div>
</template>

<script>

const emergencyTypes = [null, 'Puerta abierta', 'Apertura sospechosa', 'Apertura no permitida', 'Batería baja']
const failureTypes = [null, 'Cerradura fuera de línea', 'Hub fuera de línea']

export default {
  name: "Alarm",
  props: ['alarm'],
  data(){
    return{

    }
  },
  methods:{
    alarmRevised(){
      this.alarm.revised = true //TODO see if it produces reactivity changes
    },
    scrollToAlarm(){
      this.$emit('scroll-to-alarm', this.alarm)
    }
  },
  computed:{
    tower(){
      return this.alarm.apartamento.split('-')[0]
    },
    apartment(){
      return '' + this.alarm.apartamento.split('-')[1] + '0' + this.alarm.apartamento.split('-')[2] // Ex: 3-4-2 => apartment 402
    },
    alarmMessage(){
      if(this.alarm.type === 'emergency')
        return emergencyTypes[parseInt(this.alarm.emergencia)]
      else if (this.alarm.type === 'failure')
        return emergencyTypes[parseInt(this.alarm.failure)]; //TODO may not work depending on structure
      else{
        console.log(this.alarm)
        return 'Emergencia desconocida';
      }
    },
    timeMessage(){
      return new Date(this.alarm.sensetime) //TODO check time alarms
    }
  }
}
</script>

<style scoped>
md-icon {
  color: #be0000;
  padding-left: 8px;
  padding-right: 8px;
}

.container {
  padding: 8px;
  border: 8px #be0000 solid;
}

.time{
  position: relative;
  right:8px;
  top: 8px;
  color: #696969;
}
</style>
