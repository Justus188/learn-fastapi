from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'fastapi'}

@app.get('/about')
async def about():
    return {'about': 'wew'}