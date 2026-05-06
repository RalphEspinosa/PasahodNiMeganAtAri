import java.util.Scanner;
import java.io.*;
import java.nio.file.*;

public class Prototype {
    static final int    MAX_EMPLOYEES   = 100;
    static final double OVERTIME_RATE   = 1.5;
    static final double REGULAR_HOURS   = 8.0;
    static final String DATA_FILE       = "payroll_data.csv";

    static String[] names        = new String[MAX_EMPLOYEES];
    static double[] hourlyRates  = new double[MAX_EMPLOYEES];
    static double[] hoursWorked  = new double[MAX_EMPLOYEES];
    static double[] basicPay     = new double[MAX_EMPLOYEES];
    static double[] overtimePay  = new double[MAX_EMPLOYEES];
    static double[] netPay       = new double[MAX_EMPLOYEES];
    static int count = 0;

    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        printHeader("PAYROLL SYSTEM");
        loadData();

        boolean running = true;
        while (running) {
            showMenu();
            String choice = scanner.nextLine().trim();
            switch (choice) {
                case "1": addEmployee();    break;
                case "2": viewPayroll();    break;
                case "3": viewSummary();    break;
                case "4": searchEmployee(); break;
                case "5": deleteEmployee(); break;
                case "6": running = false;
                          saveData();
                          System.out.println("\n  Thank you for using our service!\n");
                          break;
                default:  System.out.println("\n  [!] Invalid choice. Enter 1-6.");
            }
        }
    }

    static void saveData() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(DATA_FILE))) {
            pw.println("name,hourlyRate,hoursWorked,basicPay,overtimePay,netPay");

            for (int i = 0; i < count; i++) {
                String safeName = "\"" + names[i].replace("\"", "\"\"") + "\"";
                pw.printf("%s,%.2f,%.2f,%.2f,%.2f,%.2f%n",
                    safeName,
                    hourlyRates[i],
                    hoursWorked[i],
                    basicPay[i],
                    overtimePay[i],
                    netPay[i]);
            }

            System.out.println("\n  [✓] Data saved to " + DATA_FILE);
        } catch (IOException e) {
            System.out.println("\n  [!] Failed to save data: " + e.getMessage());
        }
    }

    static void loadData() {
        File file = new File(DATA_FILE);
        if (!file.exists()) {
            System.out.println("  [i] No saved data found. Starting fresh.\n");
            return;
        }

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line = br.readLine();
            int loaded = 0;

            while ((line = br.readLine()) != null && count < MAX_EMPLOYEES) {
                line = line.trim();
                if (line.isEmpty()) continue;

                String[] parts = parseCSVLine(line);
                if (parts.length < 6) continue;

                names[count]       = parts[0];
                hourlyRates[count] = Double.parseDouble(parts[1]);
                hoursWorked[count] = Double.parseDouble(parts[2]);
                basicPay[count]    = Double.parseDouble(parts[3]);
                overtimePay[count] = Double.parseDouble(parts[4]);
                netPay[count]      = Double.parseDouble(parts[5]);
                count++;
                loaded++;
            }

            System.out.printf("  [✓] Loaded %d employee record(s) from %s%n%n", loaded, DATA_FILE);
        } catch (IOException | NumberFormatException e) {
            System.out.println("  [!] Failed to load data: " + e.getMessage());
        }
    }

    static String[] parseCSVLine(String line) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        StringBuilder sb = new StringBuilder();
        boolean inQuotes = false;

        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);

            if (c == '"') {
                if (inQuotes && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    sb.append('"');
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (c == ',' && !inQuotes) {
                fields.add(sb.toString());
                sb.setLength(0);
            } else {
                sb.append(c);
            }
        }
        fields.add(sb.toString());
        return fields.toArray(new String[0]);
    }

    static void manualSave() {
        saveData();
    }

    static void showMenu() {
        System.out.println("==================================");
        System.out.println("|             MENU               |");
        System.out.println("==================================");
        System.out.println("|  1. Add Employee               |");
        System.out.println("|  2. View Payroll Records       |");
        System.out.println("|  3. View Payroll Summary       |");
        System.out.println("|  4. Search Employee            |");
        System.out.println("|  5. Delete Employee            |");
        System.out.println("|  6. Save & Exit                |");
        System.out.println("==================================");
        System.out.print("  Enter choice: ");
    }

    static void addEmployee() {
        if (count >= MAX_EMPLOYEES) {
            System.out.println("\n  [!] Employee limit reached.");
            return;
        }

        printHeader("ADD EMPLOYEE");

        String name  = promptNonEmpty("  Employee Name   : ");
        double rate  = promptPositiveDouble("  Hourly Rate (₱) : ");
        double hours = promptPositiveDouble("  Hours Worked    : ");
        double[] computed = computePay(rate, hours);

        names[count]       = name;
        hourlyRates[count] = rate;
        hoursWorked[count] = hours;
        basicPay[count]    = computed[0];
        overtimePay[count] = computed[1];
        netPay[count]      = computed[2];
        count++;

        System.out.println("  ============================");
        System.out.printf ("  %-22s ₱%,.2f%n", "Basic Pay:",    computed[0]);
        System.out.printf ("  %-22s ₱%,.2f%n", "Overtime Pay:", computed[1]);
        System.out.println("  ============================");
        System.out.printf ("  %-22s ₱%,.2f%n", "Net Pay:",      computed[2]);
        System.out.println("  ============================");
        System.out.println("\n  [✓] Employee record added.");

        saveData();
    }

    static void viewPayroll() {
        printHeader("PAYROLL RECORDS");

        if (count == 0) {
            System.out.println("  No employee records yet.");
            return;
        }

        for (int i = 0; i < count; i++) {
            System.out.println("  No.        : " + (i + 1));
            System.out.println("  Name       : " + names[i]);
            System.out.println("  Rate       : " + hourlyRates[i]);
            System.out.println("  Hours      : " + hoursWorked[i]);
            System.out.println("  Basic Pay  : " + basicPay[i]);
            System.out.println("  OT Pay     : " + overtimePay[i]);
            System.out.println("  Net Pay    : " + netPay[i]);
            System.out.println();
        }

        System.out.printf("  Total employees: %d%n", count);
    }

    static void viewSummary() {
        printHeader("PAYROLL SUMMARY");

        if (count == 0) {
            System.out.println("  No employee records yet.");
            return;
        }

        double totalBasic = 0, totalOvertime = 0, totalNet = 0;
        double highestNet = netPay[0], lowestNet = netPay[0];
        String highName = names[0], lowName = names[0];

        for (int i = 0; i < count; i++) {
            totalBasic    += basicPay[i];
            totalOvertime += overtimePay[i];
            totalNet      += netPay[i];

            if (netPay[i] > highestNet) { highestNet = netPay[i]; highName = names[i]; }
            if (netPay[i] < lowestNet)  { lowestNet  = netPay[i]; lowName  = names[i]; }
        }

        double avgNet = totalNet / count;

        System.out.println("  =============================");
        System.out.printf ("  %-24s ₱%,.2f%n", "Total Basic Pay:",    totalBasic);
        System.out.printf ("  %-24s ₱%,.2f%n", "Total Overtime Pay:", totalOvertime);
        System.out.println("  =============================");
        System.out.printf ("  %-24s ₱%,.2f%n", "Total Net Pay:",      totalNet);
        System.out.printf ("  %-24s ₱%,.2f%n", "Average Net Pay:",    avgNet);
        System.out.println("  =============================");
        System.out.printf ("  %-24s %s (₱%,.2f)%n", "Highest Earner:", highName, highestNet);
        System.out.printf ("  %-24s %s (₱%,.2f)%n", "Lowest Earner:",  lowName,  lowestNet);
        System.out.println("  =============================");
        System.out.printf ("  %-24s %d%n", "Total Employees:", count);
    }

    static void searchEmployee() {
        printHeader("SEARCH EMPLOYEE");

        String keyword = promptNonEmpty("  Enter name to search: ").toLowerCase();

        boolean found = false;

        for (int i = 0; i < count; i++) {
            if (names[i].toLowerCase().contains(keyword)) {
                System.out.println("  No.        : " + (i + 1));
                System.out.println("  Name       : " + names[i]);
                System.out.println("  Rate       : " + hourlyRates[i]);
                System.out.println("  Hours      : " + hoursWorked[i]);
                System.out.println("  Basic Pay  : " + basicPay[i]);
                System.out.println("  OT Pay     : " + overtimePay[i]);
                System.out.println("  Net Pay    : " + netPay[i]);
                System.out.println();
                found = true;
            }
        }

        if (!found) System.out.println("  No matching employee found.");
    }

    static void deleteEmployee() {
        printHeader("DELETE EMPLOYEE");

        if (count == 0) {
            System.out.println("  No employee records to delete.");
            return;
        }

        viewPayroll();

        System.out.print("\n  Enter employee number to delete (0 to cancel): ");
        String input = scanner.nextLine().trim();
        int index;

        try {
            index = Integer.parseInt(input) - 1;
        } catch (NumberFormatException e) {
            System.out.println("  [!] Invalid input.");
            return;
        }

        if (index == -1) {
            System.out.println("  [i] Deletion cancelled.");
            return;
        }

        if (index < 0 || index >= count) {
            System.out.println("  [!] Invalid employee number.");
            return;
        }

        String deletedName = names[index];

        for (int i = index; i < count - 1; i++) {
            names[i]       = names[i + 1];
            hourlyRates[i] = hourlyRates[i + 1];
            hoursWorked[i] = hoursWorked[i + 1];
            basicPay[i]    = basicPay[i + 1];
            overtimePay[i] = overtimePay[i + 1];
            netPay[i]      = netPay[i + 1];
        }

        count--;
        System.out.printf("%n  [✓] Employee \"%s\" deleted.%n", deletedName);
        saveData();
    }

    static double[] computePay(double rate, double hours) {
        double basic = 0, overtime = 0;
        if (hours <= REGULAR_HOURS) {
            basic = rate * hours;
        } else {
            basic    = rate * REGULAR_HOURS;
            overtime = rate * OVERTIME_RATE * (hours - REGULAR_HOURS);
        }
        return new double[]{ basic, overtime, basic + overtime };
    }

    static void printHeader(String title) {
        System.out.println("\n  ==============================");
        System.out.printf ("  %s%n", title);
        System.out.println("  ==============================");
    }

    static void printDivider(int length) {
        System.out.print("  ");
        for (int i = 0; i < length; i++) System.out.print("─");
        System.out.println();
    }

    static String promptNonEmpty(String prompt) {
        String input = "";
        while (input.isEmpty()) {
            System.out.print(prompt);
            input = scanner.nextLine().trim();
            if (input.isEmpty()) System.out.println("  [!] This field cannot be empty.");
        }
        return input;
    }

    static double promptPositiveDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();
            try {
                double value = Double.parseDouble(input);
                if (value > 0) return value;
                System.out.println("  [!] Value must be greater than 0.");
            } catch (NumberFormatException e) {
                System.out.println("  [!] Invalid number. Please try again.");
            }
        }
    }
}
