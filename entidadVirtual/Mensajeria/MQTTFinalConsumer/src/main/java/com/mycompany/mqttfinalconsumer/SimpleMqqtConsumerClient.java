package com.mycompany.mqttfinalconsumer;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIONamespace;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
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
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;

import org.json.JSONException;
import org.json.JSONObject;


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

    private static String url = "http://172.24.42.57:9000/mensaje";
    static int contador = 0;
    static long[] sumatoria = new long[100000];

    static final String ROOT = "C:/Users/s.guzmanm/Documents/201810_02_pipo/entidadVirtual/ssl";
    static final String CRT_FILE_PATH = "/mosquittoChecho";
    //static final String CTRFilesPath = "/mosquittoCarlos";
    static final String CA_FILE_PATH = "/ca.crt";
    static final String CLIENT_CRT_FILE_PATH = "/server.crt";
    static final String CLIENT_KEY_FILE_PATH = "/server.key";
    static final String MQTT_USER_NAME = "P1Centro";
    static final String MQTT_PASSWORD = "p1";
    static WebSocketManager webSocketManager;
    
    private MqttConnectOptions connOpt;
    private MqttClient mqtt;

    @Override
    public void connectionLost(Throwable cause) {
        System.out.println("Lost connection to MQTT server");
        while (true) {
            try {
                System.out.println("Attempting to reconnect to MQTT server");
                mqtt.connect(connOpt);
                mqtt.subscribe("Centro/Toscana/#");
                System.out.println("Reconnected to MQTT server, resuming");
                return;
            } catch (MqttException e) {
                System.out.println("Reconnect failed, retrying in 10 seconds");
            }
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                
            }
        }
    }
    
    public void connect() throws MqttException {
        mqtt = new MqttClient("ssl://172.24.41.182:8083", MqttClient.generateClientId());
        mqtt.setCallback(this);
        connOpt = new MqttConnectOptions();
        connOpt.setKeepAliveInterval(30);
        connOpt.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
        connOpt.setUserName(MQTT_USER_NAME);
        connOpt.setPassword(MQTT_PASSWORD.toCharArray());
        
        SSLSocketFactory socketFactory;
        try {
            socketFactory = getSocketFactory(ROOT+CRT_FILE_PATH+CA_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_CRT_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_KEY_FILE_PATH, "");
            connOpt.setSocketFactory(socketFactory);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        mqtt.connect(connOpt);
        mqtt.subscribe("Centro/Toscana/#");
    }

    public void messageArrived(String s, MqttMessage mqttMessage) throws Exception {
        //new RestPublisher(mqttMessage,url,contador).start();                
        webSocketManager.publish(mqttMessage);
        //server.getBroadcastOperations().sendEvent("emergency", mqttMessage.toString());
        ++contador;
    }

    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
        // not used in this example
    }

    public static void main(String[] args) {
        try {
            webSocketManager = new WebSocketManager();
            System.out.println("Message not received:\n\t");
            
            SimpleMqqtConsumerClient client = new SimpleMqqtConsumerClient();
            client.connect();
            //new Contador().start();
            
            
        } catch (Exception e) {
            System.out.println(contador);
            e.printStackTrace();
        }

    }

    static SSLSocketFactory getSocketFactory(final String caCrtFile, final String crtFile, final String keyFile,
            final String password) throws Exception {
        Security.addProvider(new BouncyCastleProvider());

        // load CA certificate
        PEMReader reader = new PEMReader(new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(Paths.get(caCrtFile)))));
        X509Certificate caCert = (X509Certificate) reader.readObject();
        reader.close();

        // load client certificate
        reader = new PEMReader(new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(Paths.get(crtFile)))));
        X509Certificate cert = (X509Certificate) reader.readObject();
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
        KeyPair key = (KeyPair) reader.readObject();
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
