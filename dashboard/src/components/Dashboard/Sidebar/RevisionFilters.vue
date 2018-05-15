<template>
  <div class="md-layout">
      <div v-on:click="select('not-revised')" class="md-layout-item" :class="notRevised">
        <md-icon class="md-size-2x">warning</md-icon>
        <md-tooltip md-direction="bottom">Mostar alarmas por revisar</md-tooltip>
      </div>
      <div v-on:click="select('revised')" class="md-layout-item" :class="revised">
        <md-icon class="md-size-2x">check_box</md-icon>
        <md-tooltip md-direction="bottom">Mostrar alarmas revisadas</md-tooltip>
      </div>
      <div class="md-layout-item" v-on:click="select('show-all')" :class="showAll">
        <h3>Todas</h3>
        <md-tooltip md-direction="bottom">Mostrar todas las alarmas</md-tooltip>
      </div>
  </div>
</template>


<script>
export default {
  name: "RevisionFilters",
  data() {
    return {
      notRevisedSelected: false,
      revisedSelected: false,
      showAllSelected: true
    };
  },
  methods: {
    select(type) {
      if (type === "revised") {
        this.revisedSelected = true;
        this.notRevisedSelected = false;
        this.showAllSelected = false;
      } else if (type === "not-revised") {
        this.revisedSelected = false;
        this.notRevisedSelected = true;
        this.showAllSelected = false;
      } else {
        this.revisedSelected = false;
        this.notRevisedSelected = false;
        this.showAllSelected = true;
      }

      this.$emit("revision-select", type);
    }
  },
  computed: {
    notRevised() {
      if (this.notRevisedSelected) return "selected";
      else return "not-selected";
    },
    revised() {
      if (this.revisedSelected) return "selected";
      else return "not-selected";
    },
    showAll() {
      if (this.showAllSelected) return "selected";
      else return "not-selected";
    }
  }
};
</script>


<style lang="scss" scoped>
.md-layout {
  padding: 4px;
}

h3 {
  line-height: 50px;
  max-height: 6vh;
  margin: 0;
}

.md-layout-item{
  margin: 4px;
  box-shadow: 0px 0px 0px 0px #696969;
  background-color: rgba(200,200,200,0);
  transition: box-shadow 0.2s ease-in-out;
  transition: background-color 0.2s ease-in-out;
}

.md-layout-item:hover{
  box-shadow: 0px 0px 0px 2px #696969;
}

.md-tooltip {
  background: rgb(77, 77, 77);
  color: white;
}

.selected{
  background-color: rgba(200,200,200,0.9);
  box-shadow: 0px 0px 0px 3px #2c3e50;
}

</style>
