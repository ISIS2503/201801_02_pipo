<template>
<div>
   <md-card>
        <div class="name-container">
            <p class="name">PISOS</p>
        </div>
    <div class="contenedor">
        <md-button v-on="selectPiso(piso)" v-for="(piso, index) in floorResume()" class="md-raised" :key="index">{{piso}}</md-button>
    </div>
    </md-card>
</div>
</template>


<script>
export default {
  name: 'FloorGrid',
   props: ["ur", "towerIndex"],
   computed: {
       floorResume(){
           let resp= []
           let floorNumber= this.ur.torres[towerIndex].pisos.length;
           let div= parseInt(floorNumber/6);
           for (let i = 0; i< floorNumber; i+=(div+1)) {
               resp.unshift(this.ur.torres[towerIndex].pisos[i].numero);           
           }
           return resp;
       }
   },
   methods:{
       selectPiso(number){

       }
   }
}
</script>

<style scoped>
.name-container {
    font-weight: bold;
    font-size: 1.5rem;
    padding: 1rem 0;
    margin: none;
    background: rgb(77, 77, 77);
    color: white;
}

.name {
    margin: 0 0;
}

.md-card {
    display: inline-block;
    overflow: auto;
    border: 3px rgb(77, 77, 77) solid;
}
.contenedor{
  display: inline-block;
}

.md-button {
    display: block;
    margin: 0;   
    border-bottom: 3px rgb(77, 77, 77) solid;
}

.md-button:last-child {
    border-bottom: none;
}
</style>