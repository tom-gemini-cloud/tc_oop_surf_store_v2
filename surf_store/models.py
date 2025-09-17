from typing import List
from abc import ABC, abstractmethod


class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str,
                 email: str, phone: str, address: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.orders: List['Order'] = []
        self.shopping_cart = ShoppingCart(self)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def update_contact_info(self, email: str = None, phone: str = None, address: str = None):
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address

    def get_order_history(self) -> List['Order']:
        return self.orders.copy()

    def add_order(self, order: 'Order'):
        self.orders.append(order)

    def get_total_spent(self) -> float:
        return sum(order.total_amount for order in self.orders)

    def __str__(self):
        return f"Customer: {self.get_full_name()} ({self.email})"


class ProductFamily:
    def __init__(self, family_id: int, name: str, description: str):
        self.family_id = family_id
        self.name = name
        self.description = description
        self.categories: List['ProductCategory'] = []

    def add_category(self, category: 'ProductCategory'):
        self.categories.append(category)

    def get_categories(self) -> List['ProductCategory']:
        return self.categories.copy()

    def get_all_products(self) -> List['Product']:
        all_products = []
        for category in self.categories:
            all_products.extend(category.get_products())
        return all_products

    def __str__(self):
        return f"Product Family: {self.name} ({len(self.categories)} categories)"


class ProductCategory:
    def __init__(self, category_id: int, name: str, description: str, family: ProductFamily):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.family = family
        self.products: List['Product'] = []
        family.add_category(self)

    def add_product(self, product: 'Product'):
        self.products.append(product)

    def get_products(self) -> List['Product']:
        return self.products.copy()

    def __str__(self):
        return f"Category: {self.name} ({len(self.products)} products)"


class Product(ABC):
    def __init__(self, product_id: int, name: str, description: str,
                 price: float, stock_quantity: int, category: ProductCategory):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category = category
        category.add_product(self)

    def update_stock(self, quantity: int):
        self.stock_quantity = max(0, self.stock_quantity + quantity)

    def is_available(self, quantity: int = 1) -> bool:
        return self.stock_quantity >= quantity

    def get_category(self) -> ProductCategory:
        return self.category

    def get_family(self) -> ProductFamily:
        return self.category.family

    @abstractmethod
    def get_shipping_weight(self) -> float:
        pass

    @abstractmethod
    def get_care_instructions(self) -> str:
        pass

    def get_product_info(self) -> str:
        return f"{self.name} - ${self.price:.2f} (Stock: {self.stock_quantity})"

    def __str__(self):
        return f"Product: {self.get_product_info()}"


class SurfBoard(Product):
    def __init__(self, product_id: int, name: str, description: str,
                 price: float, stock_quantity: int, category: ProductCategory,
                 length: str, board_type: str, fin_setup: str):
        super().__init__(product_id, name, description, price, stock_quantity, category)
        self.length = length
        self.board_type = board_type
        self.fin_setup = fin_setup

    def get_shipping_weight(self) -> float:
        base_weight = 3.0
        if "longboard" in self.board_type.lower():
            return base_weight + 2.0
        elif "shortboard" in self.board_type.lower():
            return base_weight + 1.0
        else:  # SUP
            return base_weight + 4.0

    def get_care_instructions(self) -> str:
        return "Rinse with fresh water after use. Store in a cool, dry place away from direct sunlight."

    def get_board_specs(self) -> str:
        return f"Length: {self.length}, Type: {self.board_type}, Fins: {self.fin_setup}"

    def __str__(self):
        return f"SurfBoard: {self.get_product_info()} | {self.get_board_specs()}"


class Wetsuit(Product):
    def __init__(self, product_id: int, name: str, description: str,
                 price: float, stock_quantity: int, category: ProductCategory,
                 thickness: str, suit_type: str, material: str):
        super().__init__(product_id, name, description, price, stock_quantity, category)
        self.thickness = thickness
        self.suit_type = suit_type
        self.material = material

    def get_shipping_weight(self) -> float:
        if "full" in self.suit_type.lower():
            return 1.5
        else:  # spring suit
            return 1.0

    def get_care_instructions(self) -> str:
        return f"Machine wash cold with {self.material}-friendly detergent. Hang dry only."

    def get_thermal_rating(self) -> str:
        thickness_map = {
            "3/2mm": "Warm water (18-23°C)",
            "4/3mm": "Cool water (12-18°C)",
            "5/4mm": "Cold water (8-14°C)"
        }
        return thickness_map.get(self.thickness, "General use")

    def __str__(self):
        return f"Wetsuit: {self.get_product_info()} | {self.thickness} {self.suit_type}"


class Accessory(Product):
    def __init__(self, product_id: int, name: str, description: str,
                 price: float, stock_quantity: int, category: ProductCategory,
                 accessory_type: str, compatibility: str = "Universal"):
        super().__init__(product_id, name, description, price, stock_quantity, category)
        self.accessory_type = accessory_type
        self.compatibility = compatibility

    def get_shipping_weight(self) -> float:
        weight_map = {
            "leash": 0.2,
            "wax": 0.1,
            "fins": 0.5,
            "tshirt": 0.3,
            "boardshorts": 0.4
        }
        return weight_map.get(self.accessory_type.lower(), 0.3)

    def get_care_instructions(self) -> str:
        if self.accessory_type.lower() in ["tshirt", "boardshorts"]:
            return "Machine wash cold, tumble dry low."
        elif self.accessory_type.lower() == "wax":
            return "Store in cool place to prevent melting."
        else:
            return "Rinse with fresh water after use."

    def __str__(self):
        return f"Accessory: {self.get_product_info()} | {self.accessory_type}"


class ShoppingCart:
    def __init__(self, customer: 'Customer'):
        self.customer = customer
        self.items: List[dict] = []
        self.discount_rate = 0.0

    def add_item(self, product: Product, quantity: int = 1):
        if not product.is_available(quantity):
            raise ValueError(f"Insufficient stock for {product.name}")

        for item in self.items:
            if item['product'].product_id == product.product_id:
                item['quantity'] += quantity
                return

        self.items.append({'product': product, 'quantity': quantity})

    def remove_item(self, product: Product, quantity: int = None):
        for i, item in enumerate(self.items):
            if item['product'].product_id == product.product_id:
                if quantity is None or quantity >= item['quantity']:
                    del self.items[i]
                else:
                    item['quantity'] -= quantity
                return

    def get_total_weight(self) -> float:
        return sum(item['product'].get_shipping_weight() * item['quantity']
                  for item in self.items)

    def get_subtotal(self) -> float:
        return sum(item['product'].price * item['quantity'] for item in self.items)

    def get_total(self) -> float:
        subtotal = self.get_subtotal()
        return subtotal * (1 - self.discount_rate)

    def apply_discount(self, rate: float):
        self.discount_rate = max(0, min(1, rate))

    def clear(self):
        self.items.clear()

    def __str__(self):
        return f"Cart for {self.customer.get_full_name()}: {len(self.items)} items, Total: ${self.get_total():.2f}"


class Inventory:
    def __init__(self):
        self.products: List[Product] = []
        self.low_stock_threshold = 5

    def add_product(self, product: Product):
        self.products.append(product)

    def get_products_by_type(self, product_type: type) -> List[Product]:
        return [p for p in self.products if isinstance(p, product_type)]

    def get_low_stock_products(self) -> List[Product]:
        return [p for p in self.products if p.stock_quantity < self.low_stock_threshold]

    def get_total_inventory_value(self) -> float:
        return sum(p.price * p.stock_quantity for p in self.products)

    def search_products(self, keyword: str) -> List[Product]:
        keyword_lower = keyword.lower()
        return [p for p in self.products
                if keyword_lower in p.name.lower() or keyword_lower in p.description.lower()]

    def __str__(self):
        return f"Inventory: {len(self.products)} products, Value: ${self.get_total_inventory_value():.2f}"