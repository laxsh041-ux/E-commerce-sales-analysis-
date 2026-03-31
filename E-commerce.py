import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

np.random.seed(42)
random.seed(42)

num_records = 3000

products = [
    ("P001", "Mobile Phone"),
    ("P002", "Laptop"),
    ("P003", "Headphones"),
    ("P004", "Smart Watch"),
    ("P005", "Keyboard"),
    ("P006", "Mouse"),
    ("P007", "Tablet"),
    ("P008", "Charger"),
    ("P009", "Power Bank"),
    ("P010", "Bluetooth Speaker")
]

countries = ["India", "USA", "UK", "Germany", "France", "Canada", "Australia"]

data = []
start_date = datetime(2024, 1, 1)

for i in range(num_records):
    product = random.choice(products)

    invoice_no = f"INV{100000 + i}"
    stock_code = product[0]
    description = product[1]
    quantity = np.random.randint(1, 10)
    invoice_date = start_date + timedelta(days=np.random.randint(0, 365),
                                          hours=np.random.randint(0, 24))
    unit_price = round(np.random.uniform(100, 1500), 2)
    customer_id = np.random.randint(1000, 1100)
    country = random.choice(countries)

    data.append([
        invoice_no, stock_code, description, quantity,
        invoice_date, unit_price, customer_id, country
    ])

columns = ["InvoiceNo", "StockCode", "Description", "Quantity",
           "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

df = pd.DataFrame(data, columns=columns)

# Add some missing values
for col in ["Description", "CustomerID"]:
    df.loc[df.sample(frac=0.01).index, col] = np.nan

print("Dataset created!")

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day
df["Hour"] = df["InvoiceDate"].dt.hour

df["Sales"] = df["Quantity"] * df["UnitPrice"]

print("Data preprocessing completed!")


top_products = df.groupby("Description")["Sales"].sum().sort_values(ascending=False).head(10)
sales_by_country = df.groupby("Country")["Sales"].sum().sort_values(ascending=False)
sales_by_month = df.groupby("Month")["Sales"].sum()
top_customers = df.groupby("CustomerID")["Sales"].sum().sort_values(ascending=False).head(5)

print("\nTop Products:\n", top_products)
print("\nSales by Country:\n", sales_by_country)
print("\nTop Customers:\n", top_customers)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

axes[0, 0].plot(sales_by_month.index, sales_by_month.values, marker='o')
axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Total Sales")
axes[0, 0].grid(True)

axes[0, 1].bar(top_products.index, top_products.values)
axes[0, 1].set_title("Top 10 Products by Sales")
axes[0, 1].set_xlabel("Product")
axes[0, 1].set_ylabel("Sales")
axes[0, 1].tick_params(axis='x', rotation=45)

axes[1, 0].pie(sales_by_country.values, labels=sales_by_country.index, autopct="%1.1f%%")
axes[1, 0].set_title("Sales by Country")

pivot_table = df.pivot_table(values="Sales", index="Day", columns="Hour", aggfunc="sum", fill_value=0)

im = axes[1, 1].imshow(pivot_table, aspect='auto')
axes[1, 1].set_title("Heatmap of Sales by Day and Hour")
axes[1, 1].set_xlabel("Hour of Day")
axes[1, 1].set_ylabel("Day of Month")

fig.colorbar(im, ax=axes[1, 1], label="Sales")

plt.tight_layout()
plt.show()

df.to_csv("ecommerce_sales_dataset.csv", index=False)
print("\nDataset saved as ecommerce_sales_dataset.csv")








	
