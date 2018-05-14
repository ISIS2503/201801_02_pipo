<template>
<div class="account">
    <h2 class="name">
        {{name}}
    </h2>
    <b-dropdown variant="link" class="dropdown-container">
        <template slot="text">
            <div class="icon-container">
                 <md-icon class="md-size-2x md-light icon">person</md-icon>
            </div>
        </template>
        <b-dropdown-item href="http://172.24.42.64/logout">Cerrar sesión</b-dropdown-item>
    </b-dropdown>
</div>
</template>

<script>
export default {
    name: "Account",
    data: function () {
        return {
            name: "Toscana"
        };
    }
};
</script>



<style scoped>
/* ddown1__BV_toggle_ 
btn btn-secondary dropdown-toggle*/

.account {
    padding-top: 5px;
    height: 7vh;
    background-color: rgb(77, 77, 77);
}

.name {
    float: left;
    color: white;
     line-height: 50px;
}

.dropdown-container{
border-top:none;
float:right;
bottom:5px;
}

.icon-container {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    background: white;
    float: right;
    border: 1px yellow solid;
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

.icon {
    position: relative;
    top: 2px;
    width: 35px;
    height: 35px;
    color: rgb(77, 77, 77);
}
</style>
