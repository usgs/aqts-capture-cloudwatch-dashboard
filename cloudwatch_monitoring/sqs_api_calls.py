"""
module for making aws sqs api calls using aws python sdk (boto3)

"""
import boto3


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

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.list_queues
        # TODO this pagination logic exists in the lambdas module as well, consider moving it into its own utility
        # TODO module or trying to get a proper boto3 paginator to work...
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
            queue_tags = self.sqs_client.list_queue_tags(QueueUrl=queue_url)

            # we only want queues that are tagged as 'IOW'
            if 'Tags' in queue_tags:
                if 'wma:organization' in queue_tags['Tags']:
                    if 'IOW' == queue_tags['Tags']['wma:organization']:
                        is_iow_queue = True

        return is_iow_queue
