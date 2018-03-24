/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.mqttfinalconsumer;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author cm.sarmiento10
 */
public class Contador extends Thread {
    
    public Contador()
    {
        
    }
    
    public void run()
    {
        try {
            Thread.sleep(600000);
        } catch (InterruptedException ex) {
            
        }
        long[] arr=SimpleMqqtConsumerClient.sumatoria;
        long contador=0;
        long acum=0;
        for (long num: arr) {
            acum+=num;
            contador++;
        }
        double resultado= acum/contador;
        System.out.println("Tiempo "+ resultado);
    }
}
