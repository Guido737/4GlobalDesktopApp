"""
This is desktop app for crypto script
Created by: Creator/Eversor
Date: 22 Feb
"""

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os
import requests
import xlsxwriter

def create_widgets(root, state, canvas):
    """
    Function: create_widgets
    Brief: create the widgets for tkinter window
    Params: root: state: dict to store widget states
    """
    
    state["upload_btn"] = tk.Button(root, text="Upload file", command=lambda: upload_file(state))
    state["file_label"] = tk.Label(root, text="")
    state["name_label"] = tk.Label(root, text="Enter Excel file name")
    state["name_entry"] = tk.Entry(root)
    state["save_btn"] = tk.Button(root, text="Save Excel File", command=lambda: save_file(state, root))
    def center_widgets(event):
        canvas_width = event.width
        canvas_height = event.height
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        canvas.coords(state["upload_btn"], center_x, center_y - 100)
        canvas.coords(state["file_label"], center_x, center_y - 50)
        canvas.coords(state["name_label"], center_x, center_y)
        canvas.coords(state["name_entry"], center_x, center_y + 30)
        canvas.coords(state["save_btn"], center_x, center_y + 80)
        
    root.bind("<Configure>", center_widgets)
    state["upload_btn_id"] = canvas.create_window(400, 150, window=state["upload_btn"])
    state["file_label_id"] = canvas.create_window(400, 200, window=state["file_label"])
    state["name_label_id"] = canvas.create_window(400, 250, window=state["name_label"])
    state["name_entry_id"] = canvas.create_window(400, 280, window=state["name_entry"])
    state["save_btn_id"] = canvas.create_window(400, 350, window=state["save_btn"])

def upload_file(state):
    """
    Function: upload_file
    Brief: handle file upload and update the label
    Parms: state: dict to store widget states
    """
    state["file_path"] = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if state["file_path"]:
        state["file_label"].config(text=f"Uploaded: {os.path.basename(state['file_path'])}")
    else:
        state["file_label"].config(text="Nothing selected")

def save_file(state, root):
    """
    Function: save_file
    Brief: Save data to excel file
    Params: state: dict to store widget states
            root: tkinter root window
    """
    if "file_path" not in state or not state["file_path"]:
        messagebox.showerror("Error", "Please upload file first")
        return

    excel_name = state["name_entry"].get()
    if not excel_name:
        messagebox.showerror("Error", "Please enter a name for Excel file")
        return

    default_save_path = os.path.join(os.path.expanduser("~/Downloads"), f"{excel_name}.xlsx")
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_save_path, initialdir=os.path.expanduser("~/Downloads"), filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return

    try:
        save_data(save_path, state)
        messagebox.showinfo("Done", f"Data saved to {save_path}")
    except Exception as error:
        messagebox.showerror("Error", f"Failed to save data: {error}")
    root.destroy()

def save_data(save_path, state):
    """
    Function: save_data
    Brief: get data from API and save to Excel file
    Params: save_path: the path to save Excel file
            state: dict of widget states
    """

    symbols = read_symbols(state)
    data = get_data()
    filtered_data = [i for i in data if i["symbol"].upper() in symbols]

    if not filtered_data:
        raise Exception("No data found for the provided symbols.")
    
    try:
        workbook = xlsxwriter.Workbook(save_path)
        worksheet = workbook.add_worksheet()
        headers = ["Name", "Symbol", "Current Price", "Market Cap", "Total Volume", "Price Change for 24 hours"]
        bold = workbook.add_format({"bold": True})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})
        for col in range(len(headers)):
            worksheet.write(0, col, headers[col], bold)
            worksheet.set_column(col, col, 23)

        row = 1
        for item in filtered_data:
            worksheet.write(row, 0, item["name"])
            worksheet.write(row, 1, item["symbol"])
            worksheet.write_number(row, 2, float(item["priceUsd"]), currency_format)
            worksheet.write_number(row, 3, float(item["marketCapUsd"]), currency_format)
            worksheet.write_number(row, 4, float(item["volumeUsd24Hr"]), currency_format)
            worksheet.write_number(row, 5, float(item["changePercent24Hr"]))

            row += 1
        workbook.close()
    except xlsxwriter.exceptions.XlsxWriterError as error:
        raise Exception(f"Error writing to Excel file: {error}")

def read_symbols(state):
    """
    Function: read_symbols
    Brief: Reading symbols from uploaded file
    Params: state: dict to store widget states
    Return: list of symbols
    """
    try:
        with open(state["file_path"]) as file:
            symbols = file.read().splitlines()
        return [symbol.upper() for symbol in symbols]
    except Exception as e:
        raise Exception(f"Error reading symbols from file: {e}")

def get_data():
    """
    Function: get_data
    Brief: Fetching data from CoinCap API
    Return: list of crypto data
    """
    url = "https://api.coincap.io/v2/assets"
    params = {"limit": 30}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise Exception(f"Error fetching data from API: {error}")

    data = response.json()
    return data["data"]

def create_main_window():
    root = tk.Tk()
    root.title("Crypto")
    root.geometry("800x600")
    canvas = tk.Canvas(root, width=3400, height=1400)
    canvas.pack()
    background_image = Image.open("/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg")
    background_resized = background_image.resize((3400, 1400), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.image = background_photo
    state = {}
    create_widgets(root, state, canvas)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
