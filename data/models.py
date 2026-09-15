# data/models.py
"""
Ilovaning asosiy ma'lumot modellari.
Hozircha oddiy Python klasslari (dataclass) ko'rinishida - kelajakda
bu klasslarni SQLite / Django REST API bilan almashtirish oson bo'ladi,
chunki qolgan barcha kod faqat shu klasslar orqali ishlaydi.
"""

from dataclasses import dataclass, field
from datetime import datetime
import itertools

# Har bir obyektga avtomatik unikal ID beruvchi hisoblagichlar
_menu_id_counter = itertools.count(1)
_order_id_counter = itertools.count(1001)


@dataclass
class MenuItem:
    """Menyudagi bitta taom/mahsulot"""
    name: str
    price: float                # narxi (so'mda)
    category: str                # masalan: "Fast Food", "Ichimliklar", "Shirinliklar"
    image: str = "assets/images/placeholder.png"  # rasm manzili
    description: str = ""
    id: int = field(default_factory=lambda: next(_menu_id_counter))


@dataclass
class CartItem:
    """Savatchadagi bitta band - taom + miqdori"""
    menu_item: MenuItem
    quantity: int = 1

    @property
    def total_price(self) -> float:
        return self.menu_item.price * self.quantity


# Buyurtma holatlari (status) - real backendda enum sifatida saqlanadi
ORDER_STATUSES = [
    "Kutilmoqda",        # yangi buyurtma
    "Tayyorlanmoqda",    # oshxonada tayyorlanmoqda
    "Yo'lda",            # kuryer yetkazmoqda
    "Yetkazildi",        # yakunlangan
]


@dataclass
class Order:
    """Mijoz tomonidan rasmiylashtirilgan buyurtma"""
    items: list              # CartItem obyektlari ro'yxati (nusxasi)
    address: str
    phone: str
    comment: str = ""
    total: float = 0.0
    status: str = ORDER_STATUSES[0]
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))
    id: int = field(default_factory=lambda: next(_order_id_counter))