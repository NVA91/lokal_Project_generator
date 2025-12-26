import tkinter as tk
from tkinter import ttk


class TemplatePreview(ttk.Frame):
    """Widget to display the folder structure of a template."""

    def __init__(self, parent, template_service):
        super().__init__(parent)
        self.template_service = template_service

        self.tree = ttk.Treeview(self)
        self.tree.heading('#0', text='Template Content', anchor='w')
        self.tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # make frame expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def load_template(self, template_name: str):
        """Load and display the given template."""
        self.tree.delete(*self.tree.get_children())
        structure = self.template_service.get_template_structure(template_name)
        for root, children in structure.items():
            self._insert_node('', root, children)

    def _insert_node(self, parent, text, children):
        node = self.tree.insert(parent, 'end', text=text, open=True)
        if children:
            for name, sub in children.items():
                self._insert_node(node, name, sub)
