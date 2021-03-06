/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.mqttfinalconsumer;

import java.net.HttpURLConnection;
import java.net.URL;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONObject;

/**
 *
 * @author s.guzmanm
 */
public class RestPublisher extends Thread {

    private String url;
    private MqttMessage mqttMessage;
    private int contador;
    private long time = System.currentTimeMillis();
    public static int contadorErrores=0;

    public RestPublisher(MqttMessage message, String url, int contador) {
        this.mqttMessage = message;
        this.url = url;
        this.contador = contador;
    }

    public void start() {
        try {
            System.out.println("MSJ:"+mqttMessage.toString());
            //Base connection with RestAPI
            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            // GET
            con.setRequestMethod("GET");
            con.setDoOutput(true);
            JSONObject jsonRequest=new JSONObject(mqttMessage.toString());
            System.out.println(mqttMessage.toString());
            if(jsonRequest.has("emergency"))
            {
                jsonRequest=jsonRequest.getJSONObject("emergency");
                System.out.println(SimpleMqqtConsumerClient.contador + " ASUNTO: Alarma del dispositivo " + jsonRequest.getString("id") + ";CONTENIDO: Hubo una emergencia en el inmueble " + jsonRequest.getString("apartamento")
                    + " de la unidad residencial " + jsonRequest.getString("conjunto") + " de la zona " + jsonRequest.getString("zona") + " de tipo " + jsonRequest.getString("emergencia") + ";REMITENTE:s.guzmanm@yale.com"
                    + ";DESTINATARIOS:se.cardenas@uniandes.edu.co,ja.manrique@uniandes.edu.co");
                if (con.getResponseCode() != 200) {
                    contadorErrores++;
                }
                SimpleMqqtConsumerClient.sumatoria[contador] = System.currentTimeMillis() - time;
                if (contador >= 999999) {
                    long acumulado = 0;
                    for (long num : SimpleMqqtConsumerClient.sumatoria) {
                        acumulado += num;
                    }
                    double resp= (acumulado / 100000);
                    System.out.println("promedio "+ resp);
                    System.out.println("Contador errores "+  contadorErrores);
                }
            }
            else if (jsonRequest.has("failure"))
            {
                jsonRequest = jsonRequest.getJSONObject("failure");
                 System.out.println(SimpleMqqtConsumerClient.contador + " ASUNTO: Fallo del dispositivo " + jsonRequest.getString("id") + ";CONTENIDO: Hubo un fallo en el inmueble " + jsonRequest.getString("apartamento")
                    + " de la unidad residencial " + jsonRequest.getString("conjunto") + " de la zona " + jsonRequest.getString("zona") + " de tipo " + jsonRequest.getString("fallo") + ";REMITENTE:s.guzmanm@yale.com"
                    + ";DESTINATARIOS:se.cardenas@uniandes.edu.co,ja.manrique@uniandes.edu.co");
                if (con.getResponseCode() != 200) {
                    contadorErrores++;
                }
                SimpleMqqtConsumerClient.sumatoria[contador] = System.currentTimeMillis() - time;
                if (contador >= 999999) {
                    long acumulado = 0;
                    for (long num : SimpleMqqtConsumerClient.sumatoria) {
                        acumulado += num;
                    }
                    double resp= (acumulado / 100000);
                    System.out.println("promedio "+ resp);
                    System.out.println("Contador errores "+  contadorErrores);
                }
            }
            
        } catch (Exception e) {
            System.out.println(SimpleMqqtConsumerClient.contador);
            e.printStackTrace();
        }

    }

}
