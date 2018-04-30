package controllers;

import com.avaje.ebean.Model;
import com.fasterxml.jackson.databind.JsonNode;
import play.libs.Json;
import play.mvc.BodyParser;
import play.mvc.Controller;
import play.mvc.Result;
import play.Logger;
import java.io.*;

import java.util.List;

/**
 * Created by s.guzmanm and js.diaz on 17/03/17.
 */
public class MensajeController extends Controller {
    BufferedWriter out;

    private static final int TAMANO_BUFFER = 100000;


    public Result initializeBuffer()
    {
        if(out==null)
        {
            try
            {
                //out = new BufferedWriter(new OutputStreamWriter(System.out), 32768);
                out = new BufferedWriter(new FileWriter(new File("./logs/prueba.txt")), 100000);
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
        }
        else
        {
            try
            {
                out.close();
                out=null;
            }
            catch(Exception e)
            {

            }

        }
        return ok("");

    }
    /**
     *
     * FORMATO JSON
     * {
     *     "remitente":"s.guzmanm@uniandes.edu.co",
     *     "destinatarios":[
     *     {
     *         "correo":"js.diaz@uniandes.edu.co"
     *     },
     *     {
     *         "correo":"js.diaz@uniandes.edu.co"
     *     },
     *     {
     *         "correo":"cm.sarmiento10@uniandes.edu.co"
     *     }
     *     ],
     *     "asunto":"Sergio está fuera",
     *     "cuerpo":"Sergio queda fuera del grupo por esta entrega"
     *
     * }
     */
    @BodyParser.Of(BodyParser.Json.class)
    public Result create() throws Exception {
        JsonNode j = Controller.request().body().asJson();
        String mensaje = "DE: " + j.findValue("remitente") + " PARA: ";
        for (JsonNode s : j.findValue("destinatarios"))
            mensaje += s.findValue("correo") + ";";
        mensaje += "ASUNTO: " + j.findValue("asunto") + ";" + "CUERPO: " + j.findValue("cuerpo");
        //System.out.println(mensaje);
        out.write(mensaje + "\n");
        //Logger.info(mensaje);
        return ok("");
    }

    public Result read() {
        return ok("");
    }
}
