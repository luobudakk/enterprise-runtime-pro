# Enterprise Runtime Pro

Enterprise-grade AI Runtime prototype for:
- grounded enterprise knowledge QA (RAG),
- controllable action execution (`preview -> confirm -> execute`),
- structured Ask session runtime (`Session / Turn / Command / Job`).

Built with `FastAPI + Next.js`, aligned with the `EMATA Runtime` architecture.

## Highlights

- **Ask Runtime**: intent routing, context/state management, command handling, job tracking.
- **RAG Pipeline**: upload -> parse -> chunk -> index -> search -> rerank -> answer with citations.
- **Controllable Actions**: message/meeting actions are previewed before execution.
- **Integration-ready**: Feishu CLI, Milvus, MinIO/filesystem, Temporal hooks.
- **Tested**: backend and frontend test suites are in place and runnable locally.

## Project Structure

```text
enterprise-runtime-pro/
├─ backend/
│  ├─ app/
│  ├─ tests/
│  ├─ requirements.txt
│  ├─ requirements-optional.txt
│  └─ requirements-dev.txt
├─ frontend/
│  ├─ app/
│  ├─ components/
│  ├─ lib/
│  └─ tests/
├─ infra/
├─ docs/
├─ scripts/
├─ docker-compose.yml
└─ .env.example
```

## Local Run (Windows)

### 1) Backend

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
py -3.11 -m pip install -r requirements-dev.txt
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2) Frontend

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm install
npm run dev
```

Open:
- API: `http://127.0.0.1:8000`
- Ask UI: `http://127.0.0.1:3000/ask`
- Knowledge UI: `http://127.0.0.1:3000/knowledge`

## Tests

### Backend

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m pytest -q
```

### Frontend

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm test -- --runInBand
```

## Key Environment Variables

See `.env.example` for full list. Common ones:

- Runtime: `EMATA_API_HOST`, `EMATA_API_PORT`, `EMATA_DATABASE_URL`
- Model/RAG: `EMATA_MODEL_*`, `EMATA_RERANK_*`, `EMATA_EMBEDDING_*`
- Knowledge storage/index: `EMATA_STORAGE_BACKEND`, `EMATA_UPLOAD_BASE_DIR`, `EMATA_MILVUS_URI`
- Feishu: `EMATA_FEISHU_APP_ID`, `EMATA_FEISHU_APP_SECRET`
  - Compatible aliases: `EMATA_LARK_APP_ID`, `EMATA_LARK_APP_SECRET`

## What To Demo In Interview

- Ask question with citations from knowledge base.
- Reuse previous answer and send as action draft.
- Preview-confirm action before actual execution.
- Explain how runtime separates:
  - routing,
  - context memory,
  - skill logic,
  - tool integrations,
  - policy/risk control.

## Upload To GitHub Checklist

- [ ] Remove secrets/private keys from `.env` and local configs.
- [ ] Keep `.env.example` only as template.
- [ ] Ensure large temp/runtime files are ignored.
- [ ] Run both test suites once before pushing.
- [ ] Add screenshots/demo GIFs under `images/demo/` if needed.

## License

No license file is currently included.
Add `LICENSE` before public open-source release.
