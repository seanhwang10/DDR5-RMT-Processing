# RMT GUI for RMT_Processing.py
# seahwang@cisco.com

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def jean_analysis():
    numData = num_data_var.get()
    folders = folder_path_var.get()
    bootstrap = "Y" if bootstrap_var.get() else "N"
    includeLine = "Y" if include_line_var.get() else "N"

    # All inputs saved into variables named above, ready to be used.

    # Test cases, to print the variable content to CP.
    print("Number of folders to analyze:", numData)
    print("Path to folder:", folders)
    print("Bootstrap?", bootstrap)
    print("VM Line?", includeLine)


    # ---- Your code should begin here ----------------------------------------------------------- #






# ---GUI Code Below ------------------------------------------------------------------------------- #

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

root = tk.Tk()
root.title("DDR5 RMT GUI (Prototype)")
root.geometry("450x200")

num_data_var = tk.StringVar()
folder_path_var = tk.StringVar()
bootstrap_var = tk.BooleanVar()
include_line_var = tk.BooleanVar()

num_label = tk.Label(root, text="Number of folders to analyze:")                                # numData
num_label.grid(row=0, column=0, padx=10, pady=5)
num_data_combobox = ttk.Combobox(root, textvariable=num_data_var, values=[1, 2, 3, 4, 5])
num_data_combobox.grid(row=0, column=1, padx=10, pady=5)

folder_label = tk.Label(root, text="Path to folder:")                                           # folder
folder_label.grid(row=1, column=0, padx=10, pady=5)
folder_entry = tk.Entry(root, textvariable=folder_path_var)
folder_entry.grid(row=1, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=10, pady=5)

bootstrap_label = tk.Label(root, text="Bootstrap?")                                             # bootstrap
bootstrap_label.grid(row=2, column=0, padx=10, pady=5)
bootstrap_yes_radio = tk.Radiobutton(root, text="Yes", variable=bootstrap_var, value=True)
bootstrap_yes_radio.grid(row=2, column=1, padx=10, pady=5)
bootstrap_no_radio = tk.Radiobutton(root, text="No", variable=bootstrap_var, value=False)
bootstrap_no_radio.grid(row=2, column=2, padx=10, pady=5)

include_line_label = tk.Label(root, text="VM Line?")                                            # includeLine
include_line_label.grid(row=3, column=0, padx=10, pady=5)
include_line_yes_radio = tk.Radiobutton(root, text="Yes", variable=include_line_var, value=True)
include_line_yes_radio.grid(row=3, column=1, padx=10, pady=5)
include_line_no_radio = tk.Radiobutton(root, text="No", variable=include_line_var, value=False)
include_line_no_radio.grid(row=3, column=2, padx=10, pady=5)

run_button = tk.Button(root, text="Run", command=jean_analysis, width=20)
run_button.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()