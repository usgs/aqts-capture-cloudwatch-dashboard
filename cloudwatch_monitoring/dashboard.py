import boto3
import json
import logging

def create_cloudwatch_dashboard():

    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    logger = logging.getLogger()

    cloudwatch_client  = boto3.client("cloudwatch")
    lambda_client = boto3.client("lambda")

    # set starting and default values for widget positioning and dimensions
    x, y = [0, 0]
    width, height = [3, 3]
    max_width = 12

    # initialize the array of widgets
    widgets = []

    logger.info('Did we make it this far?')

