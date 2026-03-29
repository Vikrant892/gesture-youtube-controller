"""
YouTube Hand Gesture Controller
Main entry point - runs the webcam loop and ties everything together.

Usage: python src/main.py
Make sure YouTube is the focused window when using gestures!
"""

import cv2
import time
import sys
import os

# add parent dir to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_detector import HandDetector
from gesture_map import recognize_gesture, GESTURE_KEYS, GESTURE_LABELS
from controller import Controller
import config


def main():
    print("Starting gesture controller...")
    print("Press 'q' to quit\n")

    cap = cv2.VideoCapture(config.WEBCAM_INDEX)
    if not cap.isOpened():
        print("ERROR: can't open webcam. Check WEBCAM_INDEX in config.py")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.WINDOW_HEIGHT)

    detector = HandDetector(
        detection_conf=config.MIN_DETECTION_CONFIDENCE,
        tracking_conf=config.MIN_TRACKING_CONFIDENCE
    )
    ctrl = Controller(cooldown=config.COOLDOWN_TIME)

    prev_time = 0
    current_gesture = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame, exiting...")
            break

        # flip horizontally so it feels like a mirror
        frame = cv2.flip(frame, 1)

        # detect hands and get landmarks
        frame = detector.find_hands(frame, draw=config.DEBUG_MODE)
        lm_list = detector.get_landmarks(frame)

        if len(lm_list) > 0:
            fingers = detector.fingers_up()
            thumb_dir = detector.get_thumb_direction()
            gesture = recognize_gesture(fingers, thumb_dir)

            if gesture and gesture in GESTURE_KEYS:
                key = GESTURE_KEYS[gesture]
                executed = ctrl.execute(gesture, key)
                current_gesture = gesture if executed else current_gesture
            else:
                current_gesture = None

            # debug info
            if config.DEBUG_MODE and fingers:
                finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                status = [f"{n}:{'UP' if f else 'DN'}" for n, f in zip(finger_names, fingers)]
                cv2.putText(frame, " | ".join(status), (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        else:
            current_gesture = None

        # fps counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
        prev_time = curr_time

        # draw overlay
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if current_gesture:
            label = GESTURE_LABELS.get(current_gesture, current_gesture)
            cv2.putText(frame, f"Gesture: {label}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Gesture Controller", frame)

        # q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Gesture controller stopped.")


if __name__ == "__main__":
    main()
