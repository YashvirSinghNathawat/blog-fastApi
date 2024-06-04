

from fastapi import FastAPI

app = FastAPI()

# Decorators
@app.get('/')
def index():
    return {
        'data': {
            'name' : 'sarthak'
        }
    }