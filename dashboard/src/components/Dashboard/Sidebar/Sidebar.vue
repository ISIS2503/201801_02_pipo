<template>
<div id="sidebar">
  <account :ur-name="urName"/>
  <div id="revisionFilters">
    <revision-filters v-on:revision-select="selectRevision"/>
  </div>

  <alarm-list @scroll-to-alarm="scrollToAlarm(...arguments)" v-bind:alarms='alarms' v-bind:filters='filters'/>

  <div id="typeFilters">
    <type-filters v-on:type-select="selectType"/>
  </div>

  <div id="detail" v-if="defaultDetail && !closed">
    <detail @close="close" :detail="defaultDetail"/>
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
import index from "vue";
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
  props: ["alarms", "urName", "detail"],
  data() {
    return {
      filters: {
        revised: false,
        notRevised: false,
        emergencies: [],
        failures: []
      },
      closed: false,
      
      /* tempora defualt...-------------- */

        defaultDetail: {
          user: {
            auth0_id: "auth0|5adcd6a941aacd1daa8999d1",
            username: "s.guzmanm",
            email: "checho@uniflayes.edu.ko",
            group: "PROPERTY_OWNER",
            scope: "Tosacana/2-4-5",
            horariosPermitidos : [],
            edad: "24",
            nombre: "Sergio Guzmán",
            telefono: "312641236"
          },
          localID: "2-4-5",
          alarm: {
            sensetime: 1526576385325,
            id: "Arduino 007",
            emergencia: "3",
            apartamento: "2-5-3",
            conjunto: "Toscana",
            zona: "Centro"
          }
        }

      /*-------- temodral default --------*/ 
    };
  },
  methods: {
    selectType(selection) {
      console.log("selectType: ", selection);
      const index = parseInt(selection.split("-")[1]);
      if (selection[0] === "e") {
        if (this.filters.emergencies.includes(index)) {
          const deleteIndex = this.filters.emergencies.indexOf(index);
          this.filters.emergencies.splice(deleteIndex, 1);
        } else {
          this.filters.emergencies.push(index);
        }
      } else if (selection[0] === "f") {
        if (this.filters.failures.includes(index)) {
          const deleteIndex = this.filters.failures.indexOf(index);
          this.filters.failures.splice(deleteIndex, 1);
        } else {
          this.filters.failures.push(index);
        }
      }
    },
    selectRevision(selection) {
      console.log("selectRevision: ", selection);
      this.filters[selection] = !this.filters[selection];
      console.log(this.filters);
    },
    scrollToAlarm(alarm) {
      //Pass event
      this.closed = false;
      this.$emit("scroll-to-alarm", alarm);
    },
    close(){
      this.closed = true;
    }
  }
};
</script>


<style scoped>
#sidebar {
  height: 100vh;
  width: calc(100% - 5px);
  border: 5px rgb(77, 77, 77) solid;
  position: relative;
}

#typeFilters {
  position: absolute;
  bottom: 0;
  width: 100%;
}

#detail{
  position: fixed;
  right:calc(25% + 20px);
  bottom:0;
}
</style>
