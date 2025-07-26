import customtkinter as ctk
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
        self.notes = ['my first note']
        self.mindmap = {}
        self.create_top_bar()
        self.create_notes_frame()

    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=50)
        self.top_bar.pack(side="top", fill="x", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.top_bar, text="MindMapAI")
        self.title_label.pack(side="left", padx=10)

        self.generate_button = ctk.CTkButton(self.top_bar, text="Generate", command=self.on_generate)
        self.generate_button.pack(side="right", padx=10)
    
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

        self.noteInput = ctk.CTkTextbox(self.notesFrame, height=10, width=500)
        self.noteInput.pack(padx=10, pady=10, fill="both", expand=True)

        self.addButton = ctk.CTkButton(self.notesFrame, text="Add Note", command=self.on_add_note)
        self.addButton.pack(side="left", padx=10, pady=10)

    def create_all_notes_frame(self):
        for note in self.notes:
            note_button = ctk.CTkButton(self.all_notes_frame, text=note)
            note_button.pack(side="top", padx=10, pady=10, fill="x")
    
    def update_notes_frame(self):
        clear_frame(self.all_notes_frame)
        self.create_all_notes_frame()


    def on_add_note(self):
        note = self.noteInput.get("1.0", "end").strip()
        if note:
            self.notes.append(note)
            self.noteInput.delete("1.0", "end")
            print(self.notes)
        self.update_notes_frame()

    def on_generate(self):
        if self.notes:
            # Here you’d call your mind map generator function
            self.mindmap = aim.generate_mindmap(self.notes)
            print(self.mindmap)
        else:
            self.status_label.configure(text="Please enter some notes!")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

