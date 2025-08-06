import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch
from app.services.cotacao_service import CotacaoService
from app.models.cotacao import Cotacao

client = TestClient(app)

@patch('app.api.v1.endpoints.cotacao_service', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_cotacao_sucesso(mock_cotacao_service):
    mock_cotacao_service.obter_cotacao.return_value = {
        "moeda_base": "USD",
        "moeda_alvo": "BRL",
        "valor": 5.25,
        "ultima_atualizacao": "2025-08-05T00:00:00",
        "fonte": "API Externa"
    }

    response = client.get("/api/v1/cotacao/USD/BRL")
    
    assert response.status_code == 200
    data = response.json()
    assert data["moeda_base"] == "USD"
    assert data["valor"] == 5.25
    mock_cotacao_service.obter_cotacao.assert_called_once_with("USD", "BRL")

@patch('app.api.v1.endpoints.cotacao_service', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_cotacao_moeda_nao_encontrada(mock_cotacao_service):
    mock_cotacao_service.obter_cotacao.return_value = {
        "mensagem": "Não foi possível obter a cotação para a moeda XYZ"
    }

    response = client.get("/api/v1/cotacao/XYZ/BRL")
    
    assert response.status_code == 404
    assert "Não foi possível obter a cotação" in response.json()["detail"]
    mock_cotacao_service.obter_cotacao.assert_called_once_with("XYZ", "BRL")