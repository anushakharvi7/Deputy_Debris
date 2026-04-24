import cv2

def run_detection(frame):
    height, width, _ = frame.shape

    # 🔴 FORCE DETECTION FOR TESTING
    detected = True

    if detected:
        x1, y1 = int(width*0.3), int(height*0.3)
        x2, y2 = int(width*0.7), int(height*0.7)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "Garbage", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    return detected, frame