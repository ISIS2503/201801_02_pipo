<template>
<div id="sidebar">
  <account/>
  <div id="filters1">
    <revision-filters v-on:revision-select="selectRevision"/>
  </div>

  <alarm-list v-bind:alarms='alarms' v-bind:fliters='filters'/>

  <div id="filters2">
    <type-filters v-on:typeSelect="selectType"/>
  </div>
</div>
</template>


<script>
import Account from "../Account/Account.vue";
import Alarm from "./Alarm.vue";
import AlarmList from "./AlarmList.vue";
import Detail from "./Detail.vue";
import RevisionFilters from "./RevisionFilters.vue";
import TypeFilters from "./TypeFilters.vue";
export default {
  name: "Sidebar",
  components: {
    Account,
    Alarm,
    AlarmList,
    Detail,
    RevisionFilters,
    TypeFilters
  },
  props: ['alarms'],
  data(){
    return {
      filters: []
    }
  },
  methods:{
    selectType(event){
      console.log('selectType: ', event)
    },
    selectRevision(event){
      console.log('selectRevision: ', event)
      const filter = {
        
      }
    }
  }
};
</script>


<style scoped>
#sidebar {
  height: 100vh;
  width: calc(100% - 17px);
  border: 5px rgb(121, 14, 42) solid;
  position: relative;
}

#filters1 {
  position: relative;
  top: -0.4vh;
  width: 100%;
}

#filters2 {
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>
