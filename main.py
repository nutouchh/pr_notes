import json
import tkinter as tk
from tkinter import messagebox
from uuid import uuid4

from storage import load_notes, save_notes


class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Заметки")
        self.root.geometry("700x420")
        self.selected_id = None

        try:
            self.notes = load_notes()
        except (OSError, json.JSONDecodeError) as error:
            messagebox.showerror("Ошибка", f"Не удалось открыть notes.json:\n{error}")
            self.root.destroy()
            return

        left = tk.Frame(root, padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left, text="Список заметок").pack(anchor="w")
        self.note_list = tk.Listbox(left, width=25, height=18)
        self.note_list.pack(fill=tk.Y, expand=True)
        self.note_list.bind("<<ListboxSelect>>", self.select_note)
        tk.Button(left, text="Новая", command=self.new_note).pack(
            fill=tk.X, pady=(8, 0)
        )

        right = tk.Frame(root, padx=10, pady=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(right, text="Заголовок").pack(anchor="w")
        self.title_entry = tk.Entry(right)
        self.title_entry.pack(fill=tk.X)
        tk.Label(right, text="Текст").pack(anchor="w", pady=(10, 0))
        self.body_text = tk.Text(right, height=15)
        self.body_text.pack(fill=tk.BOTH, expand=True)

        buttons = tk.Frame(right)
        buttons.pack(fill=tk.X, pady=(8, 0))
        tk.Button(buttons, text="Сохранить", command=self.save_note).pack(
            side=tk.LEFT
        )
        tk.Button(buttons, text="Удалить", command=self.delete_note).pack(
            side=tk.LEFT, padx=8
        )

        self.refresh_list()

    def refresh_list(self):
        self.note_list.delete(0, tk.END)
        for note in self.notes:
            self.note_list.insert(tk.END, note["title"])

    def select_note(self, event=None):
        selection = self.note_list.curselection()
        if not selection:
            return

        note = self.notes[selection[0]]
        self.selected_id = note["id"]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note["title"])
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert("1.0", note["body"])

    def new_note(self):
        self.selected_id = None
        self.note_list.selection_clear(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        self.title_entry.focus_set()

    def save_note(self):
        title = self.title_entry.get().strip()
        body = self.body_text.get("1.0", "end-1c")

        if not title:
            messagebox.showwarning("Заголовок", "Введите заголовок заметки")
            return

        if self.selected_id is None:
            note = {"id": str(uuid4()), "title": title, "body": body}
            self.notes.append(note)
            self.selected_id = note["id"]
        else:
            note = next(
                note for note in self.notes if note["id"] == self.selected_id
            )
            note["title"] = title
            note["body"] = body

        try:
            save_notes(self.notes)
        except OSError as error:
            messagebox.showerror(
                "Ошибка", f"Не удалось сохранить заметки:\n{error}"
            )
            return

        self.refresh_list()
        index = self.notes.index(note)
        self.note_list.selection_set(index)
        self.note_list.activate(index)

    def delete_note(self):
        if self.selected_id is None:
            messagebox.showinfo("Удаление", "Сначала выберите заметку")
            return

        if not messagebox.askyesno(
            "Удаление", "Удалить выбранную заметку?"
        ):
            return

        self.notes = [
            note for note in self.notes if note["id"] != self.selected_id
        ]

        try:
            save_notes(self.notes)
        except OSError as error:
            messagebox.showerror(
                "Ошибка", f"Не удалось сохранить заметки:\n{error}"
            )
            return

        self.refresh_list()
        self.new_note()


if __name__ == "__main__":
    window = tk.Tk()
    NotesApp(window)
    window.mainloop()