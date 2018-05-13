<template>
  <div class="dashboard">
   <b-card no-block>
    <b-tabs>
      <b-tab title="Tab 1">
        Tab 1 Contents
      </b-tab>
      <b-tab title="Tab 2">
        Tab 2 Contents <b-button size="md">Boop</b-button>
      </b-tab>
      <b-tab title="Tab 3" disabled>
        Tab 3 Contents
      </b-tab>
    </b-tabs>
  </b-card>
  </div>
</template>

<script>
export default {
  name: "dashboard",
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>