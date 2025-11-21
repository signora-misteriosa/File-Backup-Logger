import tkinter as tk
from tkinter import filedialog, messagebox
from backup import perform_backup, load_config, save_config

config = load_config()

def select_source():
    path = filedialog.askdirectory()
    if path:
        entry_source.delete(0, tk.END)
        entry_source.insert(0, path)

def select_destination():
    path = filedialog.askdirectory()
    if path:
        entry_dest.delete(0, tk.END)
        entry_dest.insert(0, path)

def run_backup():
    src = entry_source.get()
    dst = entry_dest.get()
    version = entry_version.get()
    zip_mode = var_zip.get()
    if not src or not dst:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return
    try:
        result_path, files, duration = perform_backup(src, dst, version, zip_mode)
        messagebox.showinfo(
            "Backup Completed",
            f"Backup created successfully!\n\nLocation: {result_path}\nFiles copied: {files}\nDuration: {duration}s"
        )
        config["last_source"] = src
        config["last_destination"] = dst
        config["zip_mode"] = zip_mode
        save_config(config)
    except Exception as e:
        messagebox.showerror("Backup Error", str(e))

root = tk.Tk()
root.title("File Backup Logger - Created by Eligia Raileanu")

tk.Label(root, text="Source Folder:").grid(row=0, column=0)
entry_source = tk.Entry(root, width=45)
entry_source.grid(row=0, column=1)
entry_source.insert(0, config.get("last_source", ""))
tk.Button(root, text="Browse", command=select_source).grid(row=0, column=2)

tk.Label(root, text="Destination Folder:").grid(row=1, column=0)
entry_dest = tk.Entry(root, width=45)
entry_dest.grid(row=1, column=1)
entry_dest.insert(0, config.get("last_destination", ""))
tk.Button(root, text="Browse", command=select_destination).grid(row=1, column=2)

tk.Label(root, text="Backup Version:").grid(row=2, column=0)
entry_version = tk.Entry(root, width=20)
entry_version.grid(row=2, column=1)
entry_version.insert(0, "v1.0")

var_zip = tk.BooleanVar(value=config.get("zip_mode", False))
tk.Checkbutton(root, text="Enable ZIP Compression", variable=var_zip).grid(row=3, column=1)

tk.Button(root, text="START BACKUP", command=run_backup, bg="lightgreen").grid(row=4, column=1, pady=10)

root.mainloop()
