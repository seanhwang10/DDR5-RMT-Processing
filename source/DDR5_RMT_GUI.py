# RMT GUI for RMT_Processing.py
# seahwang@cisco.com

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from DDR5_RMT_Processing import *

def jean_analysis():
    numData = int(num_data_var.get())
    folders = []
    for i in range(0, numData):
        # folders.append(get_folders(i + 1))
        folders.append(browse_folder())
    # askBooleanInput(numData + 1)
    bootstrap = "Y" if bootstrap_var.get() else "N"
    includeLine = "Y" if include_line_var.get() else "N"
    histogram = histogram_var.get()
    vendor_table = vendor_table_var.get()
    box_plot = box_plot_var.get()
    variable_table = variable_table_var.get()
    bit_margin = bit_margin_var.get()
    comparator = comparator_var.get()

    # All inputs saved into variables named above, ready to be used.

    # Test cases, to print the variable content to CP.
    print("Number of folders to analyze:", numData)
    print("Path to folder:", folders)
    print("Bootstrap?", bootstrap)
    print("Margin Line?", includeLine)


    # ---- Your code should begin here ----------------------------------------------------------- #
    vendorNames = []
    for i in range(0, numData):
        name = folders[i][folders[i].rfind("/")+1:folders[i].rfind("_")]
        name = name[name.find("_")+1:name.rfind("_")]
        name = name[name.find("_")+1:]
        vendorNames.append(name)

    processData(folders, vendorNames, bootstrap, includeLine, histogram, vendor_table, box_plot, variable_table, bit_margin, comparator)
    # fix comparator
    # make radio button turn off on second click




# ---GUI Code Below ------------------------------------------------------------------------------- #

def browse_folder():
    # folder_path = filedialog.askdirectory()
    # folder_path_var.set(folder_path)
    return filedialog.askdirectory()

# def get_folders(r):
#     folder_label = tk.Label(root, text="Path to folder:")                                           # folder
#     folder_label.grid(row=r, column=0, padx=10, pady=5)
#     folder_entry = tk.Entry(root, textvariable=folder_path_var)
#     folder_entry.grid(row=r, column=1, padx=10, pady=5)
#     browse_button = tk.Button(root, text="Browse", command=browse_folder)
#     browse_button.grid(row=r, column=2, padx=10, pady=5)

root = tk.Tk()
root.title("DDR5 RMT GUI")
root.geometry("500x230")

num_data_var = tk.StringVar()
folder_path_var = tk.StringVar()
bootstrap_var = tk.BooleanVar()
include_line_var = tk.BooleanVar()
histogram_var = tk.BooleanVar()
vendor_table_var = tk.BooleanVar()
box_plot_var = tk.BooleanVar()
variable_table_var = tk.BooleanVar()
bit_margin_var = tk.BooleanVar()
comparator_var = tk.BooleanVar()


num_label = tk.Label(root, text="Number of folders to analyze:")                                # numData
num_label.grid(row=0, column=0, padx=10, pady=5)
num_data_combobox = ttk.Combobox(root, textvariable=num_data_var, values=[1, 2, 3])
num_data_combobox.grid(row=0, column=1, padx=10, pady=5)

# folder_label = tk.Label(root, text="Path to folder:")                                           # folder
# folder_label.grid(row=1, column=0, padx=10, pady=5)
# folder_entry = tk.Entry(root, textvariable=folder_path_var)
# folder_entry.grid(row=1, column=1, padx=10, pady=5)
# browse_button = tk.Button(root, text="Browse", command=browse_folder)
# browse_button.grid(row=1, column=2, padx=10, pady=5)

bootstrap_label = tk.Label(root, text="Bootstrap?")                                             # bootstrap
bootstrap_label.grid(row=1, column=0, padx=10, pady=5)
bootstrap_yes_radio = tk.Radiobutton(root, text="Yes", variable=bootstrap_var, value=True)
bootstrap_yes_radio.grid(row=1, column=1, padx=10, pady=5)
bootstrap_no_radio = tk.Radiobutton(root, text="No", variable=bootstrap_var, value=False)
bootstrap_no_radio.grid(row=1, column=2, padx=10, pady=5)

include_line_label = tk.Label(root, text="Margin Line?")                                            # includeLine
include_line_label.grid(row=2, column=0, padx=10, pady=5)
include_line_yes_radio = tk.Radiobutton(root, text="Yes", variable=include_line_var, value=True)
include_line_yes_radio.grid(row=2, column=1, padx=10, pady=5)
include_line_no_radio = tk.Radiobutton(root, text="No", variable=include_line_var, value=False)
include_line_no_radio.grid(row=2, column=2, padx=10, pady=5)

graph_types_label = tk.Label(root, text="Select Graph Type:")                                           
graph_types_label.grid(row=3, column=0, padx=9, pady=5)

histogram_radio = tk.Radiobutton(root, text="Histogram", variable=histogram_var, value=True)
histogram_radio.grid(row=3, column=1, padx=10, pady=5)

vendor_table_radio = tk.Radiobutton(root, text="Vendor Table", variable=vendor_table_var, value=True)
vendor_table_radio.grid(row=3, column=2, padx=10, pady=5)

box_plot_radio = tk.Radiobutton(root, text="Box Plot", variable=box_plot_var, value=True)
box_plot_radio.grid(row=4, column=1, padx=10, pady=3)

variable_table_radio = tk.Radiobutton(root, text="Variable Table", variable=variable_table_var, value=True)
variable_table_radio.grid(row=4, column=2, padx=10, pady=3)

bit_margin_radio = tk.Radiobutton(root, text="Bit Margin", variable=bit_margin_var, value=True)
bit_margin_radio.grid(row=5, column=1, padx=10, pady=3)

comparator_radio = tk.Radiobutton(root, text="Comparator_radio", variable=bit_margin_var, value=True)
comparator_radio.grid(row=5, column=2, padx=10, pady=3)

run_button = tk.Button(root, text="Run", command=jean_analysis, width=20)
run_button.grid(row=6, column=0, columnspan=3, padx=10, pady=5)



root.mainloop()