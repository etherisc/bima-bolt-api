from base.model import Entity
from util.timestamp import LocalizedTimeStamp

class BusinessTransactionLogEntry(Entity):

    NA = '_'

    def __init__(self, process, task, message):
        super().__init__()

        if process:
            self["process_name"] = process.__class__.__name__
            self["business_tx_id"] = process.id
            self["business_tx_status"] = process.status

        if task:
            self["task_name"] = task.__class__.__name__
            self["task_id"] = task.id
            self["task_status"] = task.status
        else:
            self["task_name"] = BusinessTransactionLogEntry.NA
            self["task_id"] = BusinessTransactionLogEntry.NA
            self["task_status"] = BusinessTransactionLogEntry.NA

        self["message"] = message
        self['timestamp'] = LocalizedTimeStamp.now_utc().isoformat()
