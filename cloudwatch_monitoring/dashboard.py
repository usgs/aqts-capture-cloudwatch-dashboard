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

    # set starting and default values for widget positioning and dimensions
    x, y = [0, 0]
    width, height = [3, 3]
    max_width = 12

    # initialize the array of widgets
    widgets = []

    # get all the lambdas in the account
    all_lambdas_response = lambda_client.list_functions(MaxItems=1000)

    # grab the 'IOW' tagged lambdas and make widgets for them
    for function in all_lambdas_response['Functions']:
        function_metadata = lambda_client.get_function(FunctionName=function['FunctionName'])
        if 'Tags' in function_metadata:
            if 'wma:organization' in function_metadata['Tags']:
                if 'IOW' == function_metadata['Tags']['wma:organization']:
                    # print('The lambda function and tag: ' + function['FunctionName'] + ' ' + function_metadata['Tags']['wma:organization'])
                    widget = {
                        'type': 'metric',
                        'x': x,
                        'y': y,
                        'height': height,
                        'width': width,
                        'properties': {
                            "metrics": [
                                ["AWS/Lambda", "ConcurrentExecutions", "FunctionName", function['FunctionName']],
                                [".", "Invocations", ".", ".", {"stat": "Sum"}],
                                [".", "Duration", ".", "."],
                                [".", "Errors", ".", ".", {"stat": "Sum"}],
                                [".", "Throttles", ".", "."]
                            ],
                            "view": "singleValue",
                            "region": region,
                            "title": function['FunctionName'],
                            "period": 300,
                            "stacked": False,
                            "stat": "Average"
                        }
                    }

                    # add each widget to the widget list
                    widgets.append(widget)

                    # iterate the position on the dashboard for the next widget
                    x += width
                    if (x + width > max_width):
                        x = 0
                        y += height

    # TODO other widget iterations to follow (ec2, fargate, rds, custom widgets, etc.)

    # create the dashboard when the widget iterations are complete
    dashboard_body = {'widgets': widgets}
    dashboard_body_json = json.dumps(dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=dashboard_body_json)