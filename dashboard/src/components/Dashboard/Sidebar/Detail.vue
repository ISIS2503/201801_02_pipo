<template>
  <div>
    <div>
    <h1>
      Torre {{tower}} - Apartamento {{apartment}}
    </h1>
    <h2 class="error" v-if="error">{{parseError}}</h2>
    </div>
    <div>
      <h2>Propietario</h2>
      <p>{{owner.nombre}}</p>
      <p>{{owner.phone}}</p>
      <p v-if="owner.email">{{owner.email}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Detail',
  props: ['tower', 'apartment', 'error'],
  data(){
    return{
      owner: null
    }
  },
  mounted(){
    //retrieve owner data
  },
  computed:{
    parseError(){
      return error
    }
  }
}
</script>

<style scoped>

</style>
