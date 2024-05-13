import tkinter as tk
from tkinter import ttk

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Manager")
        self.clipboard_history = []
        self.current_clipboard_content = ""
        self.setup_ui()
        self.poll_clipboard()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.text_area = tk.Text(self.main_frame, height=10, width=40)
        self.text_area.grid(row=0, column=0, padx=10, pady=10)
        self.history_label = ttk.Label(self.main_frame, text="Clipboard History:")
        self.history_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.history_listbox = tk.Listbox(self.main_frame, height=6)
        self.history_listbox.grid(row=3, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.create_context_menu()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_from_history)
        self.history_listbox.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            self.history_listbox.selection_clear(0, tk.END)
            self.history_listbox.selection_set(self.history_listbox.nearest(event.y))
            self.context_menu.post(event.x_root, event.y_root)
        except tk.TclError:
            pass

    def copy_from_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            content = self.history_listbox.get(selection[0])
            self.root.clipboard_clear()
            self.root.clipboard_append(content)

    def poll_clipboard(self):
        try:
            new_clipboard_content = self.root.clipboard_get()
            if new_clipboard_content != self.current_clipboard_content:
                self.current_clipboard_content = new_clipboard_content
                self.clipboard_history.append(new_clipboard_content)
                self.update_display(new_clipboard_content)
        except tk.TclError:
            pass
        finally:
            self.root.after(1000, self.poll_clipboard)

    def update_display(self, content):
        self.history_listbox.insert(tk.END, content)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)

def main():
    root = tk.Tk()
    app = ClipboardManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
