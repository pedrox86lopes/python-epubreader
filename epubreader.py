import tkinter as tk
from tkinter import filedialog, messagebox
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
from tkhtmlview import HTMLLabel  # Import HTML rendering widget

class EPUBReader:
    def __init__(self, root):
        self.root = root
        self.root.title("EPUB Reader")
        self.root.geometry("800x600")

        # Menu
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open EPUB", command=self.open_epub)
        file_menu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

        # Scrollable HTML viewer
        self.html_label = HTMLLabel(self.root, wrap=tk.WORD, font=("Arial", 12), background="white")
        self.html_label.pack(expand=True, fill=tk.BOTH)

    def open_epub(self):
        file_path = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
        if file_path:
            try:
                self.load_epub(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open EPUB file: {e}")

    def load_epub(self, file_path):
        # Parse EPUB file
        book = epub.read_epub(file_path)
        full_html_content = ""

        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                # Extract HTML content and preserve formatting
                soup = BeautifulSoup(item.get_content(), "html.parser")
                full_html_content += str(soup) + "<br>"

        # Display content
        self.display_content(full_html_content)

    def display_content(self, html_content):
        # Render HTML content
        self.html_label.set_html(html_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = EPUBReader(root)
    root.mainloop()
