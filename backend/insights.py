from fastapi import APIRouter, Depends
from deps import get_database
from sqlalchemy import func, desc, text
from models import Transaction, Merchant
from math import ceil
router = APIRouter()



@router.get('/top_merchants')
def pi_spend_by_category(account_id, database=Depends(get_database)):
    res = database.query(Transaction.merchant, func.count(Transaction.merchant).label('visits'), func.sum(Transaction.amount).label('net_spend')).where(Transaction.currency=='GBP', Transaction.account_id==account_id, Transaction.amount>0).group_by(Transaction.merchant).order_by(desc(func.sum(Transaction.amount))).limit(3).all()
    return res

@router.get('/tip_jar')
def tip_jar(account_id, database=Depends(get_database)):
    """ returns pounds saved by rounding up all purchases nearest penny """

    res = database.query(Transaction.amount).where(Transaction.currency == 'GBP', Transaction.account_id == account_id).all()

    total = sum(ceil(item[0]) - item[0] for item in res)
    return round(total, 2)
