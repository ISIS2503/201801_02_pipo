<template>
  <div class="container md-layout">
    <div class="md-layout-item md-size-15">
      <md-icon class="md-size-2x">lock_open</md-icon>
    </div>
    <div class="md-layout-item md-size-85">
      <h2>Torre {{tower}}</h2>
      <h3>Apto {{apartment}}</h3>
      <p>{{alarmMessage}}</p>
    </div>
    <p class="time">{{timeMessage}}</p>
  </div>
</template>

<script>
export default {
  name: "Alarm",
  props: ['tower', 'apartment', 'alarm'],
  data(){
    return{
      alarmMessage:''
    }
  },
  methods:{
    parseAlarm(){
      return this.alarm
    }
  },
  mounted(){
    this.alarmMessage = this.parseAlarm()
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
