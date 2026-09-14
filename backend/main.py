from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import ChatRequest, ChatResponse
from backend.router import ModelRouter
from backend.providers import ProviderError
from backend.voice import profiles, split_sentences

app = FastAPI(title="FishyLLAMA API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
router = ModelRouter()

@app.get('/api/health')
async def health():
    return {'name': 'FishyLLAMA', 'status': 'online', 'providers': router.available(), 'voice': 'enabled'}

@app.get('/api/providers')
async def providers():
    return {'providers': router.available()}

@app.get('/api/voice/profiles')
async def voice_profiles():
    return {'profiles': profiles(), 'browser_fallback': True, 'features': {
        'sentence_streaming': True, 'interruptible': True, 'url_simplification': True,
        'code_omission': True, 'microphone_calibration': True, 'audio_feedback': True
    }}

@app.post('/api/voice/chunks')
async def voice_chunks(payload: dict):
    text = str(payload.get('text', ''))
    return {'chunks': split_sentences(text, int(payload.get('max_chars', 260)))}

@app.post('/api/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        content, provider, model = await router.chat(
            [m.model_dump() for m in req.messages], req.provider,
            None if req.model == 'auto' else req.model
        )
        return ChatResponse(content=content, provider=provider, model=model)
    except ProviderError as exc:
        raise HTTPException(502, str(exc))
