from fastapi import FastAPI
from app.api.v1 import endpoints as rest_endpoints
from app.api.graphql import graphql_app
from app.core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Microsserviço de consulta de cotação de moedas com APIs RESTful e GraphQL.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(rest_endpoints.router, prefix="/api/v1", tags=["Cotação (REST)"])

app.include_router(graphql_app, prefix="/graphql", tags=["Cotação (GraphQL)"])

@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "Bem-vindo ao Microsserviço de Cotação. Acesse /docs para a documentação REST ou /graphql para a interface GraphQL."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)