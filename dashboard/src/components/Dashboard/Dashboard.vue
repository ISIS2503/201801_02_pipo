<template>
<div class="dashboard">
    <div class="md-layout">
        <div class="md-layout-item md-size-75">
            <grids :ur="UR"/>
        </div>
        <div class="md-layout-item md-size-25 sidebar-container">
            <sidebar :emergencies="emergencies" :ur-name="UR.name" class="sidebar"/>
        </div>
    </div>
</div>
</template>



<script>
import axios from "axios";
import io from "socket.io-client";
import Grids from "./Grids/Grids.vue";
import Sidebar from "./Sidebar/Sidebar.vue";
export default {
  name: "dashboard",
  components: {
    Grids,
    Sidebar
  },
  data() {
    return {
      websocketConnected: false,
      //Contains incoming alarms & failures
      emergencies: [],
      //Contains tower info retrieved from REST services
      UR: {}
    };
  },
  methods: {
    //Initializes SocketIO and declares event listener for emergencies
    initWebsocket() {
      const serverIP = "http://172.24.42.33:8070";

      const namespace = "/securityWebsocket";
      //Conectarse al servidor
      let socket = io.connect(serverIP /* + namespace */);

      socket.on("connect", () => {
        console.log("Eureka");
      });

      const _this = this;
      // Event handler for server receive data.
      socket.on(this.UR.name, msg => {
        /* if (_this.websocketConnected) */ {
          console.log(msg);
          //Convert to js object
          const emergency = JSON.parse(msg);
          console.log(emergency);
          _this.emergencies.push(emergency);
        } /* else {
          if (msg == "Connected") _this.websocketConnected = true;
          else
            console.log(
              "El Websocket aún no ha sido inicializado, se esperaba 'Connected' se recibió: ",
              msg
            );
        } */
      });
    },
    //Retireves information from server and parses it to fit front-end structure
    initData() {
      const user = this.$route.params.username;

      axios
        .get("http://172.24.42.64/users/" + user)
        .then(userResponse => {
          //Make another HTTP request, depending on the UR assigned to the user
          //Only works with users with scope, YALE users won't work (tests: user6@yale.com)
          axios
            .get(
              "http://172.24.42.64/unidadesResidenciales/" +
                userResponse.data.scope +
                "/inmuebles"
            )
            .then(URResponse => {
              console.log(URResponse.data);
              let UR_temp = URResponse.data;
              let parsed_UR = {};
              parsed_UR.name = userResponse.data.scope;
              parsed_UR.torres = [];

              let UR_sorted = this.sortArray(UR_temp);
              let towerCounter = -1;
              let floorCounter = -1;
              let currentFloorNumber = -1;
              let currentTowerNumber = -1;
              for (var property of UR_sorted) {
                let params = property.localID.split("-");
                //info[0] = torre // [1] = piso // [2] = número
                //info = property.localID.split('-')
                // addPropertyTo(property, parsed_UR); Propiedad utilizable si lo de ordenar no funciona
                let currentProperty = {
                  numero: parseInt(params[2]),
                  owner: property.owner_user_id
                };
                console.log(
                  "t" + currentTowerNumber + " " + parseInt(params[0]) - 1
                );
                console.log(
                  "f" + currentFloorNumber + " " + parseInt(params[1])
                );
                if (currentTowerNumber === parseInt(params[0])) {
                  if (currentFloorNumber === parseInt(params[1])) {
                    console.log(currentTowerNumber);
                    console.log(parsed_UR);
                    parsed_UR.torres[towerCounter].pisos[
                      floorCounter
                    ].apartamentos.push(currentProperty);
                  } else {
                    let currentFloor = {
                      numero: parseInt(params[1]),
                      apartamentos: [currentProperty]
                    };
                    parsed_UR.torres[towerCounter].pisos.push(currentFloor);
                    currentFloorNumber = parseInt(params[1]);
                    floorCounter = floorCounter + 1;
                  }
                } else {
                  let currentFloor = {
                    numero: parseInt(params[1]),
                    apartamentos: [currentProperty]
                  };
                  let currentTower = {
                    numero: parseInt(params[0]),
                    pisos: [currentFloor]
                  };
                  parsed_UR.torres.push(currentTower);
                  towerCounter = towerCounter + 1;
                  floorCounter = 0;
                  currentFloorNumber = parseInt(params[1]);
                  currentTowerNumber = parseInt(params[0]);
                }
                /* if(propertyTowerNotInUR(property, parsed_UR)){
            parsed_UR.push({
              "number" : info[0],
              "floors": []
            })
          }

          if(floorNotInTower(property, parsed_UR)){

          }*/
              }
              console.log(parsed_UR);
              this.UR = parsed_UR;

              //Websocket initialization needs UR to be initialized
              this.initWebsocket();

            })
            .catch(error => {
              console.log(error);
            });
        })
        .catch(error => {
          console.log(error);
        });

      console.log(UR_temp);
    },
    propertyTowerNotInUR(property, parsed_UR) {
      let isInUR = false;
      const towerNumber = property.localID.split("-")[0];
      for (tower of parsed_UR.towers) {
        if (parsed_UR[tower].number === towerNumber) {
          isInUR = true;
          break;
        }
      }
      return isInUR;
    },
    addPropertyTo(property, parsed_UR) {
      towerIndex = -1;
      const towerNumber = property.localID.split("-")[0];
      for (i = 0; i < parsed_UR.torres.length; i++) {
        if (parsed_UR.torres[i].number === towerNumber) {
          towerIndex = i;
          break;
        }
      }
      if (towerIndex === -1) {
        parsed_UR.torres.push({ numero: towerNumber, pisos: [] });
        towerIndex = parsed_UR.torres.length - 1;
      }
      addFloorTo(towerIndex, property, parsed_UR);
    },
    addFloorTo(towerIndex, property, parsed_UR) {
      floorIndex = -1;
      const floorNumber = property.localID.split("-")[1];
      for (i = 0; i < parsed_UR.torres[towerIndex].pisos.length; i++) {
        if (parsed_UR.torres[towerIndex].pisos[i].number === floorNumber) {
          floorIndex = i;
          break;
        }
      }
      if (floorIndex === -1) {
        parsed_UR.torres[towerIndex].pisos.push({
          numero: floorNumber,
          apartamentos: []
        });
        floorIndex = parsed_UR.torres[towerIndex].pisos.length - 1;
      }
      addPropertyTo(towerIndex, floorIndex, property, parsed_UR);
    },
    addPropertyTo(towerIndex, floorIndex, property, parsed_UR) {
      floorIndex = -1;
      const floorNumber = property.localID.split("-")[1];
      parsed_UR.torres[towerIndex].pisos[floorIndex].push({
        numero: property.localID.split("-")[2],
        owner: owner_user_id
      });
    },
    sortArray(UR_temp) {
      UR_temp.sort(function(a, b) {
        let paramsa = a.localID.split("-");
        let paramsb = b.localID.split("-");
        if (parseInt(paramsa[0]) - parseInt(paramsb[0]) === 0) {
          if (parseInt(paramsa[1]) - parseInt(paramsb[1]) === 0) {
            return paramsa[2] - paramsb[2];
          }
          return -parseInt(paramsa[1]) + parseInt(paramsb[1]);
        }
        return -parseInt(paramsb[0]) + parseInt(paramsa[0]);
      });
      return UR_temp;
    }
  },
  mounted() {
    this.initData();
  }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.sidebar-container {
  position: fixed;
  right: 15px;
}
</style>
