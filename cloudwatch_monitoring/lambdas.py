"""
module for creating lambda widgets

"""
import boto3
from .lookups import (dashboard_lambdas, custom_lambda_widgets)


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

    api_calls = LambdaAPICalls(region, deploy_stage)
    # grab all the lambdas in the account/region
    all_lambda_metadata_response = api_calls.get_all_lambda_metadata()

    # iterate over the list of lambda metadata and create widgets for the assets we care about based on filters

    dv_widgets = []
    sv_widgets = []
    data_in_widgets = []
    data_purge_widgets = []
    error_widgets = []
    environment_management_widgets = []
    nwis_web_widgets = []
    misc_widgets = []

    for function in all_lambda_metadata_response['Functions']:

        if api_calls.is_iow_lambda_filter(function):

            function_name = function['FunctionName']

            # hack apart the function name to get the repo name and the descriptor
            function_name_parts = function_name.split('-')
            descriptor = function_name_parts[-1]
            function_name_parts_without_tier_or_descriptor = function_name_parts[:-2]
            repo_name = '-'.join(function_name_parts_without_tier_or_descriptor)

            # set the widget title based on the label in our lookups, defaults to the original function name

            widget_etl_branch = 'not defined'
            widget_title = function_name
            for lookup in dashboard_lambdas:
                if repo_name == dashboard_lambdas[lookup]['repo_name'] and descriptor == dashboard_lambdas[lookup]['descriptor']:
                    widget_title = dashboard_lambdas[lookup]['label']
                    widget_etl_branch = dashboard_lambdas[lookup]['etl_branch']

            # set dimensions for generic lambda widgets
            positioning.x = 0
            positioning.width = 24
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
                    "title": widget_title,
                    "period": 300,
                    "stacked": False,
                    "stat": "Average"
                }
            }

            if 'dv' == widget_etl_branch:
                dv_widgets.append(widget)
            elif 'sv' == widget_etl_branch:
                sv_widgets.append(widget)
            elif 'environment_management' == widget_etl_branch:
                environment_management_widgets.append(widget)
            elif 'error_handling' == widget_etl_branch:
                error_widgets.append(widget)
            elif 'data_ingest' == widget_etl_branch:
                data_in_widgets.append(widget)
            elif 'data_purging' == widget_etl_branch:
                data_purge_widgets.append(widget)
            elif 'nwis_web' == widget_etl_branch:
                nwis_web_widgets.append(widget)
            else:
                misc_widgets.append(widget)

            # TODO iterating the positioning among a bunch of lists that are consolidated later doesn't work...
            # positioning.iterate_positioning()

    # TODO widgets come out in exact opposite order
    # add the generic widget groups so they appear together in the dashboard
    # lambda_widgets.extend(error_widgets)
    # lambda_widgets.extend(data_in_widgets)
    # lambda_widgets.extend(dv_widgets)
    # lambda_widgets.extend(sv_widgets)
    # lambda_widgets.extend(nwis_web_widgets)
    # lambda_widgets.extend(data_purge_widgets)
    # lambda_widgets.extend(environment_management_widgets)
    # lambda_widgets.extend(misc_widgets)

    # TODO this works, though seemingly in the wrong order
    # lambda_widgets.extend(misc_widgets)
    # lambda_widgets.extend(environment_management_widgets)
    # lambda_widgets.extend(data_purge_widgets)
    # lambda_widgets.extend(nwis_web_widgets)
    # lambda_widgets.extend(sv_widgets)
    # lambda_widgets.extend(dv_widgets)
    # lambda_widgets.extend(data_in_widgets)
    # lambda_widgets.extend(error_widgets)

    # TODO does this work?
    lambda_widgets = lambda_widgets + error_widgets + data_in_widgets + dv_widgets + sv_widgets + nwis_web_widgets + data_purge_widgets + environment_management_widgets + misc_widgets

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


class LambdaAPICalls:
    def __init__(self, region, deploy_stage):
        """
        Constructor for the LambdaAPICalls class.

        :param region: usually 'us-west-2'
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_lambda_metadata(self):
        """
        Using the AWS python sdk (boto3), grab all the lambda functions for the specified account for a given region.

        :return: response: metadata about each lambda in the account.
        :rtype: dict
        """
        # TODO maybe get a paginator to work instead of 'manual' iteration
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
        response = {}
        marker = None
        while True:
            if marker:
                response_iterator = self.lambda_client.list_functions(
                    MaxItems=10,
                    Marker=marker)
                response['Functions'].extend(response_iterator['Functions'])
            else:
                response_iterator = self.lambda_client.list_functions(
                    MaxItems=10
                )
                response.update(response_iterator)
            try:
                marker = response_iterator['NextMarker']
            except KeyError:
                # no more pages, move on
                break

        return response

    def is_iow_lambda_filter(self, function):
        """
        Apply filters to determine if the function is a tagged IOW asset in the correct tier.

        :param function: A single lambda function's metadata
        :return: is_iow_lambda: is this an IOW asset or not
        :rtype: bool
        """
        function_name = function['FunctionName']

        is_iow_lambda = False

        # filtering on deploy tier
        if self.deploy_stage.upper() in function_name:

            # launch API call to grab metadata for a specific function, we are interested in the tags
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function
            function_metadata = self.lambda_client.get_function(FunctionName=function_name)

            # we only want lambdas that are tagged as 'IOW'
            if 'Tags' in function_metadata:
                if 'wma:organization' in function_metadata['Tags']:
                    if 'IOW' == function_metadata['Tags']['wma:organization']:
                        if 'CleanupFunction' not in function_name:
                            is_iow_lambda = True

        return is_iow_lambda
