<template>
  <div>
    <div>
    <h1>
      Torre {{'1'}} - Apartamento {{'XXX'}}
    </h1>
    <h2 class="error" v-if="error">{{parseError}}</h2>
    </div>
    <div>
      <h2>Propietario</h2>
      <p>{{detail.email}}</p>
      <p>{{detail.auth0_id}}</p>
      <!-- <p v-if="owner.email">{{owner.email}}</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'Detail',
  props: ['detail'],
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
