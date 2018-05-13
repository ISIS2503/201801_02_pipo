<template>
<div>
   
 <h1>Torre 1</h1>
    <div class="roof">

        <div class="middle-roof">
        </div>
        <div class="bottom-roof">
        </div>
    </div>
    <div class="container">
    <div  v-for="(piso, index) in this.unidad.torres[0].pisos" :key="index" >
        <b-container>
            <b-row>
                <b-col v-for="(apartamento, index) in piso.apartamentos" :key="index" class="apto">
                  <div class="apartment-number">
                  {{apartamento.numero}}
                  </div>
                   <div class="apartment-icon">
                  </div>
                 </b-col>
             </b-row>
         </b-container>
     </div>
     </div>
     <div class="middle-floor">
        </div>
        <div class="bottom-floor">
        </div>

</div>
</template>

<script>
import "./tower.css";

export default {
  name: "MapGrid",
  data: function() {
    return {
      unidad: {
        nombre: "toscana",
        torres: [
          {
            numero: 1,
            pisos: [
              {
                numero: 1,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  }
                ]
              },
              {
                numero: 2,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  },
                  {
                    numero: 4
                  }
                ]
              },
              {
                numero: 3,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  }
                ]
              },
              {
                numero: 4,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  },
                  {
                    numero: 4
                  }
                ]
              },
              {
                numero: 5,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  }
                ]
              },
              {
                numero: 6,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  },
                  {
                    numero: 3
                  },
                  {
                    numero: 4
                  }
                ]
              },
              {
                numero: 7,
                apartamentos: [
                  {
                    numero: 1
                  },
                  {
                    numero: 2
                  }
                ]
              }
            ]
          }
        ]
      }
    };
  }
};
</script>










<style scoped>
.roof {
  position: relative;
  z-index: 2;
}

.apartment-number {
  height: 20px;
  width: 100%;
  border: 1px black solid;
}

.apartment-icon {
  height: 100px;
  width: 100%;
  background: red;
  border: 1px black solid;
}

.apto {
  padding: 0;
}

.cuerpo {
  position: relative;
  z-index: 1;
  width: 100%;
  top: -5px;
  height: 600px;
  background: rgb(132, 96, 75);
  border-top: black 1px solid;
}

.container{
    text-align: center;
}
</style>
