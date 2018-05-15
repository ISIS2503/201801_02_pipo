<template>
<div class="dashboard">
    <div class="md-layout">
        <div class="md-layout-item md-size-75">
            <grids/>
        </div>
        <div class="md-layout-item md-size-25 sidebar-container">
            <sidebar class="sidebar"/>
        </div>
    </div>
</div>
</template>



<script>
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
      emergencies: []
    };
  },
  methods: {
    //Initializes SocketIO and declares event listener for emergencies
    initWebsocket() {
      const serverIP = "http://172.24.42.64";
      const namespace = "/securityWebsocket";
      //Conectarse al servidor
      let socket = io.connect(serverIP + namespace);

      const _this = this;
      // Event handler for server receive data.
      socket.on("emergency", msg => {
        if (_this.websocketConnected) {
          //Convert to js object
          const emergency = JSON.parse(msg);
          console.log(emergency);
          _this.emergencies.push(data);
        } else {
          if (msg == "Connected") _this.websocketConnected = true;
          else
            console.log(
              "El Websocket aún no ha sido inicializado, se esperaba 'Connected' se recibió: ",
              msg
            );
        }
      });
    },
    //Retireves information from server and parses it to fit front-end structure
    initData(){

    }
  },
  mounted() {
    this.initWebsocket()
    this.initData()
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
