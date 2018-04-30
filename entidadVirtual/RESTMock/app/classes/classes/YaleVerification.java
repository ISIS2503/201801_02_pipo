package classes;

import java.util.*;

public class YaleVerification
{
    private static HashMap<String,Date> hashMap=new HashMap<>();

    private static HashMap<String,Integer> losses=new HashMap<>();

    private int maxLosses;

    private long maxTime;

    public YaleVerification(int maxLosses,long maxTime)
    {
        this.maxLosses=maxLosses;
        this.maxTime=maxTime;
    }



    public static synchronized void newHub(String hub)
    {
        hashMap.put(hub,new Date());
        losses.put(hub,0);
    }

    public static void main (String[] args)
    {
        YaleVerification yaleVerification=new YaleVerification(1,5000);
        while(true)
        {
            for(String hub:yaleVerification.hashMap.keySet())
            {
                if(new Date().getTime()-yaleVerification.hashMap.get(hub).getTime()>yaleVerification.maxTime)
                {
                    losses.put(hub,losses.get(hub)+1);
                    if(losses.get(hub)>yaleVerification.maxLosses)
                    {
                        System.out.println("FALLA EL HUB");
                    }
                }
            }
        }
    }

}