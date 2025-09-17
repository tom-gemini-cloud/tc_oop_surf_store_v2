# Surf Store E-commerce Class Diagram Specification

## Class Overview and Relationships

### Core Classes:

1. **Customer**
   - Attributes: customer_id, first_name, last_name, email, phone, address
   - Methods: get_full_name(), update_contact_info(), get_order_history()

2. **ProductFamily**
   - Attributes: family_id, name, description
   - Methods: add_category(), get_categories(), get_all_products()
   - Example: "Surfboards", "Wetsuits", "Accessories"

3. **ProductCategory**
   - Attributes: category_id, name, description, family_id
   - Methods: add_product(), get_products()
   - Example: "Longboards", "Shortboards" (under Surfboards family)

4. **Product**
   - Attributes: product_id, name, description, price, stock_quantity, category_id
   - Methods: update_stock(), is_available(), get_category(), get_family()

5. **Order**
   - Attributes: order_id, customer_id, order_date, total_amount, status
   - Methods: add_order_detail(), calculate_total(), update_status()

6. **OrderDetail**
   - Attributes: detail_id, order_id, product_id, quantity, unit_price, subtotal
   - Methods: calculate_subtotal()

7. **Payment**
   - Attributes: payment_id, order_id, amount, payment_method, payment_date, status
   - Methods: process_payment(), refund()

8. **Delivery**
   - Attributes: delivery_id, order_id, address, delivery_date, status, tracking_number
   - Methods: update_status(), track_delivery()

9. **ProductOrderNode** (for linked list)
   - Attributes: product, order_count, next
   - Methods: For linked list implementation

## Relationships:

- Customer (1) → (M) Order
- Order (1) → (M) OrderDetail
- Order (1) → (1) Payment
- Order (1) → (1) Delivery
- Product (1) → (M) OrderDetail
- ProductCategory (1) → (M) Product
- ProductFamily (1) → (M) ProductCategory

## Surf Store Specific Examples:

### Product Families:
- Surfboards (Longboards, Shortboards, SUP boards)
- Wetsuits (Full suits, Spring suits, Accessories)
- Surf Accessories (Leashes, Wax, Fins)
- Apparel (T-shirts, Boardshorts, Rashguards)

### Sample Products:
- 9'6" Classic Longboard
- 6'2" Performance Shortboard
- 4/3mm Full Wetsuit
- Premium Surf Wax
- Competition Leash