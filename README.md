# Fast API 학습
### 목표
- FastAPI 사용하여 프로젝트를 진행하기 위한 초석을 공부하고자 한다.
---
### why FastAPI?
- 노드만큼 빠르고 직관적이며, 짧고 쉬우며, 빠르게 코드를 작성할 뿐만 아니라, 프레임워크를 통해 컨트롤 제어하므로 그만큼 버그가 적다.
---
### First Step 
- Install
    ~pip3 install "fastAPI[all]"~ 
- Hello World
~~~ 
@app.get("/")
async def root():
	return {"message" : "hello World"}
~~~
---
### 참고자료
- [FastAPI 공식 레퍼런스](https://fastapi.tiangolo.com/ko/)

---
# 명령어 
### 서버 실행
> brew services start mongodb-community@6.0
- http://localhost:27017
### 몽고쉘 실행
>mongosh
### 서버 종료
> brew services stop mongo-community@6.0
---

출처 : 
[공식 몽고DB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
[몽고DB with fastapi](https://github.com/mongodb-developer/mongodb-with-fastapi)

### Step 1. Modeling MongoDB  by using MongoEngine
- getting rid of Not Understanding concept, Study hard step by step
- getting list of Employees : `Employee.objects().to_json()`
- Reference : [FastAPI & MongoDB](https://www.youtube.com/watch?v=1h2aQhv8-oI&list=PL4iRawDSyRvWybsXRTommb3acUigWPEsj&index=3)

### Path Parameter
```python
@app.get("/get_employee/{emp_id}")
def get_employee(emp_id : int):
    employee = Employee.objects.get(emp_id=emp_id)
```

### Query parameter
```python
from fastapi import Query
from mongoengine.queryset.visitor import Q
@app.get("/search_employees")
def search_employees(name : str, age : int = Query(None, gt=18)):
    employees_list = Employee.objects.filter(Q(name__icontains=name) | Q(age=age)).to_json()
```

### RequestBody with Post type
```python
@app.post("/add_employee")
```
### Create Employee using Queryparamter 
```python
@app.get("/add_employee")
def add_employee(emp_id : int , name : str, age : int , teams : str = Query("")):
    teams_list = teams.split("_")
    employees_list = Employee.objects.filter(emp_id=emp_id).to_json()
    if len(employees_list) < 3 :
        new_employee = Employee(emp_id=emp_id,
                                name=name,
                                age=age,
                                teams=teams_list
                                )
        new_employee.save()
        return {"message": "200"}
    else:
        return {"message": "401"}
```

---
### Authentication
- `pip3 install passlib,bcrypt`를 통한 password 암호화 
- requestBody를 이용한 post 통신 및 create user
- 모델 추가 & requestBody로 받을 클래스 생성
- 로그인을 통한 서버 접속 후 , token으로 세션 유지
- jwt를 통한 세션관리, `token : str = Depends(outh2_scheme)`
    -> 로그인이 필요한 경우 파라미터 삽입
- 랜덤 시크릿 키 생성 명령어 `openssl rand -hex 32``
