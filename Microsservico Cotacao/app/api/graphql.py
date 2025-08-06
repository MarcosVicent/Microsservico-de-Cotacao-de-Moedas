import strawberry
from typing import Union, List, Dict, Any, Optional
from app.models.cotacao import Cotacao
from app.services.cotacao_service import CotacaoService
from app.crud.cotacao_repository import CotacaoRepository
from datetime import datetime

@strawberry.type
class CotacaoType(Cotacao):
    pass

@strawberry.type
class CotacaoBaseType(strawberry.BaseModel):
    moeda_base: str
    taxas: Dict[str, float]
    ultima_atualizacao: datetime
    fonte: str

cotacao_repo = CotacaoRepository()
cotacao_service = CotacaoService(repository=cotacao_repo)

@strawberry.type
class Query:
    @strawberry.field
    async def cotacao(
        self,
        moeda_base: str,
        moeda_alvo: Optional[str] = None
    ) -> Union[CotacaoType, CotacaoBaseType, str]:
        """
        Consulta a cotação de moedas.
        """
        if moeda_alvo:
            resultado = await cotacao_service.obter_cotacao(moeda_base, moeda_alvo)
            if "mensagem" in resultado:
                return resultado["mensagem"]
            return CotacaoType(**resultado)
        else:
            resultado = await cotacao_service.obter_cotacao(moeda_base)
            if "mensagem" in resultado:
                return resultado["mensagem"]
            return CotacaoBaseType(**resultado)

schema = strawberry.Schema(query=Query)