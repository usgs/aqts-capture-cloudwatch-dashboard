import boto3
import json
import os
from cloudwatch_monitoring.lambdas import create_lambda_widgets

# Entrypoint from the jenkins script
if __name__ == '__main__':
    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'
    deploy_stage = os.getenv('DEPLOY_STAGE')

    # add widgets per asset type
    widgets = []
    widgets.extend(create_lambda_widgets(region, deploy_stage))
    # TODO other widget iterations to follow (ec2, fargate, rds, custom widgets, etc.)

    # create the dashboard when the widget list is complete
    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    dashboard_body = {'widgets': widgets}
    dashboard_body_json = json.dumps(dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=dashboard_body_json)
