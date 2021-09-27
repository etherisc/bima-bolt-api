import logging
import threading
import uuid

from abc import ABC, abstractmethod
from util.nvl import nvl

class Task(object):
    
    TYPE_PROCESS = 'process'
    TYPE_TASK = 'task'

    STATUS_CREATED = 'created'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_ERROR = 'error'

    RAISE_EXCEPTIONS = 'raise_exceptions'

    def __init__(self,  id, kind, *args, **kwargs):
        super().__init__()

        logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")

        self.id = nvl(id, str(uuid.uuid4()))
        self.status = Task.STATUS_CREATED
        self.kind = kind
        self.thread = None
        self.raise_exceptions = False
        self.error_message = None
        self.error_exception = None

        if Task.RAISE_EXCEPTIONS in kwargs:
            self.raise_exceptions = kwargs[Task.RAISE_EXCEPTIONS]
            logging.info("TASK parameter {} set to {} (value stored: {})".format(Task.RAISE_EXCEPTIONS, kwargs[Task.RAISE_EXCEPTIONS], self.raise_exceptions))

        # prepare container for task/process input and output data
        self.data_in = {}
        self.data_out = {}

        # call the task/process setup logic
        self.setup(*args, **kwargs)

        # set status and create business tx entry
        self.business_tx_log('{} created'.format(self.kind))

    @abstractmethod
    def setup(self, *args, **kwargs):
        logging.warning('setup() empty base class implementation')

    @abstractmethod
    def business_logic(self):
        logging.warning('run_business_logic() empty base class implementation')

    @abstractmethod
    def business_tx_log(self, message):
        logging.warning('business_tx_log() empty base class implementation')
    
    def set_input(self, attribute, value):
        self.data_in[attribute] = value
    
    def input(self, attribute):
        if attribute in self.data_in:
            return self.data_in[attribute]

        logging.warning("unknown input attribute '{}'. returning None".format(attribute))
        return None
    
    def set_output(self, attribute, value):
        self.data_out[attribute] = value
    
    def output(self, attribute):
        if attribute in self.data_out:
            return self.data_out[attribute]

        logging.warning("unknown output attribute '{}'. returning None".format(attribute))
        return None
    
    def start(self, blocking=False):
        if self.status != Task.STATUS_CREATED:
            logging.warning('start(): task in {} status, expected: {}. nothing done'.format(self.status, Task.STATUS_CREATED))
            return False
        
        # running of the business logic is done inside _run()
        if blocking:
            self._run()
        else:
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
        
        return True

    def join(self):
        if self.thread:
            self.thread.join()
    
    def complete(self):
        if self.status != Task.STATUS_PROCESSING:
            logging.warning('complete(): task in {} status, expected: {}. nothing done'.format(self.status, Task.STATUS_PROCESSING))
            return False
        
        self.status = Task.STATUS_COMPLETED
        self.business_tx_log('{} completed'.format(self.kind))
        return True

    def error(self, message=None, exception=None):
        if self.status != Task.STATUS_PROCESSING:
            logging.warning('error(): task in {} status, expected: {}. nothing done'.format(self.status, Task.STATUS_PROCESSING))
            return False
        
        self.status = Task.STATUS_ERROR
        self.error_message = message
        self.error_exception = exception

        self.business_tx_log('{} error {} {}'.format(self.kind, nvl(message, '_'), nvl(exception, '_')))
        return True

    def is_alive(self):
        if self.thread:
            return self.thread.is_alive()
        elif self.status in [Task.STATUS_CREATED, Task.STATUS_PROCESSING]:
            return True
        
        return False

    def is_processing(self):
        return self.status == Task.STATUS_PROCESSING

    def is_completed(self):
        return self.status == Task.STATUS_COMPLETED

    def is_error(self):
        return self.status == Task.STATUS_ERROR

    def error_info(self):
        return self.error_message, self.error_exception

    def _run(self):
        self._run_debug_with_exceptions()
        return
        
        try:
            self.status = Task.STATUS_PROCESSING
            self.business_tx_log('{} started'.format(self.kind))

            # trigger the running of the custom business logic
            self.business_logic()

        except Exception as e:
            self.error('business logic exeption', e)

            # TODO FIXME does not yet work as expected
            if self.raise_exceptions:
                raise e
            
            return

    def _run_debug_with_exceptions(self):
        self.status = Task.STATUS_PROCESSING
        self.business_tx_log('{} started'.format(self.kind))

        # trigger the running of the custom business logic
        self.business_logic()
        
        # check error state
        if not self.is_error():
            self.complete()


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread (stoppable thread)
# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread/7752174#7752174 (multiprocessing)
# https://docs.python.org/3/library/threading.html#threading.Thread.is_alive
