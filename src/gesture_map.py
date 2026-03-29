"""
Maps finger states to YouTube gestures.

Finger order: [thumb, index, middle, ring, pinky]
1 = finger up, 0 = finger down
"""


def recognize_gesture(fingers, thumb_dir=None):
    """
    Takes finger state array and returns gesture name or None.
    thumb_dir is 'up' or 'down' for volume controls.
    """
    if fingers is None:
        return None

    total_up = sum(fingers)

    # open palm - all 5 fingers up = play/pause
    if fingers == [1, 1, 1, 1, 1]:
        return "play_pause"

    # fist - all fingers down = mute
    if fingers == [0, 0, 0, 0, 0]:
        return "mute"

    # thumb only - volume control
    if total_up == 1 and fingers[0] == 1:
        if thumb_dir == "up":
            return "volume_up"
        elif thumb_dir == "down":
            return "volume_down"

    # point right - only index finger extended
    # honestly this one is tricky, sometimes picks up middle finger too
    if fingers == [0, 1, 0, 0, 0]:
        return "skip_forward"

    # point left detection is handled the same way but we check
    # the x position of the index tip relative to wrist in main
    # for now just using the same as skip_forward
    # TODO: add proper left/right pointing detection using wrist-to-tip vector

    # two fingers up (index + middle) = fullscreen
    if fingers == [0, 1, 1, 0, 0]:
        return "fullscreen"

    return None


# mapping gestures to keyboard keys for youtube
GESTURE_KEYS = {
    "play_pause": "space",
    "mute": "m",
    "volume_up": "up",      # youtube uses arrow keys for volume
    "volume_down": "down",
    "skip_forward": "right",
    "skip_back": "left",
    "fullscreen": "f",
}

# just for the debug overlay
GESTURE_LABELS = {
    "play_pause": "Play/Pause",
    "mute": "Mute",
    "volume_up": "Volume Up",
    "volume_down": "Volume Down",
    "skip_forward": "Skip >>",
    "skip_back": "<< Skip",
    "fullscreen": "Fullscreen",
}
