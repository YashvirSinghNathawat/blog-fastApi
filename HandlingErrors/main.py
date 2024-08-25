from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()


@app.get('/')
def main():
    return {'message':'App has been started'}


items = {"foo":"The Food Wrestlers"}


 
@app.get('/items/{item_id}')
def getItem(item_id: str):
    if item_id not in items:    # Without this Internal Server Error
        raise HTTPException(status_code = 404,detail="Item not found" , headers={
            "X-errror":"There goes my error"
        })          # FastApi gives custom header support to HttpException
    return {'items':items[item_id]}

#Custom Exception
class UnicornException(Exception):
    def __init__(self,name):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request,exc: UnicornException):
    return JSONResponse(status_code = 418,
        content={
            "message":f"Oops! {exc.name} did something.There goes a rainbow..."
        })

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name=="yolo":
        raise UnicornException(name=name)
    return {"uvicorn_name":name}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Overide Request Validation Exceptions When a request contains invalid data, FastAPI internally raises a RequestValidationError.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    return PlainTextResponse(str(exc),status_code=400)

@app.get('/items2/{item_id}')
async def getItem(item_id: int):
    if item_id not in items:    # Without this Internal Server Error
        raise HTTPException(status_code = 404,detail="Item not found" )          # FastApi gives custom header support to HttpException
    return {'items':items[item_id]}

