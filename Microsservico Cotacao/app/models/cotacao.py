from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class Cotacao(BaseModel):
    moeda_base: str = Field(..., description="A moeda de referência (ex: USD).")
    moeda_alvo: str = Field(..., description="A moeda a ser comparada (ex: BRL).")
    valor: float = Field(..., description="O valor da cotação.")
    ultima_atualizacao: datetime = Field(..., description="Timestamp da última atualização da cotação.")
    fonte: str = Field("API Externa", description="A fonte dos dados.")

class CotacaoBase(BaseModel):
    moeda_base: str = Field(..., description="A moeda de referência (ex: USD).")
    taxas: Dict[str, float] = Field(..., description="Dicionário de taxas de câmbio para outras moedas.")
    ultima_atualizacao: datetime = Field(..., description="Timestamp da última atualização da cotação.")
    fonte: str = Field("API Externa", description="A fonte dos dados.")