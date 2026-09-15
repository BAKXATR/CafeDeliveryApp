# data/store.py
"""
AppStore - butun ilova uchun yagona (Singleton) ma'lumotlar ombori.

Nega bunday qilingan?
- Kivy'da ekranlar (Screen) orasida ma'lumot almashish uchun eng toza yo'l -
  barcha ekranlar bitta umumiy "manba"ga (single source of truth) murojaat qilishi.
- Hozir bu yerda oddiy Python ro'yxatlari (in-memory) ishlatilgan.
  Kelajakda buni SQLite yoki Firebase/REST API bilan almashtirish uchun
  faqat shu fayldagi metodlar ichini o'zgartirish kifoya - qolgan UI kodi
  butunlay o'zgarmaydi.
"""

from data.models import MenuItem, CartItem, Order, ORDER_STATUSES


class AppStore:
    _instance = None  # Singleton nusxasi

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_store()
        return cls._instance

    # ------------------------------------------------------------------
    # Boshlang'ich holat
    # ------------------------------------------------------------------
    def _init_store(self):
        self.current_user_phone = ""     # login qilgan foydalanuvchi raqami
        self.cart: list[CartItem] = []   # joriy savatcha
        self.orders: list[Order] = []    # buyurtmalar tarixi
        self.menu_items: list[MenuItem] = self._seed_menu()
        # Demo SMS-kod (real loyihada SMS-gateway orqali keladi)
        self.last_sms_code = None

    def _seed_menu(self):
        """Demo uchun boshlang'ich menyu ma'lumotlari"""
        return [
            MenuItem(name="Cheeseburger", price=28000, category="Fast Food",
                     description="Mol go'shti, pishloq, achchiq sous"),
            MenuItem(name="Margherita Pitsa", price=45000, category="Pitsa",
                     description="Pomidor sousi, mozzarella, rayhon"),
            MenuItem(name="Pepperoni Pitsa", price=52000, category="Pitsa",
                     description="Pepperoni kolbasa, mozzarella"),
            MenuItem(name="Osh (Palov)", price=25000, category="Milliy taomlar",
                     description="Qo'y go'shti bilan an'anaviy o'zbek oshi"),
            MenuItem(name="Lag'mon", price=22000, category="Milliy taomlar",
                     description="Qo'lda tortilgan xamir, sabzavotlar"),
            MenuItem(name="Coca-Cola 0.5L", price=8000, category="Ichimliklar"),
            MenuItem(name="Fresh Apelsin", price=15000, category="Ichimliklar"),
            MenuItem(name="Tiramisu", price=24000, category="Shirinliklar"),
            MenuItem(name="Cheesecake", price=26000, category="Shirinliklar"),
        ]

    # ------------------------------------------------------------------
    # Kategoriyalar
    # ------------------------------------------------------------------
    def get_categories(self):
        """Menyudagi barcha unikal kategoriyalar ro'yxati"""
        seen = []
        for item in self.menu_items:
            if item.category not in seen:
                seen.append(item.category)
        return seen

    def get_items_by_category(self, category):
        return [i for i in self.menu_items if i.category == category]

    # ------------------------------------------------------------------
    # Savatcha (Cart) bilan ishlash
    # ------------------------------------------------------------------
    def add_to_cart(self, menu_item: MenuItem, quantity: int = 1):
        """Taomni savatga qo'shish. Agar allaqachon bor bo'lsa - miqdorini oshiradi."""
        for cart_item in self.cart:
            if cart_item.menu_item.id == menu_item.id:
                cart_item.quantity += quantity
                return
        self.cart.append(CartItem(menu_item=menu_item, quantity=quantity))

    def change_quantity(self, menu_item_id: int, delta: int):
        """Savatchadagi taom miqdorini o'zgartirish (+1 / -1).
        Agar miqdor 0 yoki undan kam bo'lsa - savatdan o'chiriladi."""
        for cart_item in self.cart:
            if cart_item.menu_item.id == menu_item_id:
                cart_item.quantity += delta
                if cart_item.quantity <= 0:
                    self.cart.remove(cart_item)
                return

    def remove_from_cart(self, menu_item_id: int):
        self.cart = [c for c in self.cart if c.menu_item.id != menu_item_id]

    def get_cart_total(self) -> float:
        return sum(item.total_price for item in self.cart)

    def get_cart_count(self) -> int:
        """Savatchadagi umumiy dona son (badge uchun)"""
        return sum(item.quantity for item in self.cart)

    def clear_cart(self):
        self.cart = []

    # ------------------------------------------------------------------
    # Buyurtmalar (Orders)
    # ------------------------------------------------------------------
    def create_order(self, address: str, phone: str, comment: str = "") -> Order:
        """Savatchadan yangi buyurtma yaratish va savatchani tozalash"""
        order = Order(
            items=list(self.cart),   # joriy savat nusxasini saqlaymiz
            address=address,
            phone=phone,
            comment=comment,
            total=self.get_cart_total(),
        )
        self.orders.insert(0, order)  # eng yangisi tepada tursin
        self.clear_cart()
        return order

    def advance_order_status(self, order_id: int):
        """Demo maqsadida buyurtma holatini keyingi bosqichga o'tkazish
        (real loyihada bu backend/kuryer tomonidan yuboriladi)."""
        for order in self.orders:
            if order.id == order_id:
                current_index = ORDER_STATUSES.index(order.status)
                if current_index < len(ORDER_STATUSES) - 1:
                    order.status = ORDER_STATUSES[current_index + 1]
                return order.status
        return None


# Butun ilova bo'ylab shu bitta obyektdan foydalaniladi
store = AppStore()