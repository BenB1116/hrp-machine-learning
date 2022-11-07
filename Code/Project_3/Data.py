from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd

Tk().withdraw()

def getPatronPath():
    filename = askopenfilename()
    return(filename)

def getInventoryPath():
    filename = askopenfilename()
    return(filename)

# Remove to select folder or paste path below.
# patron_path = getPatronPath()
# inventory_pat = getInventoryPath()

patron_path = 'C:/Users/Ben/Desktop/HRP/Data/Clean_Data/Clean_Patron.csv'
inventory_path = 'C:/Users/Ben/Desktop/HRP/Data/Clean_Data/Clean_Inventory.csv'

patron_df = pd.read_csv(patron_path)
inv_df = pd.read_csv(inventory_path)

# Drop random columns
patron_df.drop(columns = 'Unnamed: 0', inplace = True)
inv_df.drop(columns = 'Unnamed: 0', inplace = True)

# Create copies of the dataframes
patron_dfc = patron_df.copy()
inv_dfc = inv_df.copy()
