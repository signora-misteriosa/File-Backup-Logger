import shutil
import os
import time
import zipfile
import json
from datetime import datetime

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {"last_source": "", "last_destination": "", "zip_mode": False}

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def copy_folder(src, dst):
    shutil.copytree(src, dst)

def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, rel_path)

def perform_backup(src, base_destination, version="v1.0", zip_mode=False):
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"backup_{timestamp}_{version}"
    final_path = os.path.join(base_destination, folder_name)
    copy_folder(src, final_path)
    if zip_mode:
        zip_path = final_path + ".zip"
        zip_folder(final_path, zip_path)
        shutil.rmtree(final_path)
        final_path = zip_path
    duration = round(time.time() - start_time, 2)
    file_count = sum(len(files) for _, _, files in os.walk(src))
    log_entry = f"[{timestamp}] Backup: {final_path} | Files: {file_count} | Duration: {duration}s\n"
    os.makedirs("logs", exist_ok=True)
    with open("logs/backup.log", "a") as log_file:
        log_file.write(log_entry)
    return final_path, file_count, duration
