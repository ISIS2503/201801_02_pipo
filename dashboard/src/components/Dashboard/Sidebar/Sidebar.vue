<template>
<div id="sidebar">
  <account/>
  <div id="revisionFilters">
    <revision-filters v-on:revision-select="selectRevision"/>
  </div>

  <alarm-list v-bind:alarms='alarms' v-bind:fliters='filters'/>

  <div id="typeFilters">
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
  border: 5px rgb(77, 77, 77) solid;
  position: relative;
}

#revisionFilters {
  /* position: relative;
  /* top: -0.4vh; 
  width: 100%; */
}

#typeFilters {
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>
