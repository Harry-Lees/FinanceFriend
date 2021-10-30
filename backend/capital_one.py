import aiohttp
from typing import Dict, Any, Optional
import asyncio
import os

class CapitalOne:
    def __init__(self, token: str) -> None:
        self.headers: Dict[str, str] = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'version': '1.0',
        }

        # create aiohttp Session and set global headers
        self.session = aiohttp.ClientSession()
        self.session.headers.update(self.headers)

        self.base_url: str = 'https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data'

    def build_url(self, path: str) -> str:
        return os.path.join(self.base_url, path)

    async def create_random_account(self, quantity: int = 1, num_transactions: int = 25, live_balance: bool = True) -> Dict[str, Any]:
        """create a random Account through the CapitalOne API"""

        data: Dict[str, Any] = {
            'quantity': quantity,
            'num_transactions': num_transactions,
            'live_balance': live_balance,
        }

        url: str = self.build_url('accounts/create')
        async with self.session.post(url, json=data) as response:
            return await response.json()


    async def create_custom_account(self, **kwargs) -> None:
        """create a custom account through the CapitalOne API"""

        url: str = self.build_url('accounts/create')
        async with self.session.post(url, json=kwargs) as response:
            return await response.json()


    async def get_all_accounts(self, filter_key: Optional[str] = None, filter_relation: Optional[str] = None, filter_value: Optional[str] = None) -> None:
        """gets all accounts created with the given auth token"""

        params: Dict[str, Any] = {
            'filterKey': filter_key,
            'filterRelation': filter_relation,
            'filterValue': filter_value,
        }
        # pop all empty items from the Dict
        params = {k: v for k, v in params.items() if v is not None}

        url: str = self.build_url('accounts')
        async with self.session.get(url, params=params) as response:
            return await response.json()['Accounts']


    async def get_account_by_id(self) -> None:
        pass


    async def create_random_transaction(self) -> None:
        pass


    async def create_custom_transaction(self) -> None:
        pass


    async def get_all_transactions(self) -> None:
        pass


    async def get_transactions_by_id(self) -> None:
        pass


    async def create_fraudulent_transaction(self) -> None:
        pass

async def main():
    token: str = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2MzQxNjk2MDAsImFwaV9zdWIiOiI0MDVjMGUyNDRlOWI3OWU4Y2M1M2ZiMGYwN2VmMTljYjIwMmUxZWQ2ZmViNWRhMzBkZjZhYmNjNGFmMjAyY2FhMTY0MjM3NzYwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTY0MjM3NzYwMCwiZGV2ZWxvcGVyX2lkIjoiNDA1YzBlMjQ0ZTliNzllOGNjNTNmYjBmMDdlZjE5Y2IyMDJlMWVkNmZlYjVkYTMwZGY2YWJjYzRhZjIwMmNhYSJ9.fNPaRoOcD1LT0niT6VTTpAkUWUq5JbLTWIOxf0x_zm08hKgrUjuYI6gWTUkWbgp579t7N5Qjkoc_u-n44dc6FQw8_MxXxFZTJY1xObTCk5expEbHBDw3B6nLrv8iL1k27dHMhh5O1u142YAz24nhuKJV4EJjqHrbDsnebg_jjTQofDu072JBwXY445f_CJbwaaimmLUIpw7_CGVTuWzd52gbxEK9Uo8Q2O4zBcTvkjOVDQ7k5S5Y6x7mU-9yePcFXpkvvYEXXs4F6w3sSIf6ecjrLZUovHh3J7vSPp_I3jy-EBlatuzNP4Qui6zUhZU598GsFmwNW_RZjFGpst4rJw'
    api = CapitalOne(token)
    response = await api.get_all_accounts()
    print(response)
    await api.session.close()

if __name__ == '__main__':
    asyncio.run(main())
