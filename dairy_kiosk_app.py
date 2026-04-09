import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import cv2
except Exception:
    cv2 = None

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

APP_TITLE = "Smart Dairy Transparency Kiosk"
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "output")
PHOTO_DIR = os.path.join(OUTPUT_DIR, "farmer_photos")
SMS_LOG = os.path.join(OUTPUT_DIR, "sms_log.txt")
PAYMENT_LOG = os.path.join(OUTPUT_DIR, "payment_log.txt")

os.makedirs(PHOTO_DIR, exist_ok=True)

class DairyKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1100x720")
        self.root.minsize(980, 640)
        self.root.configure(bg="#f4f6f8")

        self.cap = None
        self.camera_running = False
        self.current_frame = None
        self.photo_path = None
        self.preview_image = None

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Header.TLabel", background="#f4f6f8", foreground="#14213d", font=("DejaVu Sans", 20, "bold"))
        self.style.configure("Sub.TLabel", background="#f4f6f8", foreground="#5b6470", font=("DejaVu Sans", 10))
        self.style.configure("CardTitle.TLabel", background="#ffffff", foreground="#14213d", font=("DejaVu Sans", 12, "bold"))
        self.style.configure("TLabel", font=("DejaVu Sans", 10), background="#ffffff")
        self.style.configure("TButton", font=("DejaVu Sans", 10, "bold"), padding=8)
        self.style.configure("Accent.TButton", font=("DejaVu Sans", 10, "bold"), padding=10, foreground="#ffffff", background="#0b6e4f")
        self.style.map("Accent.TButton", background=[("active", "#09563e")])
        self.style.configure("Treeview", rowheight=28, font=("DejaVu Sans", 10))
        self.style.configure("Treeview.Heading", font=("DejaVu Sans", 10, "bold"))

        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#f4f6f8", padx=24, pady=16)
        header.pack(fill="x")
        ttk.Label(header, text=APP_TITLE, style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Transparent milk collection, instant payment, and farmer photo capture", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        content = tk.Frame(self.root, bg="#f4f6f8", padx=20, pady=10)
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        left = ttk.Frame(content, style="Card.TFrame", padding=20)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        right = ttk.Frame(content, style="Card.TFrame", padding=20)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        self.build_form(left)
        self.build_camera(right)

    def build_form(self, parent):
        ttk.Label(parent, text="Transaction Details", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        labels = [
            ("Farmer ID", "F101"),
            ("Farmer Name", "Ramesh Patil"),
            ("Phone Number", "9876543210"),
            ("Milk Quantity (L)", "12.5"),
            ("FAT %", "4.2"),
            ("SNF %", "8.5"),
        ]
        self.entries = {}
        for idx, (label, default) in enumerate(labels, start=1):
            ttk.Label(parent, text=label).grid(row=idx, column=0, sticky="w", pady=8, padx=(0, 10))
            entry = ttk.Entry(parent, width=34)
            entry.insert(0, default)
            entry.grid(row=idx, column=1, sticky="ew", pady=8)
            self.entries[label] = entry

        ttk.Label(parent, text="Payment Mode").grid(row=7, column=0, sticky="w", pady=8)
        self.payment_mode = ttk.Combobox(parent, values=["UPI", "Bank"], state="readonly", width=31)
        self.payment_mode.set("UPI")
        self.payment_mode.grid(row=7, column=1, sticky="ew", pady=8)

        ttk.Button(parent, text="Process Transaction", style="Accent.TButton", command=self.process_transaction).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(18, 10))
        ttk.Button(parent, text="View SMS Log", command=lambda: self.open_log(SMS_LOG, "SMS Log")).grid(row=9, column=0, sticky="ew", pady=6, padx=(0, 6))
        ttk.Button(parent, text="View Payment Log", command=lambda: self.open_log(PAYMENT_LOG, "Payment Log")).grid(row=9, column=1, sticky="ew", pady=6, padx=(6, 0))

        summary_card = tk.Frame(parent, bg="#f8fafc", bd=1, relief="solid", highlightbackground="#d9e2ec", highlightthickness=1)
        summary_card.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
        summary_card.grid_columnconfigure(0, weight=1)
        tk.Label(summary_card, text="Transaction Summary", bg="#f8fafc", fg="#14213d", font=("DejaVu Sans", 12, "bold"), anchor="w").grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 6))
        self.summary_text = tk.Text(summary_card, height=12, wrap="word", bg="#f8fafc", fg="#1f2933", relief="flat", font=("DejaVu Sans Mono", 10))
        self.summary_text.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 12))

        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(10, weight=1)

    def build_camera(self, parent):
        ttk.Label(parent, text="Farmer Face Capture", style="CardTitle.TLabel").pack(anchor="w")
        tk.Label(parent, text="Capture the farmer photo for identity and transaction record.", bg="#ffffff", fg="#5b6470", font=("DejaVu Sans", 10)).pack(anchor="w", pady=(4, 14))

        self.video_label = tk.Label(parent, bg="#dde7f0", width=420, height=280)
        self.video_label.pack(fill="x")

        btn_row = tk.Frame(parent, bg="#ffffff")
        btn_row.pack(fill="x", pady=12)
        ttk.Button(btn_row, text="Start Camera", command=self.start_camera).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Capture Face", command=self.capture_face).pack(side="left", padx=8)
        ttk.Button(btn_row, text="Stop Camera", command=self.stop_camera).pack(side="left", padx=8)

        preview_frame = tk.Frame(parent, bg="#f8fafc", bd=1, relief="solid", highlightbackground="#d9e2ec", highlightthickness=1)
        preview_frame.pack(fill="both", expand=True, pady=(12, 0))
        tk.Label(preview_frame, text="Saved Photo Preview", bg="#f8fafc", fg="#14213d", font=("DejaVu Sans", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        self.photo_preview_label = tk.Label(preview_frame, bg="#f8fafc", text="No farmer photo captured yet.", fg="#6b7280", font=("DejaVu Sans", 10))
        self.photo_preview_label.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def start_camera(self):
        if cv2 is None or Image is None or ImageTk is None:
            messagebox.showerror("Missing dependency", "Please install opencv-python and pillow to use camera capture.")
            return
        if self.camera_running:
            return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera error", "Unable to access webcam.")
            return
        self.camera_running = True
        self.update_camera_frame()

    def update_camera_frame(self):
        if not self.camera_running or self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            image = image.resize((420, 280))
            self.preview_image = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=self.preview_image, text="")
        self.root.after(20, self.update_camera_frame)

    def capture_face(self):
        farmer_id = self.entries["Farmer ID"].get().strip() or "unknown"
        farmer_name = self.entries["Farmer Name"].get().strip().replace(" ", "_") or "farmer"
        if self.current_frame is None:
            messagebox.showwarning("No frame", "Start the camera before capturing the farmer face.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.photo_path = os.path.join(PHOTO_DIR, f"{farmer_id}_{farmer_name}_{timestamp}.jpg")
        cv2.imwrite(self.photo_path, self.current_frame)

        rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb).resize((300, 200))
        self.saved_preview = ImageTk.PhotoImage(image=image)
        self.photo_preview_label.configure(image=self.saved_preview, text="")
        messagebox.showinfo("Photo captured", f"Farmer face saved successfully.\n\n{self.photo_path}")

    def stop_camera(self):
        self.camera_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.video_label.configure(image="", text="Camera stopped", fg="#6b7280")

    def calculate_payment(self, qty, fat, snf):
        rate = 18 + (fat * 6.5) + (snf * 1.8)
        amount = qty * rate
        return round(rate, 2), round(amount, 2)

    def append_logs(self, name, phone, qty, fat, snf, rate, amount, mode):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SMS_LOG, "a", encoding="utf-8") as f:
            f.write(f"{stamp} | SMS to {phone} | Farmer: {name} | Qty: {qty} L | FAT: {fat} | SNF: {snf} | Rate: Rs {rate}/L | Amount: Rs {amount}\n")
        with open(PAYMENT_LOG, "a", encoding="utf-8") as f:
            f.write(f"{stamp} | {mode} transfer | Farmer: {name} | Amount: Rs {amount} | Status: SUCCESS\n")

    def process_transaction(self):
        try:
            farmer_id = self.entries["Farmer ID"].get().strip()
            farmer_name = self.entries["Farmer Name"].get().strip()
            phone = self.entries["Phone Number"].get().strip()
            qty = float(self.entries["Milk Quantity (L)"].get().strip())
            fat = float(self.entries["FAT %"].get().strip())
            snf = float(self.entries["SNF %"].get().strip())
            payment_mode = self.payment_mode.get().strip()
            if not all([farmer_id, farmer_name, phone, payment_mode]):
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid input", "Please enter valid farmer and milk details.")
            return

        rate, amount = self.calculate_payment(qty, fat, snf)
        self.append_logs(farmer_name, phone, qty, fat, snf, rate, amount, payment_mode)

        summary = (
            f"Farmer ID      : {farmer_id}\n"
            f"Farmer Name    : {farmer_name}\n"
            f"Phone Number   : {phone}\n"
            f"Milk Quantity  : {qty} L\n"
            f"FAT            : {fat}%\n"
            f"SNF            : {snf}%\n"
            f"Rate per Litre : Rs {rate}\n"
            f"Total Payment  : Rs {amount}\n"
            f"Payment Mode   : {payment_mode}\n"
            f"SMS Status     : Sent\n"
            f"Face Photo     : {self.photo_path if self.photo_path else 'Not captured yet'}\n"
            f"Time           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        messagebox.showinfo("Transaction complete", f"Payment processed successfully.\n\nAmount: Rs {amount}")

    def open_log(self, file_path, title):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("760x420")
        text = tk.Text(win, wrap="word", font=("DejaVu Sans Mono", 10))
        text.pack(fill="both", expand=True)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                text.insert(tk.END, f.read())
        else:
            text.insert(tk.END, "No records available yet.")
        text.config(state="disabled")

    def on_close(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DairyKioskApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
