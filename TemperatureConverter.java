import java.util.Scanner;

public class TemperatureConverter {

    private static double cToF(double c) {
        return c * 9.0 / 5.0 + 32.0;
    }

    private static double fToC(double f) {
        return (f - 32.0) * 5.0 / 9.0;
    }

    private static double cToK(double c) {
        return c + 273.15;
    }

    private static double kToC(double k) {
        return k - 273.15;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("=== Temperature Converter ===");
        System.out.println("1) Celsius -> Fahrenheit");
        System.out.println("2) Fahrenheit -> Celsius");
        System.out.println("3) Celsius -> Kelvin");
        System.out.println("4) Kelvin -> Celsius");
        System.out.print("Choose option (1-4): ");

        int choice = sc.hasNextInt() ? sc.nextInt() : -1;
        if (choice < 1 || choice > 4) {
            System.out.println("Invalid option.");
            return;
        }

        System.out.print("Enter value: ");
        if (!sc.hasNextDouble()) {
            System.out.println("Invalid number.");
            return;
        }
        double val = sc.nextDouble();

        switch (choice) {
            case 1:
                System.out.printf("Result: %.2f °F%n", cToF(val));
                break;
            case 2:
                System.out.printf("Result: %.2f °C%n", fToC(val));
                break;
            case 3:
                System.out.printf("Result: %.2f K%n", cToK(val));
                break;
            case 4:
                System.out.printf("Result: %.2f °C%n", kToC(val));
                break;
        }
    }
}
