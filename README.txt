# Smart Dairy Transparency Kiosk - Python GUI

This is a professional Linux desktop version of the dairy kiosk using Python Tkinter.

## Features
- Clean GUI for milk transaction entry
- Automatic payment calculation
- SMS and payment log viewer
- Farmer face capture using webcam
- Saved photo preview and local image storage

## Run
```bash
python3 output/dairy_kiosk_app.py
```

## Install dependencies
```bash
pip install -r output/requirements.txt
```

## Ubuntu/Debian system packages if Tkinter is missing
```bash
sudo apt install python3-tk
```

## Face capture notes
- Start camera
- Capture face of farmer
- Image is saved in `output/farmer_photos/`
- Transaction summary shows saved photo path
