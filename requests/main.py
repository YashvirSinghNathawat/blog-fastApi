from fastapi import FastAPI
import requests

app = FastAPI()

@app.get('/get_html')
def getAllUser():
    data = requests.get('https://xkcd.com/353/')
    return data.text


@app.get('/get_image')
def getImage():
    data = requests.get('https://imgs.xkcd.com/comics/python.pngs')
    print(data.headers)
    if data.status_code==404:
        return {'message': 'File not found'}
    with open('comic.png','wb') as f:
        f.write(data.content)
    return {'message': 'File has been downloaded'}

@app.post('/post_data')
def postData():
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {
        'title': 'foo',
        'body': 'bar',
        'userId': '1'
    }
    response = requests.post(url,json=data,timeout=3)
    return response.text

    

@app.get('/')
def main():
    return {'message':'Welcome to out webpage'}