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
    private long time=System.currentTimeMillis();

    public RestPublisher(MqttMessage message,String url) {
        this.mqttMessage = message;
        this.url=url;
    }
    
    
    public void start()
    {
        try
        {
            //Base connection with RestAPI
            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            // GET
            con.setRequestMethod("GET");
            con.setDoOutput(true);

            JSONObject jsonRequest=new JSONObject(mqttMessage.toString()).getJSONObject("emergency");
            System.out.println(SimpleMqqtConsumerClient.contador+" ASUNTO: Alarma del dispositivo "+ jsonRequest.getString("id")+";CONTENIDO: Hubo una emergencia en el inmueble "+jsonRequest.getString("apartamento")+
                    " de la unidad residencial "+jsonRequest.getString("conjunto")+" de tipo "+jsonRequest.getString("emergencia")+";REMITENTE:s.guzmanm@yale.com"
                    +";DESTINATARIOS:se.cardenas@uniandes.edu.co,ja.manrique@uniandes.edu.co");
            if(con.getResponseCode()!=200)
                throw new Exception("Falló P1 ");
            System.out.println((System.currentTimeMillis()-time)+"");
        }
        catch(Exception e)
        {
            System.out.println(SimpleMqqtConsumerClient.contador);
            e.printStackTrace();
        }
        
    }
    
}
