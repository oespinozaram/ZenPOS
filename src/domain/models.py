from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# --- CLIENTES ---
class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: Optional[str] = None
    phone: Optional[str] = None
    rfc: Optional[str] = Field(default=None, index=True) 
    
    sales: List["Sale"] = Relationship(back_populates="client")

# --- PRODUCTOS (¡Asegúrate de tener la relación sale_items aquí!) ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    stock: int
    barcode: str = Field(unique=True)
    
    # ESTA ES LA LÍNEA QUE TE FALTA:
    sale_items: List["SaleDetail"] = Relationship(back_populates="product")

# --- VENTAS ---
class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    total: float = 0.0
    
    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    client: Optional[Client] = Relationship(back_populates="sales")
    
    items: List["SaleDetail"] = Relationship(back_populates="sale")

# --- DETALLE DE VENTA ---
class SaleDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    sale_id: int = Field(foreign_key="sale.id")
    product_id: int = Field(foreign_key="product.id")
    
    quantity: int
    unit_price: float
    subtotal: float
    
    sale: Sale = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="sale_items")