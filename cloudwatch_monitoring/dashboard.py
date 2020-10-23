import boto3
import json
import os

# Entrypoint from the jenkins script, everything inside __name__ == '__main__' will be executed
if __name__ == '__main__':

    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'
    deploy_stage = os.getenv('DEPLOY_STAGE')

    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    lambda_client = boto3.client("lambda", region_name=region)

    # set starting and default values for lambda widget positioning and dimensions
    x, y = [0, 0]
    lambda_widget_width, lambda_widget_height = [24, 3]
    lambda_widget_max_width = 24

    # initialize the array of widgets
    widgets = []

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
                    widgets.append(widget)

                    # iterate the position on the dashboard for the next widget
                    x += lambda_widget_width
                    if (x + lambda_widget_width > lambda_widget_max_width):
                        x = 0
                        y += lambda_widget_height

    # TODO other widget iterations to follow (ec2, fargate, rds, custom widgets, etc.)

    # create the dashboard when the widget iterations are complete
    dashboard_body = {'widgets': widgets}
    dashboard_body_json = json.dumps(dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=dashboard_body_json)