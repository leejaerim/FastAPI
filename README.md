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