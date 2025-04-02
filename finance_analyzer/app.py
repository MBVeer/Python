from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from finance_analyzer.expense_tracker import ExpenseTracker
from finance_analyzer.investment_analyzer import InvestmentAnalyzer
from finance_analyzer.loan_calculator import LoanCalculator
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

expense_tracker = ExpenseTracker()
investment_analyzer = InvestmentAnalyzer()
loan_calculator = LoanCalculator()

@app.route('/')
def index():
    return render_template('index.html')

# Expense Tracker Routes
@app.route('/expenses')
def expenses():
    return render_template('expenses.html', 
                         expenses=expense_tracker.expenses,
                         categories=expense_tracker.categories)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        
        expense_tracker.add_expense_web(amount, category, description)
        flash('Expense added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding expense: {str(e)}', 'error')
    
    return redirect(url_for('expenses'))

@app.route('/expense_summary')
def expense_summary():
    summary = expense_tracker.get_summary()
    return jsonify(summary)

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if expense_tracker.delete_expense(expense_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Expense not found'}), 404

@app.route('/edit_expense/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    try:
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        
        if expense_tracker.edit_expense(expense_id, amount, category, description):
            return jsonify({'success': True})
        return jsonify({'error': 'Expense not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Investment Calculator Routes
@app.route('/investments')
def investments():
    return render_template('investments.html')

@app.route('/calculate_investment', methods=['POST'])
def calculate_investment():
    try:
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = float(request.form['time'])
        compounds_per_year = int(request.form['compounds_per_year'])
        
        final_amount = investment_analyzer.calculate_compound_interest(
            principal, rate, time, compounds_per_year)
        roi = investment_analyzer.calculate_roi(principal, final_amount)
        
        return jsonify({
            'principal': principal,
            'final_amount': final_amount,
            'interest_earned': final_amount - principal,
            'roi': roi
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Loan Calculator Routes
@app.route('/loans')
def loans():
    return render_template('loans.html')

@app.route('/calculate_loan', methods=['POST'])
def calculate_loan():
    try:
        principal = float(request.form['principal'])
        annual_rate = float(request.form['annual_rate'])
        years = int(request.form['years'])
        
        monthly_payment = loan_calculator.calculate_monthly_payment(
            principal, annual_rate, years)
        total_payment = monthly_payment * years * 12
        total_interest = total_payment - principal
        
        return jsonify({
            'monthly_payment': monthly_payment,
            'total_payment': total_payment,
            'total_interest': total_interest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Add these routes for saving calculations

@app.route('/save_investment', methods=['POST'])
def save_investment():
    try:
        # Save investment calculation to a JSON file
        calculation = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'principal': float(request.form['principal']),
            'rate': float(request.form['rate']),
            'time': float(request.form['time']),
            'compounds_per_year': int(request.form['compounds_per_year']),
            'final_amount': float(request.form['final_amount']),
            'interest_earned': float(request.form['interest_earned']),
            'roi': float(request.form['roi'])
        }
        
        saved_investments = []
        if os.path.exists('saved_investments.json'):
            with open('saved_investments.json', 'r') as f:
                saved_investments = json.load(f)
        
        saved_investments.append(calculation)
        with open('saved_investments.json', 'w') as f:
            json.dump(saved_investments, f)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_saved_investments')
def get_saved_investments():
    if os.path.exists('saved_investments.json'):
        with open('saved_investments.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/save_loan', methods=['POST'])
def save_loan():
    try:
        calculation = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'principal': float(request.form['principal']),
            'annual_rate': float(request.form['annual_rate']),
            'years': int(request.form['years']),
            'monthly_payment': float(request.form['monthly_payment']),
            'total_payment': float(request.form['total_payment']),
            'total_interest': float(request.form['total_interest'])
        }
        
        saved_loans = []
        if os.path.exists('saved_loans.json'):
            with open('saved_loans', 'r') as f:
                saved_loans = json.load(f)
        
        saved_loans.append(calculation)
        with open('saved_loans.json', 'w') as f:
            json.dump(saved_loans, f)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_saved_loans')
def get_saved_loans():
    if os.path.exists('saved_loans.json'):
        with open('saved_loans.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True) 