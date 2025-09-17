from datetime import datetime
from typing import List, Optional
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class DeliveryStatus(Enum):
    PREPARING = "preparing"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"


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


class Product:
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

    def __str__(self):
        return f"Product: {self.name} - ${self.price:.2f} (Stock: {self.stock_quantity})"


class Order:
    def __init__(self, order_id: int, customer: Customer, order_date: datetime = None):
        self.order_id = order_id
        self.customer = customer
        self.order_date = order_date or datetime.now()
        self.order_details: List['OrderDetail'] = []
        self.total_amount = 0.0
        self.status = OrderStatus.PENDING
        self.payment: Optional['Payment'] = None
        self.delivery: Optional['Delivery'] = None
        customer.add_order(self)

    def add_order_detail(self, product: Product, quantity: int):
        if product.is_available(quantity):
            detail = OrderDetail(len(self.order_details) + 1, self, product, quantity)
            self.order_details.append(detail)
            product.update_stock(-quantity)
            self.calculate_total()
            return detail
        else:
            raise ValueError(f"Insufficient stock for {product.name}")

    def calculate_total(self):
        self.total_amount = sum(detail.subtotal for detail in self.order_details)

    def update_status(self, status: OrderStatus):
        self.status = status

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer.get_full_name()} - ${self.total_amount:.2f} ({self.status.value})"


class OrderDetail:
    def __init__(self, detail_id: int, order: Order, product: Product, quantity: int):
        self.detail_id = detail_id
        self.order = order
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price
        self.subtotal = self.calculate_subtotal()

    def calculate_subtotal(self) -> float:
        self.subtotal = self.unit_price * self.quantity
        return self.subtotal

    def __str__(self):
        return f"{self.quantity}x {self.product.name} @ ${self.unit_price:.2f} = ${self.subtotal:.2f}"


class Payment:
    def __init__(self, payment_id: int, order: Order, payment_method: str):
        self.payment_id = payment_id
        self.order = order
        self.amount = order.total_amount
        self.payment_method = payment_method
        self.payment_date = datetime.now()
        self.status = PaymentStatus.PENDING
        order.payment = self

    def process_payment(self) -> bool:
        try:
            self.status = PaymentStatus.COMPLETED
            self.order.update_status(OrderStatus.CONFIRMED)
            return True
        except Exception:
            self.status = PaymentStatus.FAILED
            return False

    def refund(self) -> bool:
        if self.status == PaymentStatus.COMPLETED:
            self.status = PaymentStatus.REFUNDED
            return True
        return False

    def __str__(self):
        return f"Payment #{self.payment_id} - ${self.amount:.2f} via {self.payment_method} ({self.status.value})"


class Delivery:
    def __init__(self, delivery_id: int, order: Order, address: str):
        self.delivery_id = delivery_id
        self.order = order
        self.address = address
        self.delivery_date: Optional[datetime] = None
        self.status = DeliveryStatus.PREPARING
        self.tracking_number = f"TC{delivery_id:06d}"
        order.delivery = self

    def update_status(self, status: DeliveryStatus):
        self.status = status
        if status == DeliveryStatus.DISPATCHED:
            self.order.update_status(OrderStatus.DISPATCHED)
        elif status == DeliveryStatus.DELIVERED:
            self.delivery_date = datetime.now()
            self.order.update_status(OrderStatus.DELIVERED)

    def track_delivery(self) -> str:
        return f"Tracking {self.tracking_number}: {self.status.value}"

    def __str__(self):
        return f"Delivery #{self.delivery_id} to {self.address} - {self.status.value}"


class ProductOrderNode:
    def __init__(self, product: Product, order_count: int = 0):
        self.product = product
        self.order_count = order_count
        self.next: Optional['ProductOrderNode'] = None

    def __str__(self):
        return f"{self.product.name}: {self.order_count} orders"


class ProductOrderLinkedList:
    def __init__(self):
        self.head: Optional[ProductOrderNode] = None

    def add_or_update_product(self, product: Product, quantity: int = 1):
        if not self.head:
            self.head = ProductOrderNode(product, quantity)
            return

        current = self.head
        while current:
            if current.product.product_id == product.product_id:
                current.order_count += quantity
                return
            if not current.next:
                current.next = ProductOrderNode(product, quantity)
                return
            current = current.next

    def get_product_order_count(self, product: Product) -> int:
        current = self.head
        while current:
            if current.product.product_id == product.product_id:
                return current.order_count
            current = current.next
        return 0

    def display_all(self):
        if not self.head:
            print("No products in order tracking list.")
            return

        print("\n=== Product Order Tracking (Linked List) ===")
        current = self.head
        while current:
            print(f"  * {current}")
            current = current.next

    def get_sorted_products_by_orders(self) -> List[ProductOrderNode]:
        products = []
        current = self.head
        while current:
            products.append(current)
            current = current.next
        return sorted(products, key=lambda x: x.order_count, reverse=True)


def create_sample_data():
    print("Creating Surf Store Sample Data...")

    surfboard_family = ProductFamily(1, "Surfboards", "High-quality surfboards for all skill levels")
    wetsuit_family = ProductFamily(2, "Wetsuits", "Premium wetsuits for all water conditions")
    accessories_family = ProductFamily(3, "Surf Accessories", "Essential accessories for surfers")
    apparel_family = ProductFamily(4, "Surf Apparel", "Stylish surf-inspired clothing")

    longboard_category = ProductCategory(1, "Longboards", "Classic longboards for cruising", surfboard_family)
    shortboard_category = ProductCategory(2, "Shortboards", "High-performance shortboards", surfboard_family)
    sup_category = ProductCategory(3, "SUP Boards", "Stand-up paddleboards", surfboard_family)

    fullsuit_category = ProductCategory(4, "Full Suits", "Full-body wetsuits", wetsuit_family)
    springsuit_category = ProductCategory(5, "Spring Suits", "Short-sleeve wetsuits", wetsuit_family)

    leash_category = ProductCategory(6, "Leashes", "Surfboard leashes", accessories_family)
    wax_category = ProductCategory(7, "Surf Wax", "High-quality surf wax", accessories_family)
    fins_category = ProductCategory(8, "Fins", "Surfboard fins", accessories_family)

    tshirt_category = ProductCategory(9, "T-Shirts", "Surf-themed t-shirts", apparel_family)
    boardshorts_category = ProductCategory(10, "Boardshorts", "High-performance boardshorts", apparel_family)

    products = [
        Product(1, "9'6\" Classic Longboard", "Perfect for beginners and cruising", 749.99, 5, longboard_category),
        Product(2, "8'6\" Performance Longboard", "High-performance longboard for experienced surfers", 1099.99, 3, longboard_category),
        Product(3, "6'2\" Performance Shortboard", "Competition-level shortboard", 629.99, 8, shortboard_category),
        Product(4, "5'10\" Grom Shortboard", "Perfect shortboard for younger surfers", 499.99, 6, shortboard_category),
        Product(5, "10'6\" All-Around SUP", "Versatile stand-up paddleboard", 899.99, 4, sup_category),
        Product(6, "4/3mm Full Wetsuit", "Premium neoprene full wetsuit", 249.99, 12, fullsuit_category),
        Product(7, "3/2mm Spring Suit", "Comfortable spring wetsuit", 159.99, 15, springsuit_category),
        Product(8, "Competition Leash 6ft", "Professional-grade surfboard leash", 34.99, 25, leash_category),
        Product(9, "Premium Surf Wax", "High-performance surf wax", 3.99, 100, wax_category),
        Product(10, "Thruster Fin Set", "High-quality thruster fins", 74.99, 20, fins_category),
        Product(11, "Tropical Surf Tee", "100% cotton surf-themed t-shirt", 19.99, 30, tshirt_category),
        Product(12, "Performance Boardshorts", "Quick-dry performance boardshorts", 64.99, 18, boardshorts_category),
    ]

    customers = [
        Customer(1, "Jake", "Morrison", "jake@email.com", "01234 567890", "123 Beach Road, Brighton, BN1 2AB"),
        Customer(2, "Sarah", "Chen", "sarah@email.com", "01234 567891", "456 Seafront, Bournemouth, BH2 5AA"),
        Customer(3, "Mike", "Rodriguez", "mike@email.com", "01234 567892", "789 Coastal Way, Newquay, TR7 1DB"),
        Customer(4, "Emma", "Johnson", "emma@email.com", "01234 567893", "321 Promenade, Croyde, EX33 1PA"),
        Customer(5, "Tom", "Williams", "tom@email.com", "01234 567894", "567 Coastal Drive, Polzeath, PL27 6ST"),
        Customer(6, "Lucy", "Davies", "lucy@email.com", "01234 567895", "89 Marine Parade, Saltburn, TS12 1HJ"),
        Customer(7, "Ben", "Taylor", "ben@email.com", "01234 567896", "45 Surf Street, Woolacombe, EX34 7BN"),
        Customer(8, "Amy", "Wilson", "amy@email.com", "01234 567897", "234 Bay View, Thurso, KW14 8XG"),
    ]

    return {
        'families': [surfboard_family, wetsuit_family, accessories_family, apparel_family],
        'products': products,
        'customers': customers
    }


def demonstrate_surf_store():
    print("=" * 60)
    print("          TOTAL CHAOS SURF STORE DEMONSTRATION")
    print("=" * 60)

    data = create_sample_data()
    products = data['products']
    customers = data['customers']

    order_tracker = ProductOrderLinkedList()

    print("\n=== PRODUCT FAMILIES AND CATEGORIES ===")
    for family in data['families']:
        print(f"\n{family}")
        for category in family.get_categories():
            print(f"  |-- {category}")
            for product in category.get_products():
                print(f"      |-- {product}")

    print("\n\n=== CUSTOMER INFORMATION ===")
    for customer in customers:
        print(f"  * {customer}")

    print("\n\n=== CREATING ORDERS ===")

    order1 = Order(1, customers[0])
    order1.add_order_detail(products[0], 1)  # Longboard
    order1.add_order_detail(products[5], 1)  # Wetsuit
    order1.add_order_detail(products[8], 2)  # Surf wax
    order_tracker.add_or_update_product(products[0], 1)
    order_tracker.add_or_update_product(products[5], 1)
    order_tracker.add_or_update_product(products[8], 2)

    order2 = Order(2, customers[1])
    order2.add_order_detail(products[2], 1)  # Shortboard
    order2.add_order_detail(products[7], 1)  # Leash
    order2.add_order_detail(products[9], 1)  # Fins
    order_tracker.add_or_update_product(products[2], 1)
    order_tracker.add_or_update_product(products[7], 1)
    order_tracker.add_or_update_product(products[9], 1)

    order3 = Order(3, customers[2])
    order3.add_order_detail(products[4], 1)  # SUP board
    order3.add_order_detail(products[10], 2) # T-shirts
    order3.add_order_detail(products[8], 3)  # More surf wax
    order_tracker.add_or_update_product(products[4], 1)
    order_tracker.add_or_update_product(products[10], 2)
    order_tracker.add_or_update_product(products[8], 3)

    order4 = Order(4, customers[3])
    order4.add_order_detail(products[1], 1)  # Performance longboard
    order4.add_order_detail(products[6], 1)  # Spring suit
    order4.add_order_detail(products[11], 1) # Boardshorts
    order_tracker.add_or_update_product(products[1], 1)
    order_tracker.add_or_update_product(products[6], 1)
    order_tracker.add_or_update_product(products[11], 1)

    orders = [order1, order2, order3, order4]

    for order in orders:
        print(f"\n{order}")
        for detail in order.order_details:
            print(f"  |-- {detail}")

    print("\n\n=== PAYMENT PROCESSING ===")
    payments = []
    for i, order in enumerate(orders, 1):
        payment_methods = ["Credit Card", "PayPal", "Apple Pay", "Debit Card"]
        payment = Payment(i, order, payment_methods[i-1])
        payments.append(payment)
        payment.process_payment()
        print(f"  * {payment}")

    print("\n\n=== DELIVERY SETUP ===")
    deliveries = []
    for i, order in enumerate(orders, 1):
        delivery = Delivery(i, order, order.customer.address)
        deliveries.append(delivery)
        print(f"  * {delivery}")
        print(f"    {delivery.track_delivery()}")

    print("\n\n=== ORDER STATUS UPDATES ===")
    for delivery in deliveries:
        delivery.update_status(DeliveryStatus.DISPATCHED)
        print(f"  * {delivery.order} - {delivery.track_delivery()}")

    deliveries[0].update_status(DeliveryStatus.DELIVERED)
    deliveries[1].update_status(DeliveryStatus.DELIVERED)
    print(f"\n  * First two orders delivered:")
    print(f"    - {deliveries[0].order}")
    print(f"    - {deliveries[1].order}")

    order_tracker.display_all()

    print("\n=== TOP ORDERED PRODUCTS ===")
    sorted_products = order_tracker.get_sorted_products_by_orders()
    for i, node in enumerate(sorted_products[:5], 1):
        print(f"  {i}. {node}")

    print("\n\n=== CUSTOMER ORDER HISTORY ===")
    for customer in customers:
        print(f"\n{customer}")
        orders = customer.get_order_history()
        if orders:
            for order in orders:
                print(f"  |-- Order #{order.order_id}: ${order.total_amount:.2f} ({order.status.value})")
        else:
            print("  |-- No orders")

    print("\n\n=== INVENTORY STATUS ===")
    print("Updated stock levels after orders:")
    for product in products:
        status = "LOW STOCK" if product.stock_quantity < 5 else "In Stock"
        print(f"  * {product.name}: {product.stock_quantity} units ({status})")

    print("\n" + "=" * 60)
    print("           DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_surf_store()