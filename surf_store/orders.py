from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod
from .enums import OrderStatus, PaymentStatus, DeliveryStatus
from .models import Customer, Product


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


class Payment(ABC):
    def __init__(self, payment_id: int, order: Order):
        self.payment_id = payment_id
        self.order = order
        self.amount = order.total_amount
        self.payment_date = datetime.now()
        self.status = PaymentStatus.PENDING
        order.payment = self

    @abstractmethod
    def process_payment(self) -> bool:
        pass

    @abstractmethod
    def get_transaction_fee(self) -> float:
        pass

    @abstractmethod
    def get_processing_time(self) -> str:
        pass

    def refund(self) -> bool:
        if self.status == PaymentStatus.COMPLETED:
            self.status = PaymentStatus.REFUNDED
            return True
        return False

    def get_total_amount(self) -> float:
        return self.amount + self.get_transaction_fee()

    def __str__(self):
        return f"Payment #{self.payment_id} - ${self.get_total_amount():.2f} ({self.status.value})"


class CreditCardPayment(Payment):
    def __init__(self, payment_id: int, order: Order, card_number: str, card_type: str = "Visa"):
        super().__init__(payment_id, order)
        self.card_number = f"****-****-****-{card_number[-4:]}"
        self.card_type = card_type

    def process_payment(self) -> bool:
        try:
            # Simulate credit card processing
            if self.amount > 0:
                self.status = PaymentStatus.COMPLETED
                self.order.update_status(OrderStatus.CONFIRMED)
                return True
            return False
        except Exception:
            self.status = PaymentStatus.FAILED
            return False

    def get_transaction_fee(self) -> float:
        return self.amount * 0.029  # 2.9% fee

    def get_processing_time(self) -> str:
        return "Instant"

    def __str__(self):
        return f"Credit Card Payment #{self.payment_id} - {self.card_type} {self.card_number} - ${self.get_total_amount():.2f} ({self.status.value})"


class PayPalPayment(Payment):
    def __init__(self, payment_id: int, order: Order, email: str):
        super().__init__(payment_id, order)
        self.email = email

    def process_payment(self) -> bool:
        try:
            # Simulate PayPal processing
            if self.amount > 0 and "@" in self.email:
                self.status = PaymentStatus.COMPLETED
                self.order.update_status(OrderStatus.CONFIRMED)
                return True
            return False
        except Exception:
            self.status = PaymentStatus.FAILED
            return False

    def get_transaction_fee(self) -> float:
        return self.amount * 0.034 + 0.30  # 3.4% + $0.30

    def get_processing_time(self) -> str:
        return "1-2 business days"

    def __str__(self):
        return f"PayPal Payment #{self.payment_id} - {self.email} - ${self.get_total_amount():.2f} ({self.status.value})"


class ApplePayPayment(Payment):
    def __init__(self, payment_id: int, order: Order, device_id: str):
        super().__init__(payment_id, order)
        self.device_id = device_id

    def process_payment(self) -> bool:
        try:
            # Simulate Apple Pay processing
            if self.amount > 0:
                self.status = PaymentStatus.COMPLETED
                self.order.update_status(OrderStatus.CONFIRMED)
                return True
            return False
        except Exception:
            self.status = PaymentStatus.FAILED
            return False

    def get_transaction_fee(self) -> float:
        return 0.0  # No additional fee for Apple Pay

    def get_processing_time(self) -> str:
        return "Instant"

    def __str__(self):
        return f"Apple Pay Payment #{self.payment_id} - Device: {self.device_id} - ${self.get_total_amount():.2f} ({self.status.value})"


class Delivery(ABC):
    def __init__(self, delivery_id: int, order: Order, address: str):
        self.delivery_id = delivery_id
        self.order = order
        self.address = address
        self.delivery_date: Optional[datetime] = None
        self.status = DeliveryStatus.PREPARING
        self.tracking_number = f"TC{delivery_id:06d}"
        order.delivery = self

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

    @abstractmethod
    def get_estimated_delivery_days(self) -> int:
        pass

    @abstractmethod
    def get_delivery_method(self) -> str:
        pass

    def update_status(self, status: DeliveryStatus):
        self.status = status
        if status == DeliveryStatus.DISPATCHED:
            self.order.update_status(OrderStatus.DISPATCHED)
        elif status == DeliveryStatus.DELIVERED:
            self.delivery_date = datetime.now()
            self.order.update_status(OrderStatus.DELIVERED)

    def track_delivery(self) -> str:
        return f"Tracking {self.tracking_number}: {self.status.value}"

    def get_total_weight(self) -> float:
        return sum(detail.product.get_shipping_weight() * detail.quantity
                  for detail in self.order.order_details)

    def __str__(self):
        return f"{self.get_delivery_method()} #{self.delivery_id} to {self.address} - {self.status.value}"


class StandardDelivery(Delivery):
    def __init__(self, delivery_id: int, order: Order, address: str):
        super().__init__(delivery_id, order, address)
        self.tracking_number = f"STD{delivery_id:06d}"

    def calculate_shipping_cost(self) -> float:
        weight = self.get_total_weight()
        base_cost = 5.99
        if weight > 5.0:
            return base_cost + (weight - 5.0) * 2.0
        return base_cost

    def get_estimated_delivery_days(self) -> int:
        return 5

    def get_delivery_method(self) -> str:
        return "Standard Delivery"


class ExpressDelivery(Delivery):
    def __init__(self, delivery_id: int, order: Order, address: str):
        super().__init__(delivery_id, order, address)
        self.tracking_number = f"EXP{delivery_id:06d}"

    def calculate_shipping_cost(self) -> float:
        weight = self.get_total_weight()
        base_cost = 15.99
        if weight > 3.0:
            return base_cost + (weight - 3.0) * 3.0
        return base_cost

    def get_estimated_delivery_days(self) -> int:
        return 2

    def get_delivery_method(self) -> str:
        return "Express Delivery"


class PickupDelivery(Delivery):
    def __init__(self, delivery_id: int, order: Order, pickup_location: str):
        super().__init__(delivery_id, order, pickup_location)
        self.tracking_number = f"PU{delivery_id:06d}"
        self.pickup_location = pickup_location

    def calculate_shipping_cost(self) -> float:
        return 0.0  # Free pickup

    def get_estimated_delivery_days(self) -> int:
        return 1

    def get_delivery_method(self) -> str:
        return "Store Pickup"

    def __str__(self):
        return f"Store Pickup #{self.delivery_id} at {self.pickup_location} - {self.status.value}"