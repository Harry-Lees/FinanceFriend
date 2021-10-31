import json
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


    async def create_uk_account(self, quantity: int = 1, num_transactions: int = 25, live_balance: bool = True) -> Dict[str, Any]:
        """create an active UK account using the CapitalOne API"""

        data: Dict[str, Any] = {
            'quantity': quantity,
            'num_transactions': num_transactions,
            'live_balance': live_balance,
            'currencyCode': 'GBP',
            'state': 'open'
        }

        url: str = self.build_url('accounts/create')
        async with self.session.post(url, json=data) as response:
            return await response.json()


    async def add_transactions(self, account_id: int) -> Optional[dict]:
        """create a custom transaction using the CapitalOne API"""
        url = self.build_url(f'transactions/accounts/{account_id}/create')
        data = {'quantity': 25}
        async with self.session.post(url, json=data) as response:
            if 200 <= response.status < 300:
                return await response.json()


    async def get_all_transactions(self, accountId):
        """ get all transactions for a given accountID """
        url = self.build_url(f'transactions/accounts/{accountId}/transactions')
        async with self.session.get(url) as response:
            return await response.json()


    async def add_fraud_transaction(self, account_id: int, fraud_type: Optional[str] = None):
        """generate a pseudo-fradulent transaction"""
        
        data={'fraudType': fraud_type}

        # fradType: 'overseasSpending', 'multipleDeclined', 'unusuallyLarge'
        url = self.build_url(f'fraud/transactions/accounts/{accountId}/create')
        if fraud_type is None:
            data=None

        async with self.session.post(url, json=data) as response:
            return await response.json()


async def main():
    token: str = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2MzQxNjk2MDAsImFwaV9zdWIiOiI0MDVjMGUyNDRlOWI3OWU4Y2M1M2ZiMGYwN2VmMTljYjIwMmUxZWQ2ZmViNWRhMzBkZjZhYmNjNGFmMjAyY2FhMTY0MjM3NzYwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTY0MjM3NzYwMCwiZGV2ZWxvcGVyX2lkIjoiNDA1YzBlMjQ0ZTliNzllOGNjNTNmYjBmMDdlZjE5Y2IyMDJlMWVkNmZlYjVkYTMwZGY2YWJjYzRhZjIwMmNhYSJ9.fNPaRoOcD1LT0niT6VTTpAkUWUq5JbLTWIOxf0x_zm08hKgrUjuYI6gWTUkWbgp579t7N5Qjkoc_u-n44dc6FQw8_MxXxFZTJY1xObTCk5expEbHBDw3B6nLrv8iL1k27dHMhh5O1u142YAz24nhuKJV4EJjqHrbDsnebg_jjTQofDu072JBwXY445f_CJbwaaimmLUIpw7_CGVTuWzd52gbxEK9Uo8Q2O4zBcTvkjOVDQ7k5S5Y6x7mU-9yePcFXpkvvYEXXs4F6w3sSIf6ecjrLZUovHh3J7vSPp_I3jy-EBlatuzNP4Qui6zUhZU598GsFmwNW_RZjFGpst4rJw'
    api = CapitalOne(token)
    create_account_response = await api.create_uk_account()
    accountId = create_account_response['Accounts'][0]['accountId']

    # for some reason generates 2i transactions 
    for i in range(2):
        add_transaction_response = await api.add_transactions(accountId)
    get_all_transactions_response = await api.get_all_transactions(accountId)

    add_fraud_transaction_response = await api.add_fraud_transaction(accountId, 'unusuallyLarge')

    await api.session.close()


if __name__ == '__main__':
    asyncio.run(main())
