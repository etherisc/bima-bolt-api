from process.task import Task

class BusinessProcess(Task):
    
    def __init__(self, id, log, *args, **kwargs):
        self.log_handler = log
        super().__init__(id, Task.TYPE_PROCESS, *args, **kwargs)

    def business_tx_log(self, message):
        self.log_handler.log(self, None, message)

class BusinessTask(Task):
    
    def __init__(self, id, process, *args, **kwargs):
        self.process = process
        super().__init__(id, Task.TYPE_TASK, *args, **kwargs)

    def start(self, blocking=True):
        super().start(blocking)

    def business_tx_log(self, message):
        self.process.log_handler.log(self.process, self, message)

