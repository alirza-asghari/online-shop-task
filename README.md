# Online Shop API with FastAPI, Celery, Redis, and PostgreSQL

## Overview

This project is an online shop API built using FastAPI. It supports user registration with email verification, product management, shopping cart functionality, order history, and a simulated payment process. The application uses FastAPI for web framework, PostgreSQL for database, Celery with Redis for asynchronous tasks, Alembic for database migrations and Redis for caching.

## Features

- User registration with email verification
- Product management: create, update, delete, and list products
- Shopping cart: add products, view cart, remove items, checkout, and view order history
- JWT-based authentication
- Asynchronous email sending via Celery and Redis
- Database migrations using Alembic
- Caching using Redis


## Getting Started

### Clone the Repository

```bash
git clone https://github.com/alirza-asghari/online-shop-task.git
cd online-shop-task
```

### Set Up Environment Variables

Create a `.env` file with the following:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=database
DATABASE_URL=postgresql://user:password@db:5432/database
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SENDER_EMAIL=your email
EMAIL_PASSWORD=your password
```

### Build and Start Services

Run the following:

```bash
docker-compose up --build
```

### Apply Database Migrations

Run Alembic migrations to set up the database schema:

```bash
docker-compose exec web alembic upgrade head
```

### Access the API

Open [http://localhost:9000/docs](http://localhost:9000/docs) to explore and interact with the API.

## Project Structure

```
.
├── app
│   ├── config.py
│   ├── controllers
│   ├── main.py
│   ├── models
│   ├── routes
│   ├── schemas
│   ├── utils
│   └── tasks
├── alembic/
├── database/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Usage

### User Management

- **Sign Up**: Register a new user. A verification email is sent asynchronously.
- **Log In**: Obtain a JWT token for authenticated requests.

### Product Management

- **Endpoints**: `/products/` for creating, updating, deleting, and listing products.

### Shopping Cart and Orders

- **Add to Cart**: `POST /cart/add/`
- **View Cart**: `GET /cart/`
- **Remove Item**: `DELETE /cart/remove/{product_id}/`
- **Checkout**: `POST /cart/checkout/`
- **Order History**: `GET /cart/history/`

## Database Migrations

1. Create a new migration:
   ```bash
   docker-compose exec web alembic revision --autogenerate -m "Description"
   ```
2. Apply migrations:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

## Troubleshooting

- **Database Issues**: Check `.env` for PostgreSQL configuration.
- **Email Issues**: Verify SMTP settings in `task.email.py`.

## License

This project is licensed under the my made up coffee License.