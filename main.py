# main.py
"""
Kafe/Restoran Yetkazib Berish (Delivery) ilovasi - kirish nuqtasi.

Ishga tushirish:
    python main.py

Ekranlar orasidagi navigatsiya kivy.uix.screenmanager.ScreenManager
orqali amalga oshiriladi. Har bir ekran alohida faylda (screens/) va
o'ziga tegishli .kv dizayn faylida (kv/) joylashgan - bu kodni
modulli va kengaytirish oson qiladi.
"""

from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Ekranlar
from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.cart_screen import CartScreen
from screens.checkout_screen import CheckoutScreen
from screens.orders_screen import OrdersScreen

# Desktop'da test qilish uchun telefon o'lchamiga yaqin oyna (APK'da ta'sir qilmaydi)
Window.size = (360, 640)


class DeliveryApp(MDApp):
    """Ilovaning bosh klassi - KivyMD App'dan meros oladi"""

    def build(self):
        # ---- Umumiy dizayn sozlamalari (tema) ----
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Orange"

        self.title = "TezYetkazib - Kafe va Restoranlardan Yetkazib Berish"

        # ---- ScreenManager - barcha ekranlarni ro'yxatdan o'tkazamiz ----
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen())
        sm.add_widget(MenuScreen())
        sm.add_widget(CartScreen())
        sm.add_widget(CheckoutScreen())
        sm.add_widget(OrdersScreen())

        sm.current = "login"  # ilova login ekranidan boshlanadi
        return sm


if __name__ == "__main__":
    DeliveryApp().run()