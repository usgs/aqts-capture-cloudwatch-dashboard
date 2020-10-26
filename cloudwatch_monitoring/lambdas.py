"""
module for creating lambda widgets

"""
import boto3


def create_lambda_widgets(region, deploy_stage):
    """
    Iterate over an account's list of lambdas and create generic widgets for those with
    wma:organization = 'IOW' tags.

    :return: List of lambda widgets
    :rtype: list
    """

    # create the aws python sdk lambda client
    lambda_client = boto3.client("lambda", region_name=region)

    # set starting and default values for lambda widget positioning and dimensions
    x, y = [0, 0]
    lambda_widget_width, lambda_widget_height = [24, 3]
    lambda_widget_max_width = 24

    # initialize a list of lambda widgets
    lambda_widgets = []

    # First, create generic widgets for each lambda tagged 'IOW' in the account.
    # get all the lambdas in the account
    all_lambdas_response = lambda_client.list_functions(MaxItems=1000)

    # we are only interested in a subset of lambdas in the account
    for function in all_lambdas_response['Functions']:

        # this is the name we specify in each lambda's serverless.yml config file.
        function_name = function['FunctionName']

        # first, we can limit some upcoming API calls by filtering on deploy tier
        if deploy_stage.upper() in function_name:

            # Launch a new API call to grab metadata for a specific function, specifically we are interested in the tags
            function_metadata = lambda_client.get_function(FunctionName=function_name)

            # we only want lambdas that are tagged as 'IOW'
            if 'Tags' in function_metadata:
                tags = function_metadata['Tags']
                if 'wma:organization' in tags:
                    if 'IOW' == tags['wma:organization']:
                        # Not sure what SC-807615458658-pp-7rv6atnjwitc6-D-CleanupFunction-1LIPB7Y7PMUWB is, filter it out
                        if 'CleanupFunction' not in function_name:

                            # generic widget template taken from existing custom dashboard
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

                            # add each widget to the widget list
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

    lambda_widgets.append(concurrent_lambdas)

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

    lambda_widgets.append(error_handler_activity)

    return lambda_widgets
