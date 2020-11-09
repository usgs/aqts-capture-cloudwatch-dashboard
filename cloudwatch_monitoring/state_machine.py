"""
module for creating state machine widgets

"""
from .lookups import state_machines
from .api_calls import APICalls


def create_state_machine_widgets(region, deploy_stage, positioning):
    """
    Creates the list of state machine widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :return: list of state machine widgets
    :rtype: list
    """
    api_calls = APICalls(region, 'stepfunctions', deploy_stage)
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
