<template>
  <div class="container" :target="detail.alarm ? ( detail.alarm.revised ? 'revised' : '' ) : 'revised' ">
    <div class="close">
    <div class="close-button" @click="emitClose"><md-button class="md-icon-button"><md-icon>close</md-icon></md-button></div>
    </div>
    <div>
       
    <h1>
      TORRE {{tower}} - APTO {{apartment}}
    </h1>
    <div v-if="detail.alarm">
      <h2 class="error" v-if="!detail.alarm.revised" :class="{'revised-message' : detail.alarm.revised}">{{alarmMessage}}</h2>
    </div>
    </div>
    <div class="info">
      
      <h2 class="owner">Propietario</h2>
      <div class="revise-button" v-if="detail.alarm ? !detail.alarm.revised : false">
        <md-button class="md-icon-button md-size-2x" @click="alarmRevised">
          <md-icon class="">
            done_outline
          </md-icon>
        </md-button>
        <p class="icon-tooltip">Revisar</p>
      </div>
      <div class="detailed-info">
        <md-icon class="md-size-2x">account_box</md-icon><p>{{detail.user.nombre}}</p> <!-- cuadrar para que el usuario de checho tenga nombre y teléfono -.- -->
      </div>
      <div class="detailed-info">
        <md-icon class="md-size-2x">phone</md-icon><p>{{detail.user.telefono}}</p>
      </div>
      <div class="detailed-info">
        <md-icon class="md-size-2x">mail_outline</md-icon><p>{{detail.user.email}}</p>
      </div>
    </div>
  </div>
</template>

<script>
const emergencyTypes = [
  null,
  "Puerta abierta",
  "Apertura sospechosa",
  "Apertura no permitida",
  "Batería baja"
];
const failureTypes = [null, "Cerradura fuera de línea", "Hub fuera de línea"];
export default {
  name: "Detail",
  props: ["detail"],
  data() {
    return {
      owner: null
    };
  },
  methods: {
    emitClose() {
      this.$emit("close");
    },
    alarmRevised(){
      this.detail.alarm.revised = true
    }
  },
  mounted() {
    //retrieve owner data
  },
  computed: {
    tower() {
      return this.detail.localID.split("-")[0];
    },
    apartment() {
      return (
        this.detail.localID.split("-")[1] +
        "0" +
        this.detail.localID.split("-")[2]
      ); // Ex: 3-4-2 => apartment 402
    },
    alarmMessage() {
      if (this.detail.alarm.emergencia) //TODO may not work depending on structure
        return emergencyTypes[parseInt(this.detail.alarm.emergencia)];
      else if (this.detail.alarm.fallo)
        return failureTypes[parseInt(this.detail.alarm.failure)];
      else {
        console.log(this.alarm);
        return "Emergencia desconocida";
      }
    }
  }
};
</script>

<style scoped>
.container {
  border: 5px rgb(223, 0, 22) solid;
  background: whitesmoke;
  padding: 0;
  position: relative;
}

[target="revised"]{
  border: 5px rgb(56, 165, 48) solid;
}

h1 {
  background: rgb(223, 0, 22);
  color: white;
  margin: 0;
  padding-top: 30px;
  padding: 0 10px;
}

[target="revised"] h1{
  background:  rgb(56, 165, 48);
}

.revised-message{
  background:  rgb(56, 165, 48);
}

.detailed-info p {
  display: inline-block;
  font-size: 1.5rem;
  vertical-align: middle;
  margin: 0;
  margin-left: 10px;
}

.detailed-info .md-icon {
  display: inline-block;
  vertical-align: middle;
}

.owner {
   display: inline-block;
  border-bottom: 4px rgba(223, 0, 22, 0) solid;
  background: rgba(223, 0, 22, 0);
  color: black;
}

h2 {
  background: rgb(223, 0, 22);
  color: white;
}


.info {
  text-align: left;
  padding: 0 10px;
}


.revise-button {
  /*display: inline-block; ver advertencia de vscode*/
  box-shadow: 0px 0px 0px 2px #696969;
  transform: box-shadow 0.2s ease-in;
  background: whitesmoke;
  margin-top:2px;
  float: right;
}

.revise-button:hover {
  box-shadow: 0px 0px 0px 3px #696969;
}


.close{
  background:rgb(223, 0, 22);
  width:100%;  
  position:relative;
  height:40px;
}

[target="revised"] .close{
  background:  rgb(56, 165, 48);
}

.close-button {
  display:block;
  top: 0;
  position:absolute;
  right:0;
}

.icon-tooltip{
  text-align: center;
  margin: 0;
}

.close .md-icon{  
  color:white;
}
</style>
