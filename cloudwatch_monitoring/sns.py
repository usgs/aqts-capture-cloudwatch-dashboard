"""
module for creating sns widgets

"""
import boto3

from .lookups import sns_topics
from .constants import positioning


def create_sns_widgets(region, deploy_stage):
    """
    Creates the list of SNS widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :return: list of SNS widgets
    :rtype: list
    """
    sns_widgets = []

    # set dimensions of the sns title widget
    positioning['width'] = 24
    positioning['height'] = 1

    sns_section_title_widget = {
        'type': 'text',
        'height': positioning['height'],
        'width': positioning['width'],
        'properties': {
            "markdown": "# SNS Status"
        }
    }

    sns_widgets.append(sns_section_title_widget)

    # set dimensions of the topic widget
    positioning['width'] = 12
    positioning['height'] = 6

    # create the error handler widget
    error_handler_sns_notifications_widget = {
        'type': 'metric',
        'height': positioning['height'],
        'width': positioning['width'],
        'properties': {
            "metrics": [
                ["AWS/SNS", "NumberOfMessagesPublished", "TopicName", f"aqts-capture-error-handler-{deploy_stage}-topic", {"label": "messages published"}],
                [".", "NumberOfNotificationsDelivered", ".", ".", {"label": "notifications delivered"}],
                [".", "NumberOfNotificationsFailed", ".", ".", {"label": "notifications failed"}]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "stat": "Sum",
            "period": 3600,
            "title": "Error Handler Failure Notifications (Counts per hour)"
        }
    }

    sns_widgets.append(error_handler_sns_notifications_widget)

    # create the template for the generic sns notifications widget
    sns_notifications_widget = {
        'type': 'metric',
        'height': positioning['height'],
        'width': positioning['width'],
        'properties': {
            "metrics": [],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "stat": "Sum",
            "period": 3600,
            "title": "SNS Failure Notifications (Count per hour)"
        }
    }

    api_calls = SnsApiCalls(region, deploy_stage)

    # grab all the sns topics in the account/region
    response = api_calls.get_all_sns_topics()

    # iterate over the list of sns topics and create widgets for the assets we care about based on filters
    count = 0
    for topic in response['Topics']:
        topic_arn = topic['TopicArn']
        if api_calls.is_iow_topic_filter(topic_arn):
            # incoming topic arn example: arn:aws:sns:us-west-2:579777464052:aqts-capture-error-handler-DEV-topic
            # we want the topic name after the last ":"
            arn_parts = topic_arn.split(':')
            topic_name = arn_parts[-1]
            tier_agnostic_topic_name = topic_name.replace(f"-{deploy_stage}-topic", '')

            metric = generate_number_of_messages_published_metric(topic_name, tier_agnostic_topic_name, count)
            sns_notifications_widget['properties']['metrics'].append(metric)
            count += 1

    sns_widgets.append(sns_notifications_widget)

    return sns_widgets


def generate_number_of_messages_published_metric(topic_name, tier_agnostic_topic_name, count):
    try:
        label = sns_topics[tier_agnostic_topic_name]['title']
    except KeyError:
        # No title property or possibly lookup added for this sns topic yet, default to topic name
        label = topic_name

    if count < 1:
        # the first metric in the list has some additional stuff
        metric = ["AWS/SNS", 'NumberOfMessagesPublished', "TopicName", topic_name, {"label": label}]
    else:
        metric = ["...", topic_name, {"label": label}]

    return metric


class SnsApiCalls:
    def __init__(self, region, deploy_stage):
        """
        Constructor for the SnsApiCalls class.

        :param region: usually 'us-west-2'
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.sns_client = boto3.client('sns', region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_sns_topics(self):
        """
        Using the AWS python sdk (boto3), grab all the sns topics for the specified account for a given region.

        :return: response: a page of sns topics in the account.
        :rtype: dict
        """

        # TODO maybe get a paginator to work instead of 'manual' iteration
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.list_topics
        response = {}
        next_token = None
        while True:
            if next_token:
                response_iterator = self.sns_client.list_topics(
                    NextToken=next_token)
                response['Topics'].extend(response_iterator['Topics'])
            else:
                response_iterator = self.sns_client.list_topics()
                response.update(response_iterator)
            try:
                next_token = response_iterator['NextToken']
            except KeyError:
                # no more pages, move on
                break

        return response

    def is_iow_topic_filter(self, topic_arn):
        """
        Apply filters to determine if the topic is a tagged IOW asset in the correct tier.

        :param topic_arn: A single sns topic arn
        :return: is_iow_topic: is this an IOW topic or not
        :rtype: bool
        """
        is_iow_topic = False

        # filtering on deploy tier, which we capitalize
        if self.deploy_stage.upper() in topic_arn:
            # launch API call to grab the tags for the sns topic
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.list_tags_for_resource
            topic_tags = self.sns_client.list_tags_for_resource(ResourceArn=topic_arn)

            # we only want topics that are tagged as 'IOW'
            if 'Tags' in topic_tags:
                for tag in topic_tags['Tags']:
                    if 'Key' in tag:
                        if 'wma:organization' in tag['Key']:
                            if 'IOW' == tag['Value']:
                                is_iow_topic = True

        return is_iow_topic
