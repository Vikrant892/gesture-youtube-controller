# YouTube Hand Gesture Controller

I built this because I was tired of reaching for my keyboard every time I wanted to pause or skip during YouTube binges. It uses your webcam to detect hand gestures and translates them into YouTube keyboard shortcuts.

Built with MediaPipe for hand tracking, OpenCV for the video feed, and PyAutoGUI to simulate keypresses.

## How It Works

The webcam captures your hand, MediaPipe detects 21 hand landmarks, and a simple rule-based system figures out which fingers are up or down. Each gesture maps to a YouTube shortcut key.

## Supported Gestures

| Gesture | What It Does |
|---------|-------------|
| Open Palm (all fingers up) | Play / Pause |
| Fist (all fingers closed) | Mute / Unmute |
| Thumbs Up | Volume Up |
| Thumbs Down | Volume Down |
| Point (index finger only) | Skip Forward 5s |
| Peace Sign (index + middle) | Toggle Fullscreen |

See `assets/gestures.md` for more details and tips.

## Setup

**Requirements:** Python 3.8+ and a webcam.

```bash
# clone the repo
git clone https://github.com/Vikrant892/gesture-youtube-controller.git
cd gesture-youtube-controller

# install dependencies
pip install -r requirements.txt

# run it
python src/main.py
```

Then open YouTube in your browser, start a video, and make sure the browser window is focused when you use gestures (PyAutoGUI sends keystrokes to whatever window is active).

Press `q` in the preview window to quit.

## Configuration

Edit `config.py` to tweak settings:

- `WEBCAM_INDEX` - change to 1 if you have an external webcam
- `MIN_DETECTION_CONFIDENCE` - lower this if hands aren't being detected (default 0.7)
- `COOLDOWN_TIME` - seconds between repeated actions (default 1.2)
- `DEBUG_MODE` - shows hand landmarks and finger state overlay

## Performance

Gets around 55-65 FPS on my laptop (i7-11th gen, no GPU needed). MediaPipe runs on CPU and is surprisingly fast. The bottleneck is usually the webcam capture, not the processing.

## Known Issues

- **Thumb detection is iffy** - the up/down check uses a simple y-position comparison which doesn't work well at certain angles. Need to switch to a proper vector-based approach.
- **Left hand support** - the thumb left/right logic assumes right hand. Left-handed users might get weird results for thumb-only gestures.
- **No skip backward gesture** - pointing left vs right looks the same to the detector right now. Still figuring out a reliable way to distinguish direction.
- **Lighting matters** - MediaPipe struggles in low light or with strong backlighting. Try to have a light source in front of you.
- **Window focus** - PyAutoGUI sends keys to the active window, so you need YouTube to be in focus. Alt-tabbing will send keys to the wrong app.

## Project Structure

```
gesture-youtube-controller/
├── src/
│   ├── main.py           # webcam loop + FPS counter
│   ├── hand_detector.py  # MediaPipe wrapper
│   ├── gesture_map.py    # gesture recognition rules
│   └── controller.py     # keyboard simulation
├── assets/
│   └── gestures.md       # gesture reference
├── config.py             # settings
├── requirements.txt
└── README.md
```

## Future Ideas

- Add swipe gestures for seeking (forward/back 10s)
- Use a small ML model instead of hardcoded rules for better accuracy
- GUI for configuring gesture mappings
- Support for other video players (VLC, Netflix)
- Hand tracking smoothing to reduce jitter

## License

Do whatever you want with this. No license, no warranty, no guarantees it won't accidentally fullscreen your embarrassing video at the worst possible moment.
