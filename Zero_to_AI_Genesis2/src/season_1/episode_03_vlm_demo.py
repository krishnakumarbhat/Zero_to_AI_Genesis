from pathlib import Path

from PIL import Image, ImageDraw
from transformers import BlipForQuestionAnswering, BlipProcessor


ROOT = Path(__file__).resolve().parents[2]
IMG_DIR = ROOT / "data" / "vlm_images"


def make_dummy_images():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(5):
        img = Image.new("RGB", (320, 240), (30 * i, 80, 120))
        draw = ImageDraw.Draw(img)
        draw.rectangle((40, 40, 120, 140), outline="white", width=3)
        draw.ellipse((180, 70, 280, 170), outline="yellow", width=3)
        draw.text((10, 200), f"scene-{i}", fill="white")
        img.save(IMG_DIR / f"scene_{i}.png")


def main():
    make_dummy_images()
    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

    questions = [
        "What shape appears on the left side?",
        "What color text appears near bottom?",
        "Is there a circle-like shape in the image?",
    ]

    print("\nSeason 3 / Ep 03 - Vision Language Model (BLIP VQA)")
    for img_path in sorted(IMG_DIR.glob("*.png")):
        image = Image.open(img_path).convert("RGB")
        print(f"\nImage: {img_path.name}")
        for q in questions:
            inputs = processor(images=image, text=q, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=20)
            ans = processor.decode(out[0], skip_special_tokens=True)
            print(f"Q: {q}")
            print(f"A: {ans}")


if __name__ == "__main__":
    main()
