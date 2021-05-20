package factorylogic;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author LRK
 */
public class DataFactory {
    
    static int port = 8090;

    public static void main(String args[]) {
        try {
            //List entries = Collections.synchronizedList(new ArrayList());;
            SortedSet<DataEntry> entries = Collections.synchronizedSortedSet(new TreeSet<DataEntry>());
            
            DataCreator T1 = new DataCreator(entries);
            T1.start();

            DataCreator T2 = new DataCreator(entries);
            T2.start();

            DataCreator T3 = new DataCreator(entries);
            T3.start();
            
            ApiMultiserver api = new ApiMultiserver(entries);
            api.start(port);

            System.out.println("MP");
            while (true) {
                TimeUnit.SECONDS.sleep(10);
                System.out.println("Printing: ");
                synchronized (entries) {
                    for (Object dt : entries) {
                        ObjectMapper mapper = new ObjectMapper();
                        //Converting the Object to JSONString
                        String jsonString = mapper.writeValueAsString(dt);
                        System.out.println(jsonString);
                    }
                }
            }

        } catch (InterruptedException ex) {
            Logger.getLogger(DataFactory.class.getName()).log(Level.SEVERE, null, ex);
//        } catch (JsonProcessingException ex) {
//            Logger.getLogger(DataFactory.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(DataFactory.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
