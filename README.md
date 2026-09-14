# 🐟 FISHYLLAMA

FishyLLAMA is a multi-model AI assistant with a unified Fishy Core, optional API providers, local-model support, coding integrations and a voice-first assistant interface.

## OpenClaw / JARVIS UI integration

The frontend now uses the OpenClaw/JARVIS-style HUD concept from the supplied `openclaw-jarvis-ui` project as the visual foundation, while keeping FishyLLAMA as the actual AI backend.

Integrated concepts:

- cinematic HUD / scanner frame
- system status and model telemetry
- data-center tabs for tasks, skills, memory and schedule
- audio/spectrum visualizer
- mobile-oriented controls
- Fishy Core model routing
- provider selection
- local-first option
- browser microphone input
- interruptible speech synthesis
- sentence-aware speech cleanup
- voice profiles and speech-rate/pitch controls
- OpenAI-compatible multi-provider backend
- Ollama/local AI path
- GitHub/Copilot coding adapter architecture

## Run in Codespaces

```bash
pip install -r requirements.txt
uvicorn backend.web:app --host 0.0.0.0 --port 8000
```

Open the forwarded port 8000.

## API keys

Use Codespaces/Repository secrets or a local `.env` file. Never commit real API keys.

## Architecture

```text
                    FISHYLLAMA
                         │
                    FISHY CORE
                         │
             ┌───────────┴───────────┐
             │                       │
        Model Router              Voice Core
             │                       │
   OpenAI / DeepSeek / xAI     TTS + microphone
   Groq / Mistral / Ollama     sentence streaming
             │                       │
             └───────────┬───────────┘
                         │
                  OPENCLAW HUD UI
          system / tasks / skills / memory
             schedule / audio / telemetry
```

The OpenClaw visual design is used as the UI foundation; FishyLLAMA's own backend, routing, voice and integration architecture remain the functional core.
