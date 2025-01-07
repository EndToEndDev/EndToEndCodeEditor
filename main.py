import tkinter as tk
from tkinter import filedialog, messagebox


class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")
        self.file_path = None

        # Create a text area
        self.text_area = tk.Text(self.root, wrap="none", undo=True)
        self.text_area.pack(fill="both", expand=True)

        # Add scrollbars
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.text_area.yview)
        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.text_area.xview)
        self.text_area.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        # Create a menu
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.file_path = file_path
            self.root.title(f"Python Code Editor - {file_path}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END).strip())
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                 filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END).strip())
            self.file_path = file_path
            self.root.title(f"Python Code Editor - {file_path}")

    def show_about(self):
        messagebox.showinfo("About", "Simple Python Code Editor\nCreated with Tkinter!")


if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.geometry("800x600")
    root.mainloop()
