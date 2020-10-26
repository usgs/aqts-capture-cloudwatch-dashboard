"""
Tests for the lambdas module.

"""
import json
from unittest import TestCase, mock

from ..lambdas import create_lambda_widgets


class TestCreateLambdaWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.max_items = 1000
        self.function_name = 'neat-lambda-function-in-DEV-account'
        self.function_list = {'Functions': [{'FunctionName': 'neat-lambda-function-in-DEV-account'}, {'FunctionName': 'some other function'}]}
        self.function_list_json_response = json.dumps(self.function_list)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_list_functions(self, m_client):
        mock_lambda = mock.MagicMock()
        m_client.return_value = mock_lambda

        # noinspection PyPackageRequirements
        create_lambda_widgets(self.region, self.deploy_stage)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        mock_lambda.list_functions.return_value = self.function_list_json_response

        print(mock_lambda.list_functions(MaxItems=self.max_items))

        # assert the list_functions lambda client call was made with expected arguments
        mock_lambda.list_functions.assert_called_with(
            MaxItems=self.max_items
        )

        # assert the get_function lambda client call was made with expected arguments
        mock_lambda.get_function.assert_called_with(
            FunctionName=self.function_name
        )