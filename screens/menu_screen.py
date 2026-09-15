# screens/menu_screen.py
"""
MenuScreen - Kategoriyalar bo'yicha taomlar ro'yxati.

Tuzilishi:
    - Yuqorida gorizontal kategoriya tugmalari (Chip'lar)
    - Pastda tanlangan kategoriyaga tegishli taomlar (MDCard'lar) ro'yxati
    - Har bir kartochkada "Savatga qo'shish" tugmasi bor
    - Yuqori panelda savatcha ikonkasi + ichidagi mahsulotlar soni (badge)
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar

from data.store import store

Builder.load_file("kv/menu.kv")


class CategoryChip(MDFlatButton):
    """Kategoriya tanlash tugmasi (oddiy tugma, chip ko'rinishida ishlatiladi)"""
    pass


class FoodCard(MDCard):
    """Bitta taomni ko'rsatuvchi kartochka"""
    pass


class MenuScreen(Screen):
    current_category = StringProperty("")

    def on_pre_enter(self, *args):
        """Ekranga kirishdan oldin har safar ma'lumotlarni yangilaymiz"""
        if not self.current_category:
            categories = store.get_categories()
            self.current_category = categories[0] if categories else ""
        self.build_categories()
        self.build_food_list()
        self.update_cart_badge()

    # ------------------------------------------------------------------
    # Kategoriyalar panelini qurish
    # ------------------------------------------------------------------
    def build_categories(self):
        container = self.ids.categories_box
        container.clear_widgets()

        for category in store.get_categories():
            is_selected = category == self.current_category
            chip = MDRaisedButton(
                text=category,
                md_bg_color=(0.2, 0.6, 0.9, 1) if is_selected else (0.9, 0.9, 0.9, 1),
                text_color=(1, 1, 1, 1) if is_selected else (0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                height="36dp",
            )
            # lambda ichida category=category - "late binding" xatosining oldini olish uchun
            chip.bind(on_release=lambda inst, category=category: self.select_category(category))
            container.add_widget(chip)

    def select_category(self, category):
        self.current_category = category
        self.build_categories()   # tanlangan chip rangini yangilash uchun qayta chizamiz
        self.build_food_list()

    # ------------------------------------------------------------------
    # Taomlar ro'yxatini qurish
    # ------------------------------------------------------------------
    def build_food_list(self):
        container = self.ids.food_list
        container.clear_widgets()

        items = store.get_items_by_category(self.current_category)
        for item in items:
            card = self._build_food_card(item)
            container.add_widget(card)

    def _build_food_card(self, menu_item):
        """Bitta MenuItem uchun kartochka (rasm, nom, narx, + tugma) yasaydi"""
        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height="100dp",
            padding="10dp",
            spacing="10dp",
            radius=[12, 12, 12, 12],
            elevation=2,
        )

        # Chap tarafda - matnli qism (rasm o'rniga ilova ichida shu joy qoldirilgan,
        # real loyihada Image(source=menu_item.image) qo'shiladi)
        text_box = BoxLayout(orientation="vertical", spacing="4dp")
        text_box.add_widget(MDLabel(
            text=menu_item.name, bold=True, font_style="Subtitle1",
            size_hint_y=None, height="26dp",
        ))
        text_box.add_widget(MDLabel(
            text=menu_item.description, font_style="Caption",
            theme_text_color="Secondary", size_hint_y=None, height="20dp",
        ))
        text_box.add_widget(MDLabel(
            text=f"{menu_item.price:,.0f} so'm".replace(",", " "),
            bold=True, theme_text_color="Custom", text_color=(0.2, 0.6, 0.9, 1),
            size_hint_y=None, height="26dp",
        ))
        card.add_widget(text_box)

        # O'ng tarafda - savatga qo'shish tugmasi
        add_button = MDRaisedButton(
            text="+",
            size_hint=(None, None),
            size=("48dp", "48dp"),
            pos_hint={"center_y": 0.5},
            md_bg_color=(0.2, 0.6, 0.9, 1),
        )
        add_button.bind(on_release=lambda inst, mi=menu_item: self.add_to_cart(mi))
        card.add_widget(add_button)

        return card

    # ------------------------------------------------------------------
    # Savatcha bilan bog'liq harakatlar
    # ------------------------------------------------------------------
    def add_to_cart(self, menu_item):
        store.add_to_cart(menu_item)
        self.update_cart_badge()
        Snackbar(text=f"'{menu_item.name}' savatga qo'shildi").open()

    def update_cart_badge(self):
        count = store.get_cart_count()
        self.ids.cart_badge.text = str(count) if count > 0 else ""

    def go_to_cart(self):
        self.manager.current = "cart"

    def go_to_orders(self):
        self.manager.current = "orders"