from fastapi import FastAPI, Query, Path
from uuid import UUID, uuid4
from model.data import Data
from service.service import ServiceRoot
from schema import *


service = ServiceRoot
db = Data

app = FastAPI(title="Project")

@app.get("/", tags=["root main"])
async def root():
    return {"DATA SALES": db.sales,
            "DATA CLIENT": db.client,
            "DATA ITEMS": db.items}

@app.get("/client/", tags=["client"])
async def get_clients():
    return {"DATA CLIENT": db.client}

@app.get("/client/{cpf}", tags=["client"])
async def get_client(cpf: str):
    return service.get_client(cpf=cpf)

@app.post("/client/creat", status_code=201, tags=["client"])
async def creat_client(*, cpf: str = Query(min_length=11, max_length=14), users: User):
    return service.creat_client(cpf=cpf, users=users)

@app.put("/client/change/{cpf}", tags=["client"])
async def change_client(cpf: str, user_changed: ModifyUser):
    return service.change_client(cpf=cpf, user_changed=user_changed)

@app.delete("/client/delet/{cpf}", tags=["client"])
async def delet_client(cpf: str):
    return service.delet_client(cpf=cpf)

@app.get("/items", tags=["item"])
async def get_items():
    return {"DATA ITEMS": db.items}

@app.get("/items/{id_item}", tags=["item"])
async def get_item(id_item: int):
    return service.get_item(id_item=id_item)

@app.post("/items/creat/", status_code=201, tags=["item"])
async def create_item(id_item: int, item: Item):
    return service.creat_item(id_item=id_item, item=item)

@app.put("/items/change/{id_item}", tags=["item"])
async def change_item(id_item: int, item_changed: ModifyItem):
    return service.change_item(id_item=id_item, item_changed=item_changed)

@app.delete("/items/delet/{id_item}", tags=["item"])
async def delet_item(id_item: int):
    return service.delet_item(id_item=id_item)

@app.get("/purchase", tags=["purchase"])
async def get_purchase():
    return {"DATA_PURCHASE": db.sales}

@app.get("/purchase/{id_sales}", tags=["purchase"])
async def get_purchase(id_purchase: UUID, full: bool = Query(default=False, description="Informações Detalhadas:")):
        return service.get_puchase(full=full, id_purchase=id_purchase)

@app.post("/purchase/sales/", status_code=201, tags=["purchase"])
async def creat_purchase(*, id_purchase: UUID = uuid4(), 
                         cpf: str = Query(description="CPF: 000.000.000-00"),
                         id_item: int = Query(ge=1, description="ID do item"),
                         count: int = Query(default=1, description="quantidade de item:")):
    
    return service.creat_purchase(id_purchase=id_purchase, cpf=cpf, id_item=id_item, count=count)

@app.delete("/purchase/delet/{id_purchase}", tags=["purchase"])
async def delet_purchase(id_purchase: UUID):
    return service.delet_pourchase(id_purchase)
