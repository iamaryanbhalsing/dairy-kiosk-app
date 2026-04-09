# Smart Dairy Transparency Kiosk

A Python Tkinter desktop application for dairy collection centers to record milk transactions, calculate payments, capture farmer photos, and maintain simple transaction logs. The app uses OpenCV for webcam capture and Pillow for image preview support. [file:4][file:2]

## Features

- Farmer transaction form with ID, name, phone number, milk quantity, FAT, and SNF inputs. [file:4]
- Automatic payment calculation based on milk quantity, FAT, and SNF values using the built-in pricing formula. [file:4]
- Payment mode selection with UPI or Bank transfer. [file:4]
- Webcam-based farmer face capture and saved image preview. [file:4]
- Transaction summary panel showing payment details, timestamp, and captured photo path. [file:4]
- SMS log viewer and payment log viewer for simple record tracking. [file:4]

## Tech Stack

- Python 3 [file:3]
- Tkinter for the desktop GUI [file:3][file:4]
- OpenCV (`opencv-python`) for webcam access [file:2][file:4]
- Pillow (`pillow`) for image conversion and preview display [file:2][file:4]

## Project Structure

```text
dairy-kiosk-app/
├── dairy_kiosk_app.py
├── requirements.txt
└── README.md
```

The application creates an output directory in the user home folder and stores farmer photos plus log files there during runtime. [file:4]

## Step-by-Step Installation

### 1. Clone the repository
```bash
git clone https://github.com/iamaryanbhalsing/dairy-kiosk-app.git
cd dairy-kiosk-app
```

### 2. Check Python version
Make sure Python 3 is installed:

```bash
python3 --version
```

### 3. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Tkinter if needed
On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-tk
```

### 6. Run the application
```bash
python3 dairy_kiosk_app.py
```

### 7. Use the app
- Enter farmer details
- Enter milk quantity, FAT, and SNF
- Select payment mode
- Start camera and capture face if needed
- Click **Process Transaction**

### 8. Check generated files
After running the app, these files are created in your home directory under `~/output/`:
- `~/output/farmer_photos/`
- `~/output/sms_log.txt`
- `~/output/payment_log.txt`

The current attached README uses an `output/` path, but the main script itself is the actual runnable entry point for the repository. [file:3][file:4]

## How It Works

1. Enter farmer and milk transaction details in the form. [file:4]
2. Select the payment mode as UPI or Bank. [file:4]
3. Start the webcam and capture the farmer face photo if needed. [file:4]
4. Click **Process Transaction** to calculate the rate and total amount. [file:4]
5. Review the generated summary and inspect SMS or payment logs from the built-in log viewer. [file:4]

## Payment Formula

The application calculates the milk rate and total payment using this formula:

```text
rate = 18 + (FAT × 6.5) + (SNF × 1.8)
amount = quantity × rate
```

This formula is implemented directly in the `calculate_payment` function. [file:4]

## Output Files

At runtime, the app creates and uses these paths:

- `~/output/farmer_photos/` for captured farmer images. [file:4]
- `~/output/sms_log.txt` for SMS-style transaction records. [file:4]
- `~/output/payment_log.txt` for payment transaction logs. [file:4]

## Notes

- Webcam capture requires a working camera device and the required Python packages to be installed. [file:4][file:2]
- If camera access fails, the app shows an error message instead of starting the video stream. [file:4]
- If no photo is captured, the transaction can still be processed and the summary shows that the face photo is not captured yet. [file:4]

## Future Improvements

- Export logs to CSV or Excel.
- Add database storage for farmer records.
- Add SMS gateway integration for real SMS delivery.
- Add authentication and operator login.
- Build analytics for daily milk collection and payout totals.


## License

This project is shared for educational and demonstration purposes.

