webpackJsonp([1],{0:function(e,t){},"1/oy":function(e,t){},"3n4O":function(e,t){},"4+hh":function(e,t){},"57Do":function(e,t){},"9M+g":function(e,t){},CPS6:function(e,t){},Cu3Z:function(e,t){},DqYx:function(e,t){},Id91:function(e,t){},JlB8:function(e,t){},Jmt5:function(e,t){},NHnr:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=a("7+uW"),r=a("e6fC"),n=a("Lgyv"),o=a.n(n),c=(a("Jmt5"),a("9M+g"),a("4+hh"),{render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},staticRenderFns:[]});var l=a("VU/8")({name:"App"},c,!1,function(e){a("rLam")},null,null).exports,d=a("/ocq"),u=a("bOdI"),m=a.n(u),v=a("fZjL"),p=a.n(v),f=a("BO1k"),h=a.n(f),_=a("mtWM"),b=a.n(_),C=a("DmT9"),y=a.n(C),g={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",[t("md-card",[t("div",{staticClass:"name-container"},[t("p",{staticClass:"name"},[this._v("TORRE")])]),this._v(" "),t("div",{staticClass:"contenedor"},[t("md-button",{staticClass:"md-raised"},[this._v("1")]),this._v(" "),t("md-button",{staticClass:"md-raised"},[this._v("2")]),this._v(" "),t("md-button",{staticClass:"md-raised"},[this._v("3")])],1)])],1)},staticRenderFns:[]};var S=a("VU/8")({name:"TowerGrid"},g,!1,function(e){a("cSx0")},"data-v-4fc8c512",null).exports,I={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",[t("md-card",[t("div",{staticClass:"name-container"},[t("p",{staticClass:"name"},[this._v("PISOS")])]),this._v(" "),t("div",{staticClass:"contenedor"},[t("md-button",{staticClass:"md-raised"},[this._v("1")]),this._v(" "),t("md-button",{staticClass:"md-raised"},[this._v("2")]),this._v(" "),t("md-button",{staticClass:"md-raised"},[this._v("3")])],1)])],1)},staticRenderFns:[]};var x=a("VU/8")({name:"FloorGrid"},I,!1,function(e){a("isX2")},"data-v-5d2d9f3e",null).exports,R=(a("Cu3Z"),a("xV3Z"),{render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"md-content md-scrollbar"},[a("div",{staticClass:"above"},[a("md-icon",{staticClass:"md-size-2x next cursor cursor-left"},[e._v("arrow_back_ios")]),e._v(" "),a("h1",{staticClass:"next tower-name"},[e._v("TORRE 1")]),e._v(" "),a("md-icon",{staticClass:"md-size-2x next cursor"},[e._v("arrow_forward_ios")])],1),e._v(" "),a("div",{staticClass:"container"},[e._m(0),e._v(" "),e._l(e.ur.torres[0].pisos,function(t,s){return a("div",{key:s},[a("div",{staticClass:"md-layout"},[a("div",{staticClass:"floor-number md-layout-item md-size-5"},[e._v(e._s(t.numero))]),e._v(" "),e._l(t.apartamentos,function(t,s){return a("div",{key:s,staticClass:"apto md-layout-item",on:{click:function(a){e.selectProperty(t.owner)}}},[a("div",{staticClass:"apartment-number"},[e._v("\r\n                                "+e._s(t.numero)+"\r\n                            ")]),e._v(" "),a("div",{staticClass:"apartment-icon md-layout-item"},[a("div",{staticClass:"apartment-door",attrs:{id:s}},[a("div",{staticClass:"apartment-doorbell"}),e._v(" "),a("div",{staticClass:"apartment-lock"})])])])})],2)])}),e._v(" "),a("div",{staticClass:"middle-floor"}),e._v(" "),a("div",{staticClass:"bottom-floor"})],2)])},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"roof"},[t("div",{staticClass:"middle-roof"}),this._v(" "),t("div",{staticClass:"bottom-roof"})])}]});var D={name:"Grids",components:{TowerGrid:S,FloorGrid:x,MapGrid:a("VU/8")({name:"MapGrid",props:["ur"],data:function(){return{unidad:{nombre:"toscana",torres:[{numero:1,pisos:[{numero:1,apartamentos:[{numero:1},{numero:2},{numero:3}]},{numero:2,apartamentos:[{numero:1},{numero:2},{numero:3},{numero:4}]},{numero:3,apartamentos:[{numero:1},{numero:2},{numero:3},{numero:4},{numero:5},{numero:6}]},{numero:4,apartamentos:[{numero:1},{numero:2},{numero:3},{numero:4}]},{numero:5,apartamentos:[{numero:1},{numero:2},{numero:3}]},{numero:6,apartamentos:[{numero:1},{numero:2},{numero:3},{numero:4}]},{numero:7,apartamentos:[{numero:1},{numero:2}]}]}]}}},methods:{selectProperty:function(e){this.$emit("select-detail",e)}},mounted:function(){this.torres=this.ur}},R,!1,function(e){a("mfW3")},"data-v-3cc3895e",null).exports},props:["ur","alarms"]},w={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"principal"},[a("div",{staticClass:"md-layout"},[a("div",{staticClass:"md-layout-item md-size-15"},[a("div",{staticClass:"lateral"},[a("div",{staticClass:"logo"}),e._v(" "),a("div",{staticClass:"md-layout-item md-size-100"},[a("tower-Grid",{staticClass:"towers select"})],1),e._v(" "),a("div",{staticClass:"md-layout-item md-size-100"},[a("floor-grid",{staticClass:"floors select"})],1)])]),e._v(" "),a("div",{staticClass:"md-layout-item"},[a("map-grid",{attrs:{ur:e.ur},on:{"select-detail":function(t){e.$emit("select-detail",t)}}})],1)])])},staticRenderFns:[]};var k=a("VU/8")(D,w,!1,function(e){a("UvZ7")},"data-v-21611d01",null).exports,A={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"account md-layout"},[t("h2",{staticClass:"name"},[this._v("\r\n      "+this._s(this.urName)+"\r\n  ")]),this._v(" "),t("md-menu",{attrs:{"md-direction":"bottom-end","md-offset-x":.1,"md-offset-y":.1}},[t("md-button",{staticClass:"md-icon-button md-accent",attrs:{"md-menu-trigger":""}},[t("md-icon",{staticClass:"md-size-2x"},[this._v("account_circle")])],1),this._v(" "),t("md-menu-content",[t("md-menu-item",{attrs:{href:"http://172.24.42.64/logout"}},[this._v("Cerrar sesión")])],1)],1)],1)},staticRenderFns:[]};var F=a("VU/8")({name:"Account",props:["urName"]},A,!1,function(e){a("tl9A")},"data-v-5c8f010d",null).exports,E=[null,"Puerta abierta","Apertura sospechosa","Apertura no permitida","Batería baja"],U={name:"Alarm",props:["alarm"],data:function(){return{}},computed:{tower:function(){return this.alarm.apartamento[0]},apartament:function(){return this.alarm.apartamento[2]+"0"+this.alarm.apartamento[4]},alarmMessage:function(){return"emergency"===this.alarm.type?E[parseInt(this.alarm.emergencia)]:"failure"===this.alarm.type?E[parseInt(this.alarm.failure)]:(console.log(this.alarm),"Emergencia desconocida")},timeMessage:function(){return new Date(this.alarm.sensetime)}}},P={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"container md-layout"},[a("div",{staticClass:"md-layout-item md-size-15"},[a("md-icon",{staticClass:"md-size-2x"},[e._v("lock_open")])],1),e._v(" "),a("div",{staticClass:"md-layout-item md-size-85"},[a("h2",[e._v("Torre "+e._s(e.tower))]),e._v(" "),a("h3",[e._v("Apto "+e._s(e.apartment))]),e._v(" "),a("p",[e._v(e._s(e.alarmMessage))])]),e._v(" "),a("p",{staticClass:"time"},[e._v(e._s(e.timeMessage))])])},staticRenderFns:[]};var $=a("VU/8")(U,P,!1,function(e){a("tEZc")},"data-v-0cf3c0ca",null).exports,T={name:"AlarmList",components:{Alarm:$},props:["alarms","filters"],data:function(){return{revisedAlarms:[]}},computed:{filteredAlarms:function(){var e=this;return this.alarms.filter(function(t){return!e.filters.revised||!t.revised}).filter(function(t){return!e.filters.notRevised||t.revised}).filter(function(t){return"emergency"===t.type?!e.filters.emergencies.includes(parseInt(t.emergencia)):"failure"!==t.type||!e.filters.faliures.includes(parseInt(t.falla))})}}},V={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"md-scrollbar"},this._l(this.alarms,function(e,a){return t("div",{key:a},[t("alarm",{attrs:{alarm:e}})],1)}))},staticRenderFns:[]};var j={name:"Detail",props:["detail"],data:function(){return{owner:null}},mounted:function(){},computed:{parseError:function(){return error}}},z={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",[a("h1",[e._v("\n    Torre "+e._s("1")+" - Apartamento "+e._s("XXX")+"\n  ")]),e._v(" "),e.error?a("h2",{staticClass:"error"},[e._v(e._s(e.parseError))]):e._e()]),e._v(" "),a("div",[a("h2",[e._v("Propietario")]),e._v(" "),a("p",[e._v(e._s(e.detail.email))]),e._v(" "),a("p",[e._v(e._s(e.detail.auth0_id))])])])},staticRenderFns:[]};var N={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"container"},[a("b-container",[a("b-row",[a("b-col",{staticClass:"not-checked",class:{"not-checked-selected":e.notRevisedSelected},on:{click:function(t){e.select("notRevised")}}},[a("md-tooltip",{attrs:{"md-direction":"bottom"}},[e._v("Mostrar alarmas por revisar")])],1),e._v(" "),a("b-col",{staticClass:"checked",class:{"checked-selected":e.revisedSelected},on:{click:function(t){e.select("revised")}}},[a("md-tooltip",{attrs:{"md-direction":"bottom"}},[e._v("Mostrar alarmas revisadas")])],1)],1)],1)],1)},staticRenderFns:[]};var M={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"container"},[a("b-container",[a("b-row",[a("b-col",{staticClass:"puerta-abierta",class:{"puerta-abierta-selected":e.puertaAbiertaSelected},on:{click:function(t){e.select("puertaAbierta")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Puerta abierta")])],1),e._v(" "),a("b-col",{staticClass:"apertura-sospechosa",class:{"apertura-sospechosa-selected":e.aperturaSospechosaSelected},on:{click:function(t){e.select("aperturaSospechosa")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Apertura sospechosa")])],1),e._v(" "),a("b-col",{staticClass:"apertura-no-permitida",class:{"apertura-no-permitida-selected":e.aperturaNoPermitidaSelected},on:{click:function(t){e.select("aperturaNoPermitida")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Apertura no permitida")])],1),e._v(" "),a("b-col",{staticClass:"bateria-baja",class:{"bateria-baja-selected":e.bateriaBajaSelected},on:{click:function(t){e.select("bateriaBaja")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Batería baja")])],1),e._v(" "),a("b-col",{staticClass:"cerradura-desconectada",class:{"cerradura-desconectada-selected":e.cerraduraDesconectadaSelected},on:{click:function(t){e.select("cerraduraDesconectada")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Cerradura desconectada")])],1),e._v(" "),a("b-col",{staticClass:"hub-desconectado",class:{"hub-desconectado-selected":e.hubDesconectadoSelected},on:{click:function(t){e.select("hubDesconectado")}}},[a("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Hub desconectado")])],1)],1)],1)],1)},staticRenderFns:[]};var B={name:"Sidebar",components:{Account:F,Alarm:$,AlarmList:a("VU/8")(T,V,!1,function(e){a("CPS6")},"data-v-3479c06f",null).exports,Detail:a("VU/8")(j,z,!1,function(e){a("JlB8")},"data-v-a5555324",null).exports,RevisionFilters:a("VU/8")({name:"RevisionFilters",data:function(){return{notRevisedSelected:!0,revisedSelected:!0}},methods:{select:function(e){"revised"===e?this.revisedSelected=!this.revisedSelected:"notRevised"===e&&(this.notRevisedSelected=!this.notRevisedSelected),this.$emit("revision-select",e)}}},N,!1,function(e){a("f+GS")},"data-v-474766bd",null).exports,TypeFilters:a("VU/8")({name:"TypeFitlers",data:function(){return{puertaAbiertaSelected:!0,aperturaSospechosaSelected:!0,aperturaNoPermitidaSelected:!0,bateriaBajaSelected:!0,cerraduraDesconectadaSelected:!0,hubDesconectadoSelected:!0}},methods:{select:function(e){var t="",a=-1;"puertaAbierta"===e?(this.puertaAbiertaSelected=!this.puertaAbiertaSelected,t="emergency",a=1):"aperturaSospechosa"===e?(this.aperturaSospechosaSelected=!this.aperturaSospechosaSelected,t="emergency",a=2):"aperturaNoPermitida"===e?(this.aperturaNoPermitidaSelected=!this.aperturaNoPermitidaSelected,t="emergency",a=3):"bateriaBaja"===e?(this.bateriaBajaSelected=!this.bateriaBajaSelected,t="emergency",a=4):"cerraduraDesconectada"===e?(this.cerraduraDesconectadaSelected=!this.cerraduraDesconectadaSelected,t="failure",a=1):"hubDesconectado"===e&&(this.hubDesconectadoSelected=!this.hubDesconectadoSelected,t="failure",a=2),this.$emit("revision-select",t+"-"+a)}}},M,!1,function(e){a("DqYx")},"data-v-350c9bae",null).exports},props:["alarms","urName","detail"],data:function(){return{filters:{revised:!1,notRevised:!1,emergencies:[],failures:[]}}},methods:{selectType:function(e){console.log("selectType: ",e);var t=parseInt(e.split("-")[1]);"e"===e[0]?this.filters.emergencies.includes(t)?(deleteIndex=this.filters.emergencies.indexOf(t),this.filters.emergencies.splice(deleteIndex,1)):this.filters.emergencies.push(t):"f"===e[0]&&(this.filters.failures.includes(t)?(deleteIndex=this.filters.failures.indexOf(t),this.filters.failures.splice(deleteIndex,1)):this.filters.failures.push(t))},selectRevision:function(e){console.log("selectRevision: ",e),this.filters[e]=!this.filters[e],console.log(this.filters)}}},G={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"sidebar"}},[a("account",{attrs:{"ur-name":e.urName}}),e._v(" "),a("div",{attrs:{id:"revisionFilters"}},[a("revision-filters",{on:{"revision-select":e.selectRevision}})],1),e._v(" "),a("alarm-list",{attrs:{alarms:e.alarms,filters:e.filters}}),e._v(" "),a("div",{attrs:{id:"typeFilters"}},[a("type-filters",{on:{"type-select":e.selectType}})],1),e._v(" "),a("div",{attrs:{id:"detail"}},[a("detail",{attrs:{detail:e.detail}})],1)],1)},staticRenderFns:[]};var O,Z={name:"dashboard",components:{Grids:k,Sidebar:a("VU/8")(B,G,!1,function(e){a("3n4O")},"data-v-157c6094",null).exports},data:function(){return{websocketConnected:!1,alarms:[],UR:{},userDetail:null}},methods:(O={initWebsocket:function(){var e=y.a.connect("http://172.24.42.33:8070");e.on("connect",function(){console.log("Eureka")}),e.on("disconnect",function(){console.log("RIP conn")});var t=this;e.on(this.UR.name,function(e){var a=JSON.parse(e);console.log(a);var s={};if(a.emergency){var r=!0,n=!1,i=void 0;try{for(var o,c=h()(p()(a.emergency));!(r=(o=c.next()).done);r=!0){s[f=o.value]=a.emergency[f]}}catch(e){n=!0,i=e}finally{try{!r&&c.return&&c.return()}finally{if(n)throw i}}s.type="emergency"}else if(a.failure){var l=!0,d=!1,u=void 0;try{for(var m,v=h()(p()(a.failure));!(l=(m=v.next()).done);l=!0){var f;s[f=m.value]=a.faliure[f]}}catch(e){d=!0,u=e}finally{try{!l&&v.return&&v.return()}finally{if(d)throw u}}s.type="failure"}else console.log("Alarma inválida!"),s.type="unknown";s.sensetime=a.sensetime,s.revised=!1,t.alarms.push(s)})},initData:function(){var e=this,t=this.$route.params.username;b.a.get("http://172.24.42.64/users/"+t).then(function(t){b.a.get("http://172.24.42.64/unidadesResidenciales/"+t.data.scope+"/inmuebles").then(function(a){console.log(a.data);var s=a.data,r={};r.name=t.data.scope,r.torres=[];var n=e.sortArray(s),i=-1,o=-1,c=-1,l=-1,d=!0,u=!1,m=void 0;try{for(var v,p=h()(n);!(d=(v=p.next()).done);d=!0){var f=v.value,_=f.localID.split("-"),b={numero:parseInt(_[2]),owner:f.owner_user_id};if(console.log("t"+l+" "+parseInt(_[0])-1),console.log("f"+c+" "+parseInt(_[1])),l===parseInt(_[0]))if(c===parseInt(_[1]))console.log(l),console.log(r),r.torres[i].pisos[o].apartamentos.push(b);else{var C={numero:parseInt(_[1]),apartamentos:[b]};r.torres[i].pisos.push(C),c=parseInt(_[1]),o+=1}else{var y={numero:parseInt(_[1]),apartamentos:[b]},g={numero:parseInt(_[0]),pisos:[y]};r.torres.push(g),i+=1,o=0,c=parseInt(_[1]),l=parseInt(_[0])}}}catch(e){u=!0,m=e}finally{try{!d&&p.return&&p.return()}finally{if(u)throw m}}console.log(r),e.UR=r,e.initWebsocket()}).catch(function(e){console.log(e)})}).catch(function(e){console.log(e)}),console.log(UR_temp)},addPropertyTo:function(e,t){towerIndex=-1;var a=e.localID.split("-")[0];for(i=0;i<t.torres.length;i++)if(t.torres[i].number===a){towerIndex=i;break}-1===towerIndex&&(t.torres.push({numero:a,pisos:[]}),towerIndex=t.torres.length-1),addFloorTo(towerIndex,e,t)},addFloorTo:function(e,t,a){floorIndex=-1;var s=t.localID.split("-")[1];for(i=0;i<a.torres[e].pisos.length;i++)if(a.torres[e].pisos[i].number===s){floorIndex=i;break}-1===floorIndex&&(a.torres[e].pisos.push({numero:s,apartamentos:[]}),floorIndex=a.torres[e].pisos.length-1),addPropertyTo(e,floorIndex,t,a)}},m()(O,"addPropertyTo",function(e,t,a,s){a.localID.split("-")[1];s.torres[e].pisos[-1].push({numero:a.localID.split("-")[2],owner:owner_user_id})}),m()(O,"sortArray",function(e){return e.sort(function(e,t){var a=e.localID.split("-"),s=t.localID.split("-");return parseInt(a[0])-parseInt(s[0])==0?parseInt(a[1])-parseInt(s[1])==0?a[2]-s[2]:-parseInt(a[1])+parseInt(s[1]):-parseInt(s[0])+parseInt(a[0])}),e}),m()(O,"selectDetail",function(e){console.log("SelectDetail: ",e);var t=this;b.a.get("http://172.24.42.64/users/checkAuth0/"+this.UR.name+"/"+e).then(function(e){t.userDetail=e.data}).catch(function(e){console.log(e)})}),O),mounted:function(){this.initData()}},J={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"dashboard"},[t("div",{staticClass:"md-layout"},[t("div",{staticClass:"md-layout-item md-size-75"},[t("grids",{attrs:{ur:this.UR,alarms:this.alarms},on:{"select-detail":this.selectDetail}})],1),this._v(" "),t("div",{staticClass:"md-layout-item md-size-25 sidebar-container"},[t("sidebar",{staticClass:"sidebar",attrs:{detail:this.userDetail,alarms:this.alarms,"ur-name":this.UR.name}})],1)])])},staticRenderFns:[]};var L=a("VU/8")(Z,J,!1,function(e){a("57Do")},"data-v-062497f9",null).exports;s.default.use(d.a);var W=new d.a({routes:[{path:"/dashboard/:username",name:"Dashboard",component:L}]});s.default.config.productionTip=!1,s.default.config.devtools=!0,s.default.use(r.a),s.default.use(o.a),new s.default({el:"#app",router:W,render:function(e){return e(l)},template:"<App/>"})},UvZ7:function(e,t){},cSx0:function(e,t){},"f+GS":function(e,t){},isX2:function(e,t){},mfW3:function(e,t){},rLam:function(e,t){},tEZc:function(e,t){},tl9A:function(e,t){},xV3Z:function(e,t){},zj2Q:function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.52c7ad270d5886798ab4.js.map