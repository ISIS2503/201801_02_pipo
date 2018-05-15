<template>
<div class="container">
    <b-container>
        <b-row>
            <b-col
                class="not-checked"
                v-on:click="select('revised')"
                v-bind:class="{ 'not-checked-selected': revisedSelected }"
            >
                <md-tooltip md-direction="bottom">Mostrar alarmas por revisar</md-tooltip>
                </b-col>
                <b-col
                    v-on:click="select('not-revised')"
                    class="checked"
                    v-bind:class="{ 'checked-selected': notRevisedSelected }"
                >
                    <md-tooltip md-direction="bottom">Mostrar alarmas revisadas</md-tooltip>
                    </b-col>
        </b-row>
    </b-container>
</div>
</template>
<script>
export default {
    name: "RevisionFilters",
    data() {
        return {
            notRevisedSelected: true,
            revisedSelected: true
        }
    },
    methods: {
        select(type) {
            if (type === 'revised') {
                this.revisedSelected = !this.revisedSelected
            } else if (type === 'not-revised') {
                this.notRevisedSelected = !this.notRevisedSelected
            }
            this.$emit('revision-select', type)
        }
    },
  computed: {
    notRevised() {
      if (this.notRevisedSelected) return "not-revised";
    },
    revised() {
      if (this.revisedSelected) return "revised";
    }
  }
};
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
     background: rgb(77, 77, 77);
}

.checked {  
    background:  url("../../../assets/checkedD.png") center;
    background-repeat: no-repeat;
    background-size: contain;
    margin: 0 auto;
    display: inline-block;
}

.checked-selected {
    background:url("../../../assets/checked.png") center;
    background-repeat: no-repeat;
    background-size: contain;
    margin: 0 auto;
    display: inline-block;
}

.not-checked {  
    background: url("../../../assets/porRevisarD.png") center;
    background-repeat: no-repeat;
    background-size: contain;
    margin: 0 auto;
    display: inline-block;
}

.not-checked-selected {  
      background: url("../../../assets/porRevisar.png") center;
      background-repeat: no-repeat;
    background-size: contain;
    margin: 0 auto;
    display: inline-block;
}

.container .col {
    height: 6vh;
    cursor: pointer;
}

.md-tooltip {
    background: rgb(77, 77, 77);
    color: white;
}
</style>
