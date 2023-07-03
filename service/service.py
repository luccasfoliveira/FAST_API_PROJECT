from fastapi import HTTPException, Query
from uuid import UUID, uuid4
from schema import *
from model.data import Data


db = Data

class Service:

    @classmethod
    def remover_char_especiais(cls, cpf: str) -> str:
        cpf = cpf.strip()
        if cpf.isdigit():
            return cpf
        new_cpf = ''
        for c in cpf:
            if c.isdigit():
                new_cpf += c
        return new_cpf
    
    @classmethod
    def verify_client(cls, cpf: str) -> bool:
        return cls.remover_char_especiais(cpf) in db.client


class ServiceRoot(Service):

    @classmethod
    def get_client(cls, cpf: str) -> dict | HTTPException:
        if cls.verify_client(cpf=cpf):
            return {cpf:db.client[cpf]}
        raise HTTPException(status_code=404, detail="client not exists", headers={"ERROR": "NOT FOUND 404"})

    @classmethod
    def creat_client(cls, cpf: str, users: User) -> dict:
        if cls.verify_client(cpf=cpf):
            return {"client already exists": db.client[cpf]}
        db.client.update({cpf: {
            "name":users.name,
            "middle_name": users.middle_name,
            "last_name": users.last_name,
            "age": users.age,
            "e-mail": users.email}})
        return {"client created": db.client[users.cpf]}

    @classmethod
    def change_client(cls, cpf: str, user_changed: ModifyUser) -> dict | HTTPException:
        if cls.get_client(cpf=cpf):
            user_changed = user_changed.dict()
            for attribute in user_changed:
                db.client[cpf][attribute] = user_changed[attribute]
            return {"client changed": db.client[cpf]}

    @classmethod
    def delet_client(cls, cpf: str) -> dict | HTTPException:
        if cls.get_client(cpf=cpf):
            return {"client deleted": db.client.pop(cpf)}

    @classmethod
    def get_item(cls, id_item: int) -> dict | HTTPException:
        if id_item in db.items:
            return {id_item:db.items[id_item]}
        raise HTTPException(status_code=404, detail="item not exists", headers={"ERROR": "NOT FOUND 404"})

    @classmethod
    def creat_item(cls, id_item: int, item: Item) -> dict:
        if id_item not in db.items:
            db.items.update({id_item: {
                "name": item.name,
                "value": item.value,
                "tax": item.tax / 100,
                "new_value": round(item.value * (item.tax/100 + 1), 2)}})
            
            return {"item created": db.items[id_item]}
        return {"item already exists": db.items[id_item]}

    @classmethod
    def change_item(cls, id_item: int, item_changed: ModifyItem) -> dict | HTTPException:
        if cls.get_item(id_item=id_item):
            item_changed = vars(item_changed)
            for attibute in item_changed:
                db.items[id_item][attibute] = item_changed[attibute]
                if attibute == "tax":
                    db.items[id_item]["new_value"] = round(item_changed["value"] * (item_changed[attibute]/100 + 1), 2)
            return {"item changed": db.items[id_item]}

    @classmethod
    def delet_item(cls, id_item: int) -> dict | HTTPException:
        if isinstance(cls.get_item(id_item=id_item), dict):
            return {"item deleted": db.items.pop(id_item)}

    @classmethod
    def get_puchase(cls, id_purchase: UUID,
                    full: bool = Query(default=False, description="Informações Detalhadas:") )-> dict | HTTPException:
            
            id_purchase = str(id_purchase)
            if id_purchase in db.sales:
                if full:
                    return {id_purchase: db.sales[id_purchase],
                            "client": db.client[db.sales[id_purchase]["cpf_client"]],
                            "item": db.items[db.sales[id_purchase]["id_item"]]}
                
                return {id_purchase: db.sales[id_purchase]}
            raise HTTPException(status_code=404, detail="purchase not exists", headers={"ERROR": "NOT FOUND 404"})

    @classmethod
    def creat_purchase(cls, *,
                       id_purchase: UUID,
                       cpf: str = Query(description="CPF: 000.000.000-00"),
                       id_item: int = Query(ge=1, description="ID do item"),
                       count: int = Query(default=1, description="quantidade de item:")) -> dict | HTTPException:
        
        id_purchase = str(id_purchase)
        if cls.get_client(cpf=cpf) and cls.get_item(id_item=id_item):
            db.sales.update({id_purchase: {
                "cpf_client": cls.remover_char_especiais(cpf),
                "id_item": id_item,
                "qnt": count,
                "value_total": round(db.items[id_item]['new_value'] * count, 2)}})
            return {"sales successful": db.sales[id_purchase]}

    @classmethod
    def delet_pourchase(cls, id_purchase: UUID) -> dict | HTTPException:
        if cls.get_puchase(id_purchase=id_purchase, full=False):
            return {"sales deleted": db.sales.pop(str(id_purchase))} 
