# Smart Dairy Transparency Kiosk

A Python desktop application for dairy collection centers to record milk transactions, calculate payments, capture farmer photos, and maintain simple logs.

## Features

- Farmer transaction form with ID, name, phone number, milk quantity, FAT, and SNF inputs
- Automatic payment calculation
- Payment mode selection with UPI or Bank
- Webcam-based farmer face capture
- Saved photo preview
- SMS log viewer and payment log viewer
- Transaction summary panel

## Tech Stack

- Python 3
- Tkinter
- OpenCV
- Pillow

## Project Files

```text
dairy-kiosk-app/
├── dairy_kiosk_vm_safe.py
├── run_vm_safe.sh
├── requirements.txt
├── README.md
├── README.txt
└── .gitignore
```

## Step-by-Step Installation

### 1. Clone the repository

```bash
git clone https://github.com/iamaryanbhalsing/dairy-kiosk-app.git
cd dairy-kiosk-app
```

### 2. Check Python version

```bash
python3 --version
```

### 3. Create a virtual environment

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Tkinter if needed

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-tk
```

### 6. Run the application

Main Python file:
```bash
python3 dairy_kiosk_vm_safe.py
```

Or use the shell script:
```bash
bash run_vm_safe.sh
```

## How to Use

1. Enter farmer details.
2. Enter milk quantity, FAT, and SNF values.
3. Select payment mode.
4. Start the camera and capture the farmer photo if needed.
5. Click **Process Transaction**.
6. Review the summary and logs.

## Payment Formula

```text
Rate = 18 + (FAT × 6.5) + (SNF × 1.8)
Amount = Quantity × Rate
```

## Output Files

The application creates runtime files inside the user's home directory:

- `~/output/farmer_photos/`
- `~/output/sms_log.txt`
- `~/output/payment_log.txt`

## Notes

- Webcam capture requires a working camera
- OpenCV and Pillow must be installed
- If no photo is captured, the transaction can still be processed
- Tkinter may require system installation on some Linux distributions

## Future Improvements

- Export logs to CSV or Excel
- Add a database for farmer records
- Add SMS gateway integration
- Add authentication for operators
- Add analytics dashboard

## License

This project is shared for educational and demonstration purposes.
