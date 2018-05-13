<template>
<div class="container">
    <b-container>
        <b-row>
            <b-col>
                <md-tooltip md-direction="top" >Batería baja</md-tooltip>
                <md-icon class="md-size-2x"> person</md-icon>
            </b-col>
            <b-col>
                 <md-tooltip md-direction="top" >Apertura sospechosa</md-tooltip> 
                <md-icon class="md-size-2x">person</md-icon>
            </b-col>
            <b-col>
                 <md-tooltip md-direction="top" >Apertura no permitida</md-tooltip>
                <md-icon class="md-size-2x">person</md-icon>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                 <md-tooltip md-direction="top" >Puerta abierta</md-tooltip>
                <md-icon class="md-size-2x">person</md-icon>
            </b-col>
            <b-col>
                 <md-tooltip md-direction="top" >Cerradura desconectada</md-tooltip>
                <md-icon class="md-size-2x">person</md-icon>
            </b-col>
            <b-col>
                 <md-tooltip md-direction="top" >Hub desconectado</md-tooltip>
                <md-icon class="md-size-2x">person</md-icon>
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
.container {
    width: 96%;
    padding: 0;
}

.container .col {
    height: 6vh;
    border: 1px yellow solid;
}

.container .col:hover {
    height: 6vh;
    background:black;
    color:white;
    border: 1px black solid;
}

.row{
    max-width:355px;
}

md-icon{
    font-size:50px;
}

.md-tooltip
{
    background:black;
    color:white;
}
</style>
