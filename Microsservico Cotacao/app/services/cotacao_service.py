from typing import Dict, Any, Optional
from app.crud.cotacao_repository import CotacaoRepository
from app.models.cotacao import Cotacao

class CotacaoService:
    def __init__(self, repository: CotacaoRepository):
        self.repository = repository

    async def obter_cotacao(self, moeda_base: str, moeda_alvo: Optional[str] = None) -> Dict[str, Any]:
        cotacao_base = await self.repository.get_cotacao_from_api(moeda_base)

        if not cotacao_base:
            return {"mensagem": f"Não foi possível obter a cotação para a moeda {moeda_base.upper()}"}

        if not moeda_alvo:
            return cotacao_base.model_dump()
        
        if moeda_alvo.upper() in cotacao_base.taxas:
            valor = cotacao_base.taxas[moeda_alvo.upper()]
            cotacao_final = Cotacao(
                moeda_base=moeda_base.upper(),
                moeda_alvo=moeda_alvo.upper(),
                valor=valor,
                ultima_atualizacao=cotacao_base.ultima_atualizacao,
                fonte=cotacao_base.fonte
            )
            return cotacao_final.model_dump()
        else:
            return {"mensagem": f"Moeda alvo {moeda_alvo.upper()} não encontrada na cotação de {moeda_base.upper()}"}