import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import tkinter as tk
from tkinter import messagebox

# Load dataset
df = pd.read_csv(r"C:\Users\Preeti\OneDrive\Desktop\kkk\fule_price.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("(", "").str.replace(")", "")

print("Columns:", df.columns)

# Remove date
if "date" in df.columns:
    df = df.drop(columns=["date"])

# Encode categorical
le_country = LabelEncoder()
le_region = LabelEncoder()
le_income = LabelEncoder()
le_subsidy = LabelEncoder()

df["country"] = le_country.fit_transform(df["country"])
df["region"] = le_region.fit_transform(df["region"])
df["income_level"] = le_income.fit_transform(df["income_level"])
df["subsidy_level"] = le_subsidy.fit_transform(df["subsidy_level"])

# Features & target
X = df.drop(columns=["petrol_usd_liter"])
y = df["petrol_usd_liter"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ BETTER MODEL
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)

# ---------------- GUI ---------------- #

def predict():
    try:
        country = le_country.transform([entry_country.get()])[0]
        region = le_region.transform([entry_region.get()])[0]
        income = le_income.transform([entry_income.get()])[0]
        subsidy = le_subsidy.transform([entry_subsidy.get()])[0]

        diesel = float(entry_diesel.get())
        lpg = float(entry_lpg.get())
        brent = float(entry_brent.get())
        tax = float(entry_tax.get())

        input_data = [[
            country, region, income, subsidy,
            diesel, lpg, brent, tax
        ]]

        prediction = model.predict(input_data)

        messagebox.showinfo(
            "Prediction Result",
            f"Predicted Petrol Price: {prediction[0]:.3f}\n\nModel Accuracy: {accuracy:.2f}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = tk.Tk()
root.title("Fuel Price Prediction")

labels = [
    "Country", "Region", "Income Level", "Subsidy Level",
    "Diesel Price", "LPG Price", "Brent Price", "Tax %"
]

entries = []

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    entries.append(entry)

(entry_country, entry_region, entry_income, entry_subsidy,
 entry_diesel, entry_lpg, entry_brent, entry_tax) = entries

tk.Button(root, text="Predict", command=predict).grid(row=8, column=1)

root.mainloop()