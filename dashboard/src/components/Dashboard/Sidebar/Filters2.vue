<template>
<div class="container">

    <b-container>
        <b-row>
            <b-col class="puerta-abierta">
                <md-tooltip md-direction="top">Puerta abierta</md-tooltip>
            </b-col>
            <b-col class="apertura-sospechosa">
                <md-tooltip md-direction="top">Apertura sospechosa</md-tooltip>
            </b-col>
            <b-col class="apertura-no-permitida">
                <md-tooltip md-direction="top">Apertura no permitida</md-tooltip>
            </b-col>
            <b-col class="bateria-baja">
                <md-tooltip md-direction="top">Batería baja</md-tooltip>
            </b-col>
            <b-col class="cerradura-desconectada">
                <md-tooltip md-direction="top">Cerradura desconectada</md-tooltip>
            </b-col>
            <b-col class="hub-desconectado">
                <md-tooltip md-direction="top">Hub desconectado</md-tooltip>
            </b-col>
        </b-row>
    </b-container>
</div>
</template>





<script>
export default {
    name: 'Filters2'
}
</script>





<style lang="scss" scoped>
.puerta-abierta {
    background: url("../../../assets/puertaAbiertaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.puerta-abierta:hover {
    background: url("../../../assets/puertaAbierta.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-sospechosa {
    background: url("../../../assets/aperturaSospechosaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-sospechosa:hover {
    background: url("../../../assets/aperturaSospechosa.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-no-permitida {
    background: url("../../../assets/aperturaNoPermitidaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-no-permitida:hover {
    background: url("../../../assets/aperturaNoPermitida.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.bateria-baja {
    background: url("../../../assets/bateriaCriticaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.bateria-baja:hover {
    background: url("../../../assets/bateriaCritica.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-sospechosa {
    background: url("../../../assets/puertaAbiertaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.apertura-sospechosa:hover {
    background: url("../../../assets/puertaAbierta.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.cerradura-desconectada {
    background: url("../../../assets/cerraduraFueraLineaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.cerradura-desconectada:hover {
    background: url("../../../assets/cerraduraFueraLinea.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.hub-desconectado {
    background: url("../../../assets/hubFueraLineaD.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.hub-desconectado:hover {
    background: url("../../../assets/hubFueraLinea.png");
    background-repeat: no-repeat;
    background-size: contain;
}

.container {
    width: 100%;
    padding: 0;
}

.row {
    width: 100%;
    margin: 0;
    position: relative;
    max-width:460px;
}

.container .col {
    height: 8vh;
    border: 1px rgb(254, 209, 0) solid;
    max-height: 4vw;
}

.container .col:hover {
    height: 8vh;
    color: white;
    border: 1px rgb(254, 209, 0) solid;
    cursor: pointer;
}

h3 {
    line-height: 50px;
    max-height: 6vh;
    margin: 0;
}

.md-tooltip {
    background: rgb(77, 77, 77);
    color: white;
}
</style>
