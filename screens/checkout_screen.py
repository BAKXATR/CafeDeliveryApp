# screens/checkout_screen.py
"""
CheckoutScreen - Yetkazib berish manzilini kiritish va buyurtmani
yakuniy rasmiylashtirish (tasdiqlash).
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from data.store import store

Builder.load_file("kv/checkout.kv")


class CheckoutScreen(Screen):
    dialog = None

    def on_pre_enter(self, *args):
        # Telefon raqamini avtomatik to'ldirib qo'yamiz (login vaqtida kiritilgan)
        self.ids.phone_field.text = store.current_user_phone
        self.ids.total_label.text = f"To'lov summasi: {store.get_cart_total():,.0f} so'm".replace(",", " ")

    def confirm_order(self):
        address = self.ids.address_field.text.strip()
        phone = self.ids.phone_field.text.strip()
        comment = self.ids.comment_field.text.strip()

        if not address:
            Snackbar(text="Iltimos, yetkazib berish manzilini kiriting!").open()
            return
        if not phone:
            Snackbar(text="Iltimos, telefon raqamingizni kiriting!").open()
            return

        order = store.create_order(address=address, phone=phone, comment=comment)
        self._show_success_dialog(order)

    def _show_success_dialog(self, order):
        """Buyurtma qabul qilinganini tasdiqlovchi modal oyna"""
        self.dialog = MDDialog(
            title="Buyurtma qabul qilindi! ✅",
            text=(
                f"Buyurtma raqami: #{order.id}\n"
                f"Summasi: {order.total:,.0f} so'm\n"
                f"Holati: {order.status}"
            ).replace(",", " "),
            buttons=[
                MDFlatButton(text="Tarixni ko'rish", on_release=self._go_to_orders),
            ],
        )
        self.dialog.open()

    def _go_to_orders(self, *args):
        if self.dialog:
            self.dialog.dismiss()
        # Formani tozalaymiz, keyingi buyurtma uchun tayyor bo'lsin
        self.ids.address_field.text = ""
        self.ids.comment_field.text = ""
        self.manager.current = "orders"

    def go_back(self):
        self.manager.current = "cart"