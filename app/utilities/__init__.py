import os
import uuid 
import time
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

current_log = None

def get_next(base="log"):
    i = 0
    while True:
        folder_name = f"{base}_{i}" if i > 0 else f"{base}"

        if not os.path.exists(f"log/{folder_name}"):
            os.makedirs(f"log/{folder_name}", exist_ok=True)
            return folder_name
        i += 1

def start_new_log():
    global current_log
    current_log = get_next()
    return current_log

def log_file(texto, md="full-log"):
    if current_log is None:
        start_new_log()
    
    dir = f"log/{current_log}"

    with open(dir+f"/full-log.md", "a") as main_log:
        main_log.write(str(texto) + "\n")
    
    if md != "full-log":
        file_path = Path(dir) / f"{md}.md"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "a") as specific_log:
            specific_log.write(str(texto) + "\n")

def log_prompt(prompt, prompt_result, prompt_n, log):
    log_file(f"PROMPT: \n", log)
    log_file(f"{prompt}\n", log)
    log_file(f"PROMPT RESULT: \n", log)
    log_file(f"{prompt_result}", log)