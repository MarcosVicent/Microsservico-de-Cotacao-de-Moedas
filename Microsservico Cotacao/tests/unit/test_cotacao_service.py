import pytest
from unittest.mock import AsyncMock
from app.services.cotacao_service import CotacaoService
from app.crud.cotacao_repository import CotacaoRepository
from app.models.cotacao import CotacaoBase
from datetime import datetime

@pytest.fixture
def mock_cotacao_repository():
    return AsyncMock(spec=CotacaoRepository)

@pytest.fixture
def cotacao_service(mock_cotacao_repository):
    return CotacaoService(repository=mock_cotacao_repository)

@pytest.mark.asyncio
async def test_obter_cotacao_sucesso_com_moeda_alvo(cotacao_service, mock_cotacao_repository):
    mock_cotacao_repository.get_cotacao_from_api.return_value = CotacaoBase(
        moeda_base="USD",
        taxas={"BRL": 5.25, "EUR": 0.9},
        ultima_atualizacao=datetime.now()
    )

    resultado = await cotacao_service.obter_cotacao("USD", "BRL")
    
    mock_cotacao_repository.get_cotacao_from_api.assert_called_once_with("USD")
    assert resultado["moeda_base"] == "USD"
    assert resultado["moeda_alvo"] == "BRL"
    assert resultado["valor"] == 5.25

@pytest.mark.asyncio
async def test_obter_cotacao_sucesso_sem_moeda_alvo(cotacao_service, mock_cotacao_repository):
    mock_cotacao_repository.get_cotacao_from_api.return_value = CotacaoBase(
        moeda_base="USD",
        taxas={"BRL": 5.25, "EUR": 0.9},
        ultima_atualizacao=datetime.now()
    )

    resultado = await cotacao_service.obter_cotacao("USD")
    
    mock_cotacao_repository.get_cotacao_from_api.assert_called_once_with("USD")
    assert resultado["moeda_base"] == "USD"
    assert "BRL" in resultado["taxas"]
    assert resultado["taxas"]["BRL"] == 5.25

@pytest.mark.asyncio
async def test_obter_cotacao_moeda_nao_encontrada(cotacao_service, mock_cotacao_repository):
    mock_cotacao_repository.get_cotacao_from_api.return_value = None

    resultado = await cotacao_service.obter_cotacao("XYZ", "BRL")
    
    mock_cotacao_repository.get_cotacao_from_api.assert_called_once_with("XYZ")
    assert "mensagem" in resultado
    assert "Não foi possível obter a cotação" in resultado["mensagem"]