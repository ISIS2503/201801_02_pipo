<template>
  <div class="container md-layout" @click="scrollToAlarm">
    <div class="md-layout-item md-size-30 left-container">
      <md-icon class="md-size-2x type-icon">lock_open</md-icon>
    </div>
    <div class="md-layout-item md-size-45 center-container">
      <h2>Torre {{tower}}</h2>
      <h3>Apto {{apartment}}</h3>
      <p>{{alarmMessage}}</p>
    </div>
    <div class="md-layout-item md-size md-size-25 right-container">
      <div class="revise-button">
        <md-button v-if="!alarm.revised" class="md-icon-button" @click="alarmRevised">
          <md-icon class="md-size-2x">
            done_outline
          </md-icon>
        </md-button>
        <p v-if="!alarm.revised" class="icon-tooltip">Revisado</p>
      </div>
      <p class="time">{{timeMessage}}</p>
    </div>
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
      howLong:'',
      startTimestamp:alarm.timestamp
    }
  },
  methods:{
    alarmRevised(){
      this.alarm.revised = true //TODO see if it produces reactivity changes
    },
    scrollToAlarm(){
      this.$emit('scroll-to-alarm', this.alarm)
    },
     hace(){
      var timestamp = startTimestamp;
      const now = moment();
      const expiration = moment(parseInt(timestamp));

      // get the difference between the moments
      const diff = now.diff(expiration);

      //express as a duration
      const diffDuration = moment.duration(diff);


$('#output > tbody:last').append('<tr><td>' + 'pipo' + '</td><td>' +diffDuration.hours() + ' ' + diffDuration.minutes() +' ' + diffDuration.seconds()+'</td></tr>');
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
  },
  mounted(){
    setInterval(this.hace,1000)
  }
}
</script>

<style scoped>

.container {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  border: 4px #be0000 solid;
}

.left-container{
  display: flex;
  justify-content: center;
  align-items: center;
}

.type-icon{
  flex: 1;
}

.center-container{
display: flex;
flex-direction: column;
justify-content: space-around;
align-items: center;
}

h2{
  font-size: 7rem;
}

h3{
  font-size: 4rem;
}

.right-container{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.revise-button{
  box-shadow: 0px 0px 0px 2px #696969;
  transform: box-shadow 0.2s ease-in;
  background: whitesmoke;
}

.revise-button:hover{
  box-shadow: 0px 0px 0px 3px #696969;
}

md-icon {
  color: #be0000;
  padding-left: 8px;
  padding-right: 8px;
}

.time{
  position: relative;
  right:8px;
  top: 8px;
  color: #696969;
}
</style>
