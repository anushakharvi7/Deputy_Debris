from PIL import Image
import imagehash
import os
import time

LAST_IMAGE_PATH = "assets/snapshots/last.jpg"
LAST_DETECTION_TIME = "assets/snapshots/last_time.txt"

def is_duplicate(new_image_path):
    try:
        current_time = time.time()

        # 🔴 TIME CHECK (NEW)
        if os.path.exists(LAST_DETECTION_TIME):
            with open(LAST_DETECTION_TIME, "r") as f:
                last_time = float(f.read())

            time_diff = current_time - last_time

            print(f"Time difference: {time_diff:.2f}s")

            # If detected within 20 sec → skip
            if time_diff < 20:
                print("Duplicate (time-based)")
                return True

        # 🔴 IMAGE HASH CHECK
        new_hash = imagehash.average_hash(Image.open(new_image_path))

        if not os.path.exists(LAST_IMAGE_PATH):
            print("No previous image → not duplicate")
            return False

        last_hash = imagehash.average_hash(Image.open(LAST_IMAGE_PATH))

        diff = abs(new_hash - last_hash)

        print(f"Hash difference: {diff}")

        if diff <= 5:
            print("Duplicate (image-based)")
            return True

        print("New garbage detected")
        return False

    except Exception as e:
        print("Error in duplicate check:", e)
        return False


def update_last_detection():
    # 🔴 SAVE TIME
    with open(LAST_DETECTION_TIME, "w") as f:
        f.write(str(time.time()))