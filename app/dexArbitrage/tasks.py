from .celery import app

from .price_pull import update_price, process_data


@app.task(ignore_result=True)
def priceWork():
    update_price()
    return


@app.task(ignore_result=True)
def dealWork():
    process_data()
    return