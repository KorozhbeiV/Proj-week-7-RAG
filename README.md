### Project structure
``` txt
Proj week 7 RAG/
├── src/
│   ├── domain/
│   │   ├── facades/
│   │   │   ├── abs_chunking_service.py
│   │   │   ├── abs_embeding_client.py
│   │   │   └── abs_llm_client.py
│   │   │
│   │   ├── modules/
│   │   │   ├── embeding/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chunking_service.py
│   │   │   │   └── client_creator.py
│   │   │   └── llm/
│   │   │       └── client_creator.py
│   │   │
│   │   ├── pipelines/
│   │   │   ├── ingestion.py
│   │   │   └── retrieval.py
│   │   │
│   │   └── shared/
│   │       ├── api_keys.py
│   │       └── registator/
│   │           ├── dicts.py
│   │           └── enums.py
│   │
│   ├── infrastructure/
│   │   └── api/
│   │       └── v1/
│   │           ├── endpoints.py
│   │           └── schemas.py
│   │
│   └── shared/
│       └── logger_config.py
│
├── evaluation/
│   ├── test_datasets/
│   └── run_eval.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```