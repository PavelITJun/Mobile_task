from fastapi import FastAPI
import uvicorn
from app.orders.router import router as OrderRouter
from app.products.router import router as ProductRouter


app = FastAPI()
app.include_router(ProductRouter)
app.include_router(OrderRouter)


if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
