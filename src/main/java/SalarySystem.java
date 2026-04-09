import java.util.Scanner;

public class SalarySystem {
    static final int    MAX_EMPLOYEES   = 100;
    static final double OVERTIME_RATE   = 1.5;  // 1.5x hourly rate
    static final double REGULAR_HOURS   = 8.0;  // Regular hours per day

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

        boolean running = true;
        while (running) {
            showMenu();
            String choice = scanner.nextLine().trim();
            switch (choice) {
                case "1": addEmployee();      break;
                case "2": viewPayroll();      break;
                case "3": viewSummary();      break;
                case "4": searchEmployee();   break;
                case "5": running = false;
                          System.out.println("\n  Thank you for using our service!\n");
                          break;
                default:  System.out.println("\n  [!] Invalid choice. Enter 1-5.");
            }
        }
    }
    static void showMenu() {
        System.out.println("==================================");
        System.out.println("|             MENU               |");
        System.out.println("==================================");
        System.out.println("|  1. Add Employee               |");
        System.out.println("|  2. View Payroll Records       |");
        System.out.println("|  3. View Payroll Summary       |");
        System.out.println("|  4. Search Employee            |");
        System.out.println("|  5. Exit                       |");
        System.out.println("==================================");
        System.out.print("  Enter choice: ");
        System.out.println("Ang ganda ko");
    }
    static void addEmployee() {
        if (count >= MAX_EMPLOYEES) {
            System.out.println("\n  [!] Employee limit reached.");
            return;
        }

        printHeader("ADD EMPLOYEE");

        String name = promptNonEmpty("  Employee Name   : ");

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
        System.out.printf ("  %-22s ₱%,.2f%n", "Basic Pay:",      computed[0]);
        System.out.printf ("  %-22s ₱%,.2f%n", "Overtime Pay:",   computed[1]);
        System.out.println("  ============================");
        System.out.printf ("  %-22s ₱%,.2f%n", "Net Pay:",        computed[2]);
        System.out.println("  ============================");
        System.out.println("\n  [✓] Employee record added.");
    }
    static void viewPayroll() {
        printHeader("PAYROLL RECORDS");

        if (count == 0) {
            System.out.println("  No employee records yet.");
            return;
        }

        System.out.printf("  %-4s %-18s %8s %8s %12s %12s %12s%n",
            "No.", "Name", "Rate", "Hours", "Basic Pay", "OT Pay", "Net Pay");
        printDivider(82);

        for (int i = 0; i < count; i++) {
            System.out.printf("  %-4d %-18s %8.2f %8.2f %12.2f %12.2f %12.2f%n",
                (i + 1),
                names[i],
                hourlyRates[i],
                hoursWorked[i],
                basicPay[i],
                overtimePay[i],
                netPay[i]);
        }

        printDivider(82);
        System.out.printf("  Total employees: %d%n", count);
    }
    static void viewSummary() {
        printHeader("PAYROLL SUMMARY");

        if (count == 0) {
            System.out.println("  No employee records yet.");
            return;
        }

        double totalBasic    = 0;
        double totalOvertime = 0;
        double totalNet      = 0;
        double highestNet    = netPay[0];
        double lowestNet     = netPay[0];
        String highName      = names[0];
        String lowName       = names[0];

        for (int i = 0; i < count; i++) {
            totalBasic    += basicPay[i];
            totalOvertime += overtimePay[i];
            totalNet      += netPay[i];

            if (netPay[i] > highestNet) { highestNet = netPay[i]; highName = names[i]; }
            if (netPay[i] < lowestNet)  { lowestNet  = netPay[i]; lowName  = names[i]; }
        }

        double avgNet = totalNet / count;

        System.out.println("  =============================");
        System.out.printf ("  %-24s ₱%,.2f%n",  "Total Basic Pay:",     totalBasic);
        System.out.printf ("  %-24s ₱%,.2f%n",  "Total Overtime Pay:",  totalOvertime);
        System.out.println("  =============================");
        System.out.printf ("  %-24s ₱%,.2f%n",  "Total Net Pay:",       totalNet);
        System.out.printf ("  %-24s ₱%,.2f%n",  "Average Net Pay:",     avgNet);
        System.out.println("  =============================");
        System.out.printf ("  %-24s %s (₱%,.2f)%n", "Highest Earner:", highName, highestNet);
        System.out.printf ("  %-24s %s (₱%,.2f)%n", "Lowest Earner:",  lowName,  lowestNet);
        System.out.println("  =============================");
        System.out.printf ("  %-24s %d%n",       "Total Employees:",     count);
    }

    static void searchEmployee() {
        printHeader("SEARCH EMPLOYEE");

        String keyword = promptNonEmpty("  Enter name to search: ").toLowerCase();

        boolean found = false;
        System.out.printf("  %-4s %-18s %8s %8s %12s %12s %12s%n",
            "No.", "Name", "Rate", "Hours", "Basic Pay", "OT Pay", "Net Pay");
        printDivider(82);

        for (int i = 0; i < count; i++) {
            if (names[i].toLowerCase().contains(keyword)) {
                System.out.printf("  %-4d %-18s %8.2f %8.2f %12.2f %12.2f %12.2f%n",
                    (i + 1),
                    names[i],
                    hourlyRates[i],
                    hoursWorked[i],
                    basicPay[i],
                    overtimePay[i],
                    netPay[i]);
                found = true;
            }
        }

        if (!found) System.out.println("  No matching employee found.");
    }
    static double[] computePay(double rate, double hours) {
        double basic    = 0;
        double overtime = 0;

        if (hours <= REGULAR_HOURS) {
            basic = rate * hours;
        } else {
            basic    = rate * REGULAR_HOURS;
            overtime = rate * OVERTIME_RATE * (hours - REGULAR_HOURS);
        }

        double net = basic + overtime;
        return new double[]{ basic, overtime, net };
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