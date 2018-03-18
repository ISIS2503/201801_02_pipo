/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.mqttfinalconsumer;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONObject;

/**
 *
 * @author s.guzmanm
 */
public class RestPublisher extends Thread {
    
    private MqttMessage mqttMessage;

    public RestPublisher(MqttMessage message) {
        this.mqttMessage = message;
    }
    
    
    public void start()
    {
        try
        {
                //Base connection with RestAPI
            String url = "http://172.24.42.33:9000/mensaje";

            URL obj = new URL(url);
                          System.out.println("B");

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                          System.out.println("N");

            // GET
            con.setRequestMethod("POST");



            con.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            con.setRequestProperty("Accept", "application/json; charset=UTF-8");

            con.setDoOutput(true);

                          System.out.println("B");

            JSONObject jsonRequest=new JSONObject(mqttMessage.toString()).getJSONObject("emergency");

            String contenido="Hubo una emergencia en el inmueble "+jsonRequest.getString("apartamento")+
                    " de la unidad residencial "+jsonRequest.getString("conjunto")+" de tipo "+jsonRequest.getString("emergencia");

            JSONObject jsonBody=new JSONObject();
            jsonBody.put("asunto","Alarma del dispositivo "+ jsonRequest.getString("id"));
            jsonBody.put("cuerpo",contenido);
            jsonBody.put("remitente","s.guzmanm@yale.com");
            List<String> sList = new ArrayList<String>();
            sList.add("se.cardenas@uniandes.edu.co");
            sList.add("ja.manrique@uniandes.edu.co");

            jsonBody.put("destinatarios", sList);
            System.out.println(jsonBody.toString());
            OutputStreamWriter wr = new OutputStreamWriter(con.getOutputStream());
            wr.write(jsonBody.toString());
            wr.flush();
            wr.close();
        

        
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
        
    }
    
}
