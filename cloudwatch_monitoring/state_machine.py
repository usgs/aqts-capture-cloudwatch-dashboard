"""
module for creating state machine widgets

"""
import boto3

from .lookups import state_machines


def create_state_machine_widgets(region, deploy_stage, positioning):
    """
    Creates the list of state machine widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :return: list of state machine widgets
    :rtype: list
    """
    api_calls = StepFunctionAPICalls(region, deploy_stage)
    state_machine_widgets = []

    # grab all the state machines in the account/region
    all_state_machines_response = api_calls.get_all_state_machines()

    # iterate over the list of state machines and create widgets for the assets we care about based on filters
    for state_machine in all_state_machines_response['stateMachines']:

        state_machine_arn = state_machine['stateMachineArn']

        if api_calls.is_iow_state_machine_filter(state_machine_arn):

            # incoming state machine: TODO put example here
            # we want the state machine name after the last "/"
            state_machine_name = state_machine['name']

            tier_agnostic_state_machine_name = state_machine_name.replace(f"-{deploy_stage}", '')
            
            try:
                widget_title = state_machines[tier_agnostic_state_machine_name]['title']
            except KeyError:
                # no title in the lookup for this resource
                widget_title = state_machine_name

            # set dimensions of the state machine widgets
            positioning.width = 12
            positioning.height = 6

            state_machine_widget = {
                'type': 'metric',
                'x': positioning.x,
                'y': positioning.y,
                'height': positioning.height,
                'width': positioning.width,
                'properties': {
                        "metrics": [
                            ["AWS/States", "ExecutionsStarted", "StateMachineArn", state_machine_arn],
                            [".", "ExecutionsSucceeded", ".", "."],
                            [".", "ExecutionsFailed", ".", "."],
                            [".", "ExecutionsTimedOut", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": region,
                        "stat": "Sum",
                        "period": 60,
                        "title": widget_title
                }
            }

            state_machine_widgets.append(state_machine_widget)
            positioning.iterate_positioning()

    return state_machine_widgets


class StepFunctionAPICalls:
    def __init__(self, region, deploy_stage):
        """
        Constructor for the StepFunctionAPICalls class.

        :param region: usually 'us-west-2'
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.sfn_client = boto3.client('stepfunctions', region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_state_machines(self):
        """
        Grab all the state machines for the specified account for a given region.

        :return: response: a page of state machines in the account.
        :rtype: dict
        """

        # TODO maybe get a paginator to work instead of 'manual' iteration
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_state_machines
        response = {}
        next_token = None
        while True:
            if next_token:
                response_iterator = self.sfn_client.list_state_machines(
                        # maxResults has to be set in order to receive a pagination token in the response
                        maxResults=10,
                        nextToken=next_token)
                response['stateMachines'].extend(response_iterator['stateMachines'])
            else:
                response_iterator = self.sfn_client.list_state_machines(
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
            state_machine_tags = self.sfn_client.list_tags_for_resource(resourceArn=state_machine_arn)

            # we only want state machines that are tagged as 'IOW'
            if 'tags' in state_machine_tags:
                for tag in state_machine_tags['tags']:
                    if 'key' in tag:
                        if 'wma:organization' in tag['key']:
                            if 'IOW' == tag['value']:
                                is_iow_state_machine = True

        return is_iow_state_machine
