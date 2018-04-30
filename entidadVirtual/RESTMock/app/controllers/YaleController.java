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

import classes.YaleVerification;

/**
 * Created by s.guzmanm and js.diaz on 17/03/17.
 */
public class YaleController extends Controller {
    BufferedWriter out;

    private static final int TAMANO_BUFFER = 100000;

    private YaleVerification yaleVerification;


    public Result initializeControl()
    {
        if(yaleVerification==null)
        {
            yaleVerification=new YaleVerification(1,5000);
            yaleVerification.start();
        }
        else
        {
            yaleVerification=null;
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
    public Result updateHealthCheck() throws Exception {
        JsonNode j = Controller.request().body().asJson();
        yaleVerification.newHub(j.findValue("Hub").asText());
        //Logger.info(mensaje);
        return ok("");
    }

    public Result read() {
        return ok("");
    }
}
