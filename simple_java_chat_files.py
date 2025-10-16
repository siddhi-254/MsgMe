import zipfile

# Define file contents
chat_server_code = '''import java.io.*;
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
}'''

chat_client_code = '''import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ChatClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 1234);
             Scanner sc = new Scanner(System.in);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            System.out.print("Enter your name: ");
            String name = sc.nextLine();

            new Thread(() -> {
                String msg;
                try {
                    while ((msg = in.readLine()) != null) {
                        System.out.println(msg);
                    }
                } catch (IOException ignored) {}
            }).start();

            while (true) {
                String text = sc.nextLine();
                out.println(name + ": " + text);
            }

        } catch (IOException e) {
            System.out.println("Cannot connect to server.");
        }
    }
}'''

# Create a zip file containing both java files
zip_filename = '/mnt/data/SimpleChatApp.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.writestr('ChatServer.java', chat_server_code)
    zipf.writestr('ChatClient.java', chat_client_code)

zip_filename
