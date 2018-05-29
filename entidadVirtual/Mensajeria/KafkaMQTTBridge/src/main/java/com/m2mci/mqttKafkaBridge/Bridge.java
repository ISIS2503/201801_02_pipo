package com.m2mci.mqttKafkaBridge;

import java.util.Properties;

import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;

import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.consumer.Consumer;

import org.apache.log4j.Logger;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttAsyncClient;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.kohsuke.args4j.CmdLineException;

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
import java.util.Arrays;
import java.util.logging.Level;
import org.eclipse.paho.client.mqttv3.MqttClient;

public class Bridge implements MqttCallback {
	private Logger logger = Logger.getLogger(this.getClass().getName());
	private MqttAsyncClient mqtt;
	private Producer<String, String> kafkaProducer;
        private MqttConnectOptions connOpt;
        
    static final String ROOT = "C:/Users/se.cardenas/Documents/201810_02_pipo/entidadVirtual/ssl";
    static final String CRT_FILE_PATH = "/mosquittoChecho";
    //static final String CTRFilesPath = "/mosquittoCarlos";
    static final String CA_FILE_PATH = "/ca.crt";
    static final String CLIENT_CRT_FILE_PATH = "/server.crt";
    static final String CLIENT_KEY_FILE_PATH = "/server.key";
    static final String MQTT_USER_NAME = "Yale";
    static final String MQTT_PASSWORD = "piporules";
    static final String BROKER_URL = "ssl://172.24.41.182:8083";
    
    boolean connected = false;
	
	private void connect(String serverURI, String clientId) throws MqttException {
		
            mqtt = new MqttAsyncClient(serverURI, clientId);
            mqtt.setCallback(this);
            connOpt = new MqttConnectOptions();
            connOpt.setKeepAliveInterval(30);
            connOpt.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
            connOpt.setUserName(MQTT_USER_NAME);
            connOpt.setPassword(MQTT_PASSWORD.toCharArray());

            //socket factory
            SSLSocketFactory socketFactory;
            try {
                socketFactory = getSocketFactory(ROOT+CRT_FILE_PATH+CA_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_CRT_FILE_PATH, ROOT+CRT_FILE_PATH+CLIENT_KEY_FILE_PATH, "");
                connOpt.setSocketFactory(socketFactory);
            } catch (Exception e) {
                e.printStackTrace();
            }
                
                
		IMqttToken token = mqtt.connect(connOpt);
		token.waitForCompletion();
                connected = true;
		logger.info("Connected to MQTT and Kafka");
	}

	private void reconnect() throws MqttException {
		IMqttToken token = mqtt.connect(connOpt);
		token.waitForCompletion();
	}
	

	@Override
	public void connectionLost(Throwable cause) {
                connected = false;
		logger.warn("Lost connection to MQTT server", cause);
		while (true) {
			try {
				logger.info("Attempting to reconnect to MQTT server");
				reconnect();
				logger.info("Reconnected to MQTT server, resuming");
				return;
			} catch (MqttException e) {
				logger.warn("Reconnect failed, retrying in 10 seconds", e);
			}
			try {
				Thread.sleep(10000);
			} catch (InterruptedException e) {
			}
		}
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub
            System.out.println("Delivery completed");
            
	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
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

    /**
     * @param args
     */
    public static void main(String args[])   {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:8090");
        props.put("group.id", "test");
        props.put("enable.auto.commit", "true");
        props.put("auto.commit.interval.ms", "1000");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList("Centro.Toscana.2-5-3.claves", "Centro.Toscana.2-5-3.horarios", "Arduino007.envio"));
        Bridge b = new Bridge();
        try {
            b.connect(BROKER_URL,MqttClient.generateClientId());
        } catch (MqttException ex) {
            java.util.logging.Logger.getLogger(Bridge.class.getName()).log(Level.SEVERE, null, ex);
        }
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(100);
            if(!b.connected) {
                b = new Bridge();
                try {
                    b.connect(BROKER_URL,MqttClient.generateClientId());
                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
            }
            for (ConsumerRecord<String, String> record : records) {
                try {
                    System.out.println(record.topic().replaceAll("\\.", "/"));
                    b.mqtt.publish(record.topic().replaceAll("\\.", "/"), new MqttMessage(record.value().getBytes()));
                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
                System.out.printf("value = %s, topic = %s%n", record.value(), record.topic());
            }
        }
    }
}