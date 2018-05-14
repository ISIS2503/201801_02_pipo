<template>
<div class="container">
    <b-container>
        <b-row>
            <b-col>
                <md-tooltip md-direction="bottom">Por revisar</md-tooltip>
                <md-icon class="md-size-2x">warning</md-icon>
            </b-col>
            <b-col>
                <md-tooltip md-direction="bottom">Vistas</md-tooltip>
                <md-icon class="md-size-2x">check_box</md-icon>
            </b-col>
            <b-col>
                <md-tooltip md-direction="bottom">Todas</md-tooltip>
                <h3>Todas</h3>
            </b-col>
        </b-row>
    </b-container>
</div>
</template>


<script>
export default {
    name: 'Filters1'
}
</script>


<style lang="scss" scoped>
.container {
    width: 100%;
    padding: 0;
}

.row {
    width: 100%;
    margin: 0;
    position: relative;

}

.container .col {
    height: 6vh;
    border: 1px rgb(254, 209, 0) solid;
}

.container .col:hover {
    height: 6vh;
    background: rgb(77, 77, 77);
    color: white;
    border:1px rgb(254, 209, 0) solid;
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
