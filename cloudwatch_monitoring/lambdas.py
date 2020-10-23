"""
module for creating lambda widgets

"""
import boto3


def create_lambda_widgets(region, lambda_client):
    """
    Iterate over an account's list of lambdas and create generic widgets for those with
    wma:organization = 'IOW' tags.

    :return: List of lambda widgets
    :rtype: list
    """

    # set starting and default values for lambda widget positioning and dimensions
    x, y = [0, 0]
    lambda_widget_width, lambda_widget_height = [24, 3]
    lambda_widget_max_width = 24

    # initialize a list of lambda widgets
    lambda_widgets = []

    # get all the lambdas in the account
    all_lambdas_response = lambda_client.list_functions(MaxItems=1000)

    # we are only interested in a subset of lambdas in the account
    for function in all_lambdas_response['Functions']:

        # this is the name we specify in each lambda's serverless.yml config file.
        function_name = function['FunctionName']

        # separate API call to grab metadata for a specific function, specifically we are interested in the tags
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

    return lambda_widgets
