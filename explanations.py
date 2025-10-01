# explanations.py
class OOPExplanations:
    def __init__(self):
        self.explanations = {
            "Multiple Inheritance":
                "The main GUI class inherits both from BaseWindow (which wraps tk.Tk) "
                "and ModelManager (a mixin). This allows UI methods and model-management "
                "capabilities to be combined cleanly.",
            "Encapsulation":
                "Model attributes (name, category, description) are stored as protected "
                "variables (e.g. _name). Access is via properties.",
            "Polymorphism":
                "The base AIModel defines run(), and each demo model implements run() "
                "differently. The GUI calls run() without needing to know which model "
                "type it is - that's polymorphism.",
            "Method Overriding":
                "Child classes TextToImageDemo and ImageClassificationDemo override "
                "AIModel.run() to provide specific (placeholder) behavior.",
            "Multiple Decorators":
                "Several GUI action methods have stacked decorators (logging, model-loaded "
                "check, input validation) to separate concerns and reuse logic."
        }

    def get_all(self) -> str:
        lines = []
        for k, v in self.explanations.items():
            lines.append(f"• {k}:\n    {v}\n")
        return "\n".join(lines)
