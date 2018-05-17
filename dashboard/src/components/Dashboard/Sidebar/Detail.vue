<template>
  <div>
    <div>
    <h1>
      Torre {{tower}} - Apartamento {{apartment}}
    </h1>
    <h2 class="error" v-if="detail.alarm">{{alarmMessage}}</h2>
    </div>
    <div>
      <h2>Propietario</h2>
      <p>{{detail.user.nombre}}</p> <!-- cuadrar para que el usuario de checho tenga nombre y teléfono -.- -->
      <p>{{detail.user.telefono}}</p>
      <p>{{detail.user.email}}</p>
    </div>
  </div>
</template>

<script>
const emergencyTypes = [null, 'Puerta abierta', 'Apertura sospechosa', 'Apertura no permitida', 'Batería baja']
const failureTypes = [null, 'Cerradura fuera de línea', 'Hub fuera de línea']
export default {
  name: 'Detail',
  props: ['detail'],
  data(){
    return{
      owner: null
    }
  },
  mounted(){
    //retrieve owner data
  },
  computed:{
    tower(){
      return this.detail.localID.split('-')[0]
    },
    apartment(){
      return this.detail.localID.split('-')[1] + '0' + this.detail.localID.split('-')[2] // Ex: 3-4-2 => apartment 402
    },
    alarmMessage(){
      if(this.detail.alarm.type === 'emergency')
        return emergencyTypes[parseInt(this.alarm.emergencia)]
      else if (this.detail.alarm.type === 'failure')
        return emergencyTypes[parseInt(this.alarm.failure)];//TODO may not work depending on structure
      else{
        console.log(this.alarm)
        return 'Emergencia desconocida';
      }
    }
  }
}
</script>

<style scoped>

</style>
