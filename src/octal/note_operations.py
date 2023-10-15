
import os
import json

class NoteOperations:
    def __init__(self, notes_dir, config_path):
        self.notes_dir = notes_dir
        self.config_path = config_path

    def create_note(self, note_name, content):
        note_path = os.path.join(self.notes_dir, f"{note_name}.md")
        with open(note_path, "w") as f:
            f.write(content)

    def read_note(self, note_name):
        note_path = os.path.join(self.notes_dir, f"{note_name}.md")
        with open(note_path, "r") as f:
            return f.read()

    def update_note(self, note_name, content):
        self.create_note(note_name, content)

    def delete_note(self, note_name):
        note_path = os.path.join(self.notes_dir, f"{note_name}.md")
        os.remove(note_path)

    def read_config(self):
        with open(self.config_path, "r") as f:
            return json.load(f)

    def write_config(self, data):
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)
