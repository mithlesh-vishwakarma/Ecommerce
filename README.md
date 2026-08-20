# ecommerce

"Full-stack e-commerce platform built with Django REST Framework and React, featuring JWT authentication, role-based access control, product catalog, inventory, cart, orders, payments, reviews, marketing, and admin management."

## Topics
`django` `django-rest-framework` `react` `python` `javascript` `ecommerce` `rest-api` `jwt` `rbac` `postgresql` `full-stack`

---

## Project Overview
**ecommerce** is a modern, full-stack enterprise e-commerce platform built with Django REST Framework (backend) and React (frontend). The architecture uses Django's native Group and Permission systems for robust Role-Based Access Control (RBAC), Simple JWT for stateless authentication, and clean DRF ViewSets with API versioning (`/api/v1/`).

---

## Tech Stack

### Backend
- **Language:** Python
- **Framework:** Django 5.x
- **API Framework:** Django REST Framework (DRF)
- **Authentication:** Simple JWT (JSON Web Tokens with token blacklisting)
- **Database:** PostgreSQL (Development / Production ready)
- **ORM:** Django ORM

### Frontend
- **Framework:** React
- **Language:** JavaScript / TypeScript
- **Routing:** React Router
- **HTTP Client:** Axios

---

## Project Structure
```
ecommerce/
├── backend/
│   ├── config/              # Core Django project settings & URLs
│   ├── apps/
│   │   ├── accounts/        # Custom User, Auth, Profiles, Addresses, RBAC permissions
│   │   ├── catalog/         # Categories, Brands, Attributes, Products, Variants
│   │   ├── inventory/       # Stock tracking & warehouse management (Planned)
│   │   ├── cart/            # Shopping cart management (Planned)
│   │   ├── orders/          # Order processing & lifecycle (Planned)
│   │   ├── payments/        # Payment gateway integrations (Planned)
│   │   ├── reviews/         # Product ratings & reviews (Planned)
│   │   └── marketing/       # Coupons, discounts, banners (Planned)
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                # React Application (Planned)
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## Features

### Implemented Features `[x]`
- [x] Custom User model with email authentication
- [x] JWT Authentication (Login, Refresh, Logout with Token Blacklist)
- [x] User Profile & Address CRUD APIs
- [x] Role-Based Access Control (Django Groups & Permissions)
- [x] Staff Role Assignment APIs (Super Admin, Product Manager, Order Manager, Inventory Manager, Marketing Manager, Customer Support)
- [x] Django Admin Configuration for Models
- [x] Catalog - Category Management API (CRUD with auto-generated slugs)
- [x] Catalog - Brand Management API (CRUD with logo support & auto-generated slugs)

### Planned Features `[ ]`
- [ ] Catalog - Attribute & Attribute Value APIs
- [ ] Catalog - Product, Image & Variant APIs
- [ ] Inventory Management API
- [ ] Cart & Wishlist APIs
- [ ] Order Processing & Checkout APIs
- [ ] Payment Gateway Integration
- [ ] Product Reviews & Ratings API
- [ ] Marketing & Promotions API
- [ ] Advanced Product Search, Filtering, Sorting & Pagination
- [ ] React Frontend Web Application

---

## Architecture Diagram
```
                     +---------------------------------------+
                     |           Client / Postman            |
                     +---------------------------------------+
                                         |
                                         | HTTP / REST (/api/v1/)
                                         v
                     +---------------------------------------+
                     |         Django REST Framework         |
                     +---------------------------------------+
                                         |
           +-----------------------------+-----------------------------+
           |                             |                             |
           v                             v                             v
+--------------------+        +--------------------+        +--------------------+
|  Simple JWT Auth   |        | DRF ViewSets / APIs|        | HasModelPermission |
| (Login/Refresh/    |        | (Categories,       |        | (Django Groups &   |
|  Blacklist)        |        |  Brands, Users)    |        |  Permissions)      |
+--------------------+        +--------------------+        +--------------------+
                                         |
                                         v
                              +--------------------+
                              |     Django ORM     |
                              +--------------------+
                                         |
                                         v
                              +--------------------+
                              |  PostgreSQL / DB   |
                              +--------------------+
```

---

## Authentication & Authorization / RBAC

### Security Architecture
- Frontend visibility is **never** relied upon for security; authorization is enforced on the Django backend for every protected endpoint.
- Uses Django's built-in **Groups and Permissions** system.

```
User -> Django Group -> Django Permissions -> DRF Permission Classes -> API Access
```

### Roles & Responsibilities
- **Super Admin:** Full access across all applications and role management.
- **Product Manager:** Permissions for managing Product Catalog (`categories`, `brands`, `products`, `attributes`).
- **Order Manager:** Permissions for managing orders and shipping.
- **Inventory Manager:** Permissions for managing stock and warehouses.
- **Marketing Manager:** Permissions for managing promotions and discounts.
- **Customer Support:** Permissions for viewing customer profiles, orders, and reviews.

---

## Module Specifications

### Authentication
- `POST /api/v1/accounts/register/` - User registration
- `POST /api/v1/accounts/login/` - Obtain JWT access & refresh tokens
- `POST /api/v1/accounts/token/refresh/` - Refresh access token
- `POST /api/v1/accounts/logout/` - Blacklist refresh token
- `GET/PUT/PATCH /api/v1/accounts/profile/` - Manage profile
- `POST /api/v1/accounts/change-password/` - Change user password
- `/api/v1/accounts/addresses/` - Address CRUD

### Admin & User Management
- `/api/v1/accounts/admin/users/` - Admin user list & details
- `POST /api/v1/accounts/admin/users/{id}/assign-role/` - Assign user roles

### Product Catalog
- **Categories:** `/api/v1/catalog/categories/`
- **Brands:** `/api/v1/catalog/brands/`
  - Public users: Read-only access (`list`, `retrieve`)
  - Authenticated users with permissions (`catalog.add_brand`, `catalog.change_brand`, `catalog.delete_brand`): Full modification access

---

## API Testing with Postman

### Category Endpoints
```http
GET    /api/v1/catalog/categories/
POST   /api/v1/catalog/categories/
GET    /api/v1/catalog/categories/{id}/
PUT    /api/v1/catalog/categories/{id}/
PATCH  /api/v1/catalog/categories/{id}/
DELETE /api/v1/catalog/categories/{id}/
```

### Brand Endpoints
```http
GET    /api/v1/catalog/brands/
POST   /api/v1/catalog/brands/
GET    /api/v1/catalog/brands/{id}/
PUT    /api/v1/catalog/brands/{id}/
PATCH  /api/v1/catalog/brands/{id}/
DELETE /api/v1/catalog/brands/{id}/
```

#### Example: Create Brand
```http
POST /api/v1/catalog/brands/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Nike",
  "description": "Just Do It. Premium athletic footwear and apparel.",
  "is_active": true
}
```

---

## Backend Setup

1. **Clone Repository:**
   ```bash
   git clone https://github.com/mithlesh-vishwakarma/Ecommerce.git
   cd Ecommerce/backend
   ```

2. **Virtual Environment & Dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Copy `.env.example` to `.env` and update values.
   ```bash
   cp .env.example .env
   ```

4. **Migrations & Superuser:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Server:**
   ```bash
   python manage.py runserver
   ```

---

## Frontend Setup
*(Planned - React Application)*

---

## Development Roadmap

### Backend Roadmap
- [x] Django project setup
- [x] Django REST Framework setup
- [x] Custom User model
- [x] JWT authentication (Register, Login, Refresh, Logout)
- [x] Profile & Address APIs
- [x] Role-based access control (RBAC & DRF Permissions)
- [x] Django Admin configuration
- [x] Catalog - Category API
- [x] Catalog - Brand API
- [ ] Catalog - Attribute API
- [ ] Catalog - Attribute Value API
- [ ] Catalog - Product API
- [ ] Catalog - Product Image API
- [ ] Catalog - Product Variant API
- [ ] Inventory API
- [ ] Cart API
- [ ] Wishlist API
- [ ] Order API
- [ ] Payment API
- [ ] Review API
- [ ] Marketing API
- [ ] Search, Filtering, Sorting & Pagination
- [ ] Swagger / OpenAPI Documentation
- [ ] Automated Unit & Integration Tests

### Frontend Roadmap
- [ ] React project setup
- [ ] Authentication UI
- [ ] Product listing & detail pages
- [ ] Cart & Wishlist interfaces
- [ ] Checkout flow & order history
- [ ] Admin Dashboard

---

## Security Notes
- Every sensitive API checks Django permissions on the backend.
- Passwords are hashed using PBKDF2 with SHA256.
- JWT refresh tokens are blacklisted upon logout.
- `.env` file is untracked; credentials must remain in environment variables.

---

## Project Status
Active Development (Catalog module in progress).

---

## Author Information
Developed by Mithlesh Vishwakarma.

---

## License
MIT License.
