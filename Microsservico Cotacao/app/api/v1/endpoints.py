from fastapi import APIRouter, Depends, HTTPException, status
from app.services.cotacao_service import CotacaoService
from app.crud.cotacao_repository import CotacaoRepository
from typing import Dict, Any, Optional

router = APIRouter()
cotacao_repo = CotacaoRepository()
cotacao_service = CotacaoService(repository=cotacao_repo)

@router.get(
    "/cotacao/{moeda_base}",
    summary="Obtém a cotação de uma moeda base",
    description="Retorna a cotação mais recente de uma moeda base em relação a outras moedas."
)
async def get_cotacao_base(moeda_base: str):
    resultado = await cotacao_service.obter_cotacao(moeda_base)
    if "mensagem" in resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=resultado["mensagem"])
    return resultado

@router.get(
    "/cotacao/{moeda_base}/{moeda_alvo}",
    summary="Obtém a cotação de uma moeda para outra",
    description="Retorna a cotação mais recente de uma moeda base em relação a uma moeda alvo específica."
)
async def get_cotacao(moeda_base: str, moeda_alvo: str):
    resultado = await cotacao_service.obter_cotacao(moeda_base, moeda_alvo)
    if "mensagem" in resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=resultado["mensagem"])
    return resultado