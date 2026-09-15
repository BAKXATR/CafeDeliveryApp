# screens/login_screen.py
"""
LoginScreen - Telefon raqam + SMS-kod orqali avtorizatsiya (simulyatsiya).

Real loyihada:
    - "SMS yuborish" bosilganda backend'ga POST so'rov yuboriladi (Eskiz.uz, Twilio va h.k.)
    - Kod tekshiruvi ham backend orqali amalga oshiriladi.
Hozir esa demo/portfolio maqsadida kod ilovaning o'zida generatsiya qilinadi
va ekranda ko'rsatiladi (production'da BU QILINMAYDI - faqat testing uchun!).
"""

import random

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from data.store import store

# Shu ekranga tegishli KV-fayl yuklanadi
Builder.load_file("kv/login.kv")


class LoginScreen(Screen):
    phone_number = StringProperty("")
    info_text = StringProperty("Telefon raqamingizni kiriting")
    step = StringProperty("phone")  # "phone" -> "code"

    def send_sms(self):
        """1-qadam: raqamni tekshirib, 'SMS' yuborish"""
        phone = self.ids.phone_field.text.strip()

        # Oddiy validatsiya: kamida 9 ta raqam bo'lishi kerak
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 9:
            self.info_text = "Iltimos, to'g'ri telefon raqam kiriting!"
            return

        self.phone_number = phone
        # 4 xonali demo-kod generatsiya qilamiz
        store.last_sms_code = str(random.randint(1000, 9999))

        # Production'da bu qator BO'LMAYDI - biz demo uchun kodni ekranda ko'rsatamiz
        self.info_text = f"Tasdiqlash kodi yuborildi (demo kod: {store.last_sms_code})"
        self.step = "code"
        self.ids.code_field.opacity = 1
        self.ids.code_field.disabled = False
        self.ids.action_button.text = "Tasdiqlash"

    def verify_code(self):
        """2-qadam: kiritilgan SMS-kodni tekshirish"""
        entered_code = self.ids.code_field.text.strip()

        if entered_code == store.last_sms_code:
            store.current_user_phone = self.phone_number
            self.info_text = "Muvaffaqiyatli kirdingiz!"
            # Asosiy menyu ekraniga o'tamiz
            self.manager.current = "menu"
            self._reset_form()
        else:
            self.info_text = "Kod noto'g'ri, qaytadan urinib ko'ring"

    def on_action_button(self):
        """Bitta tugma ikki bosqichda ishlaydi: avval SMS yuborish, keyin tasdiqlash"""
        if self.step == "phone":
            self.send_sms()
        else:
            self.verify_code()

    def _reset_form(self):
        self.step = "phone"
        self.ids.code_field.text = ""
        self.ids.code_field.opacity = 0
        self.ids.code_field.disabled = True
        self.ids.action_button.text = "SMS yuborish"