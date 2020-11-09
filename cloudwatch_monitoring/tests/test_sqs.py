"""
Tests for the sqs module.

"""
from unittest import TestCase, mock

from ..positioning import Positioning
from ..sqs import create_sqs_widgets
from ..sqs_api_calls import SQSAPICalls


class TestCreateSQSWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.client_type = 'sqs'
        self.max_results = 10
        self.next_token = 'some huge string'
        self.valid_queue_url_1 = "https://us-west-2.queue.amazonaws.com/579777464052/aqts-capture-error-queue-DEV"
        self.valid_queue_url_2 = "https://us-west-2.queue.amazonaws.com/579777464052/aqts-capture-trigger-queue-DEV"
        self.invalid_queue_url_1 = "https://us-west-2.queue.amazonaws.com/579777464052/some-queue-TEST"
        self.valid_queue_name_1 = "aqts-capture-error-queue-DEV"
        self.valid_queue_name_2 = "aqts-capture-trigger-queue-DEV"
        self.queue_list_no_next_token = {
            "QueueUrls": [
                self.valid_queue_url_1
            ]
        }
        self.queue_list_with_next_token_1 = {
            "QueueUrls": [
                self.valid_queue_url_2,
                self.invalid_queue_url_1
            ],
            "NextToken": self.next_token
        }
        self.queue_list_after_successful_pagination = {
            "QueueUrls": [
                self.valid_queue_url_2,
                self.invalid_queue_url_1,
                self.valid_queue_url_1
            ],
            "NextToken": self.next_token
        }
        self.tags_list_for_valid_queue_url_1 = {
            'Tags': {
                'wma:organization': 'IOW'
            }
        }
        self.tags_list_empty_tags = {}
        self.tags_list_no_tags = {
            'Tags': {}
        }
        self.tags_list_no_wma_org_key = {
            'Tags': {
                'someKey': 'IOW'
            }
        }
        self.tags_list_no_iow_value = {
            'Tags': {
                'wma:organization': 'not IOW tag'
            }
        }

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_get_all_sqs_queue_urls(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # only one queue returned from list_queues
        mock_sqs_client.list_queues.return_value = self.queue_list_no_next_token

        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_sqs_queue_urls(),
            self.queue_list_no_next_token
        )

        # assert the boto3 sqs client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the sqs client called list_queues with expected arguments
        mock_sqs_client.list_queues.assert_called_with(MaxResults=self.max_results)

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_get_all_sqs_queue_urls_next_token_pagination(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # 2 queues returned, the first queue has the key NextToken that causes us to begin iterating through pages
        # of list_queues responses
        mock_sqs_client.list_queues.side_effect = [
            self.queue_list_with_next_token_1,
            self.queue_list_no_next_token
        ]
        expected = [
            mock.call(MaxResults=self.max_results),
            mock.call(MaxResults=self.max_results, NextToken=self.next_token)
        ]

        # Assert we get the expected queue list after 1 pagination iteration
        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_sqs_queue_urls(),
            self.queue_list_after_successful_pagination
        )

        # assert the boto3 sqs client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the list_queues calls were called, and in the expected order
        mock_sqs_client.list_queues.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_is_iow_queue_filter_happy_path(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        mock_sqs_client.list_queue_tags.return_value = self.tags_list_for_valid_queue_url_1
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # assert the return value is true, since list_queue_tags returned a valid response
        # noinspection PyPackageRequirements
        self.assertTrue(
            api_calls.is_iow_queue_filter(self.valid_queue_url_1)
        )

        # assert the boto3 sqs client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the sqs client called list_queue_tags with expected arguments
        mock_sqs_client.list_queue_tags.assert_called_with(QueueUrl=self.valid_queue_url_1)

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_is_iow_queue_filter_empty_tags_response(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        mock_sqs_client.list_queue_tags.return_value = self.tags_list_empty_tags
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_queue_tags returned a response with no 'Tags' key
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_queue_filter(self.valid_queue_url_1)
        )

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_is_iow_queue_filter_no_tags_response(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        mock_sqs_client.list_queue_tags.return_value = self.tags_list_no_tags
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_queue_tags returned a response with no tags in the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_queue_filter(self.valid_queue_url_1)
        )

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_is_iow_queue_filter_no_wma_org_key_response(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        mock_sqs_client.list_queue_tags.return_value = self.tags_list_no_wma_org_key
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_queue_tags returned a response with no wma:organization key in
        # the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_queue_filter(self.valid_queue_url_1)
        )

    @mock.patch('cloudwatch_monitoring.sqs_api_calls.boto3.client', autospec=True)
    def test_is_iow_queue_filter_no_iow_value_response(self, m_client):
        mock_sqs_client = mock.Mock()
        m_client.return_value = mock_sqs_client
        mock_sqs_client.list_queue_tags.return_value = self.tags_list_no_iow_value
        api_calls = SQSAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_queue_tags returned a response with a valid wma:organization
        # key, but the value is not "IOW"
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_queue_filter(self.valid_queue_url_1)
        )

    @mock.patch('cloudwatch_monitoring.sqs.SQSAPICalls', autospec=True)
    def test_create_sqs_widgets(self, m_api_calls):
        # return values
        m_api_calls.return_value.get_all_sqs_queue_urls.return_value = self.queue_list_after_successful_pagination
        m_api_calls.return_value.is_iow_queue_filter.side_effect = [
            True, False, True
        ]

        # expected calls
        expected_is_iow_queue_filter_calls = [
            mock.call(self.valid_queue_url_2),
            mock.call(self.invalid_queue_url_1),
            mock.call(self.valid_queue_url_1)
        ]

        # we do not expect the invalid queue name would have resulted in a widget
        expected_queue_list = [
            {
                'type': 'metric',
                'x': 0,
                'y': 0,
                'height': 6,
                'width': 12,
                'properties': {
                    "metrics": [
                        ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", self.valid_queue_name_2],
                        [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                        [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesDeleted", ".", "."],
                        [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": self.region,
                    "period": 60,
                    "title": "Capture Trigger Queue",
                    "stat": "Average",

                }
            },
            {
                'type': 'metric',
                'x': 12,
                'y': 0,
                'height': 6,
                'width': 12,
                'properties': {
                    "metrics": [
                        ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", self.valid_queue_name_1],
                        [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                        [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                        [".", "NumberOfMessagesDeleted", ".", "."],
                        [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": self.region,
                    "period": 60,
                    "title": "Error Queue",
                    "stat": "Average",

                }
            }
        ]

        positioning = Positioning()
        # Make sure the resultant widget list is correct
        # noinspection PyPackageRequirements
        self.assertListEqual(
            create_sqs_widgets(self.region, self.deploy_stage, positioning),
            expected_queue_list
        )

        # assert our helper methods were called the expected number of times and in the proper order
        m_api_calls.return_value.get_all_sqs_queue_urls.assert_called_once()
        m_api_calls.return_value.is_iow_queue_filter.assert_has_calls(expected_is_iow_queue_filter_calls, any_order=False)
