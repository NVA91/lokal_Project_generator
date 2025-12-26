import shutil
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .template_service import TemplateService
from .template_preview import TemplatePreview

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore
    _DND_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    TkinterDnD = tk.Tk  # type: ignore
    DND_FILES = 'DND_Files'
    _DND_AVAILABLE = False


class ProjectGeneratorGUI(TkinterDnD):  # type: ignore
    """Main GUI window for project generation."""

    def __init__(self, templates_dir: str):
        super().__init__()
        self.title('Project Generator')
        self.style = ttk.Style(self)
        # use a modern theme if available
        self.style.theme_use('clam')

        self.template_service = TemplateService(Path(templates_dir))

        # top row: template selector and import button
        selector_frame = ttk.Frame(self)
        selector_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))

        self.template_var = tk.StringVar()
        self.template_box = ttk.Combobox(selector_frame, textvariable=self.template_var, state='readonly')
        self.template_box.pack(side='left', fill='x', expand=True)
        self.template_box.bind('<<ComboboxSelected>>', self._on_select)

        import_btn = ttk.Button(selector_frame, text='Import', command=self._import_template)
        import_btn.pack(side='left', padx=5)

        self.preview = TemplatePreview(self, self.template_service)
        self.preview.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        self.progress = ttk.Progressbar(self, mode='determinate', maximum=100)
        self.progress.grid(row=2, column=0, sticky='ew', padx=5, pady=(0, 5))

        generate_btn = ttk.Button(self, text='Generate', command=self.start_generation)
        generate_btn.grid(row=3, column=0, sticky='ew', padx=5, pady=(0, 5))

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._refresh_templates()

        if self.template_service.list_templates():
            first = self.template_service.list_templates()[0]
            self.template_var.set(first)
            self.preview.load_template(first)

        if _DND_AVAILABLE:
            self.preview.drop_target_register(DND_FILES)  # type: ignore
            self.preview.dnd_bind('<<Drop>>', self._on_drop)  # type: ignore

    def _refresh_templates(self):
        names = self.template_service.list_templates()
        self.template_box['values'] = names

    def _on_select(self, _event):
        if self.template_var.get():
            self.preview.load_template(self.template_var.get())

    def _import_template(self):
        path = filedialog.askdirectory(title='Import Template')
        if path:
            try:
                dest = self.template_service.import_template(path)
            except Exception as exc:  # pragma: no cover - requires GUI
                print(f'Error importing template: {exc}')
            else:
                self._refresh_templates()
                self.template_var.set(dest.name)
                self.preview.load_template(dest.name)

    def start_generation(self):
        """Start project generation in a worker thread."""
        template_name = self.template_var.get()
        if template_name:
            self.after(0, self._update_progress, 0)
            threading.Thread(
                target=self._generate_project,
                args=(template_name,),
                daemon=True,
            ).start()

    def _generate_project(self, template_name):  # pragma: no cover - requires GUI
        """Copy the selected template into a new project folder."""
        src_root = self.template_service.templates_dir / template_name
        files = list(src_root.rglob('*'))
        total = len(files)
        dest_root = Path('generated_projects') / template_name
        if dest_root.exists():
            shutil.rmtree(dest_root)
        for idx, path in enumerate(files, 1):
            time.sleep(0.1)
            rel = path.relative_to(src_root)
            dest = dest_root / rel
            if path.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            self.after(0, self._update_progress, idx / total * 100)
        self.after(0, self._update_progress, 100)
        self.after(0, messagebox.showinfo, 'Done', f'Project generated at {dest_root}')

    def _update_progress(self, value):
        self.progress['value'] = value

    def _on_drop(self, event):  # pragma: no cover - requires GUI
        paths = self.splitlist(event.data)
        for path in paths:
            try:
                dest = self.template_service.import_template(path)
            except Exception as exc:  # pylint: disable=broad-except
                print(f'Error importing template: {exc}')
            else:
                self._refresh_templates()
                self.template_var.set(dest.name)
                self.preview.load_template(dest.name)


def main():  # pragma: no cover - manual usage
    app = ProjectGeneratorGUI('templates')
    app.mainloop()


if __name__ == '__main__':  # pragma: no cover
    main()


class ProjectGeneratorApp(TkinterDnD):  # type: ignore
    """Extended GUI with dependency management."""

    def __init__(self, templates_dir: str):
        super().__init__()
        self.title('Project Generator')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        from .dependency_management import (
            DependencyManager,
            VirtualEnvironmentManager,
        )

        self.venv_manager = VirtualEnvironmentManager()
        self.dep_manager = DependencyManager()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self._setup_project_tab(templates_dir)
        self._setup_dependency_tab()

    # --- project tab -------------------------------------------------
    def _setup_project_tab(self, templates_dir: str):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Project')

        self.template_service = TemplateService(Path(templates_dir))

        selector_frame = ttk.Frame(tab)
        selector_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))

        self.template_var = tk.StringVar()
        self.template_box = ttk.Combobox(
            selector_frame, textvariable=self.template_var, state='readonly'
        )
        self.template_box.pack(side='left', fill='x', expand=True)
        self.template_box.bind('<<ComboboxSelected>>', self._on_select)

        import_btn = ttk.Button(selector_frame, text='Import', command=self._import_template)
        import_btn.pack(side='left', padx=5)

        self.preview = TemplatePreview(tab, self.template_service)
        self.preview.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        self.progress = ttk.Progressbar(tab, mode='determinate', maximum=100)
        self.progress.grid(row=2, column=0, sticky='ew', padx=5, pady=(0, 5))

        generate_btn = ttk.Button(tab, text='Generate', command=self.start_generation)
        generate_btn.grid(row=3, column=0, sticky='ew', padx=5, pady=(0, 5))

        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        self._refresh_templates()
        if self.template_service.list_templates():
            first = self.template_service.list_templates()[0]
            self.template_var.set(first)
            self.preview.load_template(first)

        if _DND_AVAILABLE:
            self.preview.drop_target_register(DND_FILES)  # type: ignore
            self.preview.dnd_bind('<<Drop>>', self._on_drop)  # type: ignore

    # --- dependency tab ----------------------------------------------
    def _setup_dependency_tab(self):
        dep_frame = ttk.Frame(self.notebook)
        self.notebook.add(dep_frame, text='Dependencies')

        ttk.Label(dep_frame, text='Python Version').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.python_var = tk.StringVar(value=self.venv_manager.default_python_version())
        self.python_box = ttk.Combobox(
            dep_frame,
            textvariable=self.python_var,
            state='readonly',
            values=self.venv_manager.available_versions(),
        )
        self.python_box.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        ttk.Label(dep_frame, text='Dependency Sets').grid(row=1, column=0, sticky='nw', padx=5)
        self.dep_vars = {}
        for i, name in enumerate(self.dep_manager.available_sets(), start=1):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(dep_frame, text=name, variable=var)
            cb.grid(row=i, column=1, sticky='w', padx=5)
            self.dep_vars[name] = var

        self.setup_progress = ttk.Progressbar(dep_frame, mode='determinate', maximum=100)
        self.setup_progress.grid(row=5, column=0, columnspan=2, sticky='ew', padx=5, pady=(5, 0))

        setup_btn = ttk.Button(dep_frame, text='Create venv', command=self.start_setup_env)
        setup_btn.grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        dep_frame.columnconfigure(1, weight=1)

    def start_setup_env(self):  # pragma: no cover - requires GUI
        """Start environment setup in background thread."""
        deps = [n for n, v in self.dep_vars.items() if v.get()]
        py_version = self.python_var.get()
        self.setup_progress['value'] = 0
        threading.Thread(
            target=self._setup_env_worker,
            args=(py_version, deps),
            daemon=True,
        ).start()

    def _setup_env_worker(self, python_version: str, deps):  # pragma: no cover - requires GUI
        for pct in self.venv_manager.create_environment(Path('env'), python_version, deps):
            self.after(0, self.setup_progress.configure, value=pct)
        self.after(0, messagebox.showinfo, 'Done', 'Virtual environment created')
