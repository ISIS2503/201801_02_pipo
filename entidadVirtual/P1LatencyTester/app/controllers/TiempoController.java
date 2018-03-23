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
public class TiempoController extends Controller {

    private int prom=0;

    private int cantidad=0;

    public Result initializeProm()
    {
        String temp=prom+" "+cantidad;
        if(prom!=0)
        {
            prom=0;
            cantidad=0;
        }
        return ok(temp);

    }

    public Result read() {
        prom+=Integer.parseInt(Controller.request().getHeader("tiempo"));
        cantidad++;
        return ok("");
    }
}
