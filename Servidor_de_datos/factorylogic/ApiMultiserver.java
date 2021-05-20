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
import java.util.SortedSet;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author LRK
 */
public class ApiMultiserver implements Runnable {

    private ServerSocket serverSocket;
    private SortedSet data;
    private Thread t;
    private int port;

    public ApiMultiserver(SortedSet data) {
        this.data = data;
    }

    public void start(int port) throws IOException {
        System.out.println("Starting API");
        this.port = port;
        if (t == null) {
            t = new Thread(this);
            t.start();
        }
    }

    public void stop() throws IOException {
        serverSocket.close();
    }

    @Override
    public void run() {
        try {
            serverSocket = new ServerSocket(port);
            while (true) {
                new ApiMultiHandler(serverSocket.accept(), data).start();
            }
        } catch (IOException ex) {
            Logger.getLogger(ApiMultiserver.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private static class ApiMultiHandler extends Thread {

        private Socket clientSocket;
        private PrintWriter out;
        private BufferedReader in;
        private SortedSet data;

        public ApiMultiHandler(Socket socket, SortedSet data) {
            this.data = data;
            this.clientSocket = socket;
        }

        @Override
        public void run() {
            try {
                in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                String command = in.readLine();
                System.out.println("line");
                if (command != null) {
                    System.out.println(command);
                    out = new PrintWriter(clientSocket.getOutputStream(), true);
                }
                if (command != null && command.startsWith("get_updates(")) {
                    System.out.println("ksdfgbnasif");
                    if (command.equals("get_updates()")) {
                        sendData();
                    }else{
                        String[] arr1 = command.split("[(]");
                        String[] arr2 = arr1[1].split("[)]");
                        Timestamp tp1 = new Timestamp(System.currentTimeMillis());
                        tp1.setTime(Long.parseLong(arr2[0]));
                        sendData(tp1);
                    }
                }

                out.close();
                in.close();
                clientSocket.close();
            } catch (IOException ex) {
                Logger.getLogger(Api.class.getName()).log(Level.SEVERE, null, ex);
            }

        }

        private void sendData() throws IOException {

            String message = "[";
            synchronized (data) {
                for (Object dt : data) {
                    ObjectMapper mapper = new ObjectMapper();
                    //Converting the Object to JSONString
                    String jsonString = mapper.writeValueAsString(dt);
                    message += (jsonString + ",");
                }
            }
            message = message.substring(0, message.length() - 1);
            message+= "]";
            out.println(message);

        }

        private void sendData(Timestamp timestamp) throws IOException {
            String message = "[";
            DataEntry comp = new DataEntry(timestamp, 0, 0, null, 0);
            synchronized (data) {
                for (Object dt : data) {
                    if (comp.compareTo((DataEntry) dt) < 0) {
                        ObjectMapper mapper = new ObjectMapper();
                        //Converting the Object to JSONString
                        String jsonString = mapper.writeValueAsString(dt);
                        message += (jsonString + ",");
                    }
                }
            }
            message = message.substring(0, message.length() - 1);
            message+= "]";
            out.println(message);
        }

    }

}
