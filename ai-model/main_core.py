import schedule
import time
import cv2
import os
from datetime import datetime
from detect import run_detection
from duplicate_check import is_duplicate

# Create folder if not exists
os.makedirs("assets/snapshots", exist_ok=True)

def job():
    print("\n[Scheduler Triggered]")

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        print("Failed to access camera")
        cap.release()
        return

    # 🔴 Run detection ON FRAME
    detected, frame = run_detection(frame)

    if detected:
        print("Garbage detected")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔴 Add timestamp ON IMAGE
        cv2.putText(frame, timestamp, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 255), 2)

        # 🔴 Save TEMP image first
        temp_path = "assets/snapshots/temp.jpg"
        cv2.imwrite(temp_path, frame)
        # Save as last image for future comparison
        cv2.imwrite("assets/snapshots/last.jpg", frame)

        # 🔴 Duplicate check BEFORE final save
        if is_duplicate(temp_path):
            print("Duplicate → skipped")
            os.remove(temp_path)
            cap.release()
            return

        # 🔴 Save FINAL image
        final_path = f"assets/snapshots/garbage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        os.rename(temp_path, final_path)

        print(f"Image saved: {final_path}")

        # 🔴 Create structured data
        data = {
            "image_path": final_path,
            "timestamp": timestamp,
            "location": "Area A",
            "status": "pending_feedback"
        }

        print("Generated Data:")
        print(data)

    else:
        print("No garbage detected")

    cap.release()


def run_system():
    schedule.every(3).minutes.do(job)

    print("Core system started...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_system()