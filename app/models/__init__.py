from .users import User
from .orders import Order
from .products import Product
from database.database_connection import Base, engine

Base.metadata.create_all(bind=engine)