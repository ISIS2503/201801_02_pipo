package co.edu.uniandes.csw.recursos;

import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttTopic;

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

public class SimpleMqttClient implements MqttCallback {

    MqttClient myClient;
    MqttConnectOptions connOpt;

    MqttTopic topic;
    
    boolean conectado = false;
    
    private static SimpleMqttClient client = null;

    static final String BROKER_URL = "ssl://172.24.41.182:8083";
    static final String ROOT = "C:/Users/se.cardenas/Documents/201810_02_pipo/entidadVirtual/ssl";
    static final String CRT_FILE_PATH = "/mosquittoChecho";
    //static final String CTRFilesPath = "/mosquittoCarlos";
    static final String CA_FILE_PATH = "/ca.crt";
    static final String CLIENT_CRT_FILE_PATH = "/server.crt";
    static final String CLIENT_KEY_FILE_PATH = "/server.key";
    static final String MQTT_USER_NAME = "ClavesArduino007";
    static final String MQTT_PASSWORD = "piporules";
    
    //private static SimpleMqttClient mqttClient = null;

    public static SimpleMqttClient getInstance() {
        if(client==null || !client.conectado) {
            client = new SimpleMqttClient();
            client.runClient();
        }
        return client;
    }
    
    /**
     * 
     * connectionLost
     * This callback is invoked upon losing the MQTT connection.
     * 
     */
    @Override
    public void connectionLost(Throwable t) {
        System.out.println("Connection lost!");
        // code to reconnect to the broker would go here if desired
        conectado = false;
    }

    /**
     * 
     * messageArrived
     * This callback is invoked when a message is received on a subscribed topic.
     * 
     */
    public void messageArrived(MqttTopic topic, MqttMessage message) throws Exception {
            System.out.println("-------------------------------------------------");
            System.out.println("| Topic:" + topic.getName());
            System.out.println("| Message: " + new String(message.getPayload()));
            System.out.println("-------------------------------------------------");
    }
	
    /**
     * 
     * runClient
     * The main functionality of this simple example.
     * Create a MQTT client, connect to broker, pub/sub, disconnect.
     * 
     */
    public void runClient() {
            // setup MQTT Client
            connOpt = new MqttConnectOptions();
            connOpt.setCleanSession(true);
            connOpt.setKeepAliveInterval(30);
            connOpt.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
            connOpt.setUserName(MQTT_USER_NAME);
            connOpt.setPassword(MQTT_PASSWORD.toCharArray());
            //connOpt.setConnectionTimeout();
            // Connect to Broker
            SSLSocketFactory socketFactory;
            try {
                myClient = new MqttClient(BROKER_URL, MqttClient.generateClientId());
                myClient.setCallback(this);
                socketFactory = getSocketFactory(ROOT+CRT_FILE_PATH+CA_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_CRT_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_KEY_FILE_PATH, "");
                connOpt.setSocketFactory(socketFactory);
                myClient.connect(connOpt);
                System.out.println("Connected to " + BROKER_URL);
                conectado = true;
            } catch (MqttException e) {
                e.printStackTrace();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
            

            // setup topic
            // topics on m2m.io are in the form <domain>/<stuff>/<thing>
            String myTopic = "Centro/Toscana/2-5-3/claves/Arduino007";
            topic = myClient.getTopic(myTopic);
            
    }

    @Override
    public void messageArrived(String string, MqttMessage mm) throws Exception {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken imdt) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    
    public void publish(Msg msg) {
        String pubMsg = "{\"msg\":\"" + msg.msg + "\"}";
        int pubQoS = 0;
        MqttMessage message = new MqttMessage(pubMsg.getBytes());
        message.setQos(pubQoS);
        message.setRetained(false);
        // Publish the message
        System.out.println("Publishing to topic \"" + topic + "\" qos " + pubQoS);
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