# screens/orders_screen.py
"""
OrdersScreen - Foydalanuvchining barcha buyurtmalari va ularning holati
(Kutilmoqda -> Tayyorlanmoqda -> Yo'lda -> Yetkazildi).

Demo maqsadida har bir buyurtma holati "Holatni yangilash" tugmasi orqali
qo'lda o'zgartiriladi (real loyihada bu backend/WebSocket orqali avtomatik keladi).
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton

from data.store import store
from data.models import ORDER_STATUSES

Builder.load_file("kv/orders.kv")

# Har bir holat uchun rang (UI'da vizual farqlash uchun)
STATUS_COLORS = {
    "Kutilmoqda": (0.95, 0.6, 0.1, 1),
    "Tayyorlanmoqda": (0.2, 0.6, 0.9, 1),
    "Yo'lda": (0.6, 0.3, 0.9, 1),
    "Yetkazildi": (0.2, 0.7, 0.4, 1),
}


class OrdersScreen(Screen):

    def on_pre_enter(self, *args):
        self.build_orders_list()

    def build_orders_list(self):
        container = self.ids.orders_list
        container.clear_widgets()

        if not store.orders:
            container.add_widget(MDLabel(
                text="Hali buyurtmalar yo'q 📦",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="200dp",
            ))
            return

        for order in store.orders:
            container.add_widget(self._build_order_card(order))

    def _build_order_card(self, order):
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="150dp",
            padding="12dp",
            spacing="6dp",
            radius=[12, 12, 12, 12],
            elevation=2,
        )

        header = BoxLayout(size_hint_y=None, height="26dp")
        header.add_widget(MDLabel(text=f"Buyurtma #{order.id}", bold=True))
        header.add_widget(MDLabel(
            text=order.status, halign="right",
            theme_text_color="Custom",
            text_color=STATUS_COLORS.get(order.status, (0, 0, 0, 1)),
            bold=True,
        ))
        card.add_widget(header)

        card.add_widget(MDLabel(
            text=f"Manzil: {order.address}", theme_text_color="Secondary",
            size_hint_y=None, height="20dp",
        ))
        card.add_widget(MDLabel(
            text=f"Sana: {order.created_at}", theme_text_color="Secondary",
            font_style="Caption", size_hint_y=None, height="18dp",
        ))
        card.add_widget(MDLabel(
            text=f"Summasi: {order.total:,.0f} so'm".replace(",", " "),
            bold=True, size_hint_y=None, height="22dp",
        ))

        # Agar buyurtma hali yakunlanmagan bo'lsa - demo uchun holatni yangilash tugmasi
        if order.status != ORDER_STATUSES[-1]:
            update_btn = MDFlatButton(
                text="Holatni yangilash (demo)",
                size_hint_y=None,
                height="30dp",
            )
            update_btn.bind(on_release=lambda inst, oid=order.id: self.advance_status(oid))
            card.add_widget(update_btn)

        return card

    def advance_status(self, order_id):
        store.advance_order_status(order_id)
        self.build_orders_list()

    def go_back(self):
        self.manager.current = "menu"