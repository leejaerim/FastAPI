from typing import Union
from models import Employee, User
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from mongoengine import connect

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connect(db="mongo", host="localhost",port=27017)





@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}




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
class NewUser(BaseModel):
    name : str
    password :str

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)
@app.post("/sign_up")
def sign_up(new_user : NewUser):
    user = User(name = new_user.name,password=get_password_hash(new_user.password))
    user.save()
    return {"message":"new user created successfully"}

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException

from datetime import datetime, timedelta
from jose import jwt
SECRET_KEY = "b96115f6c2db831022480a8438c76abb757d0b71d34d9046cce673f1cf43269d"
ALGORITHME = "HS256"
def create_access_token(data : dict, expired_delta : timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expired_delta
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHME)
    return encode_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def auth(name,password):
    try:
        user = json.loads(User.objects.get(name=name).to_json())
    except :
        raise HTTPException(status_code=400, detail="INCORRECT USERNAME OR PASSWORD")
    if user :
        password_check = pwd_context.verify(password, user['password'])
        return password_check
    else :
        raise HTTPException(status_code=400, detail="INCORRECT USERNAME OR PASSWORD")

class login_user(BaseModel):
    username : str
    password : str

@app.post("/login")
def login(form_data: login_user):
    username = form_data.username
    password = form_data.password

    if auth(username, password) : 
        access_token = create_access_token(data={"sub":username},expired_delta=timedelta(minutes=30))
        return {"access_token" : access_token, "token_type" : "bearer"}
    else :
        raise HTTPException(status_code=400, detail="INCORRECT USERNAME OR PASSWORD")

@app.get("/")
def read_root(token : str= Depends(oauth2_scheme)):
    print(jwt.decode(token,SECRET_KEY,algorithms=ALGORITHME))

    return {"token":token}

@app.get("/get_employee/{emp_id}")
def get_employee(emp_id : int):
    employee = Employee.objects.get(emp_id=emp_id)
    return {"employee.emp_id" : employee.emp_id, "employee.name" : employee.name}


@app.get("/get_all_employees")
def get_all_employees(token : str=Depends(oauth2_scheme)):
    employees = Employee.objects().to_json()
    employees_list = json.loads(employees)
    return {"employees" : employees_list} 