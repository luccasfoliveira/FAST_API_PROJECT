from pydantic import BaseModel, EmailStr, Field


class Item(BaseModel):
    id_item: int
    name: str
    value: float = Field(example=1.0)
    tax: int | None = Field(default=0, example=1, ge=0)
    new_value: float | None = None


class ModifyItem(BaseModel):
    name: str | None = Field(default=None, example="Nome")
    value: float | None = Field(default=None, example=0.0)
    tax: int | None = Field(default=None, example=3, ge=0)


class User(BaseModel):
    name: str = Field(example="Nome do cliente")
    middle_name: str | None = Field(default=None, example="Nome do Meio", max_length=150)
    last_name: str = Field(example="Último Nome")
    age: int = Field(example=18, ge=18)
    email: EmailStr | None = Field(default=None)
    cpf: str = Field(example="123.456.789-10", max_length=14)


class ModifyUser(BaseModel):
    name: str | None = Field(example="Nome do cliente")
    middle_name: str | None = Field(default=None, example="Nome do Meio", max_length=150)
    last_name: str | None = Field(example="Último Nome")
    age: int | None = Field(example=18, ge=18, le=130)
    email: EmailStr | None = Field(default=None)
