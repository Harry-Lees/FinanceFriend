from fastapi import APIRouter, Depends
from deps import get_database
from sqlalchemy import func, desc
from models import Transaction, Merchant
router = APIRouter()



@router.get('/top_merchants')
def pi_spend_by_category(account_id, database=Depends(get_database)):
    res = database.query(Transaction.merchant, func.count(Transaction.merchant).label('visits'), func.sum(Transaction.amount).label('net_spend')).where(Transaction.currency=='GBP', Transaction.account_id==account_id, Transaction.amount>0).group_by(Transaction.merchant).order_by(desc(func.sum(Transaction.amount))).limit(3).all()
    return res
