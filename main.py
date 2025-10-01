# main.py
from gui import AIApp
from models import TextToImageDemo, ImageClassificationDemo

def main():
    # create demo model instances (these are placeholders; no heavy libs required)
    models = {
        "Text-to-Image (Demo)": TextToImageDemo(),
        "Image Classification (Demo)": ImageClassificationDemo()
    }

    app = AIApp(models)
    app.mainloop()

if __name__ == "__main__":
    main()
