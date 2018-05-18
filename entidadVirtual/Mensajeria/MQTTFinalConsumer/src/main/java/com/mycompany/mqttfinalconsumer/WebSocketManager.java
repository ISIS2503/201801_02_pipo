/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.mqttfinalconsumer;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIONamespace;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
import static com.mycompany.mqttfinalconsumer.RestPublisher.contadorErrores;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import org.json.JSONException;
import org.json.JSONObject;

/**
 *
 * @author s.guzmanm
 */
public class WebSocketManager {

    private SocketIOServer server;

    public WebSocketManager() throws Exception {
        Configuration config = new Configuration();
        config.setHostname("172.24.42.33");
        config.setPort(8070);

        server = new SocketIOServer(config);
        server.start();
    }

    public void publish(MqttMessage message) {
        JSONObject jsonRequest = new JSONObject(message.toString());
        //JSONObject jsonRequest=new JSONObject(message.toString());
        //jsonRequest=jsonRequest.getJSONObject("emergency");
        //jsonRequest.getString("id")
        System.out.println(message.toString());
        //JSONObject jsonRequest=obj.getJSONObject("emergency");
        String event = "";
        if (jsonRequest.has("emergency")) {
            jsonRequest = jsonRequest.getJSONObject("emergency");
            event = jsonRequest.getString("conjunto");

        } else if (jsonRequest.has("failure")) {
            jsonRequest = jsonRequest.getJSONObject("failure");
            event = jsonRequest.getString("conjunto");
        }

        //System.out.println(jsonRequest.toString());
        server.getBroadcastOperations().sendEvent(event, message.toString());
    }

}
