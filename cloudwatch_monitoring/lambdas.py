"""
module for creating lambda widgets

"""
from .lookups import (dashboard_lambdas, custom_lambda_widgets)
from .api_calls import APICalls


def create_lambda_widgets(region, deploy_stage, positioning):
    """
    Iterate over an account's list of lambdas and create generic widgets for those with
    wma:organization = 'IOW' tags.  It also creates some custom widgets.

    :param region: The region, for us that's usually us-west-2
    :param deploy_stage: The specified deployment environment (DEV, TEST, QA, PROD-EXTERNAL)
    :param positioning: The x, y coordinates and height, width dimensions of the widget
    :return: List of lambda widgets
    :rtype: list
    """

    lambda_widgets = []

    # set dimensions for custom lambda widgets
    positioning.width = 12
    positioning.height = 6

    # Custom widget for monitoring error handler invocation counts over time
    error_handler_activity = {
        'type': 'metric',
        'x': positioning.x,
        'y': positioning.y,
        'height': positioning.height,
        'width': positioning.width,
        'properties': {
            "metrics": [
                ["AWS/Lambda", "ConcurrentExecutions", "FunctionName",
                    lambda_properties('error_handler', deploy_stage)['name'], "Resource",
                    lambda_properties('error_handler', deploy_stage)['name']],
                [".", "Invocations", ".", ".", {"stat": "Sum"}]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "title": "Error Handler Activity",
            "period": 60,
            "stat": "Average"
        }
    }

    lambda_widgets.append(error_handler_activity)
    positioning.iterate_positioning()

    # Custom widget for monitoring concurrency of lambdas specifically involved in the ETL
    concurrent_lambdas = {
        'type': 'metric',
        'x': positioning.x,
        'y': positioning.y,
        'height': positioning.height,
        'width': positioning.width,
        'properties': {
            "metrics": generate_concurrent_lambdas_metrics(deploy_stage),
            "view": "timeSeries",
            "stacked": True,
            "region": region,
            "period": 60,
            "stat": "Average",
            "title": "Concurrent Lambdas (Average per minute)",
        }
    }

    lambda_widgets.append(concurrent_lambdas)
    positioning.iterate_positioning()

    api_calls = APICalls(region, 'lambda', deploy_stage)
    # grab all the lambdas in the account/region
    all_lambda_metadata_response = api_calls.get_all_lambda_metadata()

    # iterate over the list of lambda metadata and create widgets for the assets we care about based on filters
    for function in all_lambda_metadata_response['Functions']:

        if api_calls.is_iow_lambda_filter(function):
            function_name = function['FunctionName']

            # set dimensions for generic lambda widgets
            positioning.width = positioning.max_width
            positioning.height = 3

            # TODO add a lookup for each lambda, including a title property.  See sqs and state machine
            # modules for examples, where we use our specified title if we have it, or default to the lambda name if we
            # do not.

            widget = {
                'type': 'metric',
                'x': positioning.x,
                'y': positioning.y,
                'height': positioning.height,
                'width': positioning.width,
                'properties': {
                    "metrics": [
                        ["AWS/Lambda", "ConcurrentExecutions", "FunctionName", function_name],
                        [".", "Invocations", ".", ".", {"stat": "Sum"}],
                        [".", "Duration", ".", "."],
                        [".", "Errors", ".", ".", {"stat": "Sum"}],
                        [".", "Throttles", ".", "."]
                    ],
                    "view": "singleValue",
                    "region": region,
                    "title": function_name,
                    "period": 300,
                    "stacked": False,
                    "stat": "Average"
                }
            }

            lambda_widgets.append(widget)
            positioning.iterate_positioning()

    return lambda_widgets


def lambda_properties(lookup_name, deploy_stage):
    """
    Uses the supplied lookup name to generate lambda name and label key values.

    :param lookup_name: the name of the lookup object containing lambda properties
    :param deploy_stage: the deploy stage (DEV, TEST, QA, PROD-EXTERNAL)
    :return: the lambda name and label
    :rtype: dict
    """
    properties = dashboard_lambdas[lookup_name]
    name = f"{properties['repo_name']}-{deploy_stage}-{properties['descriptor']}"
    label = properties['label']

    return {'name': name, 'label': label}


def generate_concurrent_lambdas_metrics(deploy_stage):
    """
    Generates concurrent lambda widget's metrics.

    :param deploy_stage: The deployment tier
    :return: The list of generated metrics
    :rtype: list
    """

    metrics_list = []
    count = 0

    for name in custom_lambda_widgets['concurrent_lambdas']:
        lambda_attributes = lambda_properties(name, deploy_stage)

        if count < 1:
            # the first metric in the list has some additional stuff
            first_metric = [
                "AWS/Lambda",
                "ConcurrentExecutions",
                "FunctionName",
                lambda_attributes['name'],
                {"label": lambda_attributes['label']}
            ]
            metrics_list.append(first_metric)
        else:
            metric = [
                "...",
                lambda_attributes['name'],
                {"label": lambda_attributes['label']}
            ]
            metrics_list.append(metric)

        count += 1

    return metrics_list
