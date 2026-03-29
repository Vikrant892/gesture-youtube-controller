import mediapipe as mp
import cv2

# mediapipe is insane for this - does all the heavy lifting
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class HandDetector:
    def __init__(self, detection_conf=0.7, tracking_conf=0.6):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # only need one hand for controls
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.lm_list = []

    def find_hands(self, frame, draw=True):
        """Process frame and optionally draw landmarks."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lm in self.results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

        return frame

    def get_landmarks(self, frame):
        """Extract normalized landmark positions as list of (id, x, y)."""
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            for idx, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append((idx, cx, cy))
        return self.lm_list

    def fingers_up(self):
        """
        Returns list of which fingers are up [thumb, index, middle, ring, pinky].
        1 = up, 0 = down.

        Landmark indices (took me a while to memorize these):
        Thumb:  4 (tip), 3 (ip), 2 (mcp)
        Index:  8 (tip), 6 (pip)
        Middle: 12 (tip), 10 (pip)
        Ring:   16 (tip), 14 (pip)
        Pinky:  20 (tip), 18 (pip)
        """
        if len(self.lm_list) == 0:
            return None

        fingers = []

        # thumb - compare x position since it moves sideways
        # this is a simplification, doesn't work great when hand is flipped
        # TODO: detect handedness properly for left hand users
        if self.lm_list[4][1] < self.lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # the other 4 fingers - just check if tip is above pip joint
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        for tip, pip in zip(tip_ids, pip_ids):
            if self.lm_list[tip][2] < self.lm_list[pip][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def get_thumb_direction(self):
        """Check if thumb is pointing up or down based on tip vs wrist y-position."""
        if len(self.lm_list) == 0:
            return None

        thumb_tip_y = self.lm_list[4][2]
        wrist_y = self.lm_list[0][2]

        # 50px threshold to avoid jitter - took a while to get the threshold right
        if thumb_tip_y < wrist_y - 50:
            return "up"
        elif thumb_tip_y > wrist_y + 50:
            return "down"
        return None
