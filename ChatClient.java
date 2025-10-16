import java.io.*;
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

            // Thread to listen for messages
            new Thread(() -> {
                String msg;
                try {
                    while ((msg = in.readLine()) != null) {
                        System.out.println(msg);
                    }
                } catch (IOException ignored) {}
            }).start();

            // Send messages
            while (true) {
                String text = sc.nextLine();
                out.println(name + ": " + text);
            }

        } catch (IOException e) {
            System.out.println("Cannot connect to server.");
        }
    }
}

