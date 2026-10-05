# Contributing

Thanks for contributing to OSS AI Lab.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e packages/ragline -e packages/llmboost -e packages/agenloop pytest
cd packages/mcp-enhance && npm install && npm run build
```

## Checks

```bash
pytest -q
cd packages/mcp-enhance && npm test
```

## Guidelines

- Keep packages dependency-light and offline-demoable when possible.
- Prefer clear APIs and docstrings over clever abstractions.
- Add a short test for every new public function.
- Do not commit secrets or `.env` files.
