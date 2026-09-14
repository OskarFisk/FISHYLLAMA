from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.main import app
app.mount('/static',StaticFiles(directory='frontend/static'),name='static')
@app.get('/')
async def home(): return FileResponse('frontend/index.html')
