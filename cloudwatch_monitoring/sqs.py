"""
module for creating sqs widgets

"""
from .lookups import sqs_queues
from .api_calls import APICalls


def create_sqs_widgets(region, deploy_stage, positioning):
    """
    Creates the list of SQS widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :return: list of SQS widgets
    :rtype: list
    """
    api_calls = APICalls(region, 'sqs', deploy_stage)
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
            positioning.width = 12
            positioning.height = 6

            queue_widget = {
                'type': 'metric',
                'x': positioning.x,
                'y': positioning.y,
                'height': positioning.height,
                'width': positioning.width,
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
            positioning.iterate_positioning()

    return sqs_widgets
