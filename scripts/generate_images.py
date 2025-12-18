from google import genai
from google.genai import types
import time, os, sys, json, base64
from dotenv import load_dotenv
from PIL import Image

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BATCH_SIZE = 1
ON_LINE = False # downloading the batch is async from uploading. Make sure ON_LINE matches the value as when the batch was uploaded, so the label matches
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_results")
ON_PROMPT = """
Using the provided image, change the persons clothes, shoes, background and foot placement with respect to the line, 
ensuring the foot is ON THE LINE. Keep the original camera angle, POV, line color, and line position in 
the image exactly the same.
"""

ON_IMAGE = Image.open('./source_image/SOURCEONTHELINE.png')

OFF_IMAGE = Image.open('./source_image/SOURCEOFFTHELINE.png')

OFF_PROMPT = """
Using the provided image, change the persons clothes, shoes, background and foot placement with respect to the line, 
ensuring the foot is OFF THE LINE. Keep the original camera angle, POV, line color, and line position in 
the image exactly the same.
"""

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prefix = "X" if ON_LINE else "O"
    
    for i in range(BATCH_SIZE):
        print(f"Generating image {i+1}/{BATCH_SIZE}...")
        
        varied_prompt = f"{ON_PROMPT if ON_LINE else OFF_PROMPT}\nVariation seed: {time.time()}"
        
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

def batch_generate_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prefix = "X" if ON_LINE else "O"
    
    inline_requests = []
    for i in range(BATCH_SIZE):
        inline_requests.append({
            'contents': [{'parts': [{'text': f"{ON_PROMPT if ON_LINE else OFF_PROMPT}\nVariation seed: {i}_{time.time()}"}]}, ON_IMAGE if ON_LINE else OFF_IMAGE ]
        })
    
    batch_job = client.batches.create(
        model="gemini-2.5-flash-image",
        src=inline_requests,
        config={'display_name': f"line_detection_{prefix}_{int(time.time())}"}
    )
    
    print(f"Batch job created: {batch_job.name}")
    print(f"Status: {batch_job.state}")
    return batch_job.name

def check_batch_status(job_name):
    job = client.batches.get(name=job_name)
    print(f"Status: {job.state}")
    return job

def download_batch_results(job_name):
    job = client.batches.get(name=job_name)
    
    if job.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Job not complete. Status: {job.state}")
        return
    
    prefix = "X" if ON_LINE else "O"
    
    if job.dest and job.dest.inlined_responses:
        for i, inline_response in enumerate(job.dest.inlined_responses):
            if inline_response.response:
                for part in inline_response.response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        img_data = part.inline_data.data
                        if isinstance(img_data, str):
                            img_data = base64.b64decode(img_data)
                        filename = f"{prefix}_{i+1:03d}.png"
                        filepath = os.path.join(OUTPUT_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(img_data)
                        print(f"Saved: {filename}")
    else:
        print("No results found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_images.py single")
        print("  python generate_images.py batch")
        print("  python generate_images.py status <job_name>")
        print("  python generate_images.py download <job_name>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "single":
        print(f"Mode: {'ON LINE (X)' if ON_LINE else 'OFF LINE (O)'}")
        print(f"Generating {BATCH_SIZE} images...\n")
        generate_images()
        print("\nDone!")
    elif command == "batch":
        batch_generate_images()
    elif command == "status" and len(sys.argv) > 2:
        check_batch_status(sys.argv[2])
    elif command == "download" and len(sys.argv) > 2:
        download_batch_results(sys.argv[2])
    else:
        print("Invalid command")