# TC Surf Store - FastAPI + HTMX E-commerce Application

A modern, reactive surf store e-commerce application built with FastAPI backend and HTMX for dynamic frontend interactions.

## Features

🏄‍♂️ **Modern Surf Store Experience**
- Product catalog with categories (Surfboards, Wetsuits, Accessories, Apparel)
- Real-time shopping basket with HTMX
- Smooth checkout process
- Order confirmation and tracking
- Admin dashboard for inventory management

🚀 **Technical Highlights**
- **FastAPI** backend with Python 3.11+
- **HTMX** for reactive frontend without JavaScript frameworks
- **Tailwind CSS** for modern, responsive design
- **Object-oriented design** with proper relationships
- **Real-time updates** and smooth UX

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Application
- **Store**: http://localhost:8000
- **Products**: http://localhost:8000/products
- **Basket**: http://localhost:8000/cart
- **Admin**: http://localhost:8000/admin

## Project Structure

```
tc_oop_surf_store_v2/
├── app.py                      # FastAPI application
├── surf_store.py              # OOP models and data
├── requirements.txt           # Python dependencies
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with HTMX
│   ├── index.html            # Homepage
│   ├── products.html         # Product catalog
│   ├── cart.html             # Shopping basket
│   ├── checkout.html         # Checkout form
│   ├── order_confirmation.html # Order success
│   └── admin.html            # Admin dashboard
├── static/
│   └── css/
│       └── style.css         # Custom styles
└── README.md
```

## Key Components

### Backend (FastAPI)
- **Product Management**: Categories, families, inventory
- **Shopping Basket**: Session-based basket management
- **Order Processing**: Customer creation, payment, delivery
- **Admin Interface**: Stock management, order tracking

### Frontend (HTMX + Tailwind)
- **Reactive UI**: Add to basket, update quantities without page refresh
- **Responsive Design**: Mobile-first approach
- **Modern Animations**: Smooth transitions and loading states
- **Real-time Updates**: Basket counter, inventory status

### OOP Models
- **Customer**: Contact info, order history
- **Product Hierarchy**: Family → Category → Product
- **Order System**: Orders, order details, payments, delivery
- **Linked List**: Product order tracking implementation

## Features Demo

### 🛍️ Shopping Experience
1. Browse products by category
2. Add items to basket with real-time updates
3. Adjust quantities dynamically
4. Secure checkout process
5. Order confirmation with tracking

### 🔧 Admin Features
1. Inventory management
2. Stock level monitoring
3. Order tracking
4. Revenue dashboard
5. Low stock alerts

### 📱 Responsive Design
- Mobile-optimized interface
- Touch-friendly interactions
- Fast loading times
- Progressive enhancement

## HTMX Features Used

- `hx-post`: Dynamic form submissions
- `hx-target`: Targeted content updates
- `hx-swap`: Content replacement strategies
- `hx-indicator`: Loading states
- `hx-confirm`: User confirmations
- Event listeners for basket updates

## Sample Data

The application includes rich sample data:
- **4 Product Families**: Surfboards, Wetsuits, Accessories, Apparel
- **10+ Categories**: Longboards, Shortboards, Full suits, etc.
- **12 Products**: Complete surf gear catalog
- **4 Sample Customers**: For testing orders

## Development

### Adding New Products
Edit the `create_sample_data()` function in `surf_store.py` to add new products, categories, or families.

### Customizing Styles
Modify `static/css/style.css` or adjust Tailwind classes in templates.

### Extending Features
- Add user authentication
- Implement payment processing
- Add product images
- Create customer accounts
- Add product reviews

## Dependencies

- **fastapi**: Modern web framework
- **uvicorn**: ASGI server
- **jinja2**: Template engine
- **python-multipart**: Form handling
- **pydantic**: Data validation

## License

Educational project - feel free to use and modify!

---

**TC Surf Store** - Where Total Chaos meets perfect waves! 🏄‍♂️🌊