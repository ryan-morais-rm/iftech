from fastapi import FastAPI

from routers import classifier, llm

app = FastAPI(title="IFTech 2026 - Deploy de Modelos Classicos vs LLMs")

app.include_router(classifier.router)
app.include_router(llm.router)


@app.get("/health")
def health():
    return {"status": "ok"}
