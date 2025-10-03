# Tkinter AI GUI

A **Python GUI application** built with **Tkinter** to demonstrate AI model interactions and object-oriented programming concepts. This project provides a **modular GUI framework** for running AI demo models and displaying OOP explanations.

---

## Features

* **Multiple AI Models**

  * Text-to-Image Demo (MinDalle)
  * Image Classification Demo (ViT Image Classifier)
* **User-Friendly GUI**

  * Text, Image, and Audio input support
  * File browsing
  * Output display for model results
  * Selected model info display
  * OOP concepts explanation panel
* **OOP Concepts Demonstration**

  * Inheritance, multiple inheritance, encapsulation, polymorphism, method overriding
  * Mixins for model management
* **Decorators for Cleaner Code**

  * `@log_action` – logs GUI actions with timestamps
  * `@require_model_loaded` – ensures a model is loaded before execution
  * `@validate_input` – validates user input before running a model

---



## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/tkinter-ai-gui.git
cd tkinter-ai-gui
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies included:**

```
torch
transformers
Pillow
min-dalle
requests
```

> Note: `tkinter` is usually included with Python by default.

---

## Usage

Run the GUI:

```bash
python main.py
```

1. Select a model from the dropdown.
2. Click **Load Model**.
3. Enter text, image path, or audio path as input.
4. Click **Run Model 1** or **Run Model 2** to execute.
5. Output and model info appear in the GUI.

**Notes:**

* Text-to-Image uses MinDalle; the output image is saved locally as `generated_image.png`.
* Image Classification supports local files or image URLs.

---

## Project Structure

```
tkinter-ai-gui/
│
├── gui.py                  # Main GUI application
├── decorators.py           # Decorators for logging, validation, and model checks
├── explanations.py         # OOP explanations for GUI display
├── models.py               # AI demo models (Text2ImageDemo, ImageClassificationDemo)
├── main.py                 # Entry point to run the GUI
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## OOP Concepts Demonstrated

| Feature           | Example in Code                                            |
| ----------------- | ---------------------------------------------------------- |
| Class             | `ModelManager`, `BaseWindow`, `AIApp`                      |
| Inheritance       | `BaseWindow(tk.Tk)`, `AIApp(BaseWindow, ModelManager)`     |
| Encapsulation     | `_models`, `_loaded_model` (private attributes)            |
| Polymorphism      | `model.run(input_val)` for different model types           |
| Abstraction       | `load_model()`, `get_loaded_model_info()`, `_setup_menu()` |
| Mixins            | `ModelManager` mixed into `AIApp`                          |
| Method Overriding | `AIApp.__init__()` overriding `BaseWindow.__init__()`      |
| Decorators (meta) | `@log_action`, `@require_model_loaded`, `@validate_input`  |
| Composition       | `self.oop = OOPExplanations()`, Tkinter widgets inside GUI |

---

## Contributing

Contributions are welcome! Suggestions include:

* Add new AI models
* Enhance GUI layout
* Improve decorators or validation logic
* Fix bugs or improve documentation

---


