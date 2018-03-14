package controllers;

import com.avaje.ebean.Model;
import com.fasterxml.jackson.databind.JsonNode;
import models.Ciudad;
import models.Mueble;
import play.libs.Json;
import play.mvc.BodyParser;
import play.mvc.Controller;
import play.mvc.Result;

import java.util.List;

/**
 * Created by scvalencia606 on 8/10/15.
 */
public class MuebleController extends Controller {

    @BodyParser.Of(BodyParser.Json.class)
    public Result create() {
        JsonNode j = Controller.request().body().asJson();
        String mensaje="DE: "+j.findValue("remitente")+" PARA: ";
        for(JsonNode s:j.findValue("destinatarios"))
            mensaje+=s.findValue("correo")+";";
        mensaje+="ASUNTO: "+j.findValue("asunto")+";"+"CUERPO: "+j.findValue("cuerpo");
        return ok(mensaje);
    }

    public Result read() {
        List<Mueble> muebles = new Model.Finder(String.class, Mueble.class).all();
        return ok(Json.toJson(muebles));
    }
}
