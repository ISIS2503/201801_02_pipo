package com.mycompany.mqttfinalconsumer;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author s.guzmanm
 */
public class SimpleMqqtConsumerClient implements MqttCallback {

    private static String url="http://172.24.41.181:80/mensaje";
    static int contador=0;
    
  public void connectionLost(Throwable throwable) {
    System.out.println("Connection to MQTT broker lost!");
  }

  public void messageArrived(String s, MqttMessage mqttMessage) throws Exception {
       new RestPublisher(mqttMessage,url).start();
       ++contador;
  }

  public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
    // not used in this example
  }
  
  public static void main (String[] args)
  {
      try
      {
          System.out.println("Message not received:\n\t");
            MqttClient client=new MqttClient("tcp://172.24.42.70:8083", MqttClient.generateClientId());
            client.setCallback(new SimpleMqqtConsumerClient() );
            client.connect();
            client.subscribe("Toscana/emergencia/Centro");
      }
      catch(Exception e)
      {
          System.out.println(contador);
          e.printStackTrace();
      }
    
  }
}
