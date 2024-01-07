from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.tix import IMAGETEXT
from tkcalendar import Calendar
from setlist_manager import SetlistManager
from PIL import Image, ImageTk
from tkinter import Canvas, messagebox

class SetlistManagerUI:
    def __init__(self, setlist_manager):
        self.manager = setlist_manager
        self.root = Tk()
        self.root.title("Setlist Manager")
        self.manager.load_data()

        self.label = Label(self.root, text="Setlist Manager")
        self.label.pack()

        # Create a frame for the buttons
        button_frame = Frame(self.root)
        button_frame.pack()

        self.calendar_btn = Button(button_frame, text="Show Calendar", command=self.show_calendar)
        self.calendar_btn.pack(side='left', padx=7)

        self.add_setlist_btn = Button(button_frame, text="Add Setlist", command=self.add_setlist)
        self.add_setlist_btn.pack(side='left', padx=7)

        self.open_setlist_btn = Button(button_frame, text="Open Setlist", command=self.open_setlist_with_btn)
        self.open_setlist_btn.pack(side='left', padx=7)


        self.delete_setlist_btn = Button(button_frame, text="Delete Setlist", command=self.delete_setlist)
        self.delete_setlist_btn.pack(side='left', padx=7)

        self.setlist_listbox = Listbox(self.root, width=50, height=20)
        self.setlist_listbox.pack(fill=BOTH, expand=True)
        self.setlist_listbox.bind("<Double-Button-1>", self.open_setlist)

        self.show_setlists()

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
            if self.add_entry_btn:
                self.add_entry_btn.config(state=NORMAL)
            if self.add_image_btn:
                self.add_image_btn.config(state=NORMAL)

    def open_setlist_with_btn(self):
        selected_index = self.setlist_listbox.curselection()
        if selected_index:
            setlist_index = int(selected_index[0])
            setlist_name = self.manager.setlists[setlist_index]['name']
            self.show_setlist_entries(setlist_name)
            if self.add_entry_btn:
                self.add_entry_btn.config(state=NORMAL)
            if self.add_image_btn:
                self.add_image_btn.config(state=NORMAL)

    def show_setlist_entries(self, setlist_name):
        top = Toplevel(self.root)
        top.title(setlist_name)

        # Create a Frame to hold the content
        content_frame = Frame(top)
        content_frame.pack(fill=BOTH, expand=True)

        # Create a Frame to hold the buttons
        button_frame = Frame(content_frame)
        button_frame.pack(side='top', fill='x')

        add_entry_btn = Button(button_frame, text="Add Entry", command=lambda: self.add_entry_to_setlist(setlist_name, entries_listbox))
        add_entry_btn.pack(side='left', padx=7)

        delete_entry_btn = Button(button_frame, text="Delete Entry", command=lambda: self.delete_entry_from_setlist(entries_listbox, setlist_name))
        delete_entry_btn.pack(side='left', padx=7)

        add_image_btn = Button(button_frame, text="Pievienot notis", command=lambda: self.add_image_to_entry(setlist_name, entries_listbox))
        add_image_btn.pack(side='left', padx=7)

        fullscreen_btn = Button(button_frame, text="Toggle Fullscreen", command=lambda: self.toggle_fullscreen(top))
        fullscreen_btn.pack(side='left', padx=7)

        view_score_btn = Button(button_frame, text="View Score", command=lambda: self.view_score(setlist_name, entries_listbox))
        view_score_btn.pack(side='left', padx=7)



        entries_listbox = Listbox(content_frame, width=50, height=30, font=("Helvetica", 20))
        entries_listbox.pack(fill="both", expand=True)
        
        setlist_entries = self.manager.get_setlist_entries(setlist_name)

        for entry in sorted(setlist_entries, key=lambda x: x['index']):
            entry_text = f"{entry['index'] + 1}. {entry['description']}"
            entries_listbox.insert(END, entry_text)
            
            

        entries_listbox.bind("<ButtonPress-1>", lambda event, setlist_name=setlist_name: self.on_drag_start(event, entries_listbox, setlist_name))
        entries_listbox.bind("<B1-Motion>", lambda event, setlist_name=setlist_name: self.on_drag_motion(event, entries_listbox, setlist_name))
        entries_listbox.bind("<ButtonRelease-1>", lambda event, setlist_name=setlist_name: self.on_drag_release(event, entries_listbox, setlist_name))
        entries_listbox.bind("<Double-Button-1>", lambda event, setlist_name=setlist_name: self.view_score(setlist_name, entries_listbox))

        
        add_entry_btn.config(command=lambda: (self.add_entry_to_setlist(setlist_name, entries_listbox), self.refresh_numbers(entries_listbox, setlist_name)))
        delete_entry_btn.config(command=lambda: (self.delete_entry_from_setlist(entries_listbox, setlist_name), self.refresh_numbers(entries_listbox, setlist_name)))
        fullscreen_btn.config(command=lambda: self.toggle_fullscreen(top))
        add_image_btn.config(command=lambda: self.add_image_to_entry(setlist_name, entries_listbox))


    def view_score(self, setlist_name, entries_listbox):
        selected_index = entries_listbox.curselection()
        if selected_index:
            entry_index = int(selected_index[0])
            setlist_entries = self.manager.get_setlist_entries(setlist_name)
            entry = setlist_entries[entry_index]

            if 'sheet_music_path' in entry and entry['sheet_music_path']:
                # Open the image if the sheet music path exists
                self.open_image(entry['sheet_music_path'])
            else:
                # Prompt the user to choose a sheet music image
                file_path = filedialog.askopenfilename(title="Choose Sheet Music Image",
                                                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

                if file_path:
                    # Update the selected entry with the chosen image path
                    entry['sheet_music_path'] = file_path

                    # Refresh the listbox to display the updated information
                    self.refresh_numbers(entries_listbox, setlist_name)

                    # Open the chosen image
                    self.open_image(file_path)

                    # Add the image to the entry (optional)
                    self.add_image_to_entry(setlist_name, entries_listbox)
                else:
                    # Display a message if no sheet music is available
                    messagebox.showinfo("No Sheet Music", "No sheet music available for this entry.")


    def open_image(self, sheet_music_path):
        # Open a new window to display the image in fullscreen
        top = Toplevel(self.root)
        top.title("Sheet Music Viewer")

        # Load and display the image on a Canvas widget
        image = Image.open(sheet_music_path)

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        # Calculate the scaling factors for width and height
        width_ratio = screen_width / image.width
        height_ratio = screen_height / image.height

        # Choose the minimum scaling factor to fit the image within the screen
        min_ratio = min(width_ratio, height_ratio)

        # Resize the image while maintaining the aspect ratio
        new_width = int(image.width * min_ratio)
        new_height = int(image.height * min_ratio)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        # Convert the resized image to PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create a Canvas widget and display the resized image centered
        canvas = Canvas(top, width=screen_width, height=screen_height)
        canvas.create_image(screen_width // 2, screen_height // 2, anchor="center", image=photo)
        canvas.image = photo
        canvas.pack(fill=BOTH, expand=True)

        # Bind the escape key to close the fullscreen window
        top.bind("<Escape>", lambda event: top.destroy())





        
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
        print("1234")
        top = Toplevel(self.root)
        top.title("Mani notikumi")

        cal = Calendar(top, selectmode="day")
        cal.pack()
        
        def choose_and_attach_setlist(event):
            selected_date = cal.selection_get()
            print("123")
            setlist_name = simpledialog.askstring("Input", "Choose setlist to attach:")
            if setlist_name:
                self.manager.add_to_calendar(setlist_name, selected_date)
                top.destroy()

                # Open setlist entries upon single click
                self.show_setlist_entries(setlist_name)

        # Bind double-click event to each label in the calendar
        for row in cal._calendar:
            for lbl in row:
                lbl.bind('<Double-1>', choose_and_attach_setlist)
        
        top.mainloop()  # Add this line to keep the window open



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
            entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']}")


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
                entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']}")

            entries_listbox.selection_set(new_index)
            

    def add_entry_to_setlist(self, setlist_name, entries_listbox):
        description = simpledialog.askstring("Input", "Nosaukums:")
        if description is not None:
            self.manager.add_entry_to_setlist(setlist_name, description)
            entries_listbox.insert(END, f"{description}")

    def delete_entry_from_setlist(self, entries_listbox, setlist_name):
        selected_index = entries_listbox.curselection()
        if selected_index:
            entry_index = int(selected_index[0])
            deleted_entry = self.manager.delete_entry_from_setlist(setlist_name, entry_index)
            if deleted_entry:
                self.deleted_entries_listbox.insert(END, f"{deleted_entry['description']}")
                self.refresh_numbers(entries_listbox, setlist_name)


    def show_deleted_entry(self, deleted_entry, entries_listbox, setlist_name):
        top = Toplevel(self.root)
        top.title("Deleted Entry Viewer")

        label = Label(top, text="Deleted Entries:")
        label.pack()

        deleted_entries_text = Text(top, width=50, height=5)
        deleted_entries_text.pack(fill=BOTH, expand=True)

        # Insert the deleted entry information
        deleted_entries_text.insert(END, f"{deleted_entry['description']}")

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
            entries_listbox.insert(END, f"{entry['index'] + 1}. {entry['description']}")

        # Remove the restored entry from the deleted entries window
        deleted_entries_text.delete(1.0, END)  # Clear the entire text content

        # Add other deleted entries back to the text widget
        for entry in self.manager.get_deleted_entries(setlist_name):
            deleted_entries_text.insert(END, f"{entry['description']}")

    def add_image_to_entry(self, setlist_name, entries_listbox):
        selected_index = entries_listbox.curselection()
        if selected_index:
            entry_index = int(selected_index[0])
            setlist_entries = self.manager.get_setlist_entries(setlist_name)
            entry = setlist_entries[entry_index]

            # Ask the user to choose an image file
            file_path = filedialog.askopenfilename(title="Choose Sheet Music Image",
                                                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

            if file_path:
                # Update the selected entry with the chosen image path
                entry['sheet_music_path'] = file_path

                # Refresh the listbox to display the updated information
                self.refresh_numbers(entries_listbox, setlist_name)

    def delete_setlist(self):
        selected_index = self.setlist_listbox.curselection()
        if selected_index:
            setlist_index = int(selected_index[0])
            setlist_name = self.manager.setlists[setlist_index]['name']

            # Confirm the deletion with the user
            confirmation = messagebox.askokcancel("Confirm Deletion", f"Do you really want to delete the setlist '{setlist_name}'?")
            
            if confirmation:
                # Delete the setlist
                self.manager.delete_setlist(setlist_name)

                # Update the setlist listbox
                self.show_setlists()
                self.deleted_entries_listbox.delete(0, END)

    def run(self):
        self.root.mainloop()
        self.manager.save_data()