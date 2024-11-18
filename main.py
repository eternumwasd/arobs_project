import selenium.webdriver as webdriver
from tkinter import messagebox
from threading import Thread
from youtube import *
import tkinter as tk
import time


# Function to run the main process
def main_process(keyword, record_time):
    # Launches Google Chrome
    driver = webdriver.Chrome()
    try:
        reject_cookies(driver)
        play_from_youtube(driver, keyword, int(record_time))
        time.sleep(15)
    finally:
        driver.quit()


# Function to start the process in a separate thread
def start_process():
    keyword = keyword_entry.get()
    record_time = record_time_entry.get()

    if not keyword.strip():
        messagebox.showerror("Error", "Keyword is required.")
        return

    if not record_time.isdigit():
        messagebox.showerror("Error", "Record time must be a number.")
        return

    # Run the process in a separate thread
    thread = Thread(target=main_process, args=(keyword, record_time))
    thread.daemon = True
    thread.start()


# Setup GUI
def launch_gui():
    window = tk.Tk()
    window.title("YouTube Recorder")

    # Keyword input
    tk.Label(window, text="Search Keyword:").grid(row=0, column=0, padx=10, pady=10)
    global keyword_entry
    keyword_entry = tk.Entry(window, width=30)
    keyword_entry.grid(row=0, column=1, padx=10, pady=10)

    # Record time input
    tk.Label(window, text="Record Time (seconds):").grid(row=1, column=0, padx=10, pady=10)
    global record_time_entry
    record_time_entry = tk.Entry(window, width=30)
    record_time_entry.grid(row=1, column=1, padx=10, pady=10)

    # Start button
    start_button = tk.Button(window, text="Start", command=start_process, bg="green", fg="white")
    start_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Run the GUI loop
    window.mainloop()


if __name__ == "__main__":
    # Flag for presentation mode
    presentation_mode = False

    if presentation_mode:
        # Automatically run the main process with default parameters
        default_keyword = "me at the zoo" # The first ever video on YouTube
        default_record_time = 10
        main_process(default_keyword, default_record_time)
    else:
        # Launch the GUI for manual input
        launch_gui()
