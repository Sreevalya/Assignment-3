# test_run.py
import os
from models import TextToImageDemo, ImageClassificationDemo

os.makedirs('outputs', exist_ok=True)

def write(fname, text):
    with open(os.path.join('outputs', fname), 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    # instantiate (their code may print loading messages)
    ti = TextToImageDemo()
    ic = ImageClassificationDemo()

    # 1) Text-to-image test
    prompt = "a small cabin beside a lake at sunset"
    print("Running Text-to-Image demo...")
    try:
        res = ti.run(prompt)
    except Exception as e:
        res = f"Exception: {e}"
    print(res)
    write('text2image_result.txt', f"INPUT:\n{prompt}\n\nOUTPUT:\n{res}\n")

    # 2) Image classification test
    # put a sample image filename here or a URL. Update if your sample image has a different name.
    sample_image = 'sample_image.jpg'
    if not os.path.exists(sample_image):
        print(f"[WARN] {sample_image} not found. Place a sample image named {sample_image} in project root to test.")
        write('image_result.txt', f"No sample image found at {sample_image}.")
        return

    print("Running Image Classification demo...")
    try:
        res2 = ic.run(sample_image)
    except Exception as e:
        res2 = f"Exception: {e}"
    print(res2)
    write('image_result.txt', f"INPUT IMAGE: {sample_image}\n\nOUTPUT:\n{res2}\n")

if __name__ == '__main__':
    main()
