import java.io.*;
import java.net.*;
import java.util.*;

public class ChatServer {
    private static final int PORT = 1234;
    private static Set<Socket> clients = new HashSet<>();

    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(PORT);
        System.out.println("Server started on port " + PORT);

        while (true) {
            Socket client = server.accept();
            clients.add(client);
            System.out.println("New client connected: " + client);

            new Thread(() -> handleClient(client)).start();
        }
    }

    private static void handleClient(Socket client) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()))) {
            String msg;
            while ((msg = in.readLine()) != null) {
                System.out.println(msg);
                broadcast(msg, client);
            }
        } catch (IOException e) {
            System.out.println("Client disconnected: " + client);
        } finally {
            clients.remove(client);
        }
    }

    private static void broadcast(String msg, Socket exclude) {
        for (Socket c : clients) {
            if (c != exclude) {
                try {
                    PrintWriter out = new PrintWriter(c.getOutputStream(), true);
                    out.println(msg);
                } catch (IOException ignored) {}
            }
        }
    }
}
