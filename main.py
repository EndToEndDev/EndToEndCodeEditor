import customtkinter as ctk
from customtkinter import CTkOptionMenu
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import Menu
import subprocess
from pygments import lex
from pygments.lexers import PythonLexer


class CodeEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Code Editor")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.file_path = None

        # Main layout
        self.create_widgets()

    def create_widgets(self):
        # Text editor frame
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Line numbers
        self.line_numbers = ctk.CTkTextbox(self.editor_frame, width=40)
        self.line_numbers.pack(side="left", fill="y")

        # Text editor
        self.text_area = ctk.CTkTextbox(self.editor_frame, wrap="none", undo=True)
        self.text_area.pack(side="left", fill="both", expand=True)

        # Scrollbars
        self.scroll_y = ttk.Scrollbar(self.editor_frame, orient="vertical", command=self.scroll_text_y)
        self.scroll_x = ttk.Scrollbar(self.editor_frame, orient="horizontal", command=self.scroll_text_x)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.text_area.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Bind events
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<KeyRelease>", self.apply_syntax_highlighting, add="+")
        
        # Menu bar
        self.create_menu()

    def create_menu(self):
        menu_bar = Menu(self)  # Use the tkinter Menu class

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Search", command=self.search_text)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Run menu
        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run Code", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        # Set the menu for the application
        self.config(menu=menu_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)
            self.file_path = file_path
            self.update_line_numbers()
            self.title(f"Advanced Code Editor - {file_path}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get("1.0", "end").strip())
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                 filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", "end").strip())
            self.file_path = file_path
            self.title(f"Advanced Code Editor - {file_path}")

    def search_text(self):
        search_window = ctk.CTkToplevel(self)
        search_window.title("Search")
        search_window.geometry("300x100")

        search_label = ctk.CTkLabel(search_window, text="Search:")
        search_label.pack(pady=5)

        search_entry = ctk.CTkEntry(search_window)
        search_entry.pack(pady=5)

        def search():
            query = search_entry.get()
            start = "1.0"
            while True:
                start = self.text_area.search(query, start, stopindex="end")
                if not start:
                    break
                end = f"{start}+{len(query)}c"
                self.text_area.tag_add("highlight", start, end)
                self.text_area.tag_config("highlight", background="yellow", foreground="black")
                start = end

        search_button = ctk.CTkButton(search_window, text="Find", command=search)
        search_button.pack(pady=5)

    def run_code(self):
        if not self.file_path:
            self.save_file_as()

        if self.file_path:
            result = subprocess.run(["python", self.file_path], capture_output=True, text=True)
            output_window = ctk.CTkToplevel(self)
            output_window.title("Code Output")
            output_window.geometry("500x300")

            output_text = ctk.CTkTextbox(output_window)
            output_text.pack(fill="both", expand=True, padx=10, pady=10)
            output_text.insert("1.0", result.stdout + "\n" + result.stderr)

    def scroll_text_y(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def scroll_text_x(self, *args):
        self.text_area.xview(*args)

    def update_line_numbers(self, event=None):
        self.line_numbers.delete("1.0", "end")
        lines = self.text_area.get("1.0", "end").split("\n")
        for i in range(1, len(lines)):
            self.line_numbers.insert("end", f"{i}\n")

    def apply_syntax_highlighting(self, event=None):
        content = self.text_area.get("1.0", "end").strip()
        self.text_area.tag_remove("keyword", "1.0", "end")
        lexer = PythonLexer()
        for token, content in lex(content, lexer):
            if str(token).startswith("Token.Keyword"):
                start = f"1.0+{len(content)}c"
                self.text_area.tag_add("keyword", start, start)
                self.text_area.tag_config("keyword", foreground="cyan")


if __name__ == "__main__":
    app = CodeEditor()
    app.mainloop()
