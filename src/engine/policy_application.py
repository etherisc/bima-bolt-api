import logging

from process.business import BusinessProcess

from engine.application_task import ApplicationTask
from engine.policy_task import PolicyTask

from util.timestamp import LocalizedTimeStamp


class PolicyApplicationProcess(BusinessProcess):

    IN_MONGODB = 'mongodb'
    IN_ACTIVATION = 'activation'
    IN_IS_VALID = 'is_valid'
    IN_VALIDATION_MESSAGE = 'validation_message'
    IN_PRODUCT_CONFIG = 'product_config'

    OUT_PRODUCT_CONFIG_ID = 'product_config_id'
    OUT_APPLICATION_ID = 'application_id'
    OUT_POLICY_ID = 'policy_id'

    @staticmethod
    def create_tx_id():
        return "policy-application-{}".format(LocalizedTimeStamp.now_utc().isoformat())

    def setup(self, *args, **kwargs):

        # define process input parameters
        self.set_input(PolicyApplicationProcess.IN_MONGODB, args[0])
        self.set_input(PolicyApplicationProcess.IN_ACTIVATION, args[1])
        self.set_input(PolicyApplicationProcess.IN_IS_VALID, args[2])
        self.set_input(PolicyApplicationProcess.IN_VALIDATION_MESSAGE, args[3])
        self.set_input(PolicyApplicationProcess.IN_PRODUCT_CONFIG, args[4])


    # create and run tasks that comprise the policy application/policy creation jobs' buiness logic
    def business_logic(self):

        # process context for all tasks that define this process
        process = self

        # -------------------------------------------------
        # policy application creation task
        #   IN  mongodb
        #   IN  activation id
        #   IN  is valid
        #   IN  validation message
        #   IN  product config
        #   OUT id of newly created (and persisted) application
        mongodb = self.input(PolicyApplicationProcess.IN_MONGODB)
        activation = self.input(PolicyApplicationProcess.IN_ACTIVATION)
        is_valid = self.input(PolicyApplicationProcess.IN_IS_VALID)
        validation_message = self.input(PolicyApplicationProcess.IN_VALIDATION_MESSAGE)
        product_config = self.input(PolicyApplicationProcess.IN_PRODUCT_CONFIG)

        application_task = ApplicationTask('1', process, mongodb, activation, is_valid, validation_message, product_config)
        application_task.start()

        application = application_task.output(ApplicationTask.OUT_APPLICATION)
        self.set_output(PolicyApplicationProcess.OUT_APPLICATION_ID, application['id'])

        # continue depending on validity state
        if is_valid:
            self.set_output(PolicyApplicationProcess.OUT_PRODUCT_CONFIG_ID, product_config['id'])
        # do not continue (and do not create policy) for invalid applications
        else:
            self.set_output(PolicyApplicationProcess.OUT_PRODUCT_CONFIG_ID, None)
            self.set_output(PolicyApplicationProcess.OUT_POLICY_ID, None)
            return

        # -------------------------------------------------
        # group policy creation task
        #   IN  mongodb
        #   IN  product config
        #   OUT id of newly created (and persisted) group policy
        # TODO add implementation for group policy creation (task_id='2')in case no group policy exists so far
        # this should then trigger the scheduling of a job that calculates the sow day for this group policy
        # once the necessary rainfall data is supposed to be available

        # -------------------------------------------------
        # policy creation task
        #   IN  mongodb
        #   IN  application
        #   IN  product config
        #   OUT id of newly created (and persisted) policy
        policy_task = PolicyTask('3', process, mongodb, application, product_config)
        policy_task.start()

        policy = policy_task.output(PolicyTask.OUT_POLICY)
        self.set_output(PolicyApplicationProcess.OUT_POLICY_ID, policy['id'])
