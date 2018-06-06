<template>
<div class="dashboard">
    <div class="md-layout">
        <div class="md-layout-item md-size-80">
            <grids
              v-if="UR"
              v-on:select-detail="selectDetail(...arguments)"
              :ur="UR"
              :alarms="alarms"
              ref="grids"
            />
        </div>
        <div class="md-layout-item md-size-20 sidebar-container">
            <sidebar 
              :detail="detailSelected"
              :alarms="alarms"
              :ur-name="UR.name"
              class="sidebar"
              @scroll-to-alarm="scrollToAlarm(...arguments)"
              @alarm-deleted="deleteAlarm(...arguments)"
              @alarm-revised="alarmRevised(...arguments)"
              ref="sidebar"
            />
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
      alarms: [],
      //Contains tower info retrieved from REST services
      UR: { torres: [{ numero: "cargando" }] },
      detailSelected: null
    };
  },
  methods: {
    //Initializes SocketIO and declares event listener for alarms
    initWebsocket() {
      const serverIP = "http://ec2-34-202-239-178.compute-1.amazonaws.com:8079";

      const namespace = "/securityWebsocket";
      //Conectarse al servidor
      let socket = io.connect(serverIP /* + namespace */);

      socket.on("connect", () => {
        console.log("Eureka");
      });

      socket.on("disconnect", () => {
        console.log("RIP conn");
      });

      const _this = this;
      // Event handler for server receive data.
      socket.on(this.UR.name, msg => {
        //Convert to js object
        const alarm = JSON.parse(msg);
        console.log(alarm);

        let normalizedAlarm = {};
        //'desanidar' atributos

        if (alarm.emergency) {
          for (var attribute of Object.keys(alarm.emergency))
            normalizedAlarm[attribute] = alarm.emergency[attribute];
          normalizedAlarm.type = "emergency";
        } else if (alarm.failure) {
          for (var attribute of Object.keys(alarm.failure))
            normalizedAlarm[attribute] = alarm.failure[attribute];
          normalizedAlarm.type = "failure";
        } else {
          console.log("Alarma inválida!");
          if (alarm.fallo) console.log("Este man tiene fallo!");
          normalizedAlarm.type = "unknown";
        }
        normalizedAlarm.sensetime = alarm.sensetime;
        normalizedAlarm.timestamp = new Date().getTime();
        normalizedAlarm.revised = false;

        let dir = normalizedAlarm.apartamento.split("-");

        if (normalizedAlarm.emergencia)
          normalizedAlarm.normalType = "e-" + normalizedAlarm.emergencia;
        else if (normalizedAlarm.fallo)
          normalizedAlarm.normalType = "f-" + normalizedAlarm.fallo;
        else normalizedAlarm.normalType = "unknown";

        _this.alarms.push(normalizedAlarm);
        _this.UR.torres[dir[0]-1].pisos[_this.UR.torres[dir[0]-1].pisos.length-dir[1]].apartamentos[dir[2]-1].alarmas.push(
          normalizedAlarm
        );
         
       _this.$refs.grids.pushAlarm(dir,normalizedAlarm);
      }
      );
      console.log(this.UR);
    },
    //Retireves information from server and parses it to fit front-end structure
    initData() {
      const user = this.$route.params.username;

      axios
        .get("http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/users/" + user)
        .then(userResponse => {
          //Make another HTTP request, depending on the UR assigned to the user
          //Only works with users with scope, YALE users won't work (tests: user6@yale.com)
          axios
            .get(
              "http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/unidadesResidenciales/" +
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
                  owner: property.owner_user_id,
                  alarmas: []
                };
                if (currentTowerNumber === parseInt(params[0])) {
                  if (currentFloorNumber === parseInt(params[1])) {
                    /* console.log(currentTowerNumber);
                    console.log(parsed_UR); */
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
              }
              console.log(parsed_UR);
              this.UR = parsed_UR;

              //Websocket initialization requires UR to be initialized
              this.initWebsocket();
            })
            .catch(error => {
              console.log(error);
            });
        })
        .catch(error => {
          console.log(error);
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
    },
    selectDetail(localID, auth0_owner, selectedAlarm) {
      console.log('elDetail');
      const _this = this;
      axios
        .get(
          "http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/users/checkAuth0/" +
            this.UR.name +
            "/" +
            auth0_owner
        )
        .then(response => {
          _this.detailSelected = {};
          _this.detailSelected.user = response.data;
          _this.detailSelected.localID = localID;
          _this.detailSelected.alarm = selectedAlarm; //May be undefined

          this.$refs.sidebar.openDetail();
        })
        .catch(error => {
          console.log(
          "http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/users/checkAuth0/" +
            this.UR.name +
            "/" +
            auth0_owner
        );
        console.log( "/" + this.UR.name + "/" + auth0_owner  );
          console.log(error);

          /* tempora defualt...-------------- */
          _this.detailSelected = {
            user: {
              auth0_id: "auth0|5adcd6a941aacd1daa8999d1",
              username: "s.guzmanm",
              email: "checho@uniflayes.edu.ko",
              group: "PROPERTY_OWNER",
              scope: "Tosacana/2-4-5",
              horariosPermitidos: [],
              edad: "24",
              nombre: "Sergio Guzmán",
              telefono: "312641236"
            },
            localID: "2-4-5",
            alarm: {
              sensetime: 1526576385325,
              id: "Arduino 007",
              emergencia: "3",
              apartamento: "2-5-3",
              conjunto: "Toscana",
              zona: "Centro",
              revised: false
            }
          };
          this.$refs.sidebar.openDetail();
          /*-------- temodral default --------*/
        });
    },
    scrollToAlarm(alarm) {
      this.$refs.grids.scrollToAlarm(alarm);
    },
    alarmRevised(alarm)
    {
      let dir = alarm.apartamento.split("-"); 
      let alarmas=  this.UR.torres[dir[0]-1].pisos[this.UR.torres[dir[0]-1].pisos.length-dir[1]].apartamentos[dir[2]-1].alarmas;
      for (let i = 0; i < alarmas.length; i++) {
        if(alarmas[i].sensetime===alarm.sensetime)
        {
          alarmas.splice(i, 1);
          break;
        }
      }
      alarmas=  this.alarms;
      for (let i = 0; i < alarmas.length; i++) {
        if(alarmas[i].sensetime===alarm.sensetime)
        {
          alarmas[i].revised = true;
          break;
        }
      }
    },
    deleteAlarm(alarm)
    {
      let alarmas=  this.alarms;
      for (let i = 0; i < alarmas.length; i++) {
        if(alarmas[i].sensetime===alarm.sensetime)
        {
          alarmas.splice(i, 1);
          break;
        }
      }
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
