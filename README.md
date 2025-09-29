# Django Stripe Shop (Dockerized)

A simple Django shop with 3 products, Stripe test payments, and PostgreSQL, fully dockerized.

## Features

- Multi-product selection
- Stripe (test mode) payment
- Orders recorded and displayed on the home page
- Bootstrap frontend
- Docker + Docker Compose for easy setup

## Requirements

- Docker
- Docker Compose

## Quick Start

1. **Clone the repo**

```bash
git clone <repo_url>
cd django_stripe
```

2. **Build and start containers**

```bash
docker-compose up --build -d
```

3. **Apply migrations**

```bash
docker-compose exec web python manage.py migrate
```

4. **Create initial products**

```bash
docker-compose exec web python init_products.py
```

> Required if this is a new container or after flushing the database.

5. **Create superuser for admin panel (if needed)**

```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the app**

- Django shop: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin` (use superuser credentials)

## Notes

- Stripe is in **test mode**, use test cards like `4242 4242 4242 4242`.
- Orders and products are persisted in the PostgreSQL container.
- For development, code changes auto-reflect due to volume mapping.
