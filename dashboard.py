import boto3
import json
import os

from cloudwatch_monitoring.lambdas import (create_lambda_widgets, create_lambda_memory_usage_widgets,
                                           # create_ecosystem_switch_widgets,
get_iow_functions)
from cloudwatch_monitoring.rds import create_rds_widgets
from cloudwatch_monitoring.sqs import create_sqs_widgets
from cloudwatch_monitoring.state_machine import create_state_machine_widgets
from cloudwatch_monitoring.sns import create_sns_widgets

# Entrypoint from the jenkins script
if __name__ == '__main__':
    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'
    deploy_stage = os.getenv('DEPLOY_STAGE')

    main_dashboard_widgets = []
    memory_usage_widgets = []
    ecosystem_switch_widgets = []
    elasticsearch_widgets = []

    # grab list of iow lambda functions
    iow_functions = get_iow_functions(region, deploy_stage)
    iow_lambda_widgets = create_lambda_widgets(region, deploy_stage, iow_functions)
    aqts_capture_etl_lambda_widgets = [widget for widget in iow_lambda_widgets
                                       if 'ES logger' not in widget['properties']['title']
                                       or 'es-log-plugin' not in widget['properties']['title']]

    # main dashboard widgets
    main_dashboard_widgets.extend(create_sqs_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_rds_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_state_machine_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_sns_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_lambda_widgets(region, deploy_stage, iow_functions))

    # memory usage widgets
    memory_usage_widgets.extend(create_lambda_memory_usage_widgets(region, iow_functions))

    # ecosystem switch widgets
    # ecosystem_switch_widgets.extend(create_ecosystem_switch_widgets(region, deploy_stage, iow_functions))

    # elasticsearch widgets
    elasticsearch_widgets = [widget for widget in iow_lambda_widgets
                             if 'ES logger' in widget['properties']['title']
                             or 'es-log-plugin' in widget['properties']['title']]

    # create a dashboard for high level monitoring of aqts-capture etl
    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    main_dashboard_body = {'widgets': main_dashboard_widgets}
    main_dashboard_body_json = json.dumps(main_dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=main_dashboard_body_json)

    # create a dashboard for lambda memory usage
    memory_usage_dashboard_body = {'widgets': memory_usage_widgets}
    memory_usage_dashboard_body_json = json.dumps(memory_usage_dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-lambda-memory-usage-" + deploy_stage, DashboardBody=memory_usage_dashboard_body_json)

    # create a dashboard for elasticsearch loggers
    elasticsearch_dashboard_body = {'widgets': elasticsearch_widgets}
    elasticsearch_dashboard_body_json = json.dumps(elasticsearch_dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-elasticsearch-loggers-" + deploy_stage, DashboardBody=elasticsearch_dashboard_body_json)
