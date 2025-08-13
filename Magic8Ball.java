 import java.util.Random;
import java.util.Scanner;

public class Magic8Ball {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        String[] responses = {
            "It is certain.",
            "Without a doubt.",
            "You may rely on it.",
            "Yes, definitely.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        };

        System.out.println("🎱 Welcome to the Magic 8 Ball!");
        System.out.print("Ask me a yes or no question: ");
        scanner.nextLine(); // Read user question (but we don't actually use it)

        int index = random.nextInt(responses.length);
        System.out.println("Magic 8 Ball says: " + responses[index]);

        scanner.close();
    }
}
