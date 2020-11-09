"""
module for making aws lambda api calls using aws python sdk (boto3)

"""
import boto3


class LambdaAPICalls:
    def __init__(self, region, deploy_stage):
        """
        Constructor for the LambdaAPICalls class.

        :param region: usually 'us-west-2'
        :param deploy_stage: The deployment tier (DEV, TEST, QA, PROD-EXTERNAL)
        """
        self.region = region
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.deploy_stage = deploy_stage

    def get_all_lambda_metadata(self):
        """
        Using the AWS python sdk (boto3), grab all the lambda functions for the specified account for a given region.

        :return: response: metadata about each lambda in the account.
        :rtype: dict
        """

        # Currently you cannot get more than 50 functions from the list_functions call in a single request.  Thus, we need
        # to iterate over the entire list of available functions in the account using the provided NextMarker string, which
        # allows us to paginate. boto3 does have pagination tools, but I have found the documentation generally unhelpful,
        # so below is a more manual approach.
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
        # TODO this pagination logic exists in the sqs module as well, consider moving it into its own utility
        # TODO module or trying to get a proper boto3 paginator to work...
        response = {}
        marker = None
        while True:
            if marker:
                response_iterator = self.lambda_client.list_functions(
                    MaxItems=10,
                    Marker=marker)
                response['Functions'].extend(response_iterator['Functions'])
            else:
                response_iterator = self.lambda_client.list_functions(
                    MaxItems=10
                )
                response.update(response_iterator)
            try:
                marker = response_iterator['NextMarker']
            except KeyError:
                # no more pages, move on
                break

        return response

    def is_iow_lambda_filter(self, function):
        """
        Apply filters to determine if the function is a tagged IOW asset in the correct tier.

        :param function: A single lambda function's metadata
        :return: is_iow_lambda: is this an IOW asset or not
        :rtype: bool
        """
        function_name = function['FunctionName']

        is_iow_lambda = False

        # filtering on deploy tier
        if self.deploy_stage.upper() in function_name:

            # launch API call to grab metadata for a specific function, we are interested in the tags
            function_metadata = self.lambda_client.get_function(FunctionName=function_name)

            # we only want lambdas that are tagged as 'IOW'
            if 'Tags' in function_metadata:
                if 'wma:organization' in function_metadata['Tags']:
                    if 'IOW' == function_metadata['Tags']['wma:organization']:
                        if 'CleanupFunction' not in function_name:
                            is_iow_lambda = True

        return is_iow_lambda
