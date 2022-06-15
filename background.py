from celery import Celery
from datetime import datetime, timedelta
from celery.signals import worker_ready
from app import event_filter, nft_address, nft_instance, l


BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend = BACKEND, broker = BROKER)
celery.conf.beat_schedule = {
    "read_event": {
        "task": "read_event",
        "schedule": timedelta(seconds = 10)
    },  
}

@celery.task(name = 'read_event')
def read_event():
    global l
    print(l)
    #event_filter = nft_instance.events.Transfer.createFilter(fromBlock=1, toBlock='latest')
    #print(event_filter.get_all_entries())
    #print(nft_address)
    #print(nft_instance)
    return 'OK'