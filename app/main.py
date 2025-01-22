from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes.user_endpoints import UserEndpoint
from app.routes.product_endpoint import ProductEndpoint
from app.routes.order_endpoint import CartEndpoint

app = FastAPI(
    title="Online shop task API",
    description="An API for simulating an online shop with specific features.",
    version="1.0.0",
)

app.include_router(UserEndpoint())
app.include_router(ProductEndpoint())
app.include_router(CartEndpoint())


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Define the security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply the security globally
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

# Assign the custom_openapi function to app.openapi
app.openapi = custom_openapi #type: ignore