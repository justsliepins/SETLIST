import json
from datetime import datetime

class SetlistManager:
    def __init__(self):
        self.setlists = []
        self.calendar_entries = []
        self.current_setlist = None

    def create_setlist(self, name):
        setlist = {'name': name, 'entries': []}
        self.setlists.append(setlist)
        self.current_setlist = setlist

    def add_setlist(self, setlist_name):
        setlist = {
            'name': setlist_name,
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'entries': []
        }
        self.setlists.append(setlist)

    def save_setlist(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.setlists, file)

    def add_entry_to_setlist(self, setlist_name, description, sheet_music_path=None):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name:
                index = len(setlist['entries'])
                entry = {'description': description, 'sheet_music_path': sheet_music_path, 'index': index} if sheet_music_path else {'description': description, 'index': index}
                setlist['entries'].append(entry)

    # Inside SetlistManager class in setlist_manager.py

    def delete_entry_from_setlist(self, setlist_name, entry_index):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name and 0 <= entry_index < len(setlist['entries']):
                deleted_entry = setlist['entries'].pop(entry_index)
                return deleted_entry
        return None

    def load_setlist(self, filename):
        with open(filename, 'r') as file:
            self.setlists = json.load(file)

    def get_setlist_entries(self, setlist_name):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name:
                return setlist['entries']

    def add_setlist_to_calendar(self, setlist_name, date):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name:
                setlist_entry = {
                    'description': setlist_name,
                    'date': date.strftime('%Y-%m-%d'),
                    'setlist_index': self.setlists.index(setlist)
                }
                self.calendar_entries.append(setlist_entry)

    def rearrange_setlist_entries(self, setlist_name, old_index, new_index):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name and 0 <= old_index < len(setlist['entries']) and 0 <= new_index < len(setlist['entries']):
                entry = setlist['entries'].pop(old_index)
                setlist['entries'].insert(new_index, entry)

                for i, entry in enumerate(setlist['entries']):
                    entry['index'] = i

    def update_sequence_numbers(self, setlist_name):
        setlist = next((s for s in self.setlists if s['name'] == setlist_name), None)
        if setlist:
            for i, entry in enumerate(setlist['entries']):
                entry['index'] = i

    def show_calendar_entries(self):
        for entry in self.calendar_entries:
            print(f"Date: {entry['date']}, Setlist: {entry['description']}")
