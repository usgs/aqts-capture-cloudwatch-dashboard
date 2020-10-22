import boto3
import json

# Entrypoint from the jenkins script, everything inside __name__ == '__main__' will be executed
if __name__ == '__main__':

    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'

    cloudwatch_client  = boto3.client("cloudwatch", region_name=region)
    lambda_client = boto3.client("lambda", region_name=region)

    # set starting and default values for widget positioning and dimensions
    x, y = [0, 0]
    width, height = [3, 3]
    max_width = 12

    # initialize the array of widgets
    widgets = []

    # create lambda widgets
    # get all the lambdas in the account
    iow_lambdas = []
    all_lambdas_response = lambda_client.list_functions(MaxItems=1000)
    for function_name in all_lambdas_response['Functions']['FunctionName']:
        metadata = lambda_client.get_function(function_name)
        tags = lambda_client.list_tags(metadata['FunctionArn'])
        print(tags)
        for wma_tag in tags['wma:organization']:
            if 'IOW' in wma_tag:
                print(wma_tag)
