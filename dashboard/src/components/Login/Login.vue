<template>
  <div class="md-layout">
    <div class="md-layout-item md-size-100">
      <div class="md-elevation-8 login-window">
        <h1>ISIS 2503 - πpo Yale security dashboard</h1>
        <md-button class="md-raised" href='http://172.24.42.64/dashboardLogin'>
          <md-icon>check_circle</md-icon>
          Iniciar sesión
        </md-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  methods: {
    login(){

    }
  }
};
</script>

<style scoped>
.md-layout {
  background: linear-gradient(45deg, #fb872b, #d9e021);
  position: absolute;
  height: 100%;
  width: 100%;
}

.login-window{
  position: absolute;
  top:25%;
  left: 25%;
  width: 50%;
  background: linear-gradient(45deg, whitesmoke, beige);
  padding: 8%;
  border: lightgrey 2px solid;
}

</style>
