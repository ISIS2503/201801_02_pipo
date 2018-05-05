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

    public Contador() {

    }

    public void run() {
        try {
            Thread.sleep(600000);
        } catch (InterruptedException ex) {

        }
        long contador = 0;
        long acum = 0;
        try {
            long[] arr = SimpleMqqtConsumerClient.sumatoria;

            for (long num : arr) {
                acum += num;
                contador++;
            }
        } catch (Exception e) {

        }
        double resultado = acum / contador;
        System.out.println("Tiempo " + resultado);
        System.out.println("Contador errores "+ RestPublisher.contadorErrores);
    }
}
