# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models import TextToImageDemo, ImageClassificationDemo
from explanations import OOPExplanations
from decorators import log_action, require_model_loaded, validate_input

PAD = 6

class ModelManager:
    """Mixin to manage available models and loaded model state."""
    def __init__(self, models: dict):
        self._models = models        # mapping display name -> model instance
        self._loaded_model = None

    def load_model(self, display_name: str):
        model = self._models.get(display_name)
        self._loaded_model = model
        return model

    def get_loaded_model_info(self) -> str:
        if not self._loaded_model:
            return "No model loaded."
        return self._loaded_model.info()


class BaseWindow(tk.Tk):
    """Base window provides menu and base configuration. Allows method overriding."""
    def __init__(self, title="Tkinter AI GUI", size="900x700"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.minsize(700, 500)  # prevent collapse
        self._setup_menu()

    def _setup_menu(self):
        menubar = tk.Menu(self)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filem)

        modelm = tk.Menu(menubar, tearoff=0)
        modelm.add_command(label="Refresh models", command=lambda: None)
        menubar.add_cascade(label="Models", menu=modelm)

        helpm = tk.Menu(menubar, tearoff=0)
        helpm.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=helpm)

        self.config(menu=menubar)

    def _about(self):
        messagebox.showinfo("About", "Tkinter AI GUI demo — no real AI executed.")


class AIApp(BaseWindow, ModelManager):
    """Main GUI. Multiple inheritance: BaseWindow (tk) + ModelManager (mixin)."""
    def __init__(self, models: dict):
        BaseWindow.__init__(self)
        ModelManager.__init__(self, models)

        self.input_mode = tk.StringVar(value="Text")
        self.input_text_var = tk.StringVar()
        self.oop = OOPExplanations()

        self.create_widgets()

    def create_widgets(self):
        # Root grid
        self.rowconfigure(2, weight=1)  # main frame
        self.rowconfigure(3, weight=1)  # lower frame
        self.columnconfigure(0, weight=1)

        # Title
        header = tk.Label(self, text="Tkinter AI GUI", font=("Helvetica", 16, "bold"))
        header.grid(row=0, column=0, pady=(8, 4))

        # === Model Selection Row ===
        top_frame = tk.Frame(self)
        top_frame.grid(row=1, column=0, sticky="ew", padx=PAD, pady=(0, PAD))
        top_frame.columnconfigure(1, weight=1)

        tk.Label(top_frame, text="Model Selection:").grid(row=0, column=0, sticky="w")
        self.model_combo = ttk.Combobox(
            top_frame, values=list(self._models.keys()), state="readonly"
        )
        self.model_combo.grid(row=0, column=1, sticky="ew", padx=(4, 8))
        self.model_combo.set(list(self._models.keys())[0])

        self.btn_load = tk.Button(top_frame, text="Load Model", command=self.on_load_model)
        self.btn_load.grid(row=0, column=2, sticky="e")

        # === Main Frame (Input + Output) ===
        main_frame = tk.Frame(self)
        main_frame.grid(row=2, column=0, sticky="nsew", padx=PAD, pady=PAD)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left: User Input
        left = tk.LabelFrame(main_frame, text="User Input Section")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.rowconfigure(3, weight=1)
        left.columnconfigure(0, weight=1)

        rb_frame = tk.Frame(left)
        rb_frame.grid(row=0, column=0, sticky="w", pady=(4,2))
        tk.Radiobutton(rb_frame, text="Text", variable=self.input_mode, value="Text").pack(side="left")
        tk.Radiobutton(rb_frame, text="Image", variable=self.input_mode, value="Image").pack(side="left", padx=8)
        tk.Radiobutton(rb_frame, text="Audio", variable=self.input_mode, value="Audio").pack(side="left")

        browse_frame = tk.Frame(left)
        browse_frame.grid(row=1, column=0, sticky="ew", pady=(4,2))
        tk.Button(browse_frame, text="Browse", command=self.browse_file).pack(side="right")

        self.input_text = tk.Text(left, wrap="word")
        self.input_text.grid(row=3, column=0, sticky="nsew", pady=(4,2))

        btns = tk.Frame(left)
        btns.grid(row=4, column=0, sticky="ew", pady=(4,2))
        tk.Button(btns, text="Run Model 1", command=lambda: self.run_model(1)).pack(side="left")
        tk.Button(btns, text="Run Model 2", command=lambda: self.run_model(2)).pack(side="left", padx=6)
        tk.Button(btns, text="Clear", command=self.clear_input_output).pack(side="left")

        # Right: Model Output
        right = tk.LabelFrame(main_frame, text="Model Output Section")
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        tk.Label(right, text="Output Display:").grid(row=0, column=0, sticky="w")
        self.output_display = tk.Text(right, wrap="word")
        self.output_display.grid(row=1, column=0, sticky="nsew")

        # === Lower Frame (Info + OOP Explanations) ===
        lower = tk.Frame(self)
        lower.grid(row=3, column=0, sticky="nsew", padx=PAD, pady=PAD)
        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=1)
        lower.rowconfigure(0, weight=1)

        info_frame = tk.LabelFrame(lower, text="Selected Model Info")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.model_info_text = tk.Text(info_frame, wrap="word")
        self.model_info_text.pack(fill="both", expand=True)
        self.model_info_text.insert("end", "No model loaded.")

        oop_frame = tk.LabelFrame(lower, text="OOP Concepts Explanation")
        oop_frame.grid(row=0, column=1, sticky="nsew")
        self.oop_text = tk.Text(oop_frame, wrap="word")
        self.oop_text.pack(fill="both", expand=True)
        self.oop_text.insert("end", self.oop.get_all())

        # Notes
        notes = tk.Label(self, text="Notes: Extra notes, instructions, or references.")
        notes.grid(row=4, column=0, sticky="ew", padx=PAD, pady=(6,10))

    def browse_file(self):
        mode = self.input_mode.get()
        if mode == "Text":
            return
        f = filedialog.askopenfilename(title="Select a file")
        if f:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("end", f)

    @log_action
    @require_model_loaded
    @validate_input
    def run_model(self, which: int = 1):
        input_val = self.get_input_value()
        if which == 1:
            model = self._loaded_model
        else:
            other = [m for m in self._models.values() if m is not self._loaded_model]
            model = other[0] if other else self._loaded_model

        result = model.run(input_val)
        self.output_display.insert("end", f"=== Run Model {which} ({model.name}) ===\n{result}\n\n")

    def get_input_value(self):
        return self.input_text.get("1.0", "end").strip()

    def on_load_model(self):
        display_name = self.model_combo.get()
        if not display_name:
            self.output_display.insert("end", "⚠️ Select a model from the drop-down before loading.\n")
            return
        model = self.load_model(display_name)
        self.model_info_text.delete("1.0", "end")
        self.model_info_text.insert("end", model.info())
        self.output_display.insert("end", f"Model '{model.name}' loaded (simulated).\n")

    def clear_input_output(self):
        self.input_text.delete("1.0", "end")
        self.output_display.delete("1.0", "end")
