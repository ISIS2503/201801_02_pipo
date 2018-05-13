<template>
<div>

    <div class="above">
        <md-icon class="md-size-2x next cursor">arrow_back_ios</md-icon>
        <h1 class="next">Torre 1</h1>
        <md-icon class="md-size-2x next cursor">arrow_forward_ios</md-icon>
    </div>
    <div class="roof">

        <div class="middle-roof">
        </div>
        <div class="bottom-roof">
        </div>
    </div>
    <div class="container">
        <div
            v-for="(piso, index) in this.unidad.torres[0].pisos"
            :key="index"
        >
            <b-container>
                <b-row>
                    <b-col
                        cols="1"
                        class="floor-number"
                    >
                       {{piso.numero}}
                        </b-col>
                        <b-col
                            v-for="(apartamento, index) in piso.apartamentos"
                            :key="index"
                            class="apto"
                        >
                            <div class="apartment-number">
                                {{apartamento.numero}}
                            </div>
                            <div class="apartment-icon">
                                <div class="apartment-window1">
                                </div>
                                <div class="apartment-window2">
                                </div>
                                <div class="apartment-door">
                                </div>
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
import "./apartment-icon.css";
export default {
    name: "MapGrid",
    data: function () {
        return {
            unidad: {
                nombre: "toscana",
                torres: [{
                    numero: 1,
                    pisos: [{
                            numero: 1,
                            apartamentos: [{
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
                            apartamentos: [{
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
                            apartamentos: [{
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
                            apartamentos: [{
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
                            apartamentos: [{
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
                            apartamentos: [{
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
                            apartamentos: [{
                                    numero: 1
                                },
                                {
                                    numero: 2
                                }
                            ]
                        }
                    ]
                }]
            }
        };
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

.cursor:hover {
    cursor: pointer;
}

.roof {
    position: relative;
    z-index: 2;
    height: 70px;
}

.apartment-number {
    height: 20px;
    width: 100%;
    border: 1px black solid;
    background: rgb(223, 230, 127);
}

.apartment-number::after {
    content: '';
    width: 98%;
    box-shadow: 0px 0px 8px 2px #000000;
    top: 21px;
    left: 1%;
    position: absolute;
}

.floor-number {
    vertical-align: middle;
    display: inline-block;
    line-height: 120px;
    padding: 0;
    overflow:hidden;
    box-shadow: 1px 0px 1px 1px black;
}

.col-1{
  display: inline-block;
        height:118px;
        position:relative;
        top:1px;
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
    border-top: black 1px solid;
}

.container {
    text-align: center;
    width: 102%;
    position: relative;
    left: -10px;
}
</style>
