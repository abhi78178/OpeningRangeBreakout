# price_input_form.py

import tkinter as tk

def get_high_low_price():
    result = {"high_price": None, "low_price": None}

    def submit():
        try:
            result["high_price"] = float(entry_high.get())
            result["low_price"] = float(entry_low.get())
            root.destroy()
        except ValueError:
            label_result.config(text="Enter valid numbers!")

    # Create GUI window
    root = tk.Tk()
    root.title("Enter 30-Min High/Low")

    # Entry fields
    tk.Label(root, text="Enter 30-min High:").grid(row=0, column=0, padx=10, pady=5)
    entry_high = tk.Entry(root)
    entry_high.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Enter 30-min Low:").grid(row=1, column=0, padx=10, pady=5)
    entry_low = tk.Entry(root)
    entry_low.grid(row=1, column=1, padx=10, pady=5)

    # Submit button
    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Feedback label
    label_result = tk.Label(root, text="")
    label_result.grid(row=3, column=0, columnspan=2)

    # Start GUI event loop (blocking)
    root.mainloop()

    return result["high_price"], result["low_price"]
