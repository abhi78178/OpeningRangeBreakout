import pandas as pd

def get_leg_info(df, symbol1, option1, strike1, expiry1, symbol2, option2, strike2, expiry2):
    # Ensure columns are clean and datetime is properly parsed
    df.columns = df.columns.str.strip()
    df['ExpiryDatePlus10Y'] = pd.to_datetime(df['ExpiryDatePlus10Y'], errors='coerce')

    # Filter for Leg 1
    filtered1 = df[
        (df['pSymbolName'] == symbol1) &
        (df['pOptionType'] == option1) &
        (df['dStrikePrice;'] == float(strike1)) &
        (df['ExpiryDatePlus10Y'].dt.strftime('%Y-%m-%d') == expiry1)
    ]

    # Filter for Leg 2
    filtered2 = df[
        (df['pSymbolName'] == symbol2) &
        (df['pOptionType'] == option2) &
        (df['dStrikePrice;'] == float(strike2)) &
        (df['ExpiryDatePlus10Y'].dt.strftime('%Y-%m-%d') == expiry2)
    ]

    if not filtered1.empty and not filtered2.empty:
        leg1_symbol = filtered1.iloc[0]['pSymbol']
        leg1_trdsymbol = filtered1.iloc[0]['pTrdSymbol']
        leg2_symbol = filtered2.iloc[0]['pSymbol']
        leg2_trdsymbol = filtered2.iloc[0]['pTrdSymbol']
        return leg1_symbol, leg1_trdsymbol, leg2_symbol, leg2_trdsymbol
    else:
        print("⚠️ No matching rows found for one or both legs.")
        return None, None, None, None


import tkinter as tk
import threading

class PnLDisplay:
    """
    A simple tkinter-based window to display live PnL.
    Call `update_pnl(new_pnl)` whenever your PnL variable changes.
    """
    def __init__(self, title="Live PnL"):
        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title(title)
        self.label = tk.Label(self.root, text="PnL: 0.00", font=("Helvetica", 16))
        self.label.pack(padx=20, pady=20)

    def update_pnl(self, new_pnl):
        """
        Update the displayed PnL value.
        Should be called from your algorithm whenever PnL changes.
        """
        try:
            text = f"PnL: {new_pnl:.2f}"
        except (TypeError, ValueError):
            text = f"PnL: {new_pnl}"
        self.label.config(text=text)

    def start(self):
        """
        Start the GUI event loop in a separate daemon thread, so it doesn't block your main program.
        """
        threading.Thread(target=self.root.mainloop, daemon=True).start()

# Example of integrating into your main program:
# if __name__ == '__main__':
#     import time
#     display = PnLDisplay()
#     display.start()
#     current_pnl = 0.0
#     while True:
#         # Replace this with your real PnL calculation
#         current_pnl += 1.0
#         display.update_pnl(current_pnl)
#         time.sleep(1)

