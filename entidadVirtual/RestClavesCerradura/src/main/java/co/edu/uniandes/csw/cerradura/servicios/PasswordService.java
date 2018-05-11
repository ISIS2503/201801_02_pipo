/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package co.edu.uniandes.csw.cerradura.servicios;
import co.edu.uniandes.csw.recursos.Msg;
import co.edu.uniandes.csw.recursos.SimpleMqttClient;
import javax.ejb.Stateless;
import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.DELETE;
import javax.ws.rs.HeaderParam;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.xml.ws.WebServiceException;

/**
 *
 * @author se.cardenas
 */
@Path("/claves")
@Stateless
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class PasswordService {
    
    private static final int AGREGAR = 1;
    private static final int ACTUALIZAR = 2;
    private static final int ELIMINAR = 3;
    private static final int ELIMINAR_TODO = 4;
    
    @POST
    @Path("agregar/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg addPassword(@HeaderParam("val") Integer val, @HeaderParam("index") Integer index) {
        Msg msg = new Msg();
        if(val<0 || val>9999) {
            throw new WebServiceException("la clave ingresada no es válida");
        }
        if(index<1 || index>20) {
            throw new WebServiceException("el índice ingresado no es válido");
        }
        msg.msg = AGREGAR+";"+index+";"+val;
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
    
    @PUT
    @Path("actualizar/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg updatePassword(@HeaderParam("val") Integer val, @HeaderParam("index") Integer index) {
        Msg msg = new Msg();
        if(val<0 || val>9999) {
            throw new WebServiceException("la clave ingresada no es válida");
        }
        if(index<1 || index>20) {
            throw new WebServiceException("el índice ingresado no es válido");
        }
        msg.msg = ACTUALIZAR+";"+index+";"+val;
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
    
    @DELETE
    @Path("eliminar/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg deletePasword(@HeaderParam("index") Integer index) {
        Msg msg = new Msg();
        if(index<1 || index>20) {
            throw new WebServiceException("el índice ingresado no es válido");
        }
        msg.msg = ELIMINAR+";"+index;
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
    
    @DELETE
    @Path("eliminarTodo/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg deleteAllPasswords() {
        Msg msg = new Msg();
        msg.msg = ELIMINAR_TODO+"";
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
    
    @POST
    @Path("activar/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg activatePassword() {
        Msg msg = new Msg();
        msg.msg = "A";
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
    
    @POST
    @Path("desactivar/")
    @Produces(MediaType.APPLICATION_JSON)
    public Msg deactivatePassword() {
        Msg msg = new Msg();
        msg.msg = "D";
        //falta publicar a mosquitto
        SimpleMqttClient smc = SimpleMqttClient.getInstance();
        smc.publish(msg);
        
        return msg;
    }
}

