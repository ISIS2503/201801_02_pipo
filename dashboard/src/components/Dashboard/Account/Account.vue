<template>
<div class="account md-layout">
  <h2 class="name">
      {{name}}
  </h2>
  <md-menu md-direction="bottom-end" :md-offset-x="0.1" :md-offset-y="0.1">
    <md-button md-menu-trigger class="md-icon-button md-accent">
      <md-icon class="md-size-2x">account_circle</md-icon>
    </md-button>
    <md-menu-content>
      <md-menu-item href="http://172.24.42.64/logout">Cerrar sesión</md-menu-item>
    </md-menu-content>
  </md-menu>
</div>
</template>

<script>
export default {
  name: "Account",
  data: function() {
    return {
      name: "Toscana"
    };
  }
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

</style>
