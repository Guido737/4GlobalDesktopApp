"""
This is desktop app for voice commands script
Created by: Creator/Eversor
Date: 22 Feb
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import webbrowser
import speech_recognition as sr
import re
from PIL import Image, ImageTk

def open_firefox():
    """Function: open_firefox
    Brief: opening firefox browser
    """
    try:
        subprocess.run(["firefox"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen(["firefox"])
    except FileNotFoundError:
        print("There is no firefox or not in path")
        exit()

def search_firefox(search_term):
    """Function: search_firefox
    Brief: searching what I say in firefox
    Params: search_term: what I said
    """
    try:
        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
        webbrowser.open(url)
    except webbrowser.Error as error:
        print(f"An error occurred with the web browser: {error}")

def create_file(file_name):
    """Function: create_file
    Brief: creates a file
    Params: file_name: name of the file
    """
    try:
        with open(file_name, "w") as file:
            file.write("")
        print(f"File {file_name} created")
    except FileExistsError:
        print(f"File {file_name} already exists")
        exit()

def open_file(file_name):
    """Function: open_file
    Brief: opening file
    Params: file_name: name of the file
    """
    try:
        subprocess.Popen(["xdg-open", file_name])
    except FileNotFoundError:
        print(f"Can't open {file_name}")
        exit()

def read_file(file_name):
    """Function: read_file
    Brief: reads a file and prints its contents
    Params: file_name: name of the file to read
    """
    try:
        with open(file_name) as file:
            content = file.read()
            print(f"Contents of {file_name}")
            print(content)
    except FileNotFoundError:
        print(f"File {file_name} doesn't exist")
        exit()

def delete_file(file_name):
    """Function: delete_file
    Brief: deletes a file
    Params: file_name: the name of the file to delete
    """
    try:
        os.remove(file_name)
        print(f"File {file_name} deleted")
    except FileNotFoundError:
        print(f"File {file_name} doesn't exist")
        exit()

def create_dir(directory):
    """Function: create_dir
    Brief: creates a directory
    Params: directory: the path of the directory to create
    """
    try:
        os.makedirs(directory)
        print(f"Directory {directory} created")
    except FileExistsError:
        print(f"Directory {directory} already exists")
        exit()

def list_dir(directory):
    """Function: list_dir
    Brief: lists directory content
    Params: directory: what directory I said
    """
    try:
        files = os.listdir(directory)
        if files:
            print("Content of directory:")
            for file in files:
                print(file)
        else:
            print("Directory is empty")
    except FileNotFoundError:
        print(f"There is no {directory} directory")
        exit()

def process_command(command):
    """Function: process_command
    Brief: Processes the selected command
    Params: command: the command to process
    """
    try:
        if "open firefox" in command:
            open_firefox()
        elif "search for" in command:
            search_term = re.sub(r"search for\s+", "", command)
            search_firefox(search_term)
        elif "create file" in command:
            file_name = re.sub(r"create file\s+", "", command)
            create_file(file_name)
        elif "open file" in command:
            file_name = re.sub(r"open file\s+", "", command)
            open_file(file_name)
        elif "read file" in command:
            file_name = re.sub(r"read file\s+", "", command)
            read_file(file_name)
        elif "delete file" in command:
            file_name = re.sub(r"delete file\s+", "", command)
            delete_file(file_name)
        elif "create directory" in command:
            directory = re.sub(r"create directory\s+", "", command)
            create_dir(directory)
        elif "list directory" in command:
            directory = re.sub(r"list directory\s+", "", command)
            list_dir(directory)
        elif "stop" in command:
            print("Stopping the program...")
            exit()
        else:
            print("Command not recognized.")
    except Exception as e:
        print(f"An error occurred: {e}")


def recognize_speech():
    """Function: recognize_speech
    Brief: Recognizes speech and processes the command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {command}")
            process_command(command.lower())
        except sr.UnknownValueError:
            print("Could not understand the speech")
        except sr.RequestError:
            print("Error connecting to Google Speech Recognition service")
        except Exception as e:
            print(f"An error occurred: {e}")

def on_button_click():
    """Function: on_button_click
    Brief: Handles button click event to execute the command
    """
    command = command_var.get()
    if command:
        process_command(command)
    else:
        messagebox.showwarning("Warning", "Please select a command.")

def main():
    """Function: main
    Brief: entry point
    """
    global command_var
    root = tk.Tk()
    root.title("Voice Command Executor")
    root.geometry("800x400")
    canvas = tk.Canvas(root, width=3400, height=1400)
    canvas.pack(fill="both", expand=True)
    background_image = Image.open("/home/usernamezero00/Desktop/5_Projects/PNG/3d-rendering-abstract-black-white-waves(1).jpg")
    background_resized = background_image.resize((3400, 1400), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.image = background_photo
    label = tk.Label(root, text="Select a Command", fg="white", bg="black", font=("Arial", 14))
    label.place(x=150, y=10)
    command_var = tk.StringVar()
    command_menu = tk.OptionMenu(root, command_var, "open firefox", "search for", "create file", "open file", 
                                 "read file", "delete file", "create directory", "list directory", "stop")
    command_menu.place(x=150, y=50)
    button = tk.Button(root, text="Execute", command=on_button_click, bg="lightblue")
    button.place(x=200, y=120)
    voice_button = tk.Button(root, text="Voice Input", command=recognize_speech, bg="lightgreen")
    voice_button.place(x=200, y=160)
    root.mainloop()


if __name__ == "__main__":
    main()
