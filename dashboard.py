import boto3
import json
import os
from cloudwatch_monitoring.positioning import Positioning
from cloudwatch_monitoring.lambdas import create_lambda_widgets
from cloudwatch_monitoring.rds import create_rds_widgets
from cloudwatch_monitoring.sqs import create_sqs_widgets
from cloudwatch_monitoring.state_machine import create_state_machine_widgets

# Entrypoint from the jenkins script
if __name__ == '__main__':
    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'
    deploy_stage = os.getenv('DEPLOY_STAGE')

    widgets = []
    positioning = Positioning()

    # add widgets per asset type
    widgets.extend(create_sqs_widgets(region, deploy_stage, positioning))
    widgets.extend(create_rds_widgets(region, deploy_stage, positioning))
    widgets.extend(create_state_machine_widgets(region, deploy_stage, positioning))
    widgets.extend(create_lambda_widgets(region, deploy_stage, positioning))
    # TODO other widget iterations to follow (ec2, fargate, state machine, etc.)

    # create the dashboard when the widget list is complete
    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    dashboard_body = {'widgets': widgets}
    dashboard_body_json = json.dumps(dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=dashboard_body_json)
