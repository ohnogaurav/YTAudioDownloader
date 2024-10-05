import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for the Progressbar
import subprocess

def download_audio(url, save_path):
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    # Command to download only m4a format audio
    command = f'yt-dlp -f bestaudio[ext=m4a] -o "{save_path}/%(title)s.%(ext)s" "{url}"'
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read stdout line by line to update the progress bar
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                progress = extract_progress(output)
                if progress is not None:
                    progress_var.set(progress)
                    progress_label.config(text=f"Downloading... {int(progress)}%")  # Update progress label
                    root.update_idletasks()

        process.wait()

        if process.returncode == 0:
            messagebox.showinfo("Success", "Audio downloaded successfully!")
            progress_label.config(text="Download Complete!")  # Update label on completion
        else:
            messagebox.showerror("Error", "An error occurred during the download.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def extract_progress(output):
    """Extracts download progress from yt-dlp output."""
    try:
        # Find the line containing the percentage
        if "[" in output and "]" in output:
            # Extract the number between [ and %]
            percent_str = output.split("[download] ")[1].split("%")[0].strip()
            return float(percent_str)  # Return as float for the progress bar
    except Exception:
        pass
    return None  # If unable to extract, return None

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)  # Clear the current entry
        directory_entry.insert(0, directory)  # Insert the selected directory

def start_download():
    url = url_entry.get()
    save_path = directory_entry.get()

    if not save_path:
        messagebox.showerror("Error", "Please select a save directory.")
        return

    # Reset progress bar and label
    progress_var.set(0)
    progress_label.config(text="")  # Clear the label
    download_audio(url, save_path)

# Set up the main window
root = tk.Tk()
root.title("YouTube Audio Downloader")

# URL input
url_label = tk.Label(root, text="Enter the URL of the video:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Save directory selection
directory_label = tk.Label(root, text="Select Save Directory:")
directory_label.pack()
directory_entry = tk.Entry(root, width=50)
directory_entry.pack()
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack()

# Progress bar and label
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)  # Use ttk.Progressbar
progress_bar.pack(fill=tk.X, padx=10, pady=10)

# Progress percentage label
progress_label = tk.Label(root, text="")
progress_label.pack()

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack()

# Run the application
root.mainloop()
