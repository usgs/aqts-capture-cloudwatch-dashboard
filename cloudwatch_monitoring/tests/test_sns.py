"""
Tests for the sns module.

"""
from unittest import TestCase, mock

from .test_widgets import expected_sns_list
from ..sns import (SnsApiCalls, create_sns_widgets, generate_number_of_messages_published_metric)


class TestCreateSNSWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.client_type = 'sns'
        self.next_token = 'some huge string'
        self.topic_name_1 = "aqts-capture-error-handler-DEV-topic"
        self.tier_agnostic_topic_name_1 = "aqts-capture-error-handler"
        self.valid_topic_arn_1 = "arn:aws:sns:us-south-10:123456789012:aqts-capture-error-handler-DEV-topic"
        self.valid_topic_arn_2 = "arn:aws:sns:us-south-10:123456789012:etl-discrete-groundwater-rdb-DEV-topic"
        self.valid_topic_arn_3 = "arn:aws:sns:us-south-10:123456789012:aqts-capture-field-visit-transform-DEV-topic"
        self.invalid_topic_arn_1 = "arn:aws:sns:us-south-10:123456789012:aqts-capture-error-handler-TEST-topic"
        self.valid_topic_1 = {'TopicArn': self.valid_topic_arn_1}
        self.valid_topic_2 = {'TopicArn': self.valid_topic_arn_2}
        self.valid_topic_3 = {'TopicArn': self.valid_topic_arn_3}
        self.invalid_topic_1 = {'TopicArn': self.invalid_topic_arn_1}
        self.topic_list_no_next_token = {
            "Topics": [
                {
                    'TopicArn': self.valid_topic_arn_1
                }
            ]
        }
        self.topic_list_with_next_token_1 = {
            "Topics": [
                self.valid_topic_2,
                self.invalid_topic_1
            ],
            "NextToken": self.next_token
        }
        self.topic_list_after_successful_pagination = {
            "Topics": [
                self.valid_topic_2,
                self.invalid_topic_1,
                self.valid_topic_1
            ],
            "NextToken": self.next_token
        }
        self.tags_list_for_valid_topic_arn_1 = {
            "Tags": [
                {
                    'Key': 'wma:organization',
                    'Value': 'IOW'
                }
            ]
        }
        self.tags_list_empty_tags = {}
        self.tags_list_no_tags = {
            'Tags': [{}]
        }
        self.tags_list_no_wma_org_key = {
            'Tags': [
                {
                    'Key': 'wma:notOrganization',
                    "Value": 'IOW'
                }
            ]
        }
        self.tags_list_no_iow_value = {
            'Tags': [
                {
                    'Key': 'wma:organization',
                    "Value": 'notIOW'
                }
            ]
        }
        self.full_sns_topic_list = {
            'Topics': [
                self.valid_topic_2,
                self.invalid_topic_1,
                self.valid_topic_1,
                self.valid_topic_3
            ],
            'NextToken': self.next_token
        }

    def test_generate_number_of_messages_published_metric_first_iteration(self):
        self.assertListEqual(
            generate_number_of_messages_published_metric(self.topic_name_1, self.tier_agnostic_topic_name_1, 0),
            ["AWS/SNS", 'NumberOfMessagesPublished', "TopicName", self.topic_name_1, {"label": "Error Handler"}]
        )

    def test_generate_number_of_messages_published_metric_second_iteration(self):
        self.assertListEqual(
            generate_number_of_messages_published_metric(self.topic_name_1, self.tier_agnostic_topic_name_1, 1),
            ["...", self.topic_name_1, {"label": "Error Handler"}]
        )

    def test_generate_number_of_messages_published_metric_unknown_topic_first_iteration(self):
        self.assertListEqual(
            generate_number_of_messages_published_metric("a-topic-we-have-not-added-yet-DEV-topic", "a-topic-we-have-not-added-yet", 0),
            ["AWS/SNS", 'NumberOfMessagesPublished', "TopicName", "a-topic-we-have-not-added-yet-DEV-topic", {"label": "a-topic-we-have-not-added-yet-DEV-topic"}]
        )

    def test_generate_number_of_messages_published_metric_unknown_topic_second_iteration(self):
        self.assertListEqual(
            generate_number_of_messages_published_metric("a-topic-we-have-not-added-yet-DEV-topic", "a-topic-we-have-not-added-yet", 1),
            ["...", "a-topic-we-have-not-added-yet-DEV-topic", {"label": "a-topic-we-have-not-added-yet-DEV-topic"}]
        )

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_get_all_sns_topics(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # only one topic returned from list_topics
        mock_sns_client.list_topics.return_value = self.topic_list_no_next_token

        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_sns_topics(),
            self.topic_list_no_next_token
        )

        # assert the boto3 sns client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the sns client called list_topics with expected arguments
        mock_sns_client.list_topics.assert_called_once()

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_get_all_sns_topics_next_token_pagination(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # 2 pages returned, the first page has a NextToken key that causes us to begin iterating through pages
        # of list_topics responses
        mock_sns_client.list_topics.side_effect = [
            self.topic_list_with_next_token_1,
            self.topic_list_no_next_token
        ]
        expected = [
            mock.call(),
            mock.call(NextToken=self.next_token)
        ]

        # assert we get the expected topic list after 1 pagination iteration
        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_sns_topics(),
            self.topic_list_after_successful_pagination
        )

        # assert the boto3 sns client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the sns client called list_topics with expected arguments
        mock_sns_client.list_topics.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_is_iow_topic_filter_happy_path(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        mock_sns_client.list_tags_for_resource.return_value = self.tags_list_for_valid_topic_arn_1
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # assert the return value is true, since list_tags_for_resource returned a valid response
        # noinspection PyPackageRequirements
        self.assertTrue(
            api_calls.is_iow_topic_filter(self.valid_topic_arn_1)
        )

        # assert the boto3 sns client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the sns client called list_tags_for_resource with expected arguments
        mock_sns_client.list_tags_for_resource.assert_called_with(ResourceArn=self.valid_topic_arn_1)

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_is_iow_topic_filter_empty_tags_response(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        mock_sns_client.list_tags_for_resource.return_value = self.tags_list_empty_tags
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_tags_for_resource returned a response with no 'Tags' key
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_topic_filter(self.valid_topic_arn_1)
        )

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_is_iow_topic_filter_no_tags_response(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        mock_sns_client.list_tags_for_resource.return_value = self.tags_list_no_tags
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_tags_for_resource returned a response with no tags in the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_topic_filter(self.valid_topic_arn_1)
        )

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_is_iow_topic_filter_no_wma_org_key_response(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        mock_sns_client.list_tags_for_resource.return_value = self.tags_list_no_wma_org_key
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_tags_for_resource returned a response with no
        # wma:organization key in the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_topic_filter(self.valid_topic_arn_1)
        )

    @mock.patch('cloudwatch_monitoring.sns.boto3.client', autospec=True)
    def test_is_iow_topic_filter_no_iow_value_response(self, m_client):
        mock_sns_client = mock.Mock()
        m_client.return_value = mock_sns_client
        mock_sns_client.list_tags_for_resource.return_value = self.tags_list_no_iow_value
        api_calls = SnsApiCalls(self.region, self.deploy_stage)

        # assert the return value is False, since list_tags_for_resource returned a response with a valid
        # wma:organization key, but the value is not "IOW"
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_topic_filter(self.valid_topic_arn_1)
        )

    @mock.patch('cloudwatch_monitoring.sns.SnsApiCalls', autospec=True)
    def test_create_sns_widgets(self, m_api_calls):
        # return values
        m_api_calls.return_value.get_all_sns_topics.return_value = self.full_sns_topic_list
        m_api_calls.return_value.is_iow_topic_filter.side_effect = [
            True, False, True, True
        ]

        # expected calls
        expected_is_iow_topic_filter_calls = [
            mock.call(self.valid_topic_arn_2),
            mock.call(self.invalid_topic_arn_1),
            mock.call(self.valid_topic_arn_1),
            mock.call(self.valid_topic_arn_3)
        ]

        # Make sure the resultant widget list is correct
        # noinspection PyPackageRequirements
        self.assertListEqual(
            create_sns_widgets(self.region, self.deploy_stage),
            expected_sns_list
        )

        # assert our helper methods were called the expected number of times and in the proper order
        m_api_calls.return_value.get_all_sns_topics.assert_called_once()
        m_api_calls.return_value.is_iow_topic_filter.assert_has_calls(expected_is_iow_topic_filter_calls, any_order=False)
