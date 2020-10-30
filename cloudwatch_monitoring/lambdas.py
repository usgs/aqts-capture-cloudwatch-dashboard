"""
module for creating lambda widgets

"""

import boto3


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


def create_lambda_widgets(region, deploy_stage):
    """
    Iterate over an account's list of lambdas and create generic widgets for those with
    wma:organization = 'IOW' tags.  It also creates some custom widgets.

    :return: List of lambda widgets
    :rtype: list
    """

    # set starting and default values for lambda widget positioning and dimensions
    x, y = [0, 0]
    lambda_widget_width, lambda_widget_height = [24, 3]
    lambda_widget_max_width = 24

    lambda_widgets = []

    # grab all the lambdas in the account/region
    all_lambda_metadata_response = get_all_lambda_metadata(region)

    # iterate over the list of lambda metadata and create widgets for the assets we care about based on filters
    for function in all_lambda_metadata_response['Functions']:

        print(function)

        if is_iow_asset_filter(function, deploy_stage, region):
            function_name = function['FunctionName']

            print(function_name)

            widget = {
                'type': 'metric',
                'x': x,
                'y': y,
                'height': lambda_widget_height,
                'width': lambda_widget_width,
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

            # iterate the position on the dashboard for the next widget
            x += lambda_widget_width
            if x + lambda_widget_width > lambda_widget_max_width:
                x = 0
                y += lambda_widget_height

    # Custom widget for monitoring concurrency of lambdas specifically involved in the ETL
    concurrent_lambdas = {
        'type': 'metric',
        'x': x,
        'y': y,
        'height': lambda_widget_height + 3,
        'width': lambda_widget_width,
        'properties': {
            "metrics": [
                ["AWS/Lambda", "ConcurrentExecutions", "FunctionName", "aqts-capture-dvstat-transform-" + deploy_stage + "-transform", {"label": "DV stat Transformer"}],
                ["...", "aqts-capture-error-handler-" + deploy_stage + "-aqtsErrorHandler", {"label": "Error Handler"}],
                ["...", "aqts-capture-raw-load-" + deploy_stage + "-iowCapture", {"label": "Raw Loader"}],
                ["...", "aqts-capture-stattype-router-" + deploy_stage + "-determineRoute", {"label": "Statistic type router"}],
                ["...", "aqts-capture-trigger-" + deploy_stage + "-aqtsCaptureTrigger", {"label": "Capture trigger"}],
                ["...", "aqts-capture-ts-corrected-" + deploy_stage + "-preProcess", {"label": "TS corrected preprocessor"}],
                ["...", "aqts-capture-ts-description-" + deploy_stage + "-processTsDescription", {"label": "TS descriptions preprocessor"}],
                ["...", "aqts-ts-type-router-" + deploy_stage + "-determineRoute", {"label": "TS type router"}],
                ["...", "aqts-capture-ts-loader-" + deploy_stage + "-loadTimeSeries", {"label": "DV TS loader"}],
                ["...", "aqts-capture-ts-field-visit-" + deploy_stage + "-preProcess", {"label": "Field visit preprocessor"}],
                ["...", "aqts-capture-field-visit-transform-" + deploy_stage + "-transform", {"label": "Field visit transformer"}],
                ["...", "aqts-capture-discrete-loader-" + deploy_stage + "-loadDiscrete", {"label": "Discrete GW loader"}],
                ["...", "aqts-capture-field-visit-metadata-" + deploy_stage + "-preProcess", {"label": "Field visit metadata preprocessor"}],
                ["...", "aqts-capture-raw-load-" + deploy_stage + "-iowCaptureMedium", {"label": "Raw Load Medium"}]
            ],
            "view": "timeSeries",
            "stacked": True,
            "region": region,
            "period": 60,
            "stat": "Average",
            "title": "Concurrent Lambdas (Average per minute)",
        }
    }

    # Custom widget for monitoring error handler invocation counts over time
    error_handler_activity = {
        'type': 'metric',
        'x': x,
        'y': y,
        'height': lambda_widget_height + 3,
        'width': lambda_widget_width,
        'properties': {
            "metrics": [
                ["AWS/Lambda", "ConcurrentExecutions", "FunctionName",
                 "aqts-capture-error-handler-" + deploy_stage + "-aqtsErrorHandler", "Resource",
                 "aqts-capture-error-handler-" + deploy_stage + "-aqtsErrorHandler"],
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

    lambda_widgets.append(concurrent_lambdas)
    lambda_widgets.append(error_handler_activity)

    return lambda_widgets
