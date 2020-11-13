"""
module for creating sqs widgets

"""
import boto3

from .lookups import sqs_queues
from .constants import positioning


def create_sqs_widgets(region, deploy_stage):
    """
    Creates the list of SQS widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :return: list of SQS widgets
    :rtype: list
    """
    api_calls = SQSAPICalls(region, deploy_stage)
    sqs_widgets = []

    # grab all the sqs queue urls in the account/region
    all_sqs_queue_urls_response = api_calls.get_all_sqs_queue_urls()

    # iterate over the list of queue urls and create widgets for the assets we care about based on filters
    for queue_url in all_sqs_queue_urls_response['QueueUrls']:
        if api_calls.is_iow_queue_filter(queue_url):

            # incoming queue url: https://us-west-2.queue.amazonaws.com/579777464052/aqts-capture-error-queue-TEST
            # we want the queue name after the last "/"
            url_parts = queue_url.split('/')
            queue_name = url_parts[-1]

            tier_agnostic_queue_name = queue_name.replace(f"-{deploy_stage}", '')

            try:
                widget_title = sqs_queues[tier_agnostic_queue_name]['title']
            except KeyError:
                # no title in the lookup for this resource
                widget_title = queue_name

            # set dimensions of the queue widgets
            positioning['width'] = 12
            positioning['height'] = 6

            queue_widget = {
                'type': 'metric',
                'height': positioning['height'],
                'width': positioning['width'],
                'properties': {
                    "metrics": [
                        ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", queue_name],
                        [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                        [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesDeleted", ".", "."],
                        [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": region,
                    "period": 60,
                    "title": widget_title,
                    "stat": "Average",

                }
            }

            sqs_widgets.append(queue_widget)

    return sqs_widgets


class SQSAPICalls:
    def __init__(self, region, deploy_stage):
        """
        Constructor for the SQSAPICalls class.

        :param region: usually 'us-west-2'
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.sqs_client = boto3.client('sqs', region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_sqs_queue_urls(self):
        """
        Using the AWS python sdk (boto3), grab all the sqs queue urls for the specified account for a given region.

        :return: response: a page of sqs urls in the account.
        :rtype: dict
        """

        # TODO maybe get a paginator to work instead of 'manual' iteration
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.list_queues
        response = {}
        next_token = None
        while True:
            if next_token:
                response_iterator = self.sqs_client.list_queues(
                    # MaxResults has to be set in order to receive a pagination token in the response
                    MaxResults=10,
                    NextToken=next_token)
                response['QueueUrls'].extend(response_iterator['QueueUrls'])
            else:
                response_iterator = self.sqs_client.list_queues(
                    MaxResults=10
                )
                response.update(response_iterator)
            try:
                next_token = response_iterator['NextToken']
            except KeyError:
                # no more pages, move on
                break

        return response

    def is_iow_queue_filter(self, queue_url):
        """
        Apply filters to determine if the queue is a tagged IOW asset in the correct tier.

        :param queue_url: A single queue's url
        :return: is_iow_queue: is this an IOW queue or not
        :rtype: bool
        """
        is_iow_queue = False

        # filtering on deploy tier, which we capitalize
        if self.deploy_stage.upper() in queue_url:
            # launch API call to grab the tags for the queue
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.list_queue_tags
            queue_tags = self.sqs_client.list_queue_tags(QueueUrl=queue_url)

            # we only want queues that are tagged as 'IOW'
            if 'Tags' in queue_tags:
                if 'wma:organization' in queue_tags['Tags']:
                    if 'IOW' == queue_tags['Tags']['wma:organization']:
                        is_iow_queue = True

        return is_iow_queue
