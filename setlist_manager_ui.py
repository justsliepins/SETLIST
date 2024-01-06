from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from setlist_manager import SetlistManager

class SetlistManagerUI:
    def __init__(self, setlist_manager):
        self.manager = setlist_manager
        self.root = Tk()
        self.root.title("Setlist Manager")

        self.label = Label(self.root, text="Setlist Managr")
        self.label.pack()

        self.add_btn = Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_btn.pack()

        self.save_btn = Button(self.root, text="Save Setlist", command=self.save_setlist)
        self.save_btn.pack()

        self.load_btn = Button(self.root, text="Load Setlist", command=self.load_setlist)
        self.load_btn.pack()

    def add_entry(self):
            # Add logic to get sheet music path from the user
            desc = simpledialog.askstring("Input", "Enter description:")
            sheet_music_path = self.choose_file()

            # Add entry to the current setlist
            if desc is not None and sheet_music_path:
                self.manager.add_entry(desc, sheet_music_path)

    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Choose Sheet Music Image",
                                                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        return file_path    
    
    def save_setlist(self):
        # Add logic to get the filename from the user
        file_name = input("Enter filename to save setlist: ")
        self.manager.save_setlist(file_name)

    def load_setlist(self):
        filename = filedialog.askopenfilename(title="Load Setlist",
                                               filetypes=[("JSON Files", "*.json")])
        if filename:
            self.manager.load_setlist(filename)
    def run(self):
        self.root.mainloop()