# E-Commerce Sales Analysis & Growth Insights

A Flask application to analyze e-commerce sales, identify peak months and top products, and provide insights for optimizing inventory and marketing strategies. Includes endpoints for real-time tracking and predictive analytics.

## Features
- Upload sales data (CSV)
- Identify peak sales months
- List top products
- Visualize sales trends
- Predict next month's sales

## Usage
1. Install dependencies:
   ```
pip install -r requirements.txt
   ```
2. Run the app:
   ```
python app.py
   ```
3. Endpoints:
   - `/upload` (POST, form-data, key: `file`): Upload your sales CSV (columns: OrderDate, Product, Sales)
   - `/peak_months`: Get top 3 peak sales months
   - `/top_products`: Get top 5 products by sales
   - `/sales_trend_plot`: View sales trend plot
   - `/predict_next_month`: Predict next month's sales

## Example CSV Format
| OrderDate   | Product   | Sales |
|-------------|-----------|-------|
| 2023-01-15  | Widget A  | 120   |
| 2023-01-20  | Widget B  | 80    |
| ...         | ...       | ...   | 