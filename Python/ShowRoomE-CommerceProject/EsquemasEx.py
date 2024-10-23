#!/usr/bin/python
# -- encoding: utf-8 --
from pydantic import BaseModel
from datetime import date


class UserSchema(BaseModel):
    name: str
    password: str
    email: str
    cep: int
    city: str
    address: str
    neighborhood: str
    cellphone: str
    user_token: str
    is_active: bool
    is_superuser: bool
    is_employee: bool


class ProductSchema(BaseModel):
    name: str
    description: str
    value: float
    quantity: int


class CartSchema(BaseModel):
    fk_user: str
    fk_product: str
    quantity: float


class AuthenticationSchema(BaseModel):
    user_id: str
    access_token: str
    expiration: date


class OrderSchema(BaseModel):
    fk_user: str
    fk_product: str
    quantity: float
    order_number: int


class PaymentSchema(BaseModel):
    fk_order: int
    city: str
    address: str
    neighborhood: str
    country: str
    fk_send: int
    fk_payment_type: int
    value: int
    card_name: str
    card_number: str
    data_expiration: date


class SendTypeSchema(BaseModel):
    name: str
    password: str
    email: str
    cep: int
    cidade: str
    logradouro: str
    bairro: str
    telefone: str
    description: str


class PaymentTypeSchema(BaseModel):
    name: str
    description: str
    type: int
