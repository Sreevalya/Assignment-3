# models.py
from abc import ABC, abstractmethod
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests
import os


class AIModel(ABC):
    def __init__(self, name, category, description):
        self._name, self._category, self._description = name, category, description

    @property
    def name(self): return self._name
    @property
    def category(self): return self._category
    @property
    def description(self): return self._description

    def info(self):
        return f"• Model Name: {self._name}\n• Category: {self._category}\n• Description: {self._description}"

    @abstractmethod
    def run(self, input_data): raise NotImplementedError


class TextToImageDemo(AIModel):
    def __init__(self):
        super().__init__("Text2ImageMiniHF", "Text-to-Image", "DALL·E Mini via Hugging Face Transformers")
        self.device = 0 if torch.cuda.is_available() else -1  # GPU=0, CPU=-1
        self.model = None
        self.tokenizer = None
        self.pipe = None

        try:
            print("Loading Hugging Face DALL·E Mini...")
            # ⚠️ This will fail, since dalle-mini isn't supported in transformers
            self.tokenizer = AutoTokenizer.from_pretrained("dalle-mini/dalle-mini")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("dalle-mini/dalle-mini")
            self.pipe = pipeline(
                "text-to-image",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device
            )
            print("✅ DALL·E Mini loaded successfully.")
        except Exception as e:
            print("❌ Failed to load DALL·E Mini:", e)
            self.pipe = None

    def run(self, prompt: str, **kwargs):
        if self.pipe is None:
            return "⚠️ Model not loaded."

        try:
            result = self.pipe(prompt, num_inference_steps=20)
            img = result[0]["image"]
            file_path = "generated_image.png"
            img.save(file_path)
            return f"✅ Image generated and saved at: {file_path}"
        except Exception as e:
            return f"❌ Error during image generation: {e}"


class ImageClassificationDemo(AIModel):
    def __init__(self):
        super().__init__("ViTImageClassifier", "Image Classification",
                         "Vision Transformer (ViT) fine-tuned on ImageNet-1k")
        try:
            print("Loading Hugging Face ViT image classifier...")
            self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
            self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            print("✅ ViT loaded successfully.")
        except Exception as e:
            print("❌ Failed to load ViT model:", e)
            self.model, self.processor = None, None

    def run(self, input_data):
        """
        input_data can be either:
        - a local image file path
        - an image URL
        """
        if self.model is None or self.processor is None:
            return "⚠️ Image classifier model not loaded."

        try:
            # Handle input: URL or file
            if input_data.startswith("http://") or input_data.startswith("https://"):
                image = Image.open(requests.get(input_data, stream=True).raw).convert("RGB")
            elif os.path.exists(input_data):
                image = Image.open(input_data).convert("RGB")
            else:
                return "⚠️ Please provide a valid image path or URL."

            inputs = self.processor(images=image, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class_idx = logits.argmax(-1).item()
                label = self.model.config.id2label[predicted_class_idx]

            return f"✅ Predicted class: {label}"

        except Exception as e:
            return f"❌ Error during classification: {e}"
