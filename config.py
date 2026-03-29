# config for the gesture controller
# change these if stuff isn't working on your machine

WEBCAM_INDEX = 0  # try 1 if you have an external cam

# mediapipe confidence thresholds
# 0.7 works well for most lighting conditions, went lower and got too many false positives
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.6

# cooldown between gesture actions (seconds)
# without this it spams the same key like 30 times lol
COOLDOWN_TIME = 1.2

# set to True to see landmark drawings and debug prints
DEBUG_MODE = True

# window size for the preview
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
