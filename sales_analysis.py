import pandas as pd

# Load the sales dataset
df = pd.read_csv("sales_data.csv")

# Display dataset information
print("SALES DATA ANALYSIS")
print("-------------------")
print("Dataset shape:", df.shape)
print("Columns:", list(df.columns))

# Handle missing values
df["Product"] = df["Product"].fillna("Unknown")

# Convert sales columns to numeric values
for column in ["Quantity","Price","Total_Sales"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Calculate missing sales using quantity and price
missing = df["Total_Sales"].isna()
df.loc[missing, "Total_Sales"] = (
    df.loc[missing, "Quantity"] * df.loc[missing, "Price"]
)

# Remove duplicates and rows with missing required values
df = df.drop_duplicates()
df = df.dropna(
    subset=["Quantity", "Price", "Total_Sales"]
)

# Remove invalid negative values
df = df[
    (df["Quantity"] >= 0)
    & (df["Price"] >= 0)
    & (df["Total_Sales"] >= 0)
]

# Calculate sales metrics
total_revenue = df["Total_Sales"].sum()
total_units = df["Quantity"].sum()
average_sale = df["Total_Sales"].mean()

# Find revenue by product
product_sales = df.groupby("Product")["Total_Sales"].sum()
best_product = product_sales.idxmax()

# Display results
print(f"\nTotal Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Units Sold: {total_units}")
print(f"Average Sale Value: Rs. {average_sale:,.2f}")
print(f"Best Product: {best_product}")

print("\nRevenue by Product:")
print(product_sales.sort_values(ascending=False))

# Create the analysis report
report = f"""# Sales Data Analysis Report

## Project Overview
Analysis of sales data using Python and pandas.

## Data Cleaning
- Handled missing product names.
- Converted numeric columns.
- Calculated missing sales values when possible.
- Removed duplicate rows.
- Removed rows with missing or negative values.

## Results
- Total Revenue: Rs. {total_revenue:,.2f}
- Total Units Sold: {total_units}
- Average Sale Value: Rs. {average_sale:,.2f}
- Best Product by Revenue: {best_product}

## Revenue by Product
{product_sales.sort_values(ascending=False).to_string()}

## Conclusion
The analysis identifies total revenue and the product
generating the highest revenue.
"""

with open("analysis_report.md", "w", encoding="utf-8") as file:
    file.write(report)

print("\nReport saved as analysis_report.md")