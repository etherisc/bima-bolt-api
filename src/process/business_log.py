import logging


from base.model import BaseClass, MongoDbEntityCollection
from process.business_log_entry import BusinessTransactionLogEntry
from util.nvl import nvl

class BusinessTransactionLogHandler(BaseClass):

    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'

    def __init__(self, mongodb):
        super().__init__()

        self.mongodb = mongodb
        self.collection = MongoDbEntityCollection('business_transaction_log', BusinessTransactionLogEntry)
        
        logging.info('{} initialized'.format(self.__class__.__name__))


    def log(self, process, task, message, level=LEVEL_INFO):
        # create entry in business tx log
        self.collection.insert_one(
            self.mongodb, 
            BusinessTransactionLogEntry(process, task, message))
        
        # add entry in application log
        if level == BusinessTransactionLogHandler.LEVEL_INFO:
            logging.info(msg(process, task, message))
        elif level == BusinessTransactionLogHandler.LEVEL_WARNING:
            logging.warning(msg(process, task, message))
        elif level == BusinessTransactionLogHandler.LEVEL_ERROR:
            logging.error(msg(process, task, message))


def msg(process, task, message):
    prc = '_ _ (_)'
    tsk = '_ _ (_)'

    if process:
        prc = '{} {} ({})'.format(process.__class__.__name__, process.id, process.status)

    if task:
        tsk = '{} {} ({})'.format(task.__class__.__name__, task.id, task.status)

    return 'BusinessTxLog {} {} {}'.format(prc, tsk, message)
