import pyautogui
import time

# prevent pyautogui from moving to corner and triggering failsafe
pyautogui.FAILSAFE = False


class Controller:
    def __init__(self, cooldown=1.2):
        self.cooldown = cooldown
        self.last_action_time = 0
        self.last_gesture = None

    def execute(self, gesture, key):
        """Press a key if cooldown has elapsed. Returns True if key was pressed."""
        now = time.time()
        elapsed = now - self.last_action_time

        if elapsed < self.cooldown:
            return False

        # don't repeat the same gesture unless cooldown passed
        # this prevents holding open palm from spamming space
        if gesture == self.last_gesture and elapsed < self.cooldown * 2:
            return False

        try:
            pyautogui.press(key)
            self.last_action_time = now
            self.last_gesture = gesture
            print(f"[action] {gesture} -> pressed '{key}'")
            return True
        except Exception as e:
            # sometimes pyautogui fails if no window is focused
            print(f"[error] couldn't press key: {e}")
            return False

    def reset_cooldown(self):
        """Reset the timer - useful if you want to force an action."""
        self.last_action_time = 0
        self.last_gesture = None
