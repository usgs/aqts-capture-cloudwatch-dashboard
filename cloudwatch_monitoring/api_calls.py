"""
module for making aws api calls using aws python sdk (boto3)

"""

import boto3


class APICalls:
    def __init__(self, region, client_type, deploy_stage):
        """
        Constructor for the APICalls class.

        :param region: usually 'us-west-2'
        :param client_type: a string determining the boto3 client type (lambda, sqs, stepfunction, rds, etc.)
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.boto3_client = boto3.client(client_type, region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_state_machines(self):
        """
        Grab all the state machines for the specified account for a given region.

        :return: response: a page of state machines in the account.
        :rtype: dict
        """

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_state_machines
        # TODO this pagination logic exists in other modules as well, consider moving it into its own utility
        # TODO module or trying to get a proper boto3 paginator to work...
        response = {}
        next_token = None
        while True:
            if next_token:
                response_iterator = self.boto3_client.list_state_machines(
                        # maxResults has to be set in order to receive a pagination token in the response
                        maxResults=10,
                        nextToken=next_token)
                response['stateMachines'].extend(response_iterator['stateMachines'])
            else:
                response_iterator = self.boto3_client.list_state_machines(
                        maxResults=10
                )
                response.update(response_iterator)
            try:
                next_token = response_iterator['nextToken']
            except KeyError:
                # no more pages, move on
                break

        return response

    def is_iow_state_machine_filter(self, state_machine_arn):
        """
        Apply filters to determine if the state machine is a tagged IOW asset in the correct tier.

        :param state_machine_arn: A single state machine arn
        :return: is_iow_state_machine: is this an IOW state machine or not
        :rtype: bool
        """
        is_iow_state_machine = False

        # filtering on deploy tier, which we capitalize
        if self.deploy_stage.upper() in state_machine_arn:

            # launch API call to grab the tags for the state machine
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_tags_for_resource
            state_machine_tags = self.boto3_client.list_tags_for_resource(resourceArn=state_machine_arn)

            # we only want state machines that are tagged as 'IOW'
            if 'tags' in state_machine_tags:
                for tag in state_machine_tags['tags']:
                    if 'key' in tag:
                        if 'wma:organization' in tag['key']:
                            if 'IOW' == tag['value']:
                                is_iow_state_machine = True

        return is_iow_state_machine
