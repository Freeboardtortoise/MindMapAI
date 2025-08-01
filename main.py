import customtkinter as ctk
import tkinter as tk
import json
import copy
# API key "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"

import AI_Manager as aim

ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MindMapAI")
        self.geometry("1500x600")
        self.notes = {'my first note':"this is the context of your first note"}
        self.mindmap = {}
        self.mapFrame = ctk.CTkFrame(self)
        self.mapFrame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        self.create_top_bar()
        self.create_notes_frame()
        self.make_canvas()
        self.initialise_keyboard_shortcuts()
        self.theme = "dark"
        self.load_theme()
        self.currentNote = 0
        self.undo_stack = []
        self.undo_stack_pointer = 0
        self.undo_stack_limit = 10

    def load_theme(self):
        theme_path = f"themes/{self.theme}.json"
        with open(theme_path, 'r') as f:
            data = json.load(f)
        ctk.set_appearance_mode(data["mode"])
        ctk.set_default_color_theme(data["color_theme"])

    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=50)
        self.top_bar.pack(side="top", fill="x", padx=10, pady=10, expand=False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.top_bar, text="MindMapAI")
        self.title_label.pack(side="left", padx=10)

        self.generate_button = ctk.CTkButton(self.top_bar, text="Generate", command=self.on_generate)
        self.generate_button.pack(side="right", padx=10)

        self.saveButton = ctk.CTkButton(self.top_bar, text="Save", command=self.on_save)
        self.saveButton.pack(side="right", padx=10)

        self.loadButton = ctk.CTkButton(self.top_bar, text="Load", command=self.on_load)
        self.loadButton.pack(side="right", padx=10)

        self.projectName = ctk.CTkEntry(self.top_bar, placeholder_text="Project Name")
        self.projectName.pack(side="right", padx=10, pady=10)

        self.theme_button = ctk.CTkOptionMenu(self.top_bar, values=["dark", "light"], command=self.change_theme)
        self.theme_button.pack(side="right", padx=10)

    def change_theme(self, theme_name):
        self.theme = theme_name
        self.load_theme()
    
    def initialise_keyboard_shortcuts(self):
        self.bind_all("<Control-s>", self.on_save)

        # note stuff (adding notes and removing notes)
        self.bind_all("<Control-Return>", self.on_add_note)
        self.bind_all("<Control-BackSpace>", self.on_delete_note)

        # navigation
        self.bind_all("<Control-period>", self.next_note)
        self.bind_all("<Control-comma>", self.prev_note)

        self.noteInput.bind("<Control-Return>", self.on_add_note)
        self.noteInput.bind("<Control-BackSpace>", self.on_delete_note)

        # generating notes
        self.bind_all("<Control-E>", self.on_generate)

        # undo and redo
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-Shift-z>", self.redo)
    

    def undo(self, event=None):
        print("undo_stack ", self.undo_stack)
        print("undo_stack_pointer ", str(self.undo_stack_pointer))
        self.undo_stack_pointer -= 1
        if self.undo_stack_pointer >= 0:
            self.notes = self.undo_stack[self.undo_stack_pointer]
            self.change_graph()
            self.update_notes_frame()
        else:
            self.undo_stack_pointer = 0
    
    def redo(self, event=None):
        self.undo_stack_pointer += 1
        if self.undo_stack_pointer < len(self.undo_stack):
            self.notes = self.undo_stack[self.undo_stack_pointer]
            self.update_notes_frame()
        else:
            self.undo_stack_pointer = len(self.undo_stack)
    
    def next_note(self, event=None):
        self.currentNote += 1
        self.currentNote %= (len(self.notes))
        self.open_note(list(self.notes.keys())[self.currentNote])
    
    def prev_note(self, event=None):
        self.currentNote -= 1
        self.currentNote %= (len(self.notes))
        self.open_note(list(self.notes.keys())[self.currentNote])
    
    def on_save(self, event=None):
        with open(self.projectName.get() + ".json", "w") as f:
            json.dump(self.notes, f)
    

    def on_load(self):
        try:
            with open(self.projectName.get() + ".json", "r") as f:
                self.notes = json.load(f)
                self.change_graph()
                self.update_notes_frame()
        except FileNotFoundError:
            pass
    

    
    def create_notes_frame(self):
        self.notesFrame = ctk.CTkFrame(self)
        self.notesFrame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        self.all_notes_frame = ctk.CTkFrame(self.notesFrame)
        self.all_notes_frame.pack(side="left", padx=10, pady=10, fill="y", expand=True)

        self.create_all_notes_frame()
        self.create_new_notes_frame()
    
    def create_new_notes_frame(self):
        self.new_notes_frame = ctk.CTkFrame(self.notesFrame)
        self.new_notes_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        # self.new_notes_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.title = ctk.CTkEntry(self.new_notes_frame, placeholder_text="Title")
        self.title.pack(side="top", padx=10, pady=10, fill="x")

        self.noteInput = ctk.CTkTextbox(self.new_notes_frame, height=10, width=500)
        self.noteInput.pack(padx=10, pady=10, fill="both", expand=True)

        self.addButton = ctk.CTkButton(self.new_notes_frame, text="Save", command=self.on_add_note)
        self.addButton.pack(side="left", padx=10, pady=10)

        self.deleteButton = ctk.CTkButton(self.new_notes_frame, text="Delete", command=self.on_delete_note)
        self.deleteButton.pack(side="right", padx=10, pady=10)
    def create_all_notes_frame(self):
        self.noteButtons = []
        for note in self.notes:
            note_button = ctk.CTkButton(self.all_notes_frame, text=note, command=lambda note=note: self.open_note(note), height=10)
            note_button.pack(side="top", padx=10, pady=10, fill="x")

            self.noteButtons.append(note_button)
    
    def open_note(self, note):
        print(note)
        self.noteInput.delete("1.0", "end")
        self.noteInput.insert("1.0", self.notes[note])

        self.title.delete(0, "end")
        self.title.insert(0, note)
    
    def on_delete_note(self, event=None):
        note = self.title.get()
        if note in self.notes:
            del self.notes[note]
            self.update_notes_frame()

    
    def update_notes_frame(self):
        clear_frame(self.all_notes_frame)
        self.create_all_notes_frame()


    def on_add_note(self, event=None):
        note = self.noteInput.get("1.0", "end").strip()
        if note:
            self.notes.setdefault(self.title.get(), note)
            self.noteInput.delete("1.0", "end")

            self.title.delete(0, "end")
            self.title.focus_set()
        self.update_notes_frame()
        self.undo_stack.append(copy.deepcopy(self.notes))
        self.undo_stack_pointer += 1
        if len(self.undo_stack) > self.undo_stack_limit:
            self.undo_stack.pop(0)

    def on_generate(self):
        if self.notes:
            # Here you’d call your mind map generator function
            self.mindmap = aim.generate_mindmap(self.notes, 12, (self.map_canvas.winfo_width(), self.winfo_height()))
            print(self.mindmap)
            # print(self.mindmap)
        else:
            pass
        self.change_graph()
    
    def make_canvas(self):
        self.map_canvas = tk.Canvas(self.mapFrame, width=800, height=600, bg="#1e1e2e")
        self.map_canvas.pack(fill="both", expand=True, padx=10, pady=10, side="right", anchor="n", ipady=10, ipadx=10)
    
    def change_graph(self):
        self.map_canvas.delete("all")
        self.map_canvas.update()
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()

        print(f"self.mindmap: {self.mindmap}")


        # adding the lines

        for node in self.mindmap:
            for connection in self.mindmap[node]["connections"]:
                if connection in self.mindmap:
                    x1, x2 = self.mindmap[connection]["x"] + int(self.mindmap[connection]["width"] / 2), self.mindmap[node]["x"] + int(self.mindmap[node]["width"] / 2)
                    y1, y2 = self.mindmap[connection]["y"] + int(self.mindmap[connection]["height"] / 2), self.mindmap[node]["y"] + int(self.mindmap[node]["height"] / 2)
                    line = self.map_canvas.create_line(x1, y1, x2, y2, fill=self.mindmap[node]["color"], width=2, tags="line")
        #adding nodes
        for node in self.mindmap:
            self.map_canvas.create_rectangle(self.mindmap[node]["x"], self.mindmap[node]["y"], self.mindmap[node]["x"]+ self.mindmap[node]["width"], self.mindmap[node]["height"] + self.mindmap[node]["y"],fill=self.mindmap[node]["color"])
            self.map_canvas.create_text(self.mindmap[node]["x"] + int(self.mindmap[node]["width"] / 2), self.mindmap[node]["y"] + int(self.mindmap[node]["height"] / 2), text=node, fill=self.mindmap[node]["text-color"], font=("Arial", 12))

            

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

