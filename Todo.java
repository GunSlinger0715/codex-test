import java.io.*;
import java.nio.file.*;
import java.time.*;
import java.time.format.DateTimeParseException;
import java.util.*;

public class Todo {
    static final String DATA_FILE = "tasks.csv";
    static final List<String> PRIORITIES = Arrays.asList("low", "med", "high");

    static class Task {
        int id;
        String title;
        String priority;
        String due;
        boolean completed;
        String created;

        Task(int id, String title, String priority, String due, boolean completed, String created) {
            this.id = id;
            this.title = title;
            this.priority = priority;
            this.due = due == null ? "" : due;
            this.completed = completed;
            this.created = created;
        }

        static Task fromCsv(String line) {
            String[] p = line.split(",", -1);
            return new Task(Integer.parseInt(p[0]), p[1], p[2], p[3], Boolean.parseBoolean(p[4]), p[5]);
        }

        String toCsv() {
            return String.join(",", String.valueOf(id), title, priority, due, String.valueOf(completed), created);
        }
    }

    static List<Task> load() {
        List<Task> tasks = new ArrayList<>();
        if (!Files.exists(Path.of(DATA_FILE))) return tasks;
        try (BufferedReader br = Files.newBufferedReader(Path.of(DATA_FILE))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (!line.trim().isEmpty()) tasks.add(Task.fromCsv(line));
            }
        } catch (IOException e) {
            System.out.println("Load error: " + e.getMessage());
        }
        return tasks;
    }

    static void save(List<Task> tasks) {
        try (BufferedWriter bw = Files.newBufferedWriter(Path.of(DATA_FILE))) {
            for (Task t : tasks) bw.write(t.toCsv() + System.lineSeparator());
        } catch (IOException e) {
            System.out.println("Save error: " + e.getMessage());
        }
    }

    static int nextId(List<Task> tasks) {
        return tasks.stream().mapToInt(t -> t.id).max().orElse(0) + 1;
    }

    static String isoNow() {
        return LocalDateTime.now().withNano(0).toString();
    }

    static String readLine(Scanner sc, String prompt) {
        System.out.print(prompt);
        return sc.nextLine().trim();
    }

    static String pickPriority(Scanner sc, String current) {
        String in = readLine(sc, "Priority [low/med/high] (" + current + "): ").toLowerCase();
        if (in.isEmpty()) return current;
        if (!PRIORITIES.contains(in)) {
            System.out.println("Invalid priority; keeping current.");
            return current;
        }
        return in;
    }

    static String readDate(Scanner sc, String prompt, String current) {
        String in = readLine(sc, prompt + " (YYYY-MM-DD or blank): ");
        if (in.isEmpty()) return current;
        try {
            LocalDate.parse(in);
            return in;
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date; keeping current.");
            return current;
        }
    }

    static void list(List<Task> tasks) {
        if (tasks.isEmpty()) {
            System.out.println("No tasks.");
            return;
        }
        System.out.println("\nID  Status  Pri  Due        Title");
        for (Task t : tasks) {
            String status = t.completed ? "DONE" : "OPEN";
            String due = t.due.isEmpty() ? "—" : t.due;
            System.out.printf("%-3d %-6s  %-3s  %-10s %s%n", t.id, status, t.priority.substring(0, 3), due, t.title);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        List<Task> tasks = load();

        while (true) {
            System.out.println("\n=== To-Do List ===");
            System.out.println("1. Add task");
            System.out.println("2. List tasks");
            System.out.println("3. Mark complete");
            System.out.println("4. Remove task");
            System.out.println("5. Edit task");
            System.out.println("0. Exit");

            String ch = readLine(sc, "Choose: ");
            switch (ch) {
                case "1": {
                    String title = readLine(sc, "Task title: ");
                    if (title.isEmpty()) {
                        System.out.println("Title required.");
                        break;
                    }
                    String pr = pickPriority(sc, "med");
                    String due = readDate(sc, "Due date", "");
                    tasks.add(new Task(nextId(tasks), title, pr, due, false, isoNow()));
                    save(tasks);
                    System.out.println("Added task.");
                    break;
                }
                case "2": list(tasks); break;
                case "3": {
                    int id = Integer.parseInt(readLine(sc, "Task ID: "));
                    tasks.stream().filter(t -> t.id == id).findFirst().ifPresent(t -> t.completed = true);
                    save(tasks);
                    System.out.println("Task marked complete.");
                    break;
                }
                case "4": {
                    int id = Integer.parseInt(readLine(sc, "Task ID: "));
                    tasks.removeIf(t -> t.id == id);
                    save(tasks);
                    System.out.println("Task removed.");
                    break;
                }
                case "5": {
                    int id = Integer.parseInt(readLine(sc, "Task ID: "));
                    for (Task t : tasks) {
                        if (t.id == id) {
                            String newTitle = readLine(sc, "New title (blank to keep): ");
                            if (!newTitle.isEmpty()) t.title = newTitle;
                            t.priority = pickPriority(sc, t.priority);
                            t.due = readDate(sc, "New due date", t.due);
                        }
                    }
                    save(tasks);
                    System.out.println("Task updated.");
                    break;
                }
                case "0": return;
                default: System.out.println("Invalid choice.");
            }
        }
    }
}
