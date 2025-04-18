import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from db import Database

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("1000x600")
        
        self.db = Database()
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
        
        self.create_widgets()
        self.update_transactions_table()
        self.update_summary()

    def create_widgets(self):
        # Left Frame for Input
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Transaction Type
        ttk.Label(left_frame, text="Type:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(left_frame, textvariable=self.type_var, values=["Income", "Expense"])
        type_combo.grid(row=0, column=1, pady=5)
        type_combo.set("Expense")

        # Amount
        ttk.Label(left_frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.amount_var).grid(row=1, column=1, pady=5)

        # Category
        ttk.Label(left_frame, text="Category:").grid(row=2, column=0, sticky="w")
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, values=self.categories)
        category_combo.grid(row=2, column=1, pady=5)
        category_combo.set(self.categories[0])

        # Add Button
        ttk.Button(left_frame, text="Add Transaction", command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=10)

        # Export Button
        ttk.Button(left_frame, text="Export to CSV", command=self.export_to_csv).grid(row=4, column=0, columnspan=2, pady=5)

        # Right Frame for Display
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Transactions Table
        self.tree = ttk.Treeview(right_frame, columns=("ID", "Type", "Amount", "Category", "Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Summary Frame
        summary_frame = ttk.Frame(right_frame, padding="10")
        summary_frame.grid(row=1, column=0, sticky="nsew")

        self.summary_label = ttk.Label(summary_frame, text="")
        self.summary_label.grid(row=0, column=0, sticky="w")

        # Configure grid weights
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

    def add_transaction(self):
        try:
            amount = float(self.amount_var.get())
            type_ = self.type_var.get()
            category = self.category_var.get()

            if not type_ or not category:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            self.db.add_transaction(type_, amount, category)
            self.update_transactions_table()
            self.update_summary()
            self.amount_var.set("")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def update_transactions_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        transactions = self.db.get_all_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=transaction)

    def update_summary(self):
        now = datetime.now()
        monthly_summary = self.db.get_monthly_summary(now.month, now.year)
        
        income = 0
        expenses = 0
        for type_, amount in monthly_summary:
            if type_ == "Income":
                income = amount
            else:
                expenses = amount

        summary_text = f"Monthly Summary:\nIncome: ${income:.2f}\nExpenses: ${expenses:.2f}\nBalance: ${(income - expenses):.2f}"
        self.summary_label.config(text=summary_text)

    def export_to_csv(self):
        transactions = self.db.get_all_transactions()
        filename = f"budget_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Type", "Amount", "Category", "Date"])
            writer.writerows(transactions)
        
        messagebox.showinfo("Success", f"Report exported to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop() 