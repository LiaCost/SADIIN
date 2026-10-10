import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class DatasusClient:
    BASE_URL = "https://apidadosabertos.saude.gov.br"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        reraise=True
    )
    async def get(self, endpoint: str, params: dict = None):
        url = f"{self.BASE_URL}/{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            return response.json()