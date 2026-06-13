import tkinter as tk
from tkinter import messagebox

from payroll_data import load_employees
from payroll_operations import (
    open_add_employee,
    open_view_employees,
    open_search_employee,
    open_delete_employee,
    open_update_employee,
    open_payroll_summary,
)

PRIMARY = "#4A90E2"
SECONDARY = "#FFB6C1"


def exit_app(window):
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


def show_dashboard(window):

    clear_window(window)

    frame = tk.Frame(window, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="PAYROLL MANAGEMENT SYSTEM",
        font=("Arial", 26, "bold"),
        fg=PRIMARY,
        bg="white"
    ).pack(pady=20)

    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(pady=10)

    btn_style = {
        "font": ("Arial", 13, "bold"),
        "width": 22,
        "height": 2,
        "bg": PRIMARY,
        "fg": "white",
    }

    tk.Button(
        btn_frame,
        text="ADD EMPLOYEE",
        command=lambda: open_add_employee(window),
        **btn_style
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="VIEW EMPLOYEES",
        command=lambda: open_view_employees(window),
        **btn_style
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="SEARCH EMPLOYEE",
        command=lambda: open_search_employee(window),
        **btn_style
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="UPDATE EMPLOYEE",
        command=lambda: open_update_employee(window),
        **btn_style
    ).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="DELETE EMPLOYEE",
        command=lambda: open_delete_employee(window),
        **btn_style
    ).grid(row=2, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="PAYROLL SUMMARY",
        command=lambda: open_payroll_summary(window),
        **btn_style
    ).grid(row=2, column=1, padx=10, pady=10)

    tk.Button(
        frame,
        text="EXIT APP",
        width=15,
        height=2,
        font=("Arial", 12, "bold"),
        bg="red",
        fg="white",
        command=lambda: exit_app(window)
    ).pack(pady=15)


def main():

    load_employees()

    window = tk.Tk()
    window.title("Payroll Management System")
    window.geometry("900x650")
    window.configure(bg="white")

    show_dashboard(window)

    window.mainloop()


if __name__ == "__main__":
    main()