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
    }
}
