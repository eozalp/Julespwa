from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()
router = APIRouter()

# Placeholder for a database connection
# In a real app, this would connect to CouchDB/PouchDB
DB: Dict[str, Any] = {}

# --- Pydantic Models (from json_schemas.md) ---

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    cost: Optional[float] = None
    taxable: Optional[bool] = False
    pictures: Optional[List[str]] = []
    categoryId: Optional[str] = None
    supplierId: Optional[str] = None
    stock: int

class StockEntry(BaseModel):
    productId: str
    type: str  # "intake", "adjustment", "return"
    quantity: int
    notes: Optional[str] = None
    userId: str

class Sale(BaseModel):
    items: List[Dict[str, Any]]
    subtotal: float
    tax: float
    total: float
    paymentMethod: str
    userId: str

# --- API Endpoints ---

@router.get("/products", response_model=List[Product])
async def get_products():
    return list(DB.get("products", {}).values())

@router.post("/products", status_code=201, response_model=Product)
async def create_product(product: Product):
    product_id = f"product:{product.sku}"
    if "products" not in DB:
        DB["products"] = {}
    DB["products"][product_id] = product.dict()
    return product

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    if "products" in DB and product_id in DB["products"]:
        return DB["products"][product_id]
    raise HTTPException(status_code=404, detail="Product not found")

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    if "products" not in DB or product_id not in DB["products"]:
        raise HTTPException(status_code=404, detail="Product not found")
    DB["products"][product_id] = product.dict()
    return product

@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: str):
    if "products" in DB and product_id in DB["products"]:
        del DB["products"][product_id]
        return
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/stock-entries", status_code=201, response_model=StockEntry)
async def create_stock_entry(entry: StockEntry):
    # In a real app, update product stock based on this entry
    return entry

@router.post("/sales", status_code=201, response_model=Sale)
async def create_sale(sale: Sale):
    # In a real app, decrease product stock based on this sale
    return sale

# Placeholder for the CouchDB/PouchDB sync endpoint
@router.post("/db/_bulk_docs")
async def bulk_docs(payload: Dict[str, List[Dict[str, Any]]]):
    # This is a very simplified mock of the _bulk_docs endpoint.
    docs = payload.get("docs", [])
    results = []
    for doc in docs:
        doc_id = doc.get("_id")
        results.append({"id": doc_id, "ok": True, "rev": "1-mock-rev"})
    return results


app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "POS Backend is running"}
