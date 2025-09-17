from typing import Optional, List
from .models import Product


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