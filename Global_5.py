"""
This is desktop app all scripts
Created by: Creator/Eversor
Date: 22 Feb
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

open_processes = {}

def run_script(script_path):
    """Function: run_script
       Brief: runs the script at the specified path and returns the process
       Params: script_path (str) - the path to the Python script to execute
    """
    try:
        return subprocess.Popen(["python", script_path])
    except Exception as e:
        print(f"Error while running script: {e}")
        return None

def stop_script(process):
    """Function: stop_script
       Brief: stops the running script by terminating the process
       Params: process (Popen) - the process to terminate
    """
    try:
        process.terminate()
    except Exception as e:
        print(f"Error while stopping script: {e}")

def create_main_window():
    """Function: create_main_window
       Brief: creates the main window with icons
       Params: divided into left and right parts
    """
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("2400x950")

    left_frame = tk.Frame(root, width=933, height=800)
    left_frame.pack(side="left", fill="both", expand=2)

    """Try to load and display the background image"""
    try:
        background_image = Image.open("/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg")
        background_resized = background_image.resize((2400, 2400), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_resized)
        background_label = tk.Label(left_frame, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo
    except Exception as e:
        print(f"Error loading background: {e}")
        
    """Right panel for script controls"""
    right_frame = tk.Frame(root, width=467, height=300, bg="black")
    right_frame.pack(side="right", fill="both", expand=1)
    
    """List of scripts with their respective properties"""
    scripts = [
        {"name": "VOICE COMMANDS", "path": "/home/usernamezero00/Desktop/5_Projects/Voice_commands/voice_commands.py", "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/record.png", "description": "Voice control management", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/voice-control.png", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"},
        {"name": "ADVENTURE GAME", "path": "/home/usernamezero00/Desktop/5_Projects/Adv_game/adventure_time.py", "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/game-controller.png", "description": "Adventure in Space", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/galaxy.png", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"},
        {"name": "CRYPTO", "path": "/home/usernamezero00/Desktop/5_Projects/Desktop_app/crypto.py", "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/free-icon-role-playing-6060361.png", "description": "Cryptocurrencies and trading", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/crypto.png", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"},
        {"name": "MILLIONAIRE", "path": "script4.py", "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/billionaire.png", "description": "Play Millionaire", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/millionaire (copy 1).png", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"},
        {"name": "SELLENIUM", "path": "/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/data_collection.py", "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/online-course.png", "description": "Data collection automation using Selenium", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/data-gathering.png", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"},
        {"name": "CREATOR/EVERSOR", "path": None, "icon": "/home/usernamezero00/Desktop/5_Projects/PNG/photo_2025-03-01_17-57-37.jpg", "description": "Creator of projects @Creator/Eversor", "background": "/home/usernamezero00/Desktop/5_Projects/PNG/photo_2025-03-01_17-57-37.jpg", "photo": "/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg"}
    ]

    """Number of buttons to create"""
    num_buttons = len(scripts)
    top_frame = tk.Frame(right_frame, width=500, height=300, bg="black")
    top_frame.pack(side="top", fill="both", expand=1)
    bottom_frame = tk.Frame(right_frame, width=467, height=400, bg="black")
    bottom_frame.pack(side="bottom", fill="both", expand=1)

    """Description label"""
    description_label = tk.Label(bottom_frame, text="", font=("Arial", 12), wraplength=450, anchor="w", fg="black")
    description_label.pack(pady=20, padx=10)

    """Function to update the description and background image"""
    def update_description_and_background(script):
        description_label.config(text=script["description"])
        if os.path.exists(script["background"]):
            try:
                background_image = Image.open(script["background"])
                background_resized = background_image.resize((480, 400), Image.Resampling.LANCZOS)
                background_photo = ImageTk.PhotoImage(background_resized)

                for widget in top_frame.winfo_children():
                    widget.destroy()

                label = tk.Label(top_frame, image=background_photo)
                label.image = background_photo
                label.pack(fill="both", expand=1)
                top_frame.image = background_photo
                root.update()

            except Exception as e:
                print(f"Error loading background: {e}")
        else:
            print(f"Error: Background file not found at {script['background']}")

    """Function to smoothly resize the icon"""
    def smooth_resize(canvas, circle, script, target_size):
        initial_size = 60
        step = 1
        current_size = initial_size
        if target_size == initial_size:
            step = -1

        def update_icon():
            nonlocal current_size
            if (target_size > initial_size and current_size < target_size) or (target_size < initial_size and current_size > target_size):
                current_size += step
                original_icon_resized = Image.open(script["icon"]).resize((current_size, current_size), Image.Resampling.LANCZOS)
                icon_resized_image = ImageTk.PhotoImage(original_icon_resized)
                canvas.itemconfig(circle, outline="gray")
                canvas.create_image(60, 60, image=icon_resized_image)
                canvas.image = icon_resized_image
                canvas.after(5, update_icon)
            else:
                if target_size == initial_size:
                    canvas.itemconfig(circle, outline="black")

        update_icon()

    """Function for when a button is pressed"""
    def on_press(event, script, canvas, circle):
        smooth_resize(canvas, circle, script, 80)
        update_description_and_background(script)

    def on_release(event, script, canvas, circle):
        smooth_resize(canvas, circle, script, 60)

    def on_toggle_change(val, script, canvas):
        if val == "1":
            if script["path"] and script["path"] not in open_processes:
                process = run_script(script["path"])
                open_processes[script["path"]] = process
            canvas.itemconfig(circle, fill="gray")
        else:
            if script["path"] in open_processes:
                process = open_processes[script["path"]]
                stop_script(process)
                open_processes.pop(script["path"])
            canvas.itemconfig(circle, fill="lightgray")

    """Create buttons for each script"""
    for i in range(num_buttons):
        row = i // 3
        col = i % 3 

        try:
            original_icon = Image.open(scripts[i]["icon"])
            icon_resized = original_icon.resize((50, 50), Image.Resampling.LANCZOS)
            icon_image = ImageTk.PhotoImage(icon_resized)
        except Exception as e:
            print(f"Error loading icon: {e}")
            continue

        """Button frame for each script"""
        button_frame = tk.Frame(left_frame, height=120, width=250, padx=10, pady=10)
        button_frame.grid(row=row, column=col, padx=23, pady=25, sticky="nsew")
        canvas = tk.Canvas(button_frame, width=130, height=130)
        canvas.pack(side="left", padx=10)
        circle = canvas.create_oval(10, 10, 110, 110, fill="lightgray", outline="black")
        icon_resized = original_icon.resize((60, 60), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(icon_resized)
        canvas.create_image(60, 60, image=icon_image)

        """Optionally add additional photos to icons if available"""
        if os.path.exists(scripts[i]["photo"]):
            try:
                photo_image = Image.open(scripts[i]["photo"])
                photo_resized = photo_image.resize((65, 65), Image.Resampling.LANCZOS)
                photo_photo = ImageTk.PhotoImage(photo_resized)
                canvas.create_image(200, 150, image=photo_photo)
                canvas.image = photo_photo
            except Exception as e:
                print(f"Error loading photo for icon: {e}")
        
        canvas.image = icon_image
        text_label = tk.Label(button_frame, text=scripts[i]["name"], font=("Arial", 15), anchor="w")
        text_label.pack(side="left", fill="y", padx=10)

        """Toggle slider for enabling/disabling scripts"""
        if i != 5:
            toggle_var = tk.BooleanVar(value=False)
            toggle_slider = tk.Scale(button_frame, from_=0, to=1, orient="horizontal", length=100, showvalue=False, sliderlength=20,
                                     command=lambda val, script=scripts[i], canvas=canvas: on_toggle_change(val, script, canvas))
            toggle_slider.pack(side="bottom", pady=10)

        """Bind mouse press and release actions"""
        button_frame.bind("<ButtonPress-1>", lambda event, script=scripts[i], canvas=canvas, circle=circle: on_press(event, script, canvas, circle))
        button_frame.bind("<ButtonRelease-1>", lambda event, script=scripts[i], canvas=canvas, circle=circle: on_release(event, script, canvas, circle))

    """Configure grid for left frame to adjust column and row sizes"""
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_rowconfigure(2, weight=1)

    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_columnconfigure(1, weight=1)
    left_frame.grid_columnconfigure(2, weight=1)

    """Start the tkinter main loop"""
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.config(bg="black")
    root.mainloop()

"""Run the main window creation function"""
create_main_window()  
