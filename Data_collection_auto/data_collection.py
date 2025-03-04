"""
This script loading video data from YouTube
Created by: Creator/Eversor
Date: 22 Feb
"""

import time
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import pygame
from PIL import Image, ImageTk
import numpy as np
import threading

"""Initialize pygame mixer for audio playback"""
pygame.mixer.init()

def collect_youtube_data(artist_name, save_path):
    """Function: collect_youtube_data
       Brief: collects YouTube data based on the artist name and saves it to a file
       Params: artist_name (str), save_path (str)
    """
    firefox_options = Options()
    firefox_options.headless = False
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.get("https://www.youtube.com/")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(artist_name)
    search_box.submit()
    time.sleep(3)
    video_data = []
    videos = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")[:10]

    for video in videos:
        title = video.find_element(By.ID, "video-title").text
        try:
            views = video.find_element(By.CSS_SELECTOR, "#metadata-line span:nth-child(1)").text
        except Exception as e:
            views = "N/A"
        try:
            time_published = video.find_element(By.CSS_SELECTOR, "#metadata-line span:nth-child(2)").text
        except Exception as e:
            time_published = "N/A"
        video_data.append({
            "title": title,
            "views": views,
            "time_published": time_published
        })

    with open(save_path, 'w') as file:
        for video in video_data:
            file.write(f"Title: {video['title']}\n")
            file.write(f"Views: {video['views']}\n")
            file.write(f"Published: {video['time_published']}\n")
            file.write("\n")

    driver.quit()
    messagebox.showinfo("Success", f"Data successfully saved to {save_path}")

def open_file_dialog():
    """Function: open_file_dialog
       Brief: opens a file dialog where to save the YouTube data
       Params: file dialog to select
    """
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    return save_path

def on_search_button_click():
    """Function: on_search_button_click
       Brief: triggered to collect and save YouTube data
       Params: use buttun
    """
    artist_name = artist_name_entry.get()
    if not artist_name:
        messagebox.showerror("Error", "Please enter an artist name.") 
        return
    save_path = open_file_dialog()
    if save_path:
        collect_youtube_data(artist_name, save_path)

def stop_audio():
    """Function: stop_audio
       Brief: stops playing audio
       Params: buttun use
    """
    pygame.mixer.music.stop()

def pause_audio():
    """Function: pause_audio
       Brief: pauses playing audio
       Params: buttun use
    """
    pygame.mixer.music.pause()

def unpause_audio():
    """Function: unpause_audio
       Brief: unpauses paused audio
       Params: buttun use
    """
    pygame.mixer.music.unpause()

def set_volume(val):
    """Function: set_volume
       Brief: sets the volume of the audio
       Params: val (str) - volume as a percentage
    """
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def visualize_audio():
    """Function: visualize_audio
       Brief: visualizes the audio waveform 
       Params: vizuale window
    """
    num_bars = 50
    bar_width = 30

    while pygame.mixer.music.get_busy():
        audio_data = np.random.rand(num_bars) * 450
        canvas.delete("all")
        for i in range(num_bars):
            bar_height = int(audio_data[i])
            canvas.create_rectangle(
                i * (bar_width + 2), 450 - bar_height, 
                i * (bar_width + 2) + bar_width, 450,
                fill="black", outline="white"
            )

        canvas.update()
        time.sleep(0.05)

"""Create main application window"""
root = tk.Tk()
root.title("YouTube Data Collection")
root.geometry("666x666")

"""Set up audio file and play it"""
audio_file = "/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/audio/Kc And The Sunshine Band - Give It Up.mp3"
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)

"""Load audio control icons"""
pause_icon = Image.open("/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/png/icons8-пауза-в-кружке-30.png")
pause_icon = pause_icon.resize((30, 30))
pause_icon = ImageTk.PhotoImage(pause_icon)
play_icon = Image.open("/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/png/icons8-play-24.png")
play_icon = play_icon.resize((30, 30))
play_icon = ImageTk.PhotoImage(play_icon)
stop_icon = Image.open("/home/usernamezero00/Desktop/5_Projects/Data_collection_auto/png/icons8-стоп-30.png")
stop_icon = stop_icon.resize((30, 30))
stop_icon = ImageTk.PhotoImage(stop_icon)

"""Artist name input section"""
artist_name_frame = tk.Frame(root)
artist_name_frame.pack(pady=10, anchor="w", padx=10, fill="x")
artist_name_label = tk.Label(artist_name_frame, text="Enter Material Name")
artist_name_label.pack(side="left")
artist_name_entry = tk.Entry(artist_name_frame, width=99)
artist_name_entry.pack(side="left", padx=10)

"""Search button to collect YouTube data"""
search_button = tk.Button(root, text="Search and Save Data", command=on_search_button_click)
search_button.pack(pady=20, anchor="w", padx=10)

"""Volume control section"""
volume_frame = tk.Frame(root)
volume_frame.pack(anchor="ne", padx=10, pady=10, fill="x")
volume_label = tk.Label(volume_frame, text="VOLUME")
volume_label.pack(side="left", padx=10)
volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient="horizontal", command=set_volume)
volume_slider.set(30)
volume_slider.pack(side="left", padx=10)

"""Audio control section"""
audio_frame = tk.Frame(root)
audio_frame.pack(pady=10)
stop_button = tk.Button(audio_frame, image=stop_icon, command=stop_audio)
stop_button.pack(side="left", padx=1)
pause_button = tk.Button(audio_frame, image=pause_icon, command=pause_audio)
pause_button.pack(side="left", padx=1)
unpause_button = tk.Button(audio_frame, image=play_icon, command=unpause_audio)
unpause_button.pack(side="left", padx=1)

"""Canvas for audio visualization"""
canvas = tk.Canvas(root, width=600, height=550, bg="darkgrey")
canvas.pack(pady=90)

"""Start the audio visualization in a separate thread"""
visualization_thread = threading.Thread(target=visualize_audio)
visualization_thread.daemon = True
visualization_thread.start()

"""Set the background color of the window"""
root.config(bg="black")

"""Start the tkinter main loop"""
root.mainloop()
