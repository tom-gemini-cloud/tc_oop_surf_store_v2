from .models import (Customer, ProductFamily, ProductCategory, SurfBoard, Wetsuit,
                    Accessory, ShoppingCart, Inventory)
from .orders import (Order, CreditCardPayment, PayPalPayment, ApplePayPayment,
                    StandardDelivery, ExpressDelivery, PickupDelivery)
from .enums import DeliveryStatus
from .data_structures import ProductOrderLinkedList


def create_sample_data():
    print("Creating Enhanced Surf Store Sample Data...")
    print("Demonstrating Inheritance, Polymorphism, and Containment!")

    # Product families and categories
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

    # Creating products using inheritance hierarchy (Polymorphism in action!)
    products = [
        # SurfBoards
        SurfBoard(1, "9'6\" Classic Longboard", "Perfect for beginners and cruising",
                 749.99, 5, longboard_category, "9'6\"", "longboard", "single fin"),
        SurfBoard(2, "8'6\" Performance Longboard", "High-performance longboard for experienced surfers",
                 1099.99, 3, longboard_category, "8'6\"", "longboard", "2+1 fin setup"),
        SurfBoard(3, "6'2\" Performance Shortboard", "Competition-level shortboard",
                 629.99, 8, shortboard_category, "6'2\"", "shortboard", "thruster"),
        SurfBoard(4, "5'10\" Grom Shortboard", "Perfect shortboard for younger surfers",
                 499.99, 6, shortboard_category, "5'10\"", "shortboard", "thruster"),
        SurfBoard(5, "10'6\" All-Around SUP", "Versatile stand-up paddleboard",
                 899.99, 4, sup_category, "10'6\"", "SUP", "center fin"),

        # Wetsuits
        Wetsuit(6, "4/3mm Full Wetsuit", "Premium neoprene full wetsuit",
               249.99, 12, fullsuit_category, "4/3mm", "full suit", "neoprene"),
        Wetsuit(7, "3/2mm Spring Suit", "Comfortable spring wetsuit",
               159.99, 15, springsuit_category, "3/2mm", "spring suit", "neoprene"),

        # Accessories
        Accessory(8, "Competition Leash 6ft", "Professional-grade surfboard leash",
                 34.99, 25, leash_category, "leash", "All surfboards"),
        Accessory(9, "Premium Surf Wax", "High-performance surf wax",
                 3.99, 100, wax_category, "wax", "All surfboards"),
        Accessory(10, "Thruster Fin Set", "High-quality thruster fins",
                 74.99, 20, fins_category, "fins", "Shortboards"),
        Accessory(11, "Tropical Surf Tee", "100% cotton surf-themed t-shirt",
                 19.99, 30, tshirt_category, "tshirt"),
        Accessory(12, "Performance Boardshorts", "Quick-dry performance boardshorts",
                 64.99, 18, boardshorts_category, "boardshorts"),
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

    # Create inventory (Containment example)
    inventory = Inventory()
    for product in products:
        inventory.add_product(product)

    return {
        'families': [surfboard_family, wetsuit_family, accessories_family, apparel_family],
        'products': products,
        'customers': customers,
        'inventory': inventory
    }


def demonstrate_oop_concepts():
    print("=" * 80)
    print("          ENHANCED SURF STORE - OOP CONCEPTS DEMONSTRATION")
    print("=" * 80)

    data = create_sample_data()
    products = data['products']
    customers = data['customers']
    inventory = data['inventory']

    print("\n[INHERITANCE DEMONSTRATION]")
    print("=" * 50)
    print("Different product types with specialized behavior:")
    for product in products[:7]:
        print(f"  * {product}")
        print(f"      Weight: {product.get_shipping_weight()}kg")
        print(f"      Care: {product.get_care_instructions()}")
        if hasattr(product, 'get_board_specs'):
            print(f"      Specs: {product.get_board_specs()}")
        elif hasattr(product, 'get_thermal_rating'):
            print(f"      Thermal: {product.get_thermal_rating()}")
        print()

    print("\n[POLYMORPHISM DEMONSTRATION]")
    print("=" * 50)

    # Create an order to demonstrate polymorphic payment processing
    order = Order(1, customers[0])
    order.add_order_detail(products[0], 1)  # Longboard
    order.add_order_detail(products[5], 1)  # Wetsuit
    order.add_order_detail(products[8], 2)  # Surf wax

    print(f"Order created: {order}")
    print("\nDifferent payment methods (Polymorphism):")

    # Demonstrate different payment methods
    payment_methods = [
        CreditCardPayment(1, order, "1234567812345678", "Visa"),
        PayPalPayment(2, order, "jake@email.com"),
        ApplePayPayment(3, order, "iPhone-12-Jake")
    ]

    for payment in payment_methods:
        print(f"  * {payment.get_processing_time()}: ${payment.get_total_amount():.2f}")
        print(f"      Fee: ${payment.get_transaction_fee():.2f}")
        print(f"      Method: {payment}")
        payment.process_payment()
        print()

    # Use the first payment method for the order
    order.payment = payment_methods[0]

    print("Different delivery options (Polymorphism):")
    delivery_options = [
        StandardDelivery(1, order, order.customer.address),
        ExpressDelivery(2, order, order.customer.address),
        PickupDelivery(3, order, "Brighton Surf Shop")
    ]

    for delivery in delivery_options:
        print(f"  * {delivery.get_delivery_method()}: ${delivery.calculate_shipping_cost():.2f}")
        print(f"      ETA: {delivery.get_estimated_delivery_days()} days")
        print(f"      Details: {delivery}")
        print()

    print("\n[CONTAINMENT DEMONSTRATION]")
    print("=" * 50)

    customer = customers[1]  # Sarah Chen
    cart = customer.shopping_cart  # Contained shopping cart

    print(f"Customer: {customer}")
    print(f"Shopping Cart: {cart}")

    # Add items to cart (demonstrating containment)
    cart.add_item(products[2], 1)  # Shortboard
    cart.add_item(products[6], 1)  # Spring suit
    cart.add_item(products[9], 1)  # Fins

    print(f"After adding items: {cart}")
    print(f"Cart weight: {cart.get_total_weight():.2f}kg")
    print(f"Cart items:")
    for item in cart.items:
        print(f"  - {item['quantity']}x {item['product'].name}")

    # Apply discount
    cart.apply_discount(0.1)  # 10% discount
    print(f"After 10% discount: ${cart.get_total():.2f}")
    print()

    print("Inventory Management (Containment):")
    print(f"Inventory: {inventory}")
    print(f"SurfBoards in inventory: {len(inventory.get_products_by_type(SurfBoard))}")
    print(f"Wetsuits in inventory: {len(inventory.get_products_by_type(Wetsuit))}")
    print(f"Accessories in inventory: {len(inventory.get_products_by_type(Accessory))}")

    low_stock = inventory.get_low_stock_products()
    if low_stock:
        print(f"WARNING: Low stock products: {len(low_stock)}")
        for product in low_stock:
            print(f"    - {product.name}: {product.stock_quantity} units")

    # Search functionality
    search_results = inventory.search_products("longboard")
    print(f"Search results for 'longboard': {len(search_results)} products")
    for product in search_results:
        print(f"    - {product.name}")

    print("\n[ADVANCED OOP FEATURES]")
    print("=" * 50)

    # Method overriding demonstration
    print("Method Overriding Examples:")
    for product in products[:5]:
        print(f"  {type(product).__name__}: {product}")  # Each class has its own __str__

    print("\n" + "=" * 80)
    print("           OOP CONCEPTS DEMONSTRATION COMPLETE!")
    print("[✓] Inheritance: Product → SurfBoard/Wetsuit/Accessory")
    print("[✓] Polymorphism: Payment methods, Delivery strategies")
    print("[✓] Encapsulation: Private data with public interfaces")
    print("[✓] Abstraction: Abstract base classes with concrete implementations")
    print("[✓] Containment: Customer contains ShoppingCart, Inventory contains Products")
    print("[✓] Composition: Order composed of OrderDetails")
    print("=" * 80)


def demonstrate_surf_store():
    """Legacy function for backward compatibility"""
    demonstrate_oop_concepts()