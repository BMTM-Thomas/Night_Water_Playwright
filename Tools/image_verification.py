#/Users/n02-19/Desktop/demo.png

import base64
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
import pyautogui
import re
import time
import random

# === Load API Key ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# === Convert image to base64 ===
def image_file_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# === Ask GPT-4o to analyze the image and read instruction ===
def ask_gpt_about_image(image_path, prompt_text):
    base64_img = image_file_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt_text },
                    { "type": "image_url", "image_url": { "url": f"data:image/png;base64,{base64_img}" } }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# === Step 2 (Optional): Auto click tiles based on GPT response ===
def extract_positions_and_click(response_text):

    # Random Time Sleep
    random_Sleep = random.uniform(0.5, 1)  # Random sleep between 0.5 to 1 second

    GRID_MAP = {
        "1-1": (703,441),
        "1-2": (787,435),
        "1-3": (938,427),
        "2-1": (685,559),
        "2-2": (789,534),
        "2-3": (947,574),
    }

    positions = re.findall(r"\d-\d", response_text)
    for pos in positions:
        if pos in GRID_MAP:
            x, y = GRID_MAP[pos]
            print(f"Clicking {pos} at ({x}, {y})")
            time.sleep(random_Sleep)
            pyautogui.click(x, y)  # ← instant click at coordinate
            time.sleep(random_Sleep)
        else:
            print(f"[!] Unknown position: {pos}")

# === MAIN ===

if __name__ == "__main__":
    image_path = Path("/Users/n02-19/Desktop/demo4.png").absolute()

    # ✅ Smart instruction-aware prompt
    prompt = (
        "This is a 2x3 image grid that includes an instruction (in Chinese) and six image tiles.\n"
        "First, read and understand the instruction (e.g., it might say to select images of a specific object like “苹果” or “牡丹花”).\n"
        "Then look at the tiles and return which ones match the instruction.\n"
        "Return the result in this format:\n"
        "\"The positions containing [object] are 1-2 and 2-3.\"\n"
        "Only return the sentence. Do not add explanation."
    )

    print("🧠 Asking GPT-4o to read and reason...")
    result = ask_gpt_about_image(image_path, prompt)
    print("\n✅ GPT-4o Answer:\n", result)

    print("\n🖱️ Auto-clicking matching tiles...")
    extract_positions_and_click(result)




