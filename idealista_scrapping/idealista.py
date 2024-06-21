import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression


def extract_number(text):
    """Extract numerical value from text, handling European formatting."""
    text = text.replace(".", "").replace(",", ".")
    return float(re.sub(r"[^\d.]", "", text))


def parse_html_file(file_path):
    """Parse HTML file and extract listings data."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")
    listings = soup.find_all("div", class_="item-info-container")

    data = []
    for listing in listings:
        title = listing.find("a", class_="item-link").get_text(strip=True)
        price_text = listing.find("span", class_="item-price").get_text(strip=True)
        area_text = (
            listing.find("span", class_="item-detail").get_text(strip=True)
            if listing.find("span", class_="item-detail")
            else "0 m²"
        )
        address = (
            listing.find("span", class_="item-address").get_text(strip=True)
            if listing.find("span", class_="item-address")
            else "No address"
        )

        price = extract_number(price_text)
        area = extract_number(area_text)

        if area <= 3000:  # Filter out listings with area > 3000 m²
            data.append([title, price, area, address])

    return data


# Parse both HTML files
data1 = parse_html_file(
    "Viviendas venta. Viviendas alquiler. Pisos. Chalets — idealista.htm"
)
data2 = parse_html_file(
    "Viviendas venta. Viviendas alquiler. Pisos. Chalets — idealista 2.htm"
)
data3 = parse_html_file(
    "Viviendas venta. Viviendas alquiler. Pisos. Chalets — idealista 3.htm"
)
data4 = parse_html_file(
    "Viviendas venta. Viviendas alquiler. Pisos. Chalets — idealista 4.htm"
)
data5 = parse_html_file(
    "Viviendas venta. Viviendas alquiler. Pisos. Chalets — idealista 5.htm"
)

# Combine data from both files
all_data = data1 + data2 + data3 + data4 + data5

# Create a DataFrame
df = pd.DataFrame(all_data, columns=["Title", "Price (€)", "Area (m²)", "Address"])

# Calculate mean price and mean area
mean_price = df["Price (€)"].mean()
mean_area = df["Area (m²)"].mean()

# Number of buildings
num_buildings = len(df)

print(f"\nMean Price: {mean_price:.2f} €")
print(f"Mean Area: {mean_area:.2f} m²")
print(f"Total Buildings: {num_buildings}")

# Save DataFrame to Excel
df.to_excel("office_listings.xlsx", index=False)

# Scatter plot of metres squared vs. price per month with line of best fit
plt.figure(figsize=(10, 6))
plt.scatter(df["Area (m²)"], df["Price (€)"], alpha=0.5, label="Data points")

# Perform linear regression
X = df["Area (m²)"].values.reshape(-1, 1)  # Features (independent variable)
y = df["Price (€)"].values  # Target (dependent variable)
regressor = LinearRegression()
regressor.fit(X, y)

# Predict prices using the linear regression model
y_pred = regressor.predict(X)

# Plot the line of best fit
plt.plot(df["Area (m²)"], y_pred, color="red", label="Line of best fit")

plt.title("Scatter Plot of Metres Squared vs. Price per Month")
plt.xlabel("Metres Squared (m²)")
plt.ylabel("Price per Month (€)")
plt.legend()
plt.grid(True)
plt.show()

# Print the coefficients of the linear regression model
print(f"Linear Regression Coefficients:")
print(f"Intercept: {regressor.intercept_:.2f}")
print(f"Slope: {regressor.coef_[0]:.2f}")
