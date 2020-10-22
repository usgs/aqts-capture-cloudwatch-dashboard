import boto3
import json
import logging

# Entrypoint from the jenkins script, everything inside __name__ == '__main__' will be executed
if __name__ == '__main__':

    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    cloudwatch_client  = boto3.client("cloudwatch")
    lambda_client = boto3.client("lambda")

    # set starting and default values for widget positioning and dimensions
    x, y = [0, 0]
    width, height = [3, 3]
    max_width = 12

    # initialize the array of widgets
    widgets = []

    logger.info('Did we make it this far?')

