from datetime import datetime
import json
import os

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = ['Food', 'Transportation', 'Housing', 'Entertainment', 'Others']
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as f:
                self.expenses = json.load(f)

    def save_expenses(self):
        with open('expenses.json', 'w') as f:
            json.dump(self.expenses, f)

    def add_expense(self):
        amount = float(input("Enter amount: "))
        print("\nCategories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        category_index = int(input("Select category (number): ")) - 1
        description = input("Enter description: ")
        
        expense = {
            'amount': amount,
            'category': self.categories[category_index],
            'description': description,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        print("\nAll Expenses:")
        for expense in self.expenses:
            print(f"\nDate: {expense['date']}")
            print(f"Amount: ${expense['amount']:.2f}")
            print(f"Category: {expense['category']}")
            print(f"Description: {expense['description']}")

    def view_summary(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        category_totals = {}
        for category in self.categories:
            category_totals[category] = 0
            
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        
        print("\nExpense Summary by Category:")
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")
        
        total_expenses = sum(category_totals.values())
        print(f"\nTotal Expenses: ${total_expenses:.2f}")

    def add_expense_web(self, amount, category, description):
        expense = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.expenses.append(expense)
        self.save_expenses()

    def get_summary(self):
        if not self.expenses:
            return {'categories': {}, 'total': 0}
        
        category_totals = {}
        for category in self.categories:
            category_totals[category] = 0
            
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        
        return {
            'categories': category_totals,
            'total': sum(category_totals.values())
        }

    def delete_expense(self, expense_id):
        if 0 <= expense_id < len(self.expenses):
            del self.expenses[expense_id]
            self.save_expenses()
            return True
        return False

    def edit_expense(self, expense_id, amount, category, description):
        if 0 <= expense_id < len(self.expenses):
            expense = self.expenses[expense_id]
            expense['amount'] = amount
            expense['category'] = category
            expense['description'] = description
            expense['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (edited)"
            self.save_expenses()
            return True
        return False

    def run(self):
        while True:
            print("\n=== Expense Tracker ===")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. View Summary")
            print("4. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.view_summary()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.") 