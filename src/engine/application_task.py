import logging

from base.model import MongoDbEntityCollection
from process.business import BusinessTask
from entity.application import Application

class ApplicationTask(BusinessTask):

    IN_MONGO_DB = 'mongodb'
    IN_ACTIVATION = 'activation'
    IN_IS_VALID = 'is_valid'
    IN_VALIDATION_MESSAGE = 'validation_message'
    IN_PRODUCT_CONFIG = 'product_config'

    OUT_APPLICATION = 'application'

    COLLECTION_APPLICATIONS = 'applications'

    def setup(self, *args, **kwargs):
        self.set_input(ApplicationTask.IN_MONGO_DB, args[0])
        self.set_input(ApplicationTask.IN_ACTIVATION, args[1])
        self.set_input(ApplicationTask.IN_IS_VALID, args[2])
        self.set_input(ApplicationTask.IN_VALIDATION_MESSAGE, args[3])
        self.set_input(ApplicationTask.IN_PRODUCT_CONFIG, args[4])


    def business_logic(self):
        mongodb = self.input(ApplicationTask.IN_MONGO_DB)
        activation = self.input(ApplicationTask.IN_ACTIVATION)
        is_valid = self.input(ApplicationTask.IN_IS_VALID)
        validation_message = self.input(ApplicationTask.IN_VALIDATION_MESSAGE)
        product_config = self.input(ApplicationTask.IN_PRODUCT_CONFIG)

        task = self
        process = task.process
        application = Application(process.id, task.id, activation, is_valid, validation_message, product_config)

        application_collection = MongoDbEntityCollection(ApplicationTask.COLLECTION_APPLICATIONS, Application)
        application_collection.insert_one(mongodb, application)

        self.set_output(ApplicationTask.OUT_APPLICATION, application)
