package com.mycompany.mqttfinalconsumer;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.*;
import org.bouncycastle.openssl.PEMReader;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

import java.security.KeyPair;
import java.security.KeyStore;
import java.security.Security;
import java.security.cert.X509Certificate;

import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttTopic;


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.

 */
/**
 *
 * @author s.guzmanm
 */
public class YaleVerification implements MqttCallback {

    
    static final String ROOT = "C:/Users/js.diaz/201810_02_pipo/entidadVirtual/ssl";
    static final String CRT_FILE_PATH = "/mosquittoChecho";
    //static final String CTRFilesPath = "/mosquittoCarlos";
    static final String CA_FILE_PATH = "/ca.crt";
    static final String CLIENT_CRT_FILE_PATH = "/server.crt";
    static final String CLIENT_KEY_FILE_PATH = "/server.key";
    static final String MQTT_USER_NAME = "Yale";
    static final String MQTT_PASSWORD = "piporules";
    
    private static HashMap<String,Date> hashMap=new HashMap<>();

    private static HashMap<String,Integer> losses=new HashMap<>();

    private static HashMap<String,List<String>> to=new HashMap<>();

    private static final String FROM="admin@yale.com";

    private static int maxLosses;

    private static long maxTime;

    public YaleVerification(int maxLosses,long maxTime)
    {
        this.maxLosses=maxLosses;
        this.maxTime=maxTime;
        ArrayList<String> mails=new ArrayList<>();
        mails.add("js.diaz@uniandes.edu.co");
        mails.add("ja.manrique@uniandes.edu.co");
        mails.add("cm.sarmiento10@uniandes.edu.co");
        this.to.put("Hub007",mails);
        System.out.println(to.size());
    }



    public static synchronized void newHub(String hub)
    {
        hashMap.put(hub,new Date());
        losses.put(hub,0);
    }
    
    public void connectionLost(Throwable throwable) {
        System.out.println("Connection to MQTT broker lost!");
    }
    
    @Override
    public void messageArrived(String string, MqttMessage mm) throws Exception {
        System.out.println("MSG"+mm.toString());
        hashMap.put(string,new Date());
        losses.put(string,0);   
    }


    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
        // not used in this example
    }
  
    public static void main (String[] args)
    {
        try
        {
            System.out.println("Message not received:\n\t");
            MqttClient client=new MqttClient("ssl://172.24.41.182:8083", MqttClient.generateClientId());
            YaleVerification yale=new YaleVerification(1,10000);
            client.setCallback(yale);
            MqttConnectOptions connOpt = new MqttConnectOptions();
            connOpt.setKeepAliveInterval(30);
            connOpt.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
            connOpt.setUserName(MQTT_USER_NAME);
            connOpt.setPassword(MQTT_PASSWORD.toCharArray());
            
            String myTopic = "Centro/Toscana/fallo/hubFueraDeLinea/2-5-3";
            MqttTopic topic = client.getTopic(myTopic);

            //socket factory
            SSLSocketFactory socketFactory = getSocketFactory(ROOT+CRT_FILE_PATH+CA_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_CRT_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_KEY_FILE_PATH, "");
            connOpt.setSocketFactory(socketFactory);
            
            client.connect(connOpt);
            client.subscribe("Centro/Toscana/hub/2-5-3");
            System.out.println("ENTRA "+to.size()+" "+to.get("Hub007"));
            while(true)
            {
                System.out.println("WHILE "+yale.hashMap.size());
                for(String hub:hashMap.keySet())
                {
                    System.out.println("HUB "+hub);
                    if(new Date().getTime()-hashMap.get(hub).getTime()>maxTime)
                    {
                        losses.put(hub,losses.get(hub)+1);
                        if(losses.get(hub)>maxLosses)
                        {
                            String[] data=hub.split("/");
                            String pubMsg="{\"failTime\":\""+new Date().toString()+"\",\"failure\":{\"id\":\""+"Hub "+data[data.length-1]+"\",\"fallo\":\"2\",\"apartamento\":\"2-5-3\",\"conjunto\":\"Toscana\",\"zona\":\"Centro\"}}";
                            System.out.println(pubMsg);
                            int pubQoS = 0;
                            MqttMessage message = new MqttMessage(pubMsg.getBytes());
                            message.setQos(pubQoS);
                            message.setRetained(false);
                            // Publish the message
                            System.out.println("Publishing to topic \"" +topic.getName() + "\" qos " + pubQoS);
                            MqttDeliveryToken token = null;
                            try {
                                // publish message to broker
                                
                                token = topic.publish(message);
                                // Wait until the message has been delivered to the broker
                                token.waitForCompletion();
                                System.out.println("llegó");
                                //Thread.sleep(100);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }
                try
                {
                    Thread.sleep(10000);
                }
                catch(Exception e)
                {
                    e.printStackTrace();
                }
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    
    }
    
    static SSLSocketFactory getSocketFactory (final String caCrtFile, final String crtFile, final String keyFile, 
	                                          final String password) throws Exception
    {
        Security.addProvider(new BouncyCastleProvider());

        // load CA certificate
        PEMReader reader = new PEMReader(new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(Paths.get(caCrtFile)))));
        X509Certificate caCert = (X509Certificate)reader.readObject();
        reader.close();

        // load client certificate
        reader = new PEMReader(new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(Paths.get(crtFile)))));
        X509Certificate cert = (X509Certificate)reader.readObject();
        reader.close();

        // load client private key
        reader = new PEMReader(
            new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(Paths.get(keyFile)))),
            new PasswordFinder() {
                @Override
                public char[] getPassword() {
                        return password.toCharArray();
                }
            }
        );
        KeyPair key = (KeyPair)reader.readObject();
        reader.close();

        // CA certificate is used to authenticate server
        KeyStore caKs = KeyStore.getInstance(KeyStore.getDefaultType());
        caKs.load(null, null);
        caKs.setCertificateEntry("ca-certificate", caCert);
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(caKs);

        // client key and certificates are sent to server so it can authenticate us
        KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
        ks.load(null, null);
        ks.setCertificateEntry("certificate", cert);
        ks.setKeyEntry("private-key", key.getPrivate(), password.toCharArray(), new java.security.cert.Certificate[]{cert});
        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        kmf.init(ks, password.toCharArray());

        // finally, create SSL socket factory
        SSLContext context = SSLContext.getInstance("TLSv1.2");
        context.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

        return context.getSocketFactory();
    }
    
    
}
