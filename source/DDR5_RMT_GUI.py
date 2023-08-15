# ----------------------------------------------
# File name: DDR5_RMT_GUI.py
# Original Author: Sean Hwang (seahwang@cisco.com)
# Edited: Jean Mattekatt
# Date: 7/25/2023

# Description: RMT GUI for RMT_Processing.py
# ----------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from DDR5_RMT_Processing import *

def jean_analysis():
    numData = int(num_data_var.get())

    # assign folders to analyze
    folders = []
    for i in range(0, numData):
        folders.append(browse_folder())

    # save GUI inputs into variables, ready to be used
    bootstrap = "Y" if bootstrap_var.get() else "N"
    includeLine = "Y" if include_line_var.get() else "N"
    histogram = histogram_var.get()
    vendor_table = vendor_table_var.get()
    box_plot = box_plot_var.get()
    variable_table = variable_table_var.get()
    bit_margin = bit_margin_var.get()
    comparator = comparator_var.get()

    # Test cases, to print the variable content to CP.
    print("Number of folders to analyze:", numData)
    print("Path to folder:", folders)
    print("Bootstrap?", bootstrap)
    print("Margin Line?", includeLine)


    # ---- Your code should begin here ----------------------------------------------------------- #
    # creates list of vendor Names
    vendorNames = []
    for i in range(0, numData):
        name = folders[i][folders[i].rfind("/")+1:folders[i].rfind("_")]
        name = name[name.find("_")+1:name.rfind("_")]
        name = name[name.find("_")+1:]
        vendorNames.append(name)

    # runs DDR5_RMT_Processing.py with all GUI inputs
    processData(folders, vendorNames, bootstrap, includeLine, histogram, vendor_table, box_plot, variable_table, bit_margin, comparator)


# ---GUI Code Below ------------------------------------------------------------------------------- #

def browse_folder():
    return filedialog.askdirectory()

root = tk.Tk()
root.title("DDR5 RMT GUI")
root.geometry("500x230")

# assign variables on GUI
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

histogram_radio = tk.Checkbutton(root, text="Histogram", variable=histogram_var, onvalue = True, offvalue = False)                # histogram
histogram_radio.grid(row=3, column=1, padx=10, pady=5)

vendor_table_radio = tk.Checkbutton(root, text="Vendor Table", variable=vendor_table_var, onvalue = True, offvalue = False)       # vendor_table
vendor_table_radio.grid(row=3, column=2, padx=10, pady=5)

box_plot_radio = tk.Checkbutton(root, text="Box Plot", variable=box_plot_var, onvalue = True, offvalue = False)                   # box_plot
box_plot_radio.grid(row=4, column=1, padx=10, pady=3)

variable_table_radio = tk.Checkbutton(root, text="Variable Table", variable=variable_table_var, onvalue = True, offvalue = False) # variable_table
variable_table_radio.grid(row=4, column=2, padx=10, pady=3)

bit_margin_radio = tk.Checkbutton(root, text="Bit Margin", variable=bit_margin_var, onvalue = True, offvalue = False)             # bit_margin
bit_margin_radio.grid(row=5, column=1, padx=10, pady=3)

comparator_radio = tk.Checkbutton(root, text="Comparator", variable=comparator_var, onvalue = True, offvalue = False)             # comparator
comparator_radio.grid(row=5, column=2, padx=10, pady=3)

run_button = tk.Button(root, text="Run", command=jean_analysis, width=20)                                   # button to run jean_analysis()
run_button.grid(row=6, column=0, columnspan=3, padx=10, pady=5)



root.mainloop()