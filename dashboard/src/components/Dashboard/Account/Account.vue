<template>
<div class="account md-layout">
  <h2 class="name">
      {{urName}}
  </h2>
  <md-menu md-direction="bottom-end" :md-offset-x="0.1" :md-offset-y="0.1">
    <md-button md-menu-trigger class="md-icon-button md-accent">
      <md-icon class="md-size-2x">account_circle</md-icon>
    </md-button>
    <md-menu-content>
      <md-menu-item href="http://ec2-34-202-239-178.compute-1.amazonaws.com:8080d/logout">Cerrar sesión</md-menu-item>
    </md-menu-content>
  </md-menu>
</div>
</template>

<script>
export default {
  name: "Account",
  props: ['urName']
};
</script>



<style scoped>
.md-icon-button{
  color: white;
}

.account {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background-color: rgb(77, 77, 77);
  color: white;
}
.icon-container {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    background: white;
    float: right;
     content: none;
     overflow:hidden;
}

.dropdown-container::after {
  width:11px;
  height:11px;
  background:rgb(77, 77, 77);
  position:relative;
  z-index:100;
  content:'';
  right:73px;
  top:10px;
}

</style>
