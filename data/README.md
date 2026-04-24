# Yansu

# Prerequisites

    uv
        Install: https://docs.astral.sh/uv/getting-started/installation/

# Build the enviroment:

```bash
uv venv --python 3.12.3
```

# Activate the enviroment:

```bash
source .venv/bin/activate
```

# Install dependencies:

```bash
uv pip install -r data/requirements.txt
```

#  Run API:

```bash
fastapi run data/api.py
```