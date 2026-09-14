# 🐟 FISHYLLAMA

FishyLLAMA is a portable, multi-model AI assistant with a unified Fishy Core, optional API providers, local-model support, coding integrations and a voice-first assistant interface.

## Cross-platform architecture

FishyLLAMA is designed as a **server + browser client** rather than a platform-specific desktop executable. The core service exposes HTTP APIs, while the HUD/UI runs in a browser. This lets one FishyLLAMA server serve Windows, Linux, macOS, Synology DSM and other clients on a LAN.

### Supported development targets

- **Visual Studio Code** and GitHub Codespaces via `.devcontainer/devcontainer.json`
- Windows 10/11: native Python or Docker
- Windows Server: native Python or Docker, depending on installed server components
- Windows 7/8/8.1: use a compatible legacy runtime/container/remote-server arrangement; current Python packages are not guaranteed to install natively
- Windows XP/Vista: **legacy-client / remote-server mode**. These operating systems are obsolete and modern Python/TLS/provider SDKs are not expected to run reliably on them. Run FishyLLAMA on a current server and connect from the old machine using the lightweight `legacy/index.html` client or a compatible web proxy.
- Linux distributions: native Python or Docker/Podman
- macOS: native Python or Docker
- Synology **DSM**: Docker/Container Manager is the preferred deployment when supported by the NAS model; the included `Dockerfile` and `docker-compose.yml` are portable deployment assets.
- Other Unix-like systems: use the same HTTP/Docker architecture where Python 3.12 or containers are available.

> There is no official Windows 9 release. FishyLLAMA treats Windows 8.1 and Windows 10 as the practical versions around the requested "Windows 9" target.

## OpenClaw / JARVIS UI integration

The frontend uses the OpenClaw/JARVIS-style HUD concept from the supplied project as the visual foundation while keeping FishyLLAMA as the actual AI backend.

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

## VS Code / Codespaces

Open the repository in Visual Studio Code or GitHub Codespaces. The dev container installs Python tooling, Node.js and recommended VS Code extensions including Python, Docker and GitHub Copilot/Copilot Chat.

```bash
pip install -r requirements.txt
python -m uvicorn backend.web:app --host 0.0.0.0 --port 8000
```

Open the forwarded port 8000.

## Docker / Synology DSM / Linux / macOS / Windows

Build and run anywhere Docker is available:

```bash
docker compose up -d --build
```

The service listens on port `8000`.

For Synology DSM, create a project in Container Manager using this repository and `docker-compose.yml`, or build the `Dockerfile` and publish container port 8000 to a NAS port.

For Windows PowerShell, Linux/macOS shells and other Unix systems, the `scripts/` directory contains startup helpers.

## Legacy clients

`legacy/index.html` is a deliberately simple browser client for older machines. It communicates with the same `/api/chat` HTTP endpoint and does not require the modern HUD. It is intended primarily for **remote-client mode** on Windows XP/Vista and other systems that cannot run the modern FishyLLAMA runtime.

For old systems, do not expose an unpatched legacy OS directly to the public internet. Put FishyLLAMA behind a current reverse proxy/server and use the old machine only as a LAN client when possible.

## API keys

Use Codespaces/Repository secrets or a local `.env` file. Never commit real API keys.

## Architecture

```text
                        FISHYLLAMA SERVER
                               │
                          FISHY CORE
                               │
              ┌────────────────┴────────────────┐
              │                                 │
         Model Router                       Voice Core
              │                                 │
    cloud / local / coding               TTS / microphone
              │                                 │
              └────────────────┬────────────────┘
                               │
                         HTTP / JSON API
                               │
       ┌───────────────┬───────┼────────┬──────────────┐
       ↓               ↓       ↓        ↓              ↓
  Modern browser     VS Code  DSM     Windows      Linux/macOS
  OpenClaw HUD       agent    Docker   clients       clients
       │
       └──────────── Legacy browser client ────────────┘
```

The OpenClaw visual design is used as the UI foundation; FishyLLAMA's own backend, routing, voice and integration architecture remain the functional core.
