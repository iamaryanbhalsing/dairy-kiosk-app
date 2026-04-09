import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

APP_TITLE = "Smart Dairy Transparency Kiosk - VM Safe"
BASE_DIR = os.path.join(os.path.expanduser("~"), "DairyKioskData")
PHOTO_DIR = os.path.join(BASE_DIR, "farmer_photos")
SMS_LOG = os.path.join(BASE_DIR, "sms_log.txt")
PAYMENT_LOG = os.path.join(BASE_DIR, "payment_log.txt")
os.makedirs(PHOTO_DIR, exist_ok=True)

class DairyKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("980x680")
        self.root.minsize(860, 600)
        self.root.configure(bg="#eef2f7")
        self.photo_path = "Not uploaded"
        self.preview_image = None

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#1f2937", font=("DejaVu Sans", 10))
        style.configure("Top.TLabel", background="#eef2f7", foreground="#0f172a", font=("DejaVu Sans", 20, "bold"))
        style.configure("Sub.TLabel", background="#eef2f7", foreground="#64748b", font=("DejaVu Sans", 10))
        style.configure("Head.TLabel", background="#ffffff", foreground="#0f172a", font=("DejaVu Sans", 12, "bold"))
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#eef2f7", padx=20, pady=14)
        header.pack(fill="x")
        ttk.Label(header, text=APP_TITLE, style="Top.TLabel").pack(anchor="w")
        ttk.Label(header, text="Simple version without camera dependency. Best for virtual machines.", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        main = tk.Frame(self.root, bg="#eef2f7", padx=16, pady=10)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        form_card = ttk.Frame(main, padding=18)
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        photo_card = ttk.Frame(main, padding=18)
        photo_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)

        self.build_form(form_card)
        self.build_photo_section(photo_card)

    def build_form(self, parent):
        ttk.Label(parent, text="Milk Transaction", style="Head.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))
        self.fields = {}
        rows = [
            ("Farmer ID", "F101"),
            ("Farmer Name", "Ramesh Patil"),
            ("Phone Number", "9876543210"),
            ("Milk Quantity (L)", "12.5"),
            ("FAT %", "4.2"),
            ("SNF %", "8.5"),
        ]
        for i, (label, default) in enumerate(rows, start=1):
            ttk.Label(parent, text=label).grid(row=i, column=0, sticky="w", pady=7, padx=(0, 10))
            ent = ttk.Entry(parent, width=34)
            ent.insert(0, default)
            ent.grid(row=i, column=1, sticky="ew", pady=7)
            self.fields[label] = ent

        ttk.Label(parent, text="Payment Mode").grid(row=7, column=0, sticky="w", pady=7)
        self.payment_mode = ttk.Combobox(parent, values=["UPI", "Bank"], state="readonly", width=32)
        self.payment_mode.set("UPI")
        self.payment_mode.grid(row=7, column=1, sticky="ew", pady=7)

        ttk.Button(parent, text="Process Transaction", command=self.process_transaction).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(16, 8))
        ttk.Button(parent, text="View SMS Log", command=lambda: self.open_log(SMS_LOG, "SMS Log")).grid(row=9, column=0, sticky="ew", pady=5, padx=(0, 5))
        ttk.Button(parent, text="View Payment Log", command=lambda: self.open_log(PAYMENT_LOG, "Payment Log")).grid(row=9, column=1, sticky="ew", pady=5, padx=(5, 0))

        ttk.Label(parent, text="Summary", style="Head.TLabel").grid(row=10, column=0, columnspan=2, sticky="w", pady=(16, 8))
        self.summary = tk.Text(parent, height=13, wrap="word", font=("DejaVu Sans Mono", 10), bg="#f8fafc", relief="solid", bd=1)
        self.summary.grid(row=11, column=0, columnspan=2, sticky="nsew")
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(11, weight=1)

    def build_photo_section(self, parent):
        ttk.Label(parent, text="Farmer Photo", style="Head.TLabel").pack(anchor="w")
        ttk.Label(parent, text="Upload image manually instead of using camera.").pack(anchor="w", pady=(4, 10))

        self.status_label = tk.Label(parent, text="No photo uploaded", bg="#f8fafc", fg="#64748b", relief="solid", bd=1, height=2)
        self.status_label.pack(fill="x", pady=(0, 8))

        self.preview_label = tk.Label(parent, text="Photo preview not available\n(works without camera or extra libraries)", bg="#dbe4ee", fg="#475569", width=42, height=16, relief="solid", bd=1, justify="center")
        self.preview_label.pack(fill="both", expand=True)

        ttk.Button(parent, text="Upload Farmer Photo", command=self.upload_photo).pack(fill="x", pady=(12, 6))
        ttk.Button(parent, text="Remove Photo", command=self.remove_photo).pack(fill="x")

        note = tk.Label(parent, text="Accepted: JPG, JPEG, PNG, BMP\nPhoto file is copied to DairyKioskData/farmer_photos", bg="#ffffff", fg="#64748b", justify="left")
        note.pack(anchor="w", pady=(12, 0))

    def upload_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select farmer photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if not file_path:
            return
        farmer_id = self.fields["Farmer ID"].get().strip() or "unknown"
        farmer_name = self.fields["Farmer Name"].get().strip().replace(" ", "_") or "farmer"
        ext = os.path.splitext(file_path)[1] or ".jpg"
        filename = f"{farmer_id}_{farmer_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        dest = os.path.join(PHOTO_DIR, filename)
        shutil.copy(file_path, dest)
        self.photo_path = dest
        self.status_label.config(text=f"Photo uploaded successfully\n{dest}", fg="#166534")
        self.preview_label.config(text=f"Photo selected successfully\n\nFile: {os.path.basename(dest)}\n\nPreview disabled for maximum VM compatibility", bg="#ecfdf3", fg="#166534")
        messagebox.showinfo("Photo uploaded", f"Farmer photo saved successfully.\n\n{dest}")

    def remove_photo(self):
        self.photo_path = "Not uploaded"
        self.status_label.config(text="No photo uploaded", fg="#64748b")
        self.preview_label.config(text="Photo preview not available\n(works without camera or extra libraries)", bg="#dbe4ee", fg="#475569")

    def calculate_payment(self, qty, fat, snf):
        rate = 18 + (fat * 6.5) + (snf * 1.8)
        amount = qty * rate
        return round(rate, 2), round(amount, 2)

    def process_transaction(self):
        try:
            farmer_id = self.fields["Farmer ID"].get().strip()
            name = self.fields["Farmer Name"].get().strip()
            phone = self.fields["Phone Number"].get().strip()
            qty = float(self.fields["Milk Quantity (L)"].get().strip())
            fat = float(self.fields["FAT %"].get().strip())
            snf = float(self.fields["SNF %"].get().strip())
            mode = self.payment_mode.get().strip()
            if not farmer_id or not name or not phone or not mode:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid input", "Please enter valid farmer and milk details.")
            return

        rate, amount = self.calculate_payment(qty, fat, snf)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(SMS_LOG, "a", encoding="utf-8") as f:
            f.write(f"{stamp} | SMS to {phone} | Farmer: {name} | Qty: {qty} L | FAT: {fat} | SNF: {snf} | Rate: Rs {rate}/L | Amount: Rs {amount}\n")
        with open(PAYMENT_LOG, "a", encoding="utf-8") as f:
            f.write(f"{stamp} | {mode} transfer | Farmer: {name} | Amount: Rs {amount} | Status: SUCCESS\n")

        result = (
            f"Farmer ID      : {farmer_id}\n"
            f"Farmer Name    : {name}\n"
            f"Phone Number   : {phone}\n"
            f"Milk Quantity  : {qty} L\n"
            f"FAT            : {fat}%\n"
            f"SNF            : {snf}%\n"
            f"Rate per Litre : Rs {rate}\n"
            f"Total Payment  : Rs {amount}\n"
            f"Payment Mode   : {mode}\n"
            f"Photo Path     : {self.photo_path}\n"
            f"Time           : {stamp}\n"
        )
        self.summary.delete("1.0", tk.END)
        self.summary.insert(tk.END, result)
        messagebox.showinfo("Success", f"Transaction completed successfully.\n\nAmount: Rs {amount}")

    def open_log(self, path, title):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("760x420")
        text = tk.Text(win, wrap="word", font=("DejaVu Sans Mono", 10))
        text.pack(fill="both", expand=True)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                text.insert(tk.END, f.read())
        else:
            text.insert(tk.END, "No records available yet.")
        text.config(state="disabled")

root = tk.Tk()
app = DairyKioskApp(root)
root.mainloop()
