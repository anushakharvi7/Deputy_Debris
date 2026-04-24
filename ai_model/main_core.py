import schedule
import time
import cv2
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_model.detect import run_detection
from ai_model.duplicate_check import is_duplicate, update_last_detection

# DB IMPORT
try:
    from backend.models.db import insert_data
except Exception as e:
    print("DB import error:", e)

    def insert_data(data):
        print("Mock DB Insert:", data)


def send_alert(message):
    print("Mock Alert:", message)


os.makedirs("assets/snapshots", exist_ok=True)


def job():
    print("\n[Scheduler Triggered]")

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        cap.release()
        return

    detected, frame = run_detection(frame)

    if detected:
        print("Garbage detected")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cv2.putText(frame, timestamp, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 255), 2)

        temp_path = "assets/snapshots/temp.jpg"
        cv2.imwrite(temp_path, frame)

        if is_duplicate(temp_path):
            print("Duplicate → skipped")
            os.remove(temp_path)
            cap.release()
            return

        final_path = f"assets/snapshots/garbage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        os.rename(temp_path, final_path)

        # SAVE LAST IMAGE + TIME
        cv2.imwrite("assets/snapshots/last.jpg", frame)
        update_last_detection()

        data = {
            "image_path": final_path,
            "timestamp": timestamp,
            "location": "Area A",
            "status": "Pending"
        }

        print("Saving to DB...")
        insert_data(data)

        print("Sending alert...")
        send_alert(f"Garbage detected at {timestamp}")

    else:
        print("No garbage detected")

    cap.release()


def run_system():
    schedule.every(1).minutes.do(job)
    print("Core system started...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_system()