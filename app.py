from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import uvicorn
from surf_store import *
from datetime import datetime

app = FastAPI(title="TC Surf Store", description="Total Chaos Surf Store - Premium Surf Gear")

templates = Jinja2Templates(directory="templates")
templates.env.globals["min"] = min

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    pass

store_data = create_sample_data()
products = store_data['products']
customers = store_data['customers']
families = store_data['families']

basket_items = {}
orders_db = []
next_order_id = 1
next_customer_id = len(customers) + 1

def get_product_by_id(product_id: int):
    for product in products:
        if product.product_id == product_id:
            return product
    return None

def get_customer_by_id(customer_id: int):
    for customer in customers:
        if customer.customer_id == customer_id:
            return customer
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "families": families,
        "featured_products": products[:6]
    })

@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request, family_id: Optional[int] = None, category_id: Optional[int] = None):
    filtered_products = products

    if family_id:
        family = next((f for f in families if f.family_id == family_id), None)
        if family:
            filtered_products = family.get_all_products()

    if category_id:
        filtered_products = [p for p in filtered_products if p.category.category_id == category_id]

    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": filtered_products,
        "families": families,
        "selected_family_id": family_id,
        "selected_category_id": category_id
    })

@app.post("/cart/add")
async def add_to_basket(product_id: int = Form(...), quantity: int = Form(1)):
    product = get_product_by_id(product_id)
    if not product or not product.is_available(quantity):
        raise HTTPException(status_code=400, detail="Product not available")

    if product_id in basket_items:
        basket_items[product_id] += quantity
    else:
        basket_items[product_id] = quantity

    total_items = sum(basket_items.values())
    return {"success": True, "cart_count": total_items}

@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    basket_products = []
    total = 0

    for product_id, quantity in basket_items.items():
        product = get_product_by_id(product_id)
        if product:
            subtotal = product.price * quantity
            basket_products.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": basket_products,
        "total": total
    })

@app.post("/cart/update")
async def update_basket(product_id: int = Form(...), quantity: int = Form(...)):
    if quantity <= 0:
        basket_items.pop(product_id, None)
    else:
        product = get_product_by_id(product_id)
        if product and product.is_available(quantity):
            basket_items[product_id] = quantity
        else:
            raise HTTPException(status_code=400, detail="Insufficient stock")

    return RedirectResponse(url="/cart", status_code=303)

@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    if not basket_items:
        return RedirectResponse(url="/cart", status_code=303)

    basket_products = []
    total = 0

    for product_id, quantity in basket_items.items():
        product = get_product_by_id(product_id)
        if product:
            subtotal = product.price * quantity
            basket_products.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal

    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "cart_items": basket_products,
        "total": total
    })

@app.post("/checkout/process")
async def process_checkout(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    payment_method: str = Form(...)
):
    global next_order_id, next_customer_id

    if not basket_items:
        raise HTTPException(status_code=400, detail="Basket is empty")

    customer = Customer(next_customer_id, first_name, last_name, email, phone, address)
    customers.append(customer)
    next_customer_id += 1

    order = Order(next_order_id, customer)

    for product_id, quantity in basket_items.items():
        product = get_product_by_id(product_id)
        if product and product.is_available(quantity):
            order.add_order_detail(product, quantity)

    payment = Payment(next_order_id, order, payment_method)
    payment.process_payment()

    delivery = Delivery(next_order_id, order, address)

    orders_db.append(order)
    next_order_id += 1

    basket_items.clear()

    return templates.TemplateResponse("order_confirmation.html", {
        "request": request,
        "order": order,
        "payment": payment,
        "delivery": delivery
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "products": products,
        "orders": orders_db,
        "families": families
    })

@app.post("/admin/product/update")
async def update_product_stock(product_id: int = Form(...), stock: int = Form(...)):
    product = get_product_by_id(product_id)
    if product:
        product.stock_quantity = stock
        return {"success": True}
    raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)