from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import ChatRequest,ChatResponse
from backend.router import ModelRouter
from backend.providers import ProviderError
app=FastAPI(title="FishyLLAMA API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
router=ModelRouter()
@app.get('/api/health')
async def health():return {'name':'FishyLLAMA','status':'online','providers':router.available()}
@app.get('/api/providers')
async def providers():return {'providers':router.available()}
@app.post('/api/chat',response_model=ChatResponse)
async def chat(req:ChatRequest):
    try:
        content,provider,model=await router.chat([m.model_dump() for m in req.messages],req.provider,None if req.model=='auto' else req.model)
        return ChatResponse(content=content,provider=provider,model=model)
    except ProviderError as exc: raise HTTPException(502,str(exc))
