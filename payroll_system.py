import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "employees.txt"

employees = []  # each row = full payroll record


# =====================
# PAYROLL CALCULATION
# =====================

def calculate_payroll(salary, overtime_hours):

    overtime_rate = 150
    overtime_pay = overtime_hours * overtime_rate

    gross_pay = salary + overtime_pay

    income_tax = gross_pay * 0.10
    sss = gross_pay * 0.04
    philhealth = gross_pay * 0.02

    total_deductions = income_tax + sss + philhealth
    net_pay = gross_pay - total_deductions

    return (
        overtime_pay,
        gross_pay,
        income_tax,
        sss,
        philhealth,
        total_deductions,
        net_pay
    )


# =====================
# TABLE FUNCTIONS
# =====================

def refresh_table(data=None):

    tree.delete(*tree.get_children())

    source = data if data is not None else employees

    for emp in source:
        tree.insert("", tk.END, values=emp)


def clear_fields():

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_overtime.delete(0, tk.END)


# =====================
# ADD EMPLOYEE
# =====================

def add_employee():

    try:
        name = entry_name.get().strip()
        age = int(entry_age.get())
        salary = float(entry_salary.get())
        overtime = float(entry_overtime.get())

        if not name:
            messagebox.showerror("Error", "Name required")
            return

        (
            overtime_pay,
            gross,
            income_tax,
            sss,
            philhealth,
            deductions,
            net
        ) = calculate_payroll(salary, overtime)

        employees.append([
            name,
            age,
            salary,
            overtime,
            gross,
            income_tax,
            sss,
            philhealth,
            deductions,
            net
        ])

        refresh_table()
        clear_fields()

        messagebox.showinfo("Success", "Employee Added")

    except ValueError:
        messagebox.showerror("Error", "Invalid numeric input")


# =====================
# SEARCH (SAFE VERSION)
# =====================

def search_employee():

    keyword = search_entry.get().lower().strip()

    if not keyword:
        refresh_table()
        return

    filtered = [
        emp for emp in employees
        if keyword in emp[0].lower()
    ]

    refresh_table(filtered)


# =====================
# SELECT ROW
# =====================

selected_index = None

def select_employee(event):

    global selected_index

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    # find real index in full list
    for i, emp in enumerate(employees):
        if emp == list(values):
            selected_index = i
            break

    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[0])

    entry_age.delete(0, tk.END)
    entry_age.insert(0, values[1])

    entry_salary.delete(0, tk.END)
    entry_salary.insert(0, values[2])

    entry_overtime.delete(0, tk.END)
    entry_overtime.insert(0, values[3])


# =====================
# EDIT EMPLOYEE
# =====================

def edit_employee():

    global selected_index

    if selected_index is None:
        messagebox.showwarning("Warning", "Select employee first")
        return

    try:
        name = entry_name.get().strip()
        age = int(entry_age.get())
        salary = float(entry_salary.get())
        overtime = float(entry_overtime.get())

        (
            overtime_pay,
            gross,
            income_tax,
            sss,
            philhealth,
            deductions,
            net
        ) = calculate_payroll(salary, overtime)

        employees[selected_index] = [
            name,
            age,
            salary,
            overtime,
            gross,
            income_tax,
            sss,
            philhealth,
            deductions,
            net
        ]

        refresh_table()
        clear_fields()

        messagebox.showinfo("Success", "Employee Updated")

    except ValueError:
        messagebox.showerror("Error", "Invalid input")


# =====================
# DELETE EMPLOYEE (FIXED)
# =====================

def delete_employee():

    global selected_index

    if selected_index is None:
        messagebox.showwarning("Warning", "Select employee first")
        return

    employees.pop(selected_index)

    selected_index = None

    refresh_table()
    clear_fields()

    messagebox.showinfo("Deleted", "Employee Removed")


# =====================
# PAYROLL SUMMARY
# =====================

def payroll_summary():

    total_gross = sum(emp[4] for emp in employees)
    total_tax = sum(emp[5] + emp[6] + emp[7] for emp in employees)
    total_net = sum(emp[9] for emp in employees)

    messagebox.showinfo(
        "Payroll Summary",
        f"Employees: {len(employees)}\n\n"
        f"Total Gross Pay: ₱{total_gross:,.2f}\n"
        f"Total Tax (All Deductions): ₱{total_tax:,.2f}\n"
        f"Total Net Pay: ₱{total_net:,.2f}"
    )


# =====================
# GUI
# =====================

root = tk.Tk()
root.title("Payroll Management System")
root.geometry("1200x600")

tk.Label(
    root,
    text="Payroll Management System",
    font=("Arial", 18, "bold")
).pack(pady=10)


# INPUTS
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(frame)
entry_age.grid(row=1, column=1)

tk.Label(frame, text="Salary").grid(row=2, column=0)
entry_salary = tk.Entry(frame)
entry_salary.grid(row=2, column=1)

tk.Label(frame, text="Overtime").grid(row=3, column=0)
entry_overtime = tk.Entry(frame)
entry_overtime.grid(row=3, column=1)


# BUTTONS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_employee, bg="green", fg="white").grid(row=0, column=0)
tk.Button(btn_frame, text="Edit", command=edit_employee, bg="orange").grid(row=0, column=1)
tk.Button(btn_frame, text="Delete", command=delete_employee, bg="red", fg="white").grid(row=0, column=2)
tk.Button(btn_frame, text="Summary", command=payroll_summary, bg="blue", fg="white").grid(row=0, column=3)


# SEARCH
search_frame = tk.Frame(root)
search_frame.pack()

tk.Label(search_frame, text="Search").pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)

tk.Button(search_frame, text="Search", command=search_employee).pack(side=tk.LEFT)
tk.Button(search_frame, text="Reset", command=lambda: refresh_table()).pack(side=tk.LEFT)


# TABLE
columns = (
    "Name", "Age", "Salary", "OT Hours",
    "Gross", "Tax", "SSS", "PhilHealth",
    "Deductions", "Net"
)

tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=110)

tree.pack(fill="both", expand=True)

tree.bind("<ButtonRelease-1>", select_employee)

refresh_table()

root.mainloop()