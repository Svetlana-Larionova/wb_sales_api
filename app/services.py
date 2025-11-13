import aiohttp
from typing import List, Dict, Any


class WoysaDataLoader:
    def __init__(self):
        self.base_url = "https://woysa.club"

    async def fetch_category_data(self, category_id: int) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/stat/cat"
        params = {
            "id_cat": category_id,
            "price_min": 0,
            "price_max": 1060225,
            "sort": "sum_sale",
            "sort_dir": -1
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])
                    else:
                        print(f"Ошибка: {response.status}")
                        return []
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return []