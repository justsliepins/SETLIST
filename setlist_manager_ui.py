from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.tix import IMAGETEXT
from tkcalendar import Calendar
from setlist_manager import SetlistManager

class SetlistManagerUI:
    def __init__(self, setlist_manager):
        self.manager = setlist_manager
        self.root = Tk()
        self.root.title("Setlist Manager")

        self.label = Label(self.root, text="Setlist Manager")
        self.label.pack()

        self.load_btn = Button(self.root, text="Load Setlist", command=self.load_setlist)
        self.load_btn.pack()

        self.calendar_btn = Button(self.root, text="Show Calendar", command=self.show_calendar)
        self.calendar_btn.pack()

        self.add_setlist_btn = Button(self.root, text="Add Setlist", command=self.add_setlist)
        self.add_setlist_btn.pack()

        self.setlist_listbox = Listbox(self.root, width=50, height=20)
        self.setlist_listbox.pack(fill=BOTH, expand=True)
        self.setlist_listbox.bind("<Double-Button-1>", self.open_setlist)

        self.show_setlists()

        self.add_entry_btn = Button(self.root, text="Add Entry", command=self.add_entry, state=DISABLED)
        self.add_entry_btn.pack()


        self.open_setlist_btn = Button(self.root, text="Open Setlist", command=self.open_setlist)
        self.open_setlist_btn.pack()

        self.deleted_entries_label = Label(self.root, text="Deleted Entries:")
        self.deleted_entries_label.pack()

        self.deleted_entries_listbox = Listbox(self.root, width=50, height=5)
        self.deleted_entries_listbox.pack(fill=BOTH, expand=True)
        self.deleted_entries_listbox.bind("<Double-Button-1>", self.restore_deleted_entry)
        
    def add_setlist(self):
        setlist_name = simpledialog.askstring("Input", "Enter setlist name:")
        if setlist_name:
            self.manager.add_setlist(setlist_name)
            self.show_setlists()
    
    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Choose Sheet Music Image",
                                                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        return file_path    
    
    def save_setlist(self):
        file_name = input("Enter filename to save setlist: ")
        self.manager.save_setlist(file_name)

    def load_setlist(self):
        filename = filedialog.askopenfilename(title="Load Setlist",
                                               filetypes=[("JSON Files", "*.json")])
        if filename:
            self.manager.load_setlist(filename)

    def show_setlists(self):
        self.setlist_listbox.delete(0, END)
        for idx, setlist in enumerate(self.manager.setlists):
            setlist_name = setlist['name']
            self.setlist_listbox.insert(END, f"{idx + 1}. {setlist_name}")

    def open_setlist(self, event):
        selected_index = self.setlist_listbox.curselection()
        if selected_index:
            setlist_index = int(selected_index[0])
            setlist_name = self.manager.setlists[setlist_index]['name']
            self.show_setlist_entries(setlist_name)
            self.add_entry_btn.config(state=NORMAL)

    def show_setlist_entries(self, setlist_name):
        top = Toplevel(self.root)
        top.title(setlist_name)

        # Create a Frame to hold the content
        content_frame = Frame(top)
        content_frame.pack(fill=BOTH, expand=True)

        label = Label(content_frame, text=f"Setlist: {setlist_name}")
        label.pack()

        entries_listbox = Listbox(content_frame, width=50, height=30)
        entries_listbox.pack(fill=BOTH, expand=True)

        setlist_entries = self.manager.get_setlist_entries(setlist_name)

        for entry in sorted(setlist_entries, key=lambda x: x['index']):
            entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']} | View Score")

        entries_listbox.bind("<ButtonPress-1>", lambda event, setlist_name=setlist_name: self.on_drag_start(event, entries_listbox, setlist_name))
        entries_listbox.bind("<B1-Motion>", lambda event, setlist_name=setlist_name: self.on_drag_motion(event, entries_listbox, setlist_name))
        entries_listbox.bind("<ButtonRelease-1>", lambda event, setlist_name=setlist_name: self.on_drag_release(event, entries_listbox, setlist_name))

        add_entry_btn = Button(content_frame, text="Add Entry", command=lambda: self.add_entry_to_setlist(setlist_name, entries_listbox))
        add_entry_btn.pack()

        delete_entry_btn = Button(content_frame, text="Delete Entry", command=lambda: self.delete_entry_from_setlist(entries_listbox, setlist_name))
        delete_entry_btn.pack()

        fullscreen_btn = Button(content_frame, text="Toggle Fullscreen", command=lambda: self.toggle_fullscreen(top))
        fullscreen_btn.pack()
        # Store the initial window size for toggling fullscreen
        top.initial_geometry = top.geometry()

        add_entry_btn.config(command=lambda: (self.add_entry_to_setlist(setlist_name, entries_listbox), self.refresh_numbers(entries_listbox, setlist_name)))
        delete_entry_btn.config(command=lambda: (self.delete_entry_from_setlist(entries_listbox, setlist_name), self.refresh_numbers(entries_listbox, setlist_name)))
        fullscreen_btn.config(command=lambda: self.toggle_fullscreen(top))

    def toggle_fullscreen(self, window):
        if window.attributes("-fullscreen"):
            window.attributes("-fullscreen", False)
            window.geometry(window.initial_geometry)
        else:
            window.attributes("-fullscreen", True)
            window.initial_geometry = window.geometry()  # Update initial geometry

    # Function to toggle fullscreen
        

    def show_setlists(self):
        self.setlist_listbox.delete(0, END)
        for idx, setlist in enumerate(self.manager.setlists):
            setlist_name = setlist['name']
            self.setlist_listbox.insert(END, setlist_name)

    def show_calendar(self):
        top = Toplevel(self.root)
        top.title("Mani notikumi")

        cal = Calendar(top, selectmode="day")
        cal.pack()

        setlist_name = simpledialog.askstring("Input", "Enter setlist name:")
        if setlist_name:
            date = cal.selection_get()
            self.manager.add_to_calendar(setlist_name, date) 

    def show_sheet_music(self, setlist_entry):
        top = Toplevel(self.root)
        top.title("Sheet Music Viewer")

        image = Image.open(setlist_entry['sheet_music_path'])
        photo = IMAGETEXT.PhotoImage(image)

        label = Label(top, image=photo)
        label.image = photo
        label.pack()

    def add_entry(self):
        description = simpledialog.askstring("Input", "Enter description:")
        sheet_music_path = self.choose_file()

        # Add entry to the current setlist
        if description is not None and sheet_music_path:
            self.manager.add_entry(description, sheet_music_path)
            self.show_sheet_music({'description': description, 'sheet_music_path': sheet_music_path})

    def refresh_numbers(self, entries_listbox, setlist_name):
        entries_listbox.delete(0, END)
        setlist_entries = self.manager.get_setlist_entries(setlist_name)
        for entry in sorted(setlist_entries, key=lambda x: x['index']):
            entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']} | View Score")


    def on_drag_start(self, event, entries_listbox, setlist_name):
        index = entries_listbox.nearest(event.y)
        self.drag_data = {"index": index, "x": event.x, "y": event.y, "setlist_name": setlist_name}

    def on_drag_motion(self, event, entries_listbox, setlist_name):
        if "index" in self.drag_data:
            index = entries_listbox.nearest(event.y)
            entries_listbox.selection_clear(0, END)
            entries_listbox.selection_set(index)
            entries_listbox.activate(index)
            entries_listbox.yview_scroll(int((event.y - self.drag_data["y"]) / 20), "units")

    def on_drag_release(self, event, entries_listbox, setlist_name):
        if "index" in self.drag_data:
            new_index = entries_listbox.nearest(event.y)
            entry = entries_listbox.get(self.drag_data["index"])
            entries_listbox.delete(self.drag_data["index"])
            entries_listbox.insert(new_index, entry)

            # Rearrange entries in the manager
            self.manager.rearrange_setlist_entries(setlist_name, self.drag_data["index"], new_index)

            # Manually reassign sequence numbers
            setlist_entries = self.manager.get_setlist_entries(setlist_name)
            for i, entry in enumerate(setlist_entries):
                entry['index'] = i

            # Refresh the numbers in the listbox
            entries_listbox.delete(0, END)
            for entry in sorted(setlist_entries, key=lambda x: x['index']):
                entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']} | View Score")

            entries_listbox.selection_set(new_index)

    def add_entry_to_setlist(self, setlist_name, entries_listbox):
        description = simpledialog.askstring("Input", "Nosaukums:")
        if description is not None:
            self.manager.add_entry_to_setlist(setlist_name, description)
            entries_listbox.insert(END, f"{description} | View Score")

    def delete_entry_from_setlist(self, entries_listbox, setlist_name):
        selected_index = entries_listbox.curselection()
        if selected_index:
            entry_index = int(selected_index[0])
            deleted_entry = self.manager.delete_entry_from_setlist(setlist_name, entry_index)
            if deleted_entry:
                self.deleted_entries_listbox.insert(END, f"{deleted_entry['description']} | View Score")
                self.refresh_numbers(entries_listbox, setlist_name)


    def show_deleted_entry(self, deleted_entry, entries_listbox, setlist_name):
        top = Toplevel(self.root)
        top.title("Deleted Entry Viewer")

        label = Label(top, text="Deleted Entries:")
        label.pack()

        deleted_entries_text = Text(top, width=50, height=5)
        deleted_entries_text.pack(fill=BOTH, expand=True)

        # Insert the deleted entry information
        deleted_entries_text.insert(END, f"{deleted_entry['description']} | View Score | Restore\n")

        # Bind double-click event to restore the entry
        deleted_entries_text.tag_configure("clickable", foreground="blue", underline=True)
        deleted_entries_text.tag_bind("clickable", "<Double-1>", lambda event, entry=deleted_entry, el=entries_listbox, sln=setlist_name, det=deleted_entries_text: self.restore_deleted_entry(entry, el, sln, det))

        # Apply the clickable tag to the "Restore" part of the text
        deleted_entries_text.tag_add("clickable", "2.0", "2.end")
        deleted_entries_text.config(state=DISABLED)  # Disable editing

        top.mainloop()  # Add this line to keep the window open




    def restore_deleted_entry(self, deleted_entry, entries_listbox, setlist_name, deleted_entries_text):
        # Restore the entry to the setlist
        description = deleted_entry['description']
        sheet_music_path = deleted_entry['sheet_music_path']
        self.manager.restore_deleted_entry(setlist_name, description, sheet_music_path)

        # Refresh the numbers in the listbox
        setlist_entries = self.manager.get_setlist_entries(setlist_name)
        entries_listbox.delete(0, END)
        for entry in sorted(setlist_entries, key=lambda x: x['index']):
            entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']} | View Score")

        # Remove the restored entry from the deleted entries window
        deleted_entries_text.delete(1.0, END)  # Clear the entire text content

        # Add other deleted entries back to the text widget
        for entry in self.manager.get_deleted_entries(setlist_name):
            deleted_entries_text.insert(END, f"{entry['description']} | View Score | Restore\n")

    def run(self):
        self.root.mainloop()