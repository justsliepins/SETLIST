import json
from datetime import datetime

class SetlistManager:
    def __init__(self):
        self.setlists = []
        self.calendar = {}
        self.deleted_entries = []
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

        def add_to_calendar(self, setlist_name, date):
            # Convert the date to a string for storage
            formatted_date = date.strftime('%Y-%m-%d')
            self.calendar[formatted_date] = setlist_name

    def get_setlist_for_date(self, date):
        # Convert the date to a string for retrieval
        formatted_date = date.strftime('%Y-%m-%d')
        return self.calendar.get(formatted_date, None)
    
    def delete_setlist(self, setlist_name):
        for setlist in self.setlists:
            if setlist['name'] == setlist_name:
                self.setlists.remove(setlist)
                break

    def save_data(self):
        # Save setlists and deleted entries to a file (e.g., using JSON)
        data = {'setlists': self.setlists, 'deleted_entries': self.deleted_entries}
        with open('setlist_data.json', 'w') as file:
            json.dump(data, file)


    def load_data(self):
        # Load setlists and deleted entries from a file (e.g., using JSON)
        try:
            with open('setlist_data.json', 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.setlists = data.get('setlists', [])
                    self.deleted_entries = data.get('deleted_entries', [])
        except FileNotFoundError:
            pass  # Ignore if the file is not found
