import os

FILE_NAME = "employees.txt"

employee_ids = []
employee_names = []
employee_ages = []
basic_salaries = []
overtime_hours = []
overtime_pays = []
income_taxes = []
sss_deductions = []
philhealth_deductions = []
pagibig_deductions = []
gross_pays = []
net_pays = []


def load_employees():
    """Load employee records from file."""

    try:
        if os.path.exists(FILE_NAME):

            with open(FILE_NAME, "r") as file:

                for line in file:

                    data = line.strip().split("|")

                    if len(data) == 12:

                        try:
                            employee_ids.append(data[0])
                            employee_names.append(data[1])
                            employee_ages.append(int(data[2]))
                            basic_salaries.append(float(data[3]))
                            overtime_hours.append(float(data[4]))
                            overtime_pays.append(float(data[5]))
                            income_taxes.append(float(data[6]))
                            sss_deductions.append(float(data[7]))
                            philhealth_deductions.append(float(data[8]))
                            pagibig_deductions.append(float(data[9]))
                            gross_pays.append(float(data[10]))
                            net_pays.append(float(data[11]))

                        except ValueError:
                            print("Invalid employee record skipped.")

    except Exception as e:
        print(f"Error loading employees: {e}")


def save_employees():
    """Save all employee records."""

    try:

        with open(FILE_NAME, "w") as file:

            for i in range(len(employee_ids)):

                file.write(
                    f"{employee_ids[i]}|"
                    f"{employee_names[i]}|"
                    f"{employee_ages[i]}|"
                    f"{basic_salaries[i]}|"
                    f"{overtime_hours[i]}|"
                    f"{overtime_pays[i]}|"
                    f"{income_taxes[i]}|"
                    f"{sss_deductions[i]}|"
                    f"{philhealth_deductions[i]}|"
                    f"{pagibig_deductions[i]}|"
                    f"{gross_pays[i]}|"
                    f"{net_pays[i]}\n"
                )

    except Exception as e:
        print(f"Error saving employees: {e}")
