# decorators.py
from functools import wraps
from datetime import datetime

def log_action(func):
    """Logs call to the console with timestamp."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        now = datetime.now().isoformat(timespec='seconds')
        print(f"{now} - ACTION: calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def require_model_loaded(func):
    """Ensure a model has been loaded via ModelManager.load_model()."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not getattr(self, "_loaded_model", None):
            # assume GUI has output_display Text widget
            self.output_display.insert("end", "⚠️ Please load a model first.\n")
            return
        return func(*args, **kwargs)
    return wrapper

def validate_input(func):
    """
    Ensure some user input exists. GUI must implement get_input_value().
    This decorator demonstrates separation of concerns (validation) from action logic.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not hasattr(self, "get_input_value"):
            return func(*args, **kwargs)
        val = self.get_input_value()
        if not val:
            self.output_display.insert("end", "⚠️ Please provide input (text/image/audio) before running.\n")
            return
        return func(*args, **kwargs)
    return wrapper
