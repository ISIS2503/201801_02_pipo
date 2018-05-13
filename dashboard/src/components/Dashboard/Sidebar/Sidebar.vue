<template>
<div id="sidebar">
  <account></account>
  <div id="filters1">
 <filters1></filters1>
  </div>

  <div id="filters2">
 <filters2></filters2>
  </div>
</div>

</template>


<script>
import Account from '../Account/Account.vue'
import Alarm from './Alarm.vue'
import AlarmList from './AlarmList.vue'
import Detail from './Detail.vue'
import Filters1 from './Filters1.vue'
import Filters2 from './Filters2.vue'
export default {
    name: "Sidebar", 
    components: {
        Account,
        Alarm,
        AlarmList,
        Detail,
        Filters1,
        Filters2
    },
};
</script>


<style scoped>
#sidebar {

    height: 100vh;
    width: 100%;
    border: 5px rgb(254, 209, 0) solid;
}

#filters1{
  position:relative;
  top:0;
  width:100%;
}

#filters2{
  position:absolute;
  bottom:0;
  width:100%;
}
</style>
