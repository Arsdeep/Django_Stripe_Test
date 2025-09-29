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

````

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

5. **Create superuser for admin panel (if needed)**

> Required if this is a new container or after flushing the database.

```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the app**

- Django shop: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin` (use superuser credentials)

## Environment Variables

Set the following in `docker-compose.yml`:

- `STRIPE_PUBLIC_KEY` — your Stripe test public key
- `STRIPE_SECRET_KEY` — your Stripe test secret key
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — database credentials

## Reset Database

- To clear all data and reset sequences:

```bash
docker-compose exec web python manage.py flush
```

- Or remove PostgreSQL volume and start fresh:

```bash
docker-compose down
docker volume rm django_stripe_postgres_data
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python init_products.py
```

## Notes

- Stripe is in **test mode**, use test cards like `4242 4242 4242 4242`.
- Orders and products are persisted in the PostgreSQL container.
- For development, code changes auto-reflect due to volume mapping.
````
