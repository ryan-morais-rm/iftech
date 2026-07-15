# Autonomous Infrastructure: Deploying LLMs in the Cloud

This project was developed for the **IFTech 2026** presentation. Its goal is to demonstrate how to provision a scalable cloud infrastructure using **Infrastructure as Code (IaC)** and deploy a private **Large Language Model (LLM)** integrated with an interactive application for participants.

The repository is structured as a **Monorepo**, combining both the infrastructure layer (IaC) and the application layer.

---

## Repository Structure

```text
iftech/
├── iac/                       # Infrastructure as Code
│   ├── terraform/             # Cloud resource provisioning (VM, VPC, Security Groups)
│   └── ansible/               # Server configuration (Docker installation and dependencies)
└── app/                       # Application and Artificial Intelligence
    ├── frontend/              # Web interface for participant interaction
    ├── backend/               # API integration with the LLM
    └── docker-compose.yml     # Local service orchestration (App + Ollama/vLLM)
```

## Technologies Used

* **Terraform:** Virtual machine provisioning and network rule management.
* **Ansible:** Server configuration automation and Docker provisioning.
* **Docker & Docker Compose:** Containerization of the application and the LLM inference environment.
* **Ollama / vLLM:** Local inference server for running the LLM in the cloud.
* **Python (FastAPI / Langflow):** Backend and AI agent orchestration.

## Authors

* **Ryan Morais Correia** – Infrastructure Lead (Terraform & Ansible)
* **João Pedro Marques** – Application & AI Engineering Lead
