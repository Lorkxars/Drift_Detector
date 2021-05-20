package factorylogic;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.sql.Timestamp;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author LRK
 */
public class Api implements Runnable {

    private Thread t;
    private List data;

    public Api(List data) {
        this.data = data;
    }

    @Override
    public void run() {
        try {
            int portNumber = 8080;
            ServerSocket serverSocket = new ServerSocket(portNumber);
            Socket clientSocket = serverSocket.accept();
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            String command = in.readLine();
            System.out.println("line");
             if (command != null){
                 System.out.println(command);
             }
            if (command != null && command.startsWith("get_updates(")) {
                System.out.println("ksdfgbnasif");
                if (command.equals("get_updates()")) {
                    sendData(clientSocket);
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(Api.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    public void start() {
        System.out.println("Starting API");
        if (t == null) {
            t = new Thread(this);
            t.start();
        }
        
    }

    private void sendData(Socket clientSocket) throws IOException {
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        String message = "";
        synchronized (data) {
            for (Object dt : data) {
                ObjectMapper mapper = new ObjectMapper();
                //Converting the Object to JSONString
                String jsonString = mapper.writeValueAsString(dt);
                message += (jsonString + "\n");
            }
        }
        out.println(message);
    }

    private void sendData(Socket clientSocket, Timestamp timestamp) throws IOException {
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

    }

}
