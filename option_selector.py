import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_leg_info(df):
    # Ensure columns are clean and datetime is properly parsed
    df.columns = df.columns.str.strip()
    df['ExpiryDatePlus10Y'] = pd.to_datetime(df['ExpiryDatePlus10Y'], errors='coerce')

    symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY']
    option_types = sorted(df['pOptionType'].dropna().unique())
    strike_prices = sorted([s for s in df['dStrikePrice;'].dropna().unique() if 2200000 <= s <= 2600000])
    expiry_dates = sorted(df['ExpiryDatePlus10Y'].dropna().dt.strftime('%Y-%m-%d').unique())

    def submit_form():
        sel_1 = (symbol_cb1.get(), option_cb1.get(), strike_cb1.get(), expiry_cb1.get())
        sel_2 = (symbol_cb2.get(), option_cb2.get(), strike_cb2.get(), expiry_cb2.get())

        if not all(sel_1) or not all(sel_2):
            messagebox.showerror("Input Error", "All fields for both legs are required.")
            return

        filtered1 = df[
            (df['pSymbolName'] == sel_1[0]) &
            (df['pOptionType'] == sel_1[1]) &
            (df['dStrikePrice;'] == float(sel_1[2])) &
            (df['ExpiryDatePlus10Y'].dt.strftime('%Y-%m-%d') == sel_1[3])
        ]

        filtered2 = df[
            (df['pSymbolName'] == sel_2[0]) &
            (df['pOptionType'] == sel_2[1]) &
            (df['dStrikePrice;'] == float(sel_2[2])) &
            (df['ExpiryDatePlus10Y'].dt.strftime('%Y-%m-%d') == sel_2[3])
        ]

        if not filtered1.empty and not filtered2.empty:
            root.leg1_p_symbol = filtered1.iloc[0]['pSymbol']
            root.leg1_p_trdsymbol = filtered1.iloc[0]['pTrdSymbol']
            root.leg2_p_symbol = filtered2.iloc[0]['pSymbol']
            root.leg2_p_trdsymbol = filtered2.iloc[0]['pTrdSymbol']
            root.destroy()
        else:
            messagebox.showwarning("No Match", "No matching rows found for one or both legs.")

    # GUI setup
    root = tk.Tk()
    root.title("Select Leg 1 and Leg 2 Options")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0)

    def add_leg_ui(prefix, row):
        ttk.Label(frame, text=f"{prefix} Symbol").grid(row=row, column=0, padx=(0, 76), pady=5)
        cb1 = ttk.Combobox(frame, values=symbols, width=15)
        cb1.grid(row=row + 1, column=0)

        ttk.Label(frame, text=f"{prefix} Option").grid(row=row, column=1, padx=(0, 76), pady=5)
        cb2 = ttk.Combobox(frame, values=option_types, width=15)
        cb2.grid(row=row + 1, column=1)

        ttk.Label(frame, text=f"{prefix} Strike").grid(row=row, column=2, padx=(0, 76), pady=5)
        cb3 = ttk.Combobox(frame, values=[str(s) for s in strike_prices], width=15)
        cb3.grid(row=row + 1, column=2)

        ttk.Label(frame, text=f"{prefix} Expiry").grid(row=row, column=3, padx=(0, 76), pady=5)
        cb4 = ttk.Combobox(frame, values=expiry_dates, width=15)
        cb4.grid(row=row + 1, column=3)

        return cb1, cb2, cb3, cb4

    # Add UI elements for both legs
    symbol_cb1, option_cb1, strike_cb1, expiry_cb1 = add_leg_ui("Leg 1", 0)
    symbol_cb2, option_cb2, strike_cb2, expiry_cb2 = add_leg_ui("Leg 2", 2)

    submit_btn = ttk.Button(root, text="Submit", command=submit_form)
    submit_btn.grid(row=3, column=0, pady=10)

    root.bind('<Return>', lambda event: submit_form())

    root.mainloop()

    try:
        return (
            root.leg1_p_symbol, root.leg1_p_trdsymbol,
            root.leg2_p_symbol, root.leg2_p_trdsymbol
        )
    except AttributeError:
        return None, None, None, None


# MAIN EXECUTION BLOCK

# Read the CSV from URL
# url = "https://lapi.kotaksecurities.com/wso2-scripmaster/v1/prod/2025-05-16/transformed/nse_fo.csv"
# df = pd.read_csv(url)

# # Clean and transform DataFrame in memory
# df.columns = df.columns.str.strip()
# df['ExpiryDateFormatted'] = df['lExpiryDate'].apply(
#     lambda x: datetime.fromtimestamp(x) if pd.notnull(x) else None
# )
# df['ExpiryDatePlus10Y'] = df['ExpiryDateFormatted'].apply(
#     lambda x: x + relativedelta(years=10) if pd.notnull(x) else None
# )

# # Use the DataFrame in GUI form directly
# leg1_symbol, leg1_trdsymbol, leg2_symbol, leg2_trdsymbol = get_leg_info(df)

# # Print the result
# print("✅ Leg 1 Symbol:", leg1_symbol)
# print("✅ Leg 1 TrdSymbol:", leg1_trdsymbol)
# print("✅ Leg 2 Symbol:", leg2_symbol)
# print("✅ Leg 2 TrdSymbol:", leg2_trdsymbol)
