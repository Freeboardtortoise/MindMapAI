import customtkinter as ctk
import tkinter as tk
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
        self.geometry("800x600")
        self.notes = {'my first note':"this is the context of your first note"}
        self.mindmap = {}
        self.mapFrame = ctk.CTkFrame(self)
        self.mapFrame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        self.create_top_bar()
        self.create_notes_frame()
        self.make_canvas()

    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=50)
        self.top_bar.pack(side="top", fill="x", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.top_bar, text="MindMapAI")
        self.title_label.pack(side="left", padx=10)

        self.generate_button = ctk.CTkButton(self.top_bar, text="Generate", command=self.on_generate)
        self.generate_button.pack(side="right", padx=10)

        self.saveButton = ctk.CTkButton(self.top_bar, text="Save", command=self.on_save)
        self.saveButton.pack(side="right", padx=10)
    
    def on_save(self):
        with open("notes.json", "w") as f:
            json.dump(self.notes, f)
    
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
            note_button = ctk.CTkButton(self.all_notes_frame, text=note, command=lambda note=note: self.open_note(note))
            note_button.pack(side="top", padx=10, pady=10, fill="x")

            self.noteButtons.append(note_button)
    
    def open_note(self, note):
        print(note)
        self.noteInput.delete("1.0", "end")
        self.noteInput.insert("1.0", self.notes[note])

        self.title.delete(0, "end")
        self.title.insert(0, note)
    
    def on_delete_note(self):
        note = self.title.get()
        if note in self.notes:
            del self.notes[note]
            self.update_notes_frame()

    
    def update_notes_frame(self):
        clear_frame(self.all_notes_frame)
        self.create_all_notes_frame()


    def on_add_note(self):
        note = self.noteInput.get("1.0", "end").strip()
        if note:
            self.notes.setdefault(self.title.get(), note)
            self.noteInput.delete("1.0", "end")
        self.update_notes_frame()

    def on_generate(self):
        if self.notes:
            # Here you’d call your mind map generator function
            self.mindmap = aim.generate_mindmap(self.notes)
            # print(self.mindmap)
        else:
            self.status_label.configure(text="Please enter some notes!")
        self.change_graph()
    
    def make_canvas(self):
        self.map_canvas = tk.Canvas(self.mapFrame, width=800, height=600, bg="#1e1e2e")
        self.map_canvas.pack(fill="both", expand=True)
        self.map_canvas.create_oval(50, 50, 90, 90, fill="#89b4fa", outline="")
        self.map_canvas.create_text(70, 70, text="Note A", fill="#cdd6f4")
    
    def change_graph(self):
        self.map_canvas.delete("all")
        # adding the lines
        node_stuff = aim.generate_node_stuff(self.mindmap)
        for node in self.mindmap:
            for connection in self.mindmap[node]["connections"]:
                x1, x2 = node_stuff[connection]["x"] + int(node_stuff[connection]["width"] / 2), node_stuff[node]["x"] + int(node_stuff[node]["width"] / 2)
                y1, y2 = node_stuff[connection]["y"] + int(node_stuff[connection]["height"] / 2), node_stuff[node]["y"] + int(node_stuff[node]["height"] / 2)
                line = self.map_canvas.create_line(x1, y1, x2, y2, fill="#89b4fa", width=2, tags="line")
        #adding nodes
        for node in node_stuff:
            self.map_canvas.create_rectangle(node_stuff[node]["x"], node_stuff[node]["y"], node_stuff[node]["x"]+ node_stuff[node]["width"], node_stuff[node]["height"] + node_stuff[node]["y"], fill="#89b4fa")
            self.map_canvas.create_text(node_stuff[node]["x"] + int(node_stuff[node]["width"] / 2), node_stuff[node]["y"] + int(node_stuff[node]["height"] / 2), text=node, fill="#cdd6f4")

            

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

