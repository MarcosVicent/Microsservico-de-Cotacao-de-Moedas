import httpx
import redis
import json
from datetime import datetime
from typing import Dict, Optional
from app.models.cotacao import CotacaoBase
from app.core.config import settings

class CotacaoRepository:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.cache_ttl = settings.CACHE_TTL_SECONDS
        self.api_key = settings.API_KEY_FINANCEIRA
        self.api_url = "https://open.er-api.com/v6/latest/"

    async def get_cotacao_from_api(self, moeda_base: str) -> Optional[CotacaoBase]:
        """Busca a cotação de uma API externa (simulada)."""
        cache_key = f"cotacao_{moeda_base.upper()}"
        cached_data = self.redis_client.get(cache_key)

        if cached_data:
            print(f"Cotação para {moeda_base} recuperada do Redis Cache.")
            data = json.loads(cached_data)
            return CotacaoBase(
                moeda_base=data['moeda_base'],
                taxas=data['taxas'],
                ultima_atualizacao=datetime.fromisoformat(data['ultima_atualizacao'])
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}{moeda_base.upper()}")
                response.raise_for_status()
                data = response.json()

                if data.get("result") != "success":
                    print(f"Erro na API externa: {data.get('error-type')}")
                    return None

                cotacao_data = CotacaoBase(
                    moeda_base=data["base_code"],
                    taxas=data["rates"],
                    ultima_atualizacao=datetime.fromtimestamp(data["time_last_update_unix"])
                )

                self.redis_client.setex(cache_key, self.cache_ttl, cotacao_data.model_dump_json())
                print(f"Cotação para {moeda_base} salva no Redis Cache.")
                return cotacao_data
        except httpx.HTTPStatusError as e:
            print(f"Erro HTTP ao buscar dados da API: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar cotação: {e}")
            return None