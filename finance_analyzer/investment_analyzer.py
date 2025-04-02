class InvestmentAnalyzer:
    def calculate_compound_interest(self, principal, rate, time, compounds_per_year):
        rate = rate / 100  # Convert percentage to decimal
        amount = principal * (1 + rate/compounds_per_year)**(compounds_per_year * time)
        return amount

    def calculate_roi(self, initial_investment, final_value):
        roi = ((final_value - initial_investment) / initial_investment) * 100
        return roi

    def analyze_investment(self):
        principal = float(input("Enter initial investment amount: $"))
        rate = float(input("Enter annual interest rate (%): "))
        time = float(input("Enter time period (years): "))
        compounds_per_year = int(input("Enter number of times interest is compounded per year: "))

        final_amount = self.calculate_compound_interest(principal, rate, time, compounds_per_year)
        roi = self.calculate_roi(principal, final_amount)

        print("\nInvestment Analysis:")
        print(f"Initial Investment: ${principal:.2f}")
        print(f"Final Amount: ${final_amount:.2f}")
        print(f"Total Interest Earned: ${(final_amount - principal):.2f}")
        print(f"Return on Investment (ROI): {roi:.2f}%")

    def run(self):
        while True:
            print("\n=== Investment Analyzer ===")
            print("1. Analyze Investment")
            print("2. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == '1':
                self.analyze_investment()
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.") 