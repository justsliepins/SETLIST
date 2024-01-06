import json
class SetlistManager:
    def __init__(self):
        self.setlists = []
        self.current_setlist = None

    def create_setlist(self, name):
        setlist = {'name': name, 'entries': []}
        self.setlists.append(setlist)
        self.current_setlist = setlist

    def add_entry(self, desc, score_file_path):
        entry = {'description': desc, 'score': score_file_path}
        self.current_setlist['entries'].append(entry)

    def save_setlist(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.setlists, file)

    def load_setlist(self, filename):
        with open(filename, 'r') as file:
            self.setlists = json.load(file)