import os
import shutil
import hashlib
import json

SOURCE_DIR = "./data"
BACKUP_DIR = "./backup"
STATE_FILE = "backup_state.json"


def ensure_directories():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def file_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def backup_files():
    state = load_state()
    updated = False

    for file in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, file)
        if not os.path.isfile(src_path):
            continue

        current_hash = file_hash(src_path)
        if state.get(file) != current_hash:
            shutil.copy2(src_path, BACKUP_DIR)
            state[file] = current_hash
            print(f"Backed up: {file}")
            updated = True
        else:
            print(f"Skipped (unchanged): {file}")

    if updated:
        save_state(state)


if __name__ == "__main__":
    ensure_directories()
    backup_files()

