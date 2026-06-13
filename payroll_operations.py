import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "employees.txt"

from payroll_data import (
    employee_ids,
    employee_names,
    employee_ages,
    basic_salaries,
    overtime_hours,
    overtime_pays,
    income_taxes,
    sss_deductions,
    philhealth_deductions,
    pagibig_deductions,
    gross_pays,
    net_pays,
    save_employees
)

LIGHTBLUE = "#B0E2FF"
LIGHTPINK = "#FFAEB9"


# =====================================================
# PAYROLL CALCULATIONS
# =====================================================

def calculate_payroll(salary, overtime):

    overtime_rate = 150

    overtime_pay = overtime * overtime_rate

    gross_pay = salary + overtime_pay

    income_tax = gross_pay * 0.10
    sss = gross_pay * 0.04
    philhealth = gross_pay * 0.02
    pagibig = gross_pay * 0.01

    total_deductions = (
        income_tax +
        sss +
        philhealth +
        pagibig
    )

    net_pay = gross_pay - total_deductions

    return (
        overtime_pay,
        income_tax,
        sss,
        philhealth,
        pagibig,
        gross_pay,
        net_pay
    )


# =====================================================
# ADD EMPLOYEE
# =====================================================

def open_add_employee(root):

    win = tk.Toplevel(root)
    win.title("Add Employee")
    win.geometry("450x550")
    win.configure(bg="white")

    frame = tk.Frame(win, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="ADD EMPLOYEE",
        font=("Arial", 22, "bold"),
        fg=LIGHTBLUE,
        bg="white"
    ).pack(pady=10)

    def labeled_entry(label):

        tk.Label(
            frame,
            text=label,
            bg="white"
        ).pack()

        entry = tk.Entry(
            frame,
            width=25,
            font=("Arial", 12)
        )

        entry.pack(pady=5)

        return entry

    id_entry = labeled_entry("Employee ID")
    name_entry = labeled_entry("Employee Name")
    age_entry = labeled_entry("Age")
    salary_entry = labeled_entry("Basic Salary")
    overtime_entry = labeled_entry("Overtime Hours")

    def save():

        emp_id = id_entry.get().strip()
        name = name_entry.get().strip()

        if not emp_id or not name:
            messagebox.showerror(
                "Error",
                "Please complete all fields."
            )
            return

        if emp_id in employee_ids:
            messagebox.showerror(
                "Error",
                "Employee ID already exists."
            )
            return

        try:
            age = int(age_entry.get())
            salary = float(salary_entry.get())
            overtime = float(overtime_entry.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid numeric input."
            )
            return

        (
            overtime_pay,
            income_tax,
            sss,
            philhealth,
            pagibig,
            gross_pay,
            net_pay
        ) = calculate_payroll(
            salary,
            overtime
        )

        employee_ids.append(emp_id)
        employee_names.append(name)
        employee_ages.append(age)

        basic_salaries.append(salary)
        overtime_hours.append(overtime)

        overtime_pays.append(overtime_pay)

        income_taxes.append(income_tax)
        sss_deductions.append(sss)
        philhealth_deductions.append(philhealth)
        pagibig_deductions.append(pagibig)

        gross_pays.append(gross_pay)
        net_pays.append(net_pay)

        save_employees()

        messagebox.showinfo(
            "Success",
            "Employee added successfully."
        )

        win.destroy()

    tk.Button(
        frame,
        text="SAVE",
        bg=LIGHTBLUE,
        fg="white",
        width=15,
        command=save
    ).pack(pady=15)


# =====================================================
# VIEW EMPLOYEES
# =====================================================

def open_view_employees(root):

    win = tk.Toplevel(root)
    win.title("View Employees")
    win.geometry("1000x500")

    columns = (
        "ID",
        "Name",
        "Age",
        "Salary",
        "OT Hours",
        "Gross Pay",
        "Net Pay"
    )

    tree = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    tree.pack(
        fill="both",
        expand=True
    )

    for col in columns:
        tree.heading(col, text=col)

    for i in range(len(employee_ids)):

        tree.insert(
            "",
            "end",
            values=(
                employee_ids[i],
                employee_names[i],
                employee_ages[i],
                basic_salaries[i],
                overtime_hours[i],
                gross_pays[i],
                net_pays[i]
            )
        )


# =====================================================
# SEARCH EMPLOYEE
# =====================================================

def open_search_employee(root):

    win = tk.Toplevel(root)
    win.title("Search Employee")
    win.geometry("500x500")

    tk.Label(
        win,
        text="Employee ID"
    ).pack(pady=5)

    id_entry = tk.Entry(win)
    id_entry.pack()

    result = tk.Text(
        win,
        width=50,
        height=15
    )

    result.pack(pady=10)

    def search():

        emp_id = id_entry.get().strip()

        result.delete(
            "1.0",
            tk.END
        )

        if emp_id not in employee_ids:

            result.insert(
                tk.END,
                "Employee not found."
            )

            return

        i = employee_ids.index(emp_id)

        result.insert(
            tk.END,
            f"Employee ID: {employee_ids[i]}\n"
        )

        result.insert(
            tk.END,
            f"Name: {employee_names[i]}\n"
        )

        result.insert(
            tk.END,
            f"Age: {employee_ages[i]}\n"
        )

        result.insert(
            tk.END,
            f"Basic Salary: ₱{basic_salaries[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"Overtime Pay: ₱{overtime_pays[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"Income Tax: ₱{income_taxes[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"SSS: ₱{sss_deductions[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"PhilHealth: ₱{philhealth_deductions[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"Pag-IBIG: ₱{pagibig_deductions[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"Gross Pay: ₱{gross_pays[i]:,.2f}\n"
        )

        result.insert(
            tk.END,
            f"Net Pay: ₱{net_pays[i]:,.2f}\n"
        )

    tk.Button(
        win,
        text="SEARCH",
        command=search
    ).pack(pady=10)


# =====================================================
# DELETE EMPLOYEE
# =====================================================

def open_delete_employee(root):

    emp_id = tk.simpledialog.askstring(
        "Delete Employee",
        "Enter Employee ID"
    )

    if not emp_id:
        return

    if emp_id not in employee_ids:

        messagebox.showerror(
            "Error",
            "Employee not found."
        )

        return

    i = employee_ids.index(emp_id)

    for lst in (
        employee_ids,
        employee_names,
        employee_ages,
        basic_salaries,
        overtime_hours,
        overtime_pays,
        income_taxes,
        sss_deductions,
        philhealth_deductions,
        pagibig_deductions,
        gross_pays,
        net_pays
    ):
        lst.pop(i)

    save_employees()

    messagebox.showinfo(
        "Success",
        "Employee deleted."
    )


# =====================================================
# UPDATE EMPLOYEE
# =====================================================

def open_update_employee(root):

    messagebox.showinfo(
        "Notice",
        "Double-click employee in View Employees to edit."
    )


# =====================================================
# PAYROLL SUMMARY
# =====================================================

def open_payroll_summary(root):

    total_employees = len(employee_ids)

    total_gross = sum(gross_pays)
    total_net = sum(net_pays)

    total_tax = sum(income_taxes)
    total_sss = sum(sss_deductions)
    total_philhealth = sum(philhealth_deductions)
    total_pagibig = sum(pagibig_deductions)

    messagebox.showinfo(
        "Payroll Summary",

        f"Total Employees: {total_employees}\n\n"

        f"Gross Payroll: ₱{total_gross:,.2f}\n"
        f"Net Payroll: ₱{total_net:,.2f}\n\n"

        f"Income Tax: ₱{total_tax:,.2f}\n"
        f"SSS: ₱{total_sss:,.2f}\n"
        f"PhilHealth: ₱{total_philhealth:,.2f}\n"
        f"Pag-IBIG: ₱{total_pagibig:,.2f}"
    )