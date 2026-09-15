# screens/cart_screen.py
"""
CartScreen - Savatchadagi taomlarni ko'rish, miqdorini o'zgartirish,
umumiy summani chiqarish va buyurtmani rasmiylashtirishga o'tish.
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton

from data.store import store

Builder.load_file("kv/cart.kv")


class CartScreen(Screen):

    def on_pre_enter(self, *args):
        self.build_cart_list()
        self.update_total()

    def build_cart_list(self):
        container = self.ids.cart_list
        container.clear_widgets()

        if not store.cart:
            container.add_widget(MDLabel(
                text="Savatchangiz bo'sh 🛒",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="200dp",
            ))
            return

        for cart_item in store.cart:
            container.add_widget(self._build_cart_row(cart_item))

    def _build_cart_row(self, cart_item):
        row = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height="80dp",
            padding="10dp",
            spacing="10dp",
            radius=[10, 10, 10, 10],
            elevation=1,
        )

        # Nomi va narxi
        info_box = BoxLayout(orientation="vertical")
        info_box.add_widget(MDLabel(
            text=cart_item.menu_item.name, bold=True, size_hint_y=None, height="24dp",
        ))
        info_box.add_widget(MDLabel(
            text=f"{cart_item.total_price:,.0f} so'm".replace(",", " "),
            theme_text_color="Custom", text_color=(0.2, 0.6, 0.9, 1),
            size_hint_y=None, height="20dp",
        ))
        row.add_widget(info_box)

        # Miqdorni boshqarish (- son +)
        qty_box = BoxLayout(orientation="horizontal", size_hint_x=None, width="140dp")

        minus_btn = MDIconButton(icon="minus-circle-outline")
        minus_btn.bind(on_release=lambda inst, mi=cart_item.menu_item.id: self.change_qty(mi, -1))

        qty_label = MDLabel(text=str(cart_item.quantity), halign="center")

        plus_btn = MDIconButton(icon="plus-circle-outline")
        plus_btn.bind(on_release=lambda inst, mi=cart_item.menu_item.id: self.change_qty(mi, 1))

        qty_box.add_widget(minus_btn)
        qty_box.add_widget(qty_label)
        qty_box.add_widget(plus_btn)
        row.add_widget(qty_box)

        return row

    def change_qty(self, menu_item_id, delta):
        store.change_quantity(menu_item_id, delta)
        self.build_cart_list()
        self.update_total()

    def update_total(self):
        total = store.get_cart_total()
        self.ids.total_label.text = f"Jami: {total:,.0f} so'm".replace(",", " ")
        # Savat bo'sh bo'lsa - "Buyurtma berish" tugmasini o'chirib qo'yamiz
        self.ids.checkout_button.disabled = len(store.cart) == 0

    def go_to_checkout(self):
        if store.cart:
            self.manager.current = "checkout"

    def go_back(self):
        self.manager.current = "menu"