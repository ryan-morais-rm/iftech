# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monorepo for **IFTech 2026**, a 4-hour educational event on "Deploying Classic Models vs LLMs". It demonstrates provisioning cloud infrastructure with IaC and serving two kinds of models side by side:

- A **classic NLP model** (IMDB sentiment analysis) loaded in-memory by the API at startup.
- An **LLM** (e.g. `llama3.2` 3B) running as a separate **Ollama** service, accessed through a backend proxy route.

Code should stay clean and didactic — the audience is beginners, so favor simplicity and ease of explanation over cleverness.

## Stack

- **Infrastructure:** Terraform (provisions an Ubuntu VM on AWS EC2 / GCP, outputs the public IP) and Ansible (installs Docker, pre-pulls the Ollama model, runs the compose stack).
- **Containers:** Docker + Docker Compose (3 services: `backend`, `frontend`, `ollama` using the official `ollama/ollama` image, all on a shared network).
- **Backend:** FastAPI (Python).
- **Frontend:** Streamlit (Python).

## Repository Structure

```text
.
├── iac/
│   ├── terraform/       # main.tf, variables.tf, outputs.tf — VM + public IP output
│   └── ansible/         # Playbooks: install Docker, `docker exec ollama ollama pull llama3.2`, run compose
└── app/
    ├── docker-compose.yml
    ├── backend/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── main.py            # Only initializes the app and includes the routers
    │   ├── routers/
    │   │   ├── llm.py         # POST route that proxies prompts to the Ollama container via HTTP
    │   │   └── classifier.py  # POST route returning sentiment (Positivo/Negativo); mock model
    │   └── ml/
    │       └── model/         # Empty dir for the model artifact (.joblib/.pkl)
    └── frontend/
        ├── Dockerfile
        ├── requirements.txt
        └── app.py             # Streamlit app with st.tabs(["Classificador IMDB", "Chat LLM"])
```

## Architecture Notes

- **`backend/main.py`** must stay minimal: create the FastAPI app and include the two routers, nothing else.
- **`classifier.py`** simulates loading a model artifact from `ml/model/` during app startup (startup event), then serves a simple POST endpoint (text in → sentiment JSON out). The model is currently a mock; the real `.joblib`/`.pkl` artifact will live in `ml/model/`.
- **`llm.py`** does not run inference itself — it forwards the prompt over HTTP to the Ollama container (reachable as `http://ollama:11434` on the compose network) and returns the response.
- **`frontend/app.py`** has two tabs: tab 1 uses `st.text_area` + button calling the classifier route; tab 2 is a chat UI (`st.chat_input` / `st.chat_message`) calling the LLM route. The frontend only talks to the backend, never to Ollama directly.
- **Ansible** pre-pulls the LLM (`docker exec ollama ollama pull llama3.2`) so the model download does not delay the live demo.

## Common Commands

```bash
# Run the full stack locally (from app/)
docker compose up -d --build

# Pre-pull the LLM inside the running Ollama container
docker exec ollama ollama pull llama3.2

# Provision the VM (from iac/terraform/)
terraform init && terraform plan && terraform apply

# Configure the server and deploy (from iac/ansible/)
ansible-playbook -i inventory.ini playbooks/deploy.yml
```

Service ports: backend `8000`, frontend `8501`, Ollama `11434`.

## Authors

- Ryan Morais Correia — Infrastructure Lead (Terraform & Ansible)
- João Pedro Marques — Application & AI Engineering Lead
