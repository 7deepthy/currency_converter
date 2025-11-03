import requests
import tkinter as tk
from tkinter import ttk, messagebox

# --- Function to get live exchange rate ---
def get_rate():
    base = base_currency.get()
    target = target_currency.get()
    amount = amount_entry.get()

    if not amount:
        messagebox.showwarning("Input Required", "Please enter an amount!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number!")
        return

    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url)
        data = response.json()

        if "rates" in data and target in data["rates"]:
            rate = data["rates"][target]
            converted = amount * rate
            rate_var.set(f"1 {base} = {rate:.4f} {target}")
            converted_var.set(f"{amount} {base} = {converted:.4f} {target}")
            status_var.set("✅ Updated successfully")
        else:
            rate_var.set("N/A")
            converted_var.set("N/A")
            status_var.set("⚠️ Unable to fetch rate")
    except Exception as e:
        rate_var.set("N/A")
        converted_var.set("N/A")
        status_var.set(f"❌ Error: {e}")


# --- Fancy background ---
def create_gradient(canvas, color1, color2):
    for i in range(0, 400):
        r = int(color1[1:3], 16) + (int(color2[1:3], 16) - int(color1[1:3], 16)) * i // 400
        g = int(color1[3:5], 16) + (int(color2[3:5], 16) - int(color1[3:5], 16)) * i // 400
        b = int(color1[5:7], 16) + (int(color2[5:7], 16) - int(color1[5:7], 16)) * i // 400
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, 420, i, fill=color)

# --- GUI Setup ---
root = tk.Tk()
root.title("💱 Global Currency Converter")
root.geometry("420x430")
root.resizable(False, False)

# Gradient background
canvas = tk.Canvas(root, width=420, height=430, highlightthickness=0)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, "#b3d9ff", "#e6f2ff")

# White Frame
frame = tk.Frame(canvas, bg="#ffffff", bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=370)

# Variables
base_currency = tk.StringVar(value="USD")
target_currency = tk.StringVar(value="INR")
rate_var = tk.StringVar()
converted_var = tk.StringVar()
status_var = tk.StringVar()

# --- Title ---
tk.Label(frame, text="🌍 Global Currency Converter", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#007acc").pack(pady=10)

# --- Frame for currency selection ---
curr_frame = tk.Frame(frame, bg="#ffffff")
curr_frame.pack(pady=10)

# 🌐 Expanded Currency List (50+)
currencies = [
    "USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD",
    "NZD", "ZAR", "AED", "SAR", "QAR", "OMR", "BHD", "KWD", "LKR", "NPR",
    "PKR", "BDT", "THB", "MYR", "IDR", "VND", "PHP", "HKD", "TWD", "KRW",
    "TRY", "ILS", "RUB", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "MXN",
    "BRL", "ARS", "CLP", "EGP", "NGN", "KES", "GHS", "COP", "UAH", "RON"
]

# From currency
ttk.Label(curr_frame, text="From:", background="#ffffff").grid(row=0, column=0, padx=5)
ttk.Combobox(curr_frame, textvariable=base_currency, values=currencies, width=12, state="readonly").grid(row=0, column=1)

# To currency
ttk.Label(curr_frame, text="To:", background="#ffffff").grid(row=0, column=2, padx=5)
ttk.Combobox(curr_frame, textvariable=target_currency, values=currencies, width=12, state="readonly").grid(row=0, column=3)

# --- Amount input ---
tk.Label(frame, text="Enter Amount:", bg="#ffffff", fg="#333333").pack()
amount_entry = tk.Entry(frame, width=20, justify="center", font=("Segoe UI", 12), relief="solid", bd=1)
amount_entry.pack(pady=5)

# --- Convert Button ---
convert_btn = tk.Button(
    frame, text="Convert", command=get_rate,
    bg="#007acc", fg="white", font=("Segoe UI", 11, "bold"),
    activebackground="#005f99", activeforeground="white",
    width=15, relief="flat", bd=0
)
convert_btn.pack(pady=10)
convert_btn.config(cursor="hand2")

# --- Result labels ---
tk.Label(frame, textvariable=converted_var, font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#007acc").pack(pady=5)
tk.Label(frame, textvariable=rate_var, font=("Segoe UI", 12), bg="#ffffff", fg="#555555").pack()
tk.Label(frame, textvariable=status_var, font=("Segoe UI", 10, "italic"), bg="#ffffff", fg="gray").pack(pady=5)

# --- Initialize ---
converted_var.set("")
status_var.set("Waiting for input...")

# --- Footer credit ---
#tk.Label(root, text="Created by Deepthy Krishnamurthy © 2025", font=("Segoe UI", 9, "italic"), bg="#e6f2ff", fg="#555").place(relx=0.5, rely=0.97, anchor="center")

root.mainloop()