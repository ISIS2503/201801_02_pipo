<template>
<div class="md-content md-scrollbar">
    <div class="above">
        <md-icon class="md-size-2x next cursor cursor-left">arrow_back_ios</md-icon>
        <h1 class="next tower-name">TORRE 1</h1>
        <md-icon class="md-size-2x next cursor">arrow_forward_ios</md-icon>
    </div>

    <div class="container">
        <div class="roof">
            <div class="middle-roof">
            </div>
            <div class="bottom-roof">
            </div>
        </div>
        <div v-for="(piso, index) in this.unidad.torres[0].pisos" :key="index">
            <div class="md-layout">
                <!-- <b-row> -->
                    <div class="floor-number md-layout-item md-size-5">{{piso.numero}}</div>

                        <div v-for="(apartamento, index) in piso.apartamentos" :key="index" v-on:click="reversedMessage" class="apto md-layout-item">
                            <div class="apartment-number" >
                                {{apartamento.numero}}
                            </div>
                            <div class="apartment-icon md-layout-item">
                                <div :id="index"  class="apartment-door">
                                    <div class="apartment-doorbell"/>
                                    <div class="apartment-lock"/>
                                </div>
                            </div>
                        </div>

                <!-- </b-row> -->
            </div>
        </div>
            <div class="middle-floor">
            </div>
            <div class="bottom-floor">
            </div>
    </div>


</div>
</template>

<script>
import "../../../styles/tower.css";
import "../../../styles/apartment-icon.css";
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
                  },
                  {
                    numero: 4
                  },
                  {
                    numero: 5
                  },
                  {
                    numero: 6
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
  },
  methods:{
    // a computed getter
    reversedMessage: function () {
      // `this` points to the vm instance
      console.log('llega');
      return 2;
    }
  }
};
</script>

<style scoped>
.above {
  margin-top: 10px;
}

.next {
  display: inline-block;
  vertical-align: middle;
}

.tower-name {
  font-weight: bold;
  font-size: 3rem;
}

.cursor{
  width:55px;
  height: 55px;
  background:  rgb(77, 77, 77);
  color:white;
  border-radius: 50%;
  line-height: 55px;
  text-align: center;
}


.cursor:hover {
  cursor: pointer;
}

.cursor-left{
  position:relative;
  padding-left: 11px;
}


.floor-container {
  position: relative;
  display: flex;
  width: 90%;
}

.roof {
  position: relative;
  z-index: 2;
  height: 70px;
}

.apartment-number {
  height: 50px;
  width: 100%;
  border: 1px rgb(77, 77, 77) solid;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  line-height: 50px;
  font-weight: bold;
  font-size: 2rem;
  position: relative;
}



.floor-number {
  vertical-align: middle;
  display: inline-block;
  line-height: 140px;
  padding: 0;
  overflow: hidden;
  box-shadow: 1px 0px 1px 1px black;
  font-weight: bold;
  font-size: 2rem;
  height: unset !important;
  border-radius: 15% 0 0 15%;
}

.col-1 {
  display: inline-block;
  height: 118px;
  position: relative;
  top: 1px;
}

.apto {
  display: inline-block;
  padding: 0;
  vertical-align: middle;
}

.cuerpo {
  position: relative;
  z-index: 1;
  width: 100%;
  top: -5px;
  height: 600px;
  background: rgb(132, 96, 75);
  border-top: rgb(77, 77, 77) 1px solid;
}

.container {
  text-align: center;
  width: 102%;
  position: relative;
  left: -10px;
}
</style>
