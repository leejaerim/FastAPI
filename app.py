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

@app.get("/get_employee/{emp_id}")
def get_employee(emp_id : int):
    employee = Employee.objects.get(emp_id=emp_id)
    return {"employee.emp_id" : employee.emp_id, "employee.name" : employee.name}

from fastapi import Query
from mongoengine.queryset.visitor import Q
@app.get("/search_employees")
def search_employees(name : str, age : int = Query(None, gt=18)):
    employees_list = Employee.objects.filter(Q(name__icontains=name) | Q(age=age)).to_json()
    
    return {"employees" : json.loads(employees_list)} 

from pydantic import BaseModel
from fastapi import Body

class NewEmployee(BaseModel):
    emp_id : int
    name : str
    age : int = Body(None, gt=18)
    teams : list = Body(None)

@app.post("/add_employee")
def add_employee(employee: NewEmployee):
    new_employee = Employee(emp_id=employee.emp_id,
                            name=employee.name,
                            age=employee.age,
                            teams=employee.teams
                            )
    new_employee.save()

    return {"message": "Employee is added."}

@app.get("/add_employee")
def add_employee(emp_id : int , name : str, age : int , teams : str = Query("")):
    teams_list = teams.split("_")
    employees_list = Employee.objects.filter(emp_id=emp_id).to_json()
    print(len(employees_list))
    if len(employees_list) < 3 :
        new_employee = Employee(emp_id=emp_id,
                                name=name,
                                age=age,
                                teams=teams_list
                                )
        print(new_employee.save())

        return {"message": "Employee is added."}
    else:
        return {"message": "Employee isn't added."}
