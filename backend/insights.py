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
    res = database.execute(text("select amount from transaction_tab where currency='GBP' and account_id=(:account_id) and amount>0"),{'account_id': int(account_id)}).all()
    #database.execute(text('SELECT * FROM vehicle(:sensor_id)'), {'sensor_id': sensor_id}).first()
    total=0
    for item in res:
        total+=ceil(item[0])-item[0]
    total=round(total, 2)
    print(total)
    return total

@router.get('/online_vs_instore')
def online_vs_instore(account_id, database=Depends(get_database)):
    """ returns a dict with keys 'online' and 'instore' which represent number of transactions of each type """
    instore = database.execute(text("select count(1) from transaction_tab where account_id=(:account_id) and currency='GBP' and point_of_sale='In-store'"), {'account_id': int(account_id)}).all()
    online = database.execute(text("select count(1) from transaction_tab where account_id=(:account_id) and currency='GBP' and point_of_sale='Online'"), {'account_id': int(account_id)}).all()
    ret = {'online':online[0][0],
            'instore':instore[0][0]
            }
    print(ret)
    return ret

