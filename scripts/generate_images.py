from google import genai
from google.genai import types
import time, os

BATCH_SIZE = 2
ON_LINE = True  # True = stepping ON line (X prefix), False = NOT on line (O prefix)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_results")
PROMPT = """
Generate a realistic photo of a person's foot/shoe in a parking lot, 
taken from a low angle similar to a ground-level camera. 
The image should show a white parking line on asphalt.
The person is wearing casual shoes (sneakers, converse, etc).
{"The foot should be STEPPING DIRECTLY ON the white line.}
Make it look like a real photograph, not AI generated.
Vary the shoe style, lighting conditions, and camera angle slightly.
"""

# add key here
client = genai.Client(api_key="")

def generate_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prefix = "X" if ON_LINE else "O"
    
    for i in range(BATCH_SIZE):
        print(f"Generating image {i+1}/{BATCH_SIZE}...")
        
        varied_prompt = f"{PROMPT}\nVariation seed: {time.time()}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[varied_prompt],
        )
        
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                filename = f"{prefix}_{i+1:03d}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)
                image.save(filepath)
                print(f"  Saved: {filename}")
            elif part.text is not None:
                print(f"  Model text: {part.text}")
        
        time.sleep(1)

if __name__ == "__main__":
    print(f"Mode: {'ON LINE (X)' if ON_LINE else 'OFF LINE (O)'}")
    print(f"Generating {BATCH_SIZE} images...\n")
    generate_images()
    print("\nDone!")