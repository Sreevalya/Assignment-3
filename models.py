# models.py
from abc import ABC, abstractmethod

class AIModel(ABC):
    """
    Abstract base model.
    Encapsulation: attributes are protected (single underscore).
    Polymorphism + Method overriding: run() is abstract and overridden by children.
    """
    def __init__(self, name: str, category: str, description: str):
        self._name = name
        self._category = category
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    def info(self) -> str:
        return f"• Model Name: {self._name}\n• Category: {self._category}\n• Description: {self._description}"

    @abstractmethod
    def run(self, input_data):
        """Return a placeholder result (no real AI)."""
        raise NotImplementedError


class TextToImageDemo(AIModel):
    def __init__(self):
        super().__init__(
            name="DemoText2Image",
            category="Text-to-Image",
            description="Demo placeholder that would turn text into an image (no real inference)."
        )

    def run(self, input_data):
        # Method overriding: child provides model-specific run behaviour (placeholder)
        return f"[TextToImageDemo placeholder output for: {input_data}]"


class ImageClassificationDemo(AIModel):
    def __init__(self):
        super().__init__(
            name="DemoImageClassifier",
            category="Image Classification",
            description="Demo placeholder that would classify an image (no real inference)."
        )

    def run(self, input_data):
        return f"[ImageClassificationDemo placeholder class: 'cat' for input {input_data}]"
