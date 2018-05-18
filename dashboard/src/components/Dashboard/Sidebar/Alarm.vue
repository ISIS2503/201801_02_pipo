<template>
  <div class="container md-layout" :target="alarm.revised ? 'revised' : 'not-revised' " @click="scrollToAlarm">
    <div class="md-layout-item md-size-35 left-container">
      <div class="type-icon" :class="assignIcon"></div>
    </div>
    <div class="md-layout-item md-size-45 center-container">
      <h2>TORRE {{tower}}</h2>
      <h3>APTO {{apartment}}</h3>
      <p class="alarm-message">{{alarmMessage}}</p>
    </div>
    <div class="md-layout-item md-size md-size-20 right-container">

<div v-if="alarm.revised" class="button-delete" @click="alarmDeleted">
        <md-button class="md-icon-button">
          <md-icon>
            delete
          </md-icon>
        </md-button>
      </div>
      <div  class="time-container">
        <p class="time"><md-icon class="time-icon">access_time</md-icon>{{howLongStr}}</p>
      </div>

      <div v-if="!alarm.revised" class="revise-button" @click="alarmRevised">
        <md-button class="md-icon-button">
          <md-icon>
            done_outline
          </md-icon>
        </md-button>
        <p class="icon-tooltip">Revisar</p>
      </div>
      
    </div>
  </div>
</template>

<script>
import moment from "moment";

const emergencyTypes = [
  null,
  "Puerta abierta",
  "Apertura sospechosa",
  "Apertura no permitida",
  "Batería baja"
];
const failureTypes = [null, "Cerradura fuera de línea", "Hub fuera de línea"];

export default {
  name: "Alarm",
  props: ["alarm"],
  data() {
    return {
      howLong: {
        secs: -1,
        min: -1,
        hours: -1
      },
      startTimestamp: this.alarm.timestamp
    };
  },
  methods: {
    alarmRevised() {
      /* this.alarm.revised = true; //TODO see if it produces reactivity changes */
      this.$emit("alarm-revised", this.alarm);
    },
    alarmDeleted() {
      /* this.alarm.revised = true; //TODO see if it produces reactivity changes */
      this.$emit("alarm-deleted", this.alarm);
    },
    scrollToAlarm() {
      this.$emit("scroll-to-alarm", this.alarm);
    },
    hace() {
      var timestamp = this.startTimestamp;
      const now = moment();
      const expiration = moment(parseInt(timestamp));

      // get the difference between the moments
      const diff = now.diff(expiration);

      //express as a duration
      const diffDuration = moment.duration(diff);
      this.howLong.hours = diffDuration.hours();
      this.howLong.min = diffDuration.minutes();
      this.howLong.secs = diffDuration.seconds();
    }
  },
  computed: {
    tower() {
      return this.alarm.apartamento.split("-")[0];
    },
    apartment() {
      return (
        "" +
        this.alarm.apartamento.split("-")[1] +
        "0" +
        this.alarm.apartamento.split("-")[2]
      ); // Ex: 3-4-2 => apartment 402
    },
    alarmMessage() {
      if (this.alarm.emergencia)
        return emergencyTypes[parseInt(this.alarm.emergencia)];
      else if (this.alarm.fallo)
        return emergencyTypes[parseInt(this.alarm.failure)];
      else {
        //TODO may not work depending on structure
        console.log("Unknown Alarm: ",this.alarm);
        return "Emergencia desconocida";
      }
    },
    timeMessage() {
      return new Date(this.alarm.sensetime); //TODO check time alarms
    },
    howLongStr() {
      let resp = " ";
      if (this.howLong.hours > 0) {
        resp += this.howLong.hours + " h, ";
        resp += this.howLong.min + " m ";
      } else {
        if (this.howLong.min > 0) {
          resp += this.howLong.min + " m ";
          resp += this.howLong.secs + " s";
        } else {
          resp += this.howLong.secs + " s ";
        }
      }
      return resp;
    },
    assignIcon() {
      let classObject = {};
      classObject[this.alarm.normalType] = true;
      return classObject;
    }
  },
  mounted() {
    setInterval(this.hace, 1000);
    this.alarm.timestamp = new Date().getTime();
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  padding: 0px;
  margin-top: 2px;
  border: 4px rgb(223, 0, 22) solid;
  transform: background-color 0.3s ease-in;
  transform: border-color 0.3s ease-in;
  transform: border-width 0.3s ease-in;
}

[target="revised"] {
  border: 4px rgb(56, 165, 48) solid;
}

.container:hover,
.container:active {
  cursor: pointer;
  background-color: lightgray;
  border-color: rgb(133, 6, 19);
}

[target="revised"]:hover,
[target="revised"]:active {
  border: 4px rgb(24, 97, 18) solid;
}

.left-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Puerta abierta */
.e-1 {
  background: url("../../../assets/puertaAbierta.png");
}

[target="revised"] .e-1 {
  background: url("../../../assets/puertaAbiertaV.png");
}

/* Apertura sospechosa */
.e-2 {
  background: url("../../../assets/aperturaSospechosa.png");
}

[target="revised"] .e-2 {
  background: url("../../../assets/aperturaSospechosaV.png");
}

/* Apertura no permitida */
.e-3 {
  background: url("../../../assets/aperturaNoPermitida.png");
}

[target="revised"] .e-3 {
  background: url("../../../assets/aperturaNoPermitidaV.png");
}

/* Batería baja */
.e-4 {
  background: url("../../../assets/bateriaCritica.png");
}

[target="revised"] .e-4 {
  background: url("../../../assets/bateriaCriticaV.png");
}

/* Cerradura fuera de linea */
.f-1 {
  background: url("../../../assets/cerraduraFueraLinea.png");
}

[target="revised"] .f-1 {
  background: url("../../../assets/cerraduraFueraLineaV.png");
}

/* Hub fuer de linea */
.f-2 {
  background: url("../../../assets/hubFueraLinea.png");
}

[target="revised"] .f-2 {
  background: url("../../../assets/hubFueraLineaV.png");
}

[target="revised"] .type-icon,
[target="not-revised"] .type-icon {
  flex: 1;
  height: 100%;
  width: 100%;
  background-repeat: no-repeat;
  background-size: contain;
}

.center-container {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: left;
  text-align: left;
}

p {
  margin: 0;
}

h2 {
  font-size: 1.7rem;
  margin: 0;
}

h3 {
  font-size: 1.9rem;
  margin: 0;
}

.alarm-message {
  color: rgb(223, 0, 22);
  font-weight: bold;
  font-size: 1.2rem;
  margin: 0;
}

[target="revised"] .alarm-message {
  color: rgb(56, 165, 48);
}

.right-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position:relative;
}

.revise-button {
  box-shadow: 0px 0px 0px 2px #696969;
  transform: box-shadow 0.2s ease-in;
  background: whitesmoke;
  margin-top: 2px;
}

.revise-button:hover {
  box-shadow: 0px 0px 0px 3px #696969;
}

md-icon {
  color: rgb(223, 0, 22);
  padding-left: 8px;
  padding-right: 8px;
}

.button-delete {
  top: 0;
  right: 0;
  background: rgb(56, 165, 48);
  max-width: 50px;
  margin: 0;
  position:relative;
  left:40%;
}

[target="revised"] md-icon {
  color: rgb(56, 165, 48);
}

.time-container {
  margin-right: 15px;
}

.time {
  width: 100px;
  color: #696969;
}
</style>
