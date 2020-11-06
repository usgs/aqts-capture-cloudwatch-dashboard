"""
module for creating lambda widgets

"""

import boto3
from .lookups import (dashboard_lambdas, custom_lambda_widgets)


def get_all_lambda_metadata(region):
    """
    Using the AWS python sdk (boto3), grab all the lambda functions for the specified account for a given region.

    :param region: The region, for us that's usually us-west-2
    :return: response: metadata about each lambda in the account.
    :rtype: dict
    """
    lambda_client = boto3.client("lambda", region_name=region)

    # Currently you cannot get more than 50 functions from the list_functions call in a single request.  Thus, we need
    # to iterate over the entire list of available functions in the account using the provided NextMarker string, which
    # allows us to paginate. boto3 does have pagination tools, but I have found the documentation generally unhelpful,
    # so below is a more manual approach.
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
    # TODO this pagination logic exists in the sqs module as well, consider moving it into its own utility
    # TODO module or trying to get a proper boto3 paginator to work...
    response = {}
    marker = None
    while True:
        if marker:
            response_iterator = lambda_client.list_functions(
                     MaxItems=10,
                     Marker=marker)
            response['Functions'].extend(response_iterator['Functions'])
        else:
            response_iterator = lambda_client.list_functions(
                    MaxItems=10
            )
            response.update(response_iterator)
        try:
            marker = response_iterator['NextMarker']
        except KeyError:
            # no more pages, move on
            break

    return response


def is_iow_asset_filter(function, deploy_stage, region):
    """
    Apply filters to determine if the function is a tagged IOW asset in the correct tier.

    :param function: A single lambda function's metadata
    :param deploy_stage: The specified deployment environment (DEV, TEST, QA, PROD-EXTERNAL)
    :param region: typically 'us-west-2'
    :return: is_iow_lambda: is this an IOW asset or not
    :rtype: bool
    """
    lambda_client = boto3.client("lambda", region_name=region)

    # this is the name we specify in each lambda's serverless.yml config file.
    function_name = function['FunctionName']

    is_iow_lambda = False

    # filtering on deploy tier
    if deploy_stage.upper() in function_name:

        # launch API call to grab metadata for a specific function, we are interested in the tags
        function_metadata = lambda_client.get_function(FunctionName=function_name)

        # we only want lambdas that are tagged as 'IOW'
        if 'Tags' in function_metadata:
            if 'wma:organization' in function_metadata['Tags']:
                if 'IOW' == function_metadata['Tags']['wma:organization']:
                    if 'CleanupFunction' not in function_name:
                        is_iow_lambda = True

    return is_iow_lambda


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

    # grab all the lambdas in the account/region
    all_lambda_metadata_response = get_all_lambda_metadata(region)

    # iterate over the list of lambda metadata and create widgets for the assets we care about based on filters
    for function in all_lambda_metadata_response['Functions']:

        if is_iow_asset_filter(function, deploy_stage, region):
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
