class LoanCalculator:
    def calculate_monthly_payment(self, principal, annual_rate, years):
        monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly decimal
        num_payments = years * 12
        
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        return monthly_payment

    def calculate_loan(self):
        principal = float(input("Enter loan amount: $"))
        annual_rate = float(input("Enter annual interest rate (%): "))
        years = int(input("Enter loan term (years): "))

        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        total_payment = monthly_payment * years * 12
        total_interest = total_payment - principal

        print("\nLoan Analysis:")
        print(f"Loan Amount: ${principal:.2f}")
        print(f"Monthly Payment: ${monthly_payment:.2f}")
        print(f"Total Payment: ${total_payment:.2f}")
        print(f"Total Interest: ${total_interest:.2f}")

    def run(self):
        while True:
            print("\n=== Loan Calculator ===")
            print("1. Calculate Loan")
            print("2. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == '1':
                self.calculate_loan()
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.") 