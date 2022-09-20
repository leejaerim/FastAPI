from typing import Union
from models import Employee
from fastapi import FastAPI
import json
from mongoengine import connect

app = FastAPI()
connect(db="mongo", host="localhost",port=27017)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/get_all_employees")
def get_all_employees():
    employees = Employee.objects().to_json()
    employees_list = json.loads(employees)
    return {"employees" : employees_list} 