from PIL import Image
import imagehash
import os

LAST_IMAGE_PATH = "assets/snapshots/last.jpg"

def is_duplicate(new_image_path):
    try:
        new_hash = imagehash.average_hash(Image.open(new_image_path))

        # If no previous image → not duplicate
        if not os.path.exists(LAST_IMAGE_PATH):
            return False

        last_hash = imagehash.average_hash(Image.open(LAST_IMAGE_PATH))

        diff = abs(new_hash - last_hash)

        print(f"Hash difference: {diff}")

        if diff < 5:   # more tolerant now
            print("Duplicate detected!")
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False