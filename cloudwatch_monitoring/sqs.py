"""
module for creating sqs widgets

"""

import boto3


def create_sqs_widgets(region, deploy_stage, positioning):
    """
    Creates the list of SQS widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :return: list of SQS widgets
    :rtype: list
    """
    sqs_widgets = []

    # grab all the sqs queue urls in the account/region
    all_sqs_queue_urls_response = get_all_sqs_queue_urls(region)
    print(all_sqs_queue_urls_response)

    # TODO do stuff

    return sqs_widgets


def get_all_sqs_queue_urls(region):
    """
    Using the AWS python sdk (boto3), grab all the sqs queue urls for the specified account for a given region.

    :param region: The region, for us that's usually us-west-2
    :return: response: a page of sqs urls in the account.
    :rtype: dict
    """
    sqs_client = boto3.client("sqs", region_name=region)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.list_queues
    response = {}
    next_token = None
    while True:
        if next_token:
            response_iterator = sqs_client.list_queues(
                    # MaxResults has to be set in order to receive a pagination token in the response
                    MaxResults=10,
                    NextToken=next_token)
            response['QueueUrls'].extend(response_iterator['QueueUrls'])
        else:
            response_iterator = sqs_client.list_queues(
                    MaxResults=10
            )
            response.update(response_iterator)
        try:
            next_token = response_iterator['NextToken']
        except KeyError:
            # no more pages, move on
            break

    return response
