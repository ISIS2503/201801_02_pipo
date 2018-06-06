<template>
<div class="container">

    <b-container>
        <b-row>
            <b-col class="puerta-abierta" v-bind:class="{ 'puerta-abierta-selected': puertaAbiertaSelected }" v-on:click="select('puertaAbierta')">
                <md-tooltip md-direction="top">Puerta abierta</md-tooltip>
            </b-col>
            <b-col class="apertura-sospechosa" v-bind:class="{ 'apertura-sospechosa-selected': aperturaSospechosaSelected }" v-on:click="select('aperturaSospechosa')">
                <md-tooltip md-direction="top">Apertura sospechosa</md-tooltip>
            </b-col>
            <b-col class="apertura-no-permitida" v-bind:class="{ 'apertura-no-permitida-selected': aperturaNoPermitidaSelected }" v-on:click="select('aperturaNoPermitida')">
                <md-tooltip md-direction="top">Apertura no permitida</md-tooltip>
            </b-col>
            <b-col class="bateria-baja" v-bind:class="{ 'bateria-baja-selected': bateriaBajaSelected }" v-on:click="select('bateriaBaja')">
                <md-tooltip md-direction="top">Batería baja</md-tooltip>
            </b-col>
            <b-col class="cerradura-desconectada" v-bind:class="{ 'cerradura-desconectada-selected': cerraduraDesconectadaSelected }" v-on:click="select('cerraduraDesconectada')">
                <md-tooltip md-direction="top">Cerradura desconectada</md-tooltip>
            </b-col>
            <b-col class="hub-desconectado" v-bind:class="{ 'hub-desconectado-selected': hubDesconectadoSelected }" v-on:click="select('hubDesconectado')">
                <md-tooltip md-direction="top">Hub desconectado</md-tooltip>
            </b-col>
        </b-row>
    </b-container>
</div>
</template>

<script>
export default {
  name: "TypeFitlers",
  data() {
    return {
      puertaAbiertaSelected: true,
      aperturaSospechosaSelected: true,
      aperturaNoPermitidaSelected: true,
      bateriaBajaSelected: true,
      cerraduraDesconectadaSelected: true,
      hubDesconectadoSelected: true
    };
  },
  methods: {
    select(type) {
      let category = "";
      let index = -1;
      if (type === "puertaAbierta") {
        this.puertaAbiertaSelected = !this.puertaAbiertaSelected;
        category = "emergency";
        index = 1;
      } else if (type === "aperturaSospechosa") {
        this.aperturaSospechosaSelected = !this.aperturaSospechosaSelected;
        category = "emergency";
        index = 2;
      } else if (type === "aperturaNoPermitida") {
        this.aperturaNoPermitidaSelected = !this.aperturaNoPermitidaSelected;
        category = "emergency";
        index = 3;
      } else if (type === "bateriaBaja") {
        this.bateriaBajaSelected = !this.bateriaBajaSelected;
        category = "emergency";
        index = 4;
      } else if (type === "cerraduraDesconectada") {
        this.cerraduraDesconectadaSelected = !this
          .cerraduraDesconectadaSelected;
        category = "failure";
        index = 1;
      } else if (type === "hubDesconectado") {
        this.hubDesconectadoSelected = !this.hubDesconectadoSelected;
        category = "failure";
        index = 2;
      }
      this.$emit("type-select", category + "-" + index);
    }
  }
};
</script>





<style lang="scss" scoped>

$activated: rgb(230,0,2);
$deactivated: rgb(140,0,1);
.puerta-abierta {
  background-color:$deactivated;
  background: url("../../../assets/puertaAbiertaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.puerta-abierta-selected {
  background-color:$deactivated;
  background: url("../../../assets/puertaAbierta.png");
  background-size: contain;
  background-repeat: no-repeat;
}

.apertura-sospechosa {
  background-color:$deactivated;
  background: url("../../../assets/aperturaSospechosaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.apertura-sospechosa-selected {
  background-color:$deactivated;
  background: url("../../../assets/aperturaSospechosa.png");
  background-size: contain;
  background-repeat: no-repeat;
}

.apertura-no-permitida {
  background-color:$deactivated;
  background: url("../../../assets/aperturaNoPermitidaD.png");
  background-size: contain;
  background-repeat: no-repeat;
}

.apertura-no-permitida-selected {
  background-color:$deactivated;
  background: url("../../../assets/aperturaNoPermitida.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.bateria-baja {
  background-color:$deactivated;
  background: url("../../../assets/bateriaCriticaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.bateria-baja-selected {
  background-color:$deactivated;
  background: url("../../../assets/bateriaCritica.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.apertura-sospechosa {
  background-color:$deactivated;
  background: url("../../../assets/aperturaSospechosaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.apertura-sospechosa-selected {
  background-color:$deactivated;
  background: url("../../../assets/aperturaSospechosa.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.cerradura-desconectada {
  background-color:$deactivated;
  background: url("../../../assets/cerraduraFueraLineaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.cerradura-desconectada-selected {
  background-color:$deactivated;
  background: url("../../../assets/cerraduraFueraLinea.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.hub-desconectado {
  background-color:$deactivated;
  background: url("../../../assets/hubFueraLineaD.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.hub-desconectado-selected {
  background-color:$deactivated;
  background: url("../../../assets/hubFueraLinea.png");
  background-repeat: no-repeat;
  background-size: contain;
}

.container {
  width: 100%;
  padding: 0;
  background: rgb(77, 77, 77);
}

.row {
  width: 100%;
  margin: 0;
  position: absolute;
  max-width: 460px;
  bottom: 0;
  border-top:rgb(77, 77, 77) 5px solid;
}

.container .col {
  height: 6.5vh;
  max-height: 4vw;
}

.container .col:hover {
  height: 8.5vh;
  color: white;
  cursor: pointer;
}

.md-tooltip {
  background: rgb(77, 77, 77);
  color: white;
}
</style>
