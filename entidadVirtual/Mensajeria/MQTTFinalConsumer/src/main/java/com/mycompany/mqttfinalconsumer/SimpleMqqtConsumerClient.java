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
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;


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

    private static String url="http://172.24.42.57:9000/mensaje";
    static int contador=0;
    static long[] sumatoria=new long[100000];
    
    static final String ROOT = "C:/Users/se.cardenas/Documents/201810_02_pipo/entidadVirtual";
    static final String CA_FILE_PATH = "/ssl/ca.crt";
    static final String CLIENT_CRT_FILE_PATH = "/ssl/server.crt";
    static final String CLIENT_KEY_FILE_PATH = "/ssl/server.key";
    static final String MQTT_USER_NAME = "P1Centro";
    static final String MQTT_PASSWORD = "p1";
    
    public void connectionLost(Throwable throwable) {
        System.out.println("Connection to MQTT broker lost!");
    }

    public void messageArrived(String s, MqttMessage mqttMessage) throws Exception {
        new RestPublisher(mqttMessage,url,contador).start();
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
            MqttClient client=new MqttClient("ssl://172.24.41.182:8083", MqttClient.generateClientId());
            client.setCallback(new SimpleMqqtConsumerClient() );
            MqttConnectOptions connOpt = new MqttConnectOptions();
            connOpt.setKeepAliveInterval(30);
            connOpt.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
            connOpt.setUserName(MQTT_USER_NAME);
            connOpt.setPassword(MQTT_PASSWORD.toCharArray());
            
            //socket factory
            SSLSocketFactory socketFactory = getSocketFactory(ROOT+CA_FILE_PATH, ROOT+CLIENT_CRT_FILE_PATH, ROOT+CLIENT_KEY_FILE_PATH, "");
            connOpt.setSocketFactory(socketFactory);
            
            client.connect(connOpt);
            client.subscribe("Centro/Toscana/emergencia/#");
            new Contador().start();
        }
        catch(Exception e)
        {
            System.out.println(contador);
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
