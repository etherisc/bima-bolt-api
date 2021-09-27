import logging

from base.model import BaseModel

class BaseTask(BaseModel):

    def __init__(self, task_id=None):
        super().__init__(task_id)

        self.assign('id', task_id)

    def run(self):
        logging.warning("run method not implemented")

