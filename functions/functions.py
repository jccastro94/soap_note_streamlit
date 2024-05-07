
import os
import datetime


def log_txt(conversation, patient_id):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = f"{log_folder}/{patient_id}_{timestamp}.txt"
    try:
        with open(log_file, "a", encoding="utf-8") as f: 
            if isinstance(conversation, str):
                f.write(conversation + "\n") 
            elif isinstance(conversation, dict):
                f.writelines([f"{msg['role']}: {msg['content']}\n" for msg in conversation]) 
            else:
                f.write("Unsupported data type for conversation\n")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
