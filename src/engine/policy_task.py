import logging

from base.model import MongoDbEntityCollection
from process.business import BusinessTask
from entity.policy import Policy
from entity.group_policy import GroupPolicy

class PolicyTask(BusinessTask):

    IN_MONGO_DB = 'mongodb'
    IN_APPLICATION = 'application'
    IN_PRODUCT_CONFIG = 'product_config'

    OUT_POLICY = 'policy'

    COLLECTION_POLICIES = 'policies'
    COLLECTION_GROUP_POLICIES = 'group_policies'

    def setup(self, *args, **kwargs):
        mongodb = args[0]
        application = args[1]
        product_config = args[2]

        self.set_input(PolicyTask.IN_MONGO_DB, mongodb)
        self.set_input(PolicyTask.IN_APPLICATION, application)
        self.set_input(PolicyTask.IN_PRODUCT_CONFIG, product_config)


    def business_logic(self):
        mongodb = self.input(PolicyTask.IN_MONGO_DB)
        application = self.input(PolicyTask.IN_APPLICATION)
        product_config = self.input(PolicyTask.IN_PRODUCT_CONFIG)

        task = self
        process = task.process
        # TODO refactor once policy constructor is refactored to use application
        phone_no = None
        voucher_no = None
        crop = None
        group_policy = PolicyTask._get_group_policy(mongodb, product_config)
        policy = Policy(process.id, task.id, phone_no, voucher_no, crop, application, group_policy)

        policy_collection = MongoDbEntityCollection(PolicyTask.COLLECTION_POLICIES, Policy)
        policy_collection.insert_one(mongodb, policy)

        self.set_output(PolicyTask.OUT_POLICY, policy)


    # TODO handle missing group policy:
    # 
    @staticmethod
    def _get_group_policy(mongodb, product_config):
        product_config_id = product_config['id']
        group_policy_collection = MongoDbEntityCollection(PolicyTask.COLLECTION_GROUP_POLICIES, GroupPolicy)
        group_policy = group_policy_collection.find_one_for_id(mongodb, product_config_id)

        if not group_policy:
            logging.warning("no group policy found for id '{}'".format(product_config_id))

        return group_policy
