from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()
router = APIRouter()

# Placeholder for a database connection
# In a real app, this would connect to CouchDB/PouchDB
DB: Dict[str, Any] = {}

# --- Pydantic Models (from json_schemas.md) ---

class Product(BaseModel):
    name: str
    price: float
    stock: int

class Sale(BaseModel):
    items: List[Dict[str, Any]]
    total: float
    userId: str

# --- API Endpoints ---

@router.get("/products")
async def get_products():
    return list(DB.get("products", {}).values())

@router.post("/products", status_code=201)
async def create_product(product: Product):
    # In a real app, generate a proper ID
    product_id = f"product:{product.name.lower().replace(' ', '-')}"
    if "products" not in DB:
        DB["products"] = {}
    DB["products"][product_id] = product.dict()
    return {"id": product_id, **product.dict()}

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    if "products" in DB and product_id in DB["products"]:
        return DB["products"][product_id]
    raise HTTPException(status_code=404, detail="Product not found")

@router.put("/products/{product_id}")
async def update_product(product_id: str, product: Product):
    if "products" not in DB or product_id not in DB["products"]:
        raise HTTPException(status_code=404, detail="Product not found")
    DB["products"][product_id] = product.dict()
    return {"id": product_id, **product.dict()}

@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: str):
    if "products" in DB and product_id in DB["products"]:
        del DB["products"][product_id]
        return
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/sales", status_code=201)
async def create_sale(sale: Sale):
    # In a real app, generate a proper ID
    sale_id = f"sale:{len(DB.get('sales', [])) + 1}"
    if "sales" not in DB:
        DB["sales"] = []
    DB["sales"].append({"id": sale_id, **sale.dict()})
    return {"id": sale_id, **sale.dict()}

# Placeholder for the CouchDB/PouchDB sync endpoint
@router.post("/db/_bulk_docs")
async def bulk_docs(payload: Dict[str, List[Dict[str, Any]]]):
    # This is a very simplified mock of the _bulk_docs endpoint.
    # A real implementation would need to handle revisions, conflicts, and deletions.
    docs = payload.get("docs", [])
    results = []
    for doc in docs:
        doc_id = doc.get("_id")
        # Simple upsert logic
        # A real implementation is much more complex
        results.append({"id": doc_id, "ok": True, "rev": "1-mock-rev"})
    return results


app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "POS Backend is running"}
