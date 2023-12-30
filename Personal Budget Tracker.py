
from tabulate import tabulate
import csv
import os

class BudgetTracker:
    def __init__(self):
            self.transactions = []
            self.categories = set()
            self.file_path = "budgets_data.csv"
            self.load_data()

    def load_data(self):
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    self.transactions = list(reader)
                    self.categories = set(row['Category'] for row in self.transactions)

    def save_data(self):
            with open(self.file_path, 'w', newline='') as file:
                fieldnames = ['Category', 'Type', 'Amount']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.transactions)


    def add_transaction(self, category, transaction_type, amount):
        self.transactions.append({'Category': category, 'Type': transaction_type, 'Amount': amount})
        self.categories.add(category)
        self.save_data()

    def calculate_budget(self):
        income = sum(float(row['Amount']) for row in self.transactions if row['Type'] == 'Income')
        expenses = sum(float(row['Amount']) for row in self.transactions if row['Type'] == 'Expense')
        return income - expenses

    def analyze_expenses(self):
        expense_data = {}
        for category in self.categories:
            expenses = [float(row['Amount']) for row in self.transactions if
                        row['Category'] == category and row['Type'] == 'Expense']
            total_expense = sum(expenses)
            expense_data[category] = total_expense
        return expense_data

    def display_budget(self):
        remaining_budget = self.calculate_budget()
        print("\nRemaining Budget: ${}".format(remaining_budget))

    def display_expense_analysis(self):
        expense_data = self.analyze_expenses()
        table = []
        for category, total_expense in expense_data.items():
            table.append([category, total_expense])

        print("\nExpense Analysis:")
        print(tabulate(table, headers=['Category', 'Total Expense'], tablefmt='grid'))

    def start(self):
        while True:
            print("\n Welcome To Our Personal Budget Tracker Application\n")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Budget")
            print("4. View Expense Analysis")
            print("5. Exit")

            ch = input("Enter your choice: ")

            if ch == '5':
                print("Exiting Budget Tracker Application")
                break
            elif ch == '1':
                category = input("Enter income category: ")
                amount = float(input("Enter income amount: "))
                self.add_transaction(category, 'Income', amount)
            elif ch == '2':
                category = input("Enter expense category: ")
                amount = float(input("Enter expense amount: "))
                self.add_transaction(category, 'Expense', amount)
            elif ch == '3':
                self.display_budget()
            elif ch == '4':
                self.display_expense_analysis()
            else:
                print("Invalid choice. Please enter a number between 1 and 5")


if __name__ == "__main__":
    budget_tracker = BudgetTracker()
    budget_tracker.start()
