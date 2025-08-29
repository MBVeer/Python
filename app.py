from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# Store uploaded data in memory for demo purposes
data = None

@app.route('/')
def home():
    return "<h2>E-Commerce Sales Analysis & Growth Insights</h2><p>Use /upload to POST a CSV file of sales data.</p>"

@app.route('/upload', methods=['POST'])
def upload():
    global data
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    data = pd.read_csv(file)
    return 'File uploaded and data loaded!', 200

@app.route('/peak_months')
def peak_months():
    global data
    if data is None:
        return 'No data uploaded', 400
    if 'OrderDate' not in data.columns:
        return 'OrderDate column missing', 400
    data['OrderDate'] = pd.to_datetime(data['OrderDate'])
    data['Month'] = data['OrderDate'].dt.to_period('M')
    monthly_sales = data.groupby('Month')['Sales'].sum().sort_values(ascending=False)
    return jsonify(monthly_sales.head(3).to_dict())

@app.route('/top_products')
def top_products():
    global data
    if data is None:
        return 'No data uploaded', 400
    if 'Product' not in data.columns:
        return 'Product column missing', 400
    top = data.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)
    return jsonify(top.to_dict())

@app.route('/sales_trend_plot')
def sales_trend_plot():
    global data
    if data is None:
        return 'No data uploaded', 400
    data['OrderDate'] = pd.to_datetime(data['OrderDate'])
    data['Month'] = data['OrderDate'].dt.to_period('M')
    monthly_sales = data.groupby('Month')['Sales'].sum()
    plt.figure(figsize=(8,4))
    monthly_sales.plot(marker='o')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')

@app.route('/predict_next_month', methods=['GET'])
def predict_next_month():
    global data
    if data is None:
        return 'No data uploaded', 400
    data['OrderDate'] = pd.to_datetime(data['OrderDate'])
    data['Month'] = data['OrderDate'].dt.to_period('M')
    monthly_sales = data.groupby('Month')['Sales'].sum().reset_index()
    monthly_sales['MonthNum'] = range(len(monthly_sales))
    X = monthly_sales[['MonthNum']]
    y = monthly_sales['Sales']
    model = LinearRegression()
    model.fit(X, y)
    next_month = [[monthly_sales['MonthNum'].max() + 1]]
    pred = model.predict(next_month)[0]
    return jsonify({'predicted_next_month_sales': round(pred, 2)})

if __name__ == '__main__':
    app.run(debug=True) 