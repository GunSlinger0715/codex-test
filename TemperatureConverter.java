import java.util.Scanner;

public class TemperatureConverter {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Temperature Converter");
        System.out.print("Enter temperature value: ");
        if (!scanner.hasNextDouble()) {
            System.out.println("Invalid temperature.");
            scanner.close();
            return;
        }
        double value = scanner.nextDouble();
        System.out.print("Convert to (C/F): ");
        String unit = scanner.next().trim().toUpperCase();
        if (unit.equals("C")) {
            double celsius = (value - 32) * 5.0 / 9.0;
            System.out.printf("%.2f F = %.2f C%n", value, celsius);
        } else if (unit.equals("F")) {
            double fahrenheit = value * 9.0 / 5.0 + 32;
            System.out.printf("%.2f C = %.2f F%n", value, fahrenheit);
        } else {
            System.out.println("Unknown unit. Please use 'C' or 'F'.");
        }
        scanner.close();
=======

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
