package classes;

import java.text.SimpleDateFormat;
import java.util.*;

public class YaleVerification extends Thread
{
    private static HashMap<String,Date> hashMap=new HashMap<>();

    private static HashMap<String,Integer> losses=new HashMap<>();

    private static HashMap<String,List<String>> to=new HashMap<>();

    private static final String FROM="admin@yale.com";

    private int maxLosses;

    private long maxTime;

    public YaleVerification(int maxLosses,long maxTime)
    {
        this.maxLosses=maxLosses;
        this.maxTime=maxTime;
        ArrayList<String> mails=new ArrayList<>();
        mails.add("js.diaz@uniandes.edu.co");
        mails.add("ja.manrique@uniandes.edu.co");
        mails.add("cm.sarmiento10@uniandes.edu.co");
        this.to.put("Hub007",mails);
        System.out.println(to.size());
    }



    public static synchronized void newHub(String hub)
    {
        hashMap.put(hub,new Date());
        losses.put(hub,0);
    }


    public void run()
    {
        System.out.println("ENTRA "+to.size()+" "+to.get("Hub007"));
        while(true)
        {
            System.out.println("WHILE");
            for(String hub:hashMap.keySet())
            {
                System.out.println("HUB "+hub);
                if(new Date().getTime()-hashMap.get(hub).getTime()>maxTime)
                {
                    losses.put(hub,losses.get(hub)+1);
                    if(losses.get(hub)>maxLosses)
                    {
                        String msj="";
                        for(String mail:to.get(hub))
                        {
                            msj+=mail+" ";
                        }
                        String mensaje = "DE: " +FROM + " PARA: "+msj;
                        mensaje += "ASUNTO: " + "FALLA EL HUB" + ";" + "CUERPO: " + "EL HUB 007 ESTA FALLANDO EN LA FECHA "+new SimpleDateFormat("yyyy-MM-dd kk:mm:ss").format(new Date());
                        System.out.println(mensaje);
                    }
                }
            }
            try
            {
                Thread.sleep(1000);
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
        }
    }

}