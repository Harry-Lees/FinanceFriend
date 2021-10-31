from fastapi import APIRouter, Depends
from deps import get_database
from sqlalchemy import func, desc, text
from models import Transaction, Merchant
from math import ceil
from datetime import datetime

router = APIRouter()


@router.get('/top_merchants')
def pi_spend_by_category(account_id, database=Depends(get_database)):
    res = database.query(Transaction.merchant, func.count(Transaction.merchant).label('visits'), func.sum(Transaction.amount).label('net_spend')).where(Transaction.currency=='GBP', Transaction.account_id==account_id, Transaction.amount>0).group_by(Transaction.merchant).order_by(desc(func.sum(Transaction.amount))).limit(3).all()
    return res


@router.get('/tip_jar')
def tip_jar(account_id, database=Depends(get_database)):
    """returns pounds saved by rounding up all purchases nearest penny"""

    res = database.query(Transaction.amount).where(Transaction.currency == 'GBP', Transaction.account_id == account_id).all()

    total = sum(ceil(item[0]) - item[0] for item in res)
    return round(total, 2)


@router.get('/online_vs_instore')
def online_vs_instore(account_id, database=Depends(get_database)):
    """returns a dict with keys 'online' and 'instore' which represent number of transactions of each type"""
    res = database.query(Transaction.point_of_sale, func.count(Transaction.point_of_sale).label('count')).where(Transaction.account_id == account_id, Transaction.currency == 'GBP').group_by(Transaction.point_of_sale).all()
    return res 

@router.get('/weekend_vs_weekday')
def weekend_vs_weekday(account_id, database=Depends(get_database)):
    timestamps = database.execute(text("select timestamp, amount from transaction_tab where account_id=(:account_id) and currency='GBP' and amount>0"), {'account_id': int(account_id)}).all()
    n_weekends=0
    spend_weekends=0
    n_weekdays=0
    spend_weekdays=0
    for time in timestamps:
        # this is stupid lol
        month = int(str(time[0])[5]+str(time[0])[6])
        day = int(str(time[0])[8]+str(time[0])[9])
        d=datetime(2021, month, day)
        if d.weekday() >4:
            n_weekends+=1
            spend_weekends+=time[1]
        else:
            n_weekdays+=1
            spend_weekdays+=time[1]
    ret = {'n_weekends':round(n_weekends, 2),
            'spend_weekends':round(spend_weekends,2),
            'n_weekdays':round(n_weekdays, 2),
            'spend_weekdays':round(spend_weekdays, 2)}
    return ret
