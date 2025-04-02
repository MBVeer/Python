from finance_analyzer.expense_tracker import ExpenseTracker
from finance_analyzer.investment_analyzer import InvestmentAnalyzer
from finance_analyzer.loan_calculator import LoanCalculator

def main():
    while True:
        print("\n=== Finance Analyzer ===")
        print("1. Expense Tracking")
        print("2. Investment Analysis")
        print("3. Loan Calculator")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            expense_tracker = ExpenseTracker()
            expense_tracker.run()
        elif choice == '2':
            investment_analyzer = InvestmentAnalyzer()
            investment_analyzer.run()
        elif choice == '3':
            loan_calculator = LoanCalculator()
            loan_calculator.run()
        elif choice == '4':
            print("Thank you for using Finance Analyzer!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 