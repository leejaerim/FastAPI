from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
	return {"message" : "hello World"}

@app.get("/item/{item_id}")
async def read_item(item_id):
	return {"item_id" : item_id}