"""
Tests for the state machine module.

"""
from unittest import TestCase, mock

from ..positioning import Positioning
from ..state_machine import (create_state_machine_widgets, get_all_state_machines, is_iow_state_machine_filter)


class TestCreateStateMachineWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.max_results = 10
        self.next_token = 'some huge string'
        self.valid_state_machine_arn_1 = 'arn:aws:states:us-west-2:807615458658:stateMachine:aqts-ecosystem-switch-grow-capture-db-DEV'
        self.valid_state_machine_arn_2 = 'arn:aws:states:us-west-2:807615458658:stateMachine:aqts-ecosystem-switch-shrink-capture-db-DEV'
        self.invalid_state_machine_arn = 'arn:aws:states:us-west-2:807615458658:stateMachine:some-state-machine-TEST'
        self.valid_state_machine_name_1 = 'aqts-ecosystem-switch-grow-capture-db-DEV'
        self.valid_state_machine_name_2 = 'aqts-ecosystem-switch-shrink-capture-db-DEV'
        self.invalid_state_machine_name = 'some-state-machine-TEST'
        self.state_machine_list_no_next_token = {
            'stateMachines': [
                {
                    'stateMachineArn': self.valid_state_machine_arn_1,
                    'name': self.valid_state_machine_name_1
                }
            ]
        }
        self.state_machine_list_with_next_token_1 = {
            'stateMachines': [
                {
                    'stateMachineArn': self.valid_state_machine_arn_2,
                    'name': self.valid_state_machine_name_2
                },
                {
                    'stateMachineArn': self.invalid_state_machine_arn,
                    'name': self.invalid_state_machine_name
                }
            ],
            'nextToken': self.next_token
        }
        self.state_machine_list_after_successful_pagination = {
            'stateMachines': [
                {
                    'stateMachineArn': self.valid_state_machine_arn_2,
                    'name': self.valid_state_machine_name_2
                },
                {
                    'stateMachineArn': self.invalid_state_machine_arn,
                    'name': self.invalid_state_machine_name
                },
                {
                    'stateMachineArn': self.valid_state_machine_arn_1,
                    'name': self.valid_state_machine_name_1
                },
            ],
            'nextToken': self.next_token
        }
        self.tags_list_for_valid_state_machine_arn_1 = {
            "tags": [
                {
                    'key': 'wma:organization',
                    "value": 'IOW'
                }
            ]
        }
        self.tags_list_empty_tags = {}
        self.tags_list_no_tags = {
            'tags': [{}]
        }
        self.tags_list_no_wma_org_key = {
            'tags': [
                {
                    'key': 'wma:notOrganization',
                    "value": 'IOW'
                }
            ]
        }
        self.tags_list_no_iow_value = {
            'tags': [
                {
                    'key': 'wma:organization',
                    "value": 'notIOW'
                }
            ]
        }

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_get_all_state_machines(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client

        # only one state machine returned from list_state_machines
        mock_stepfunctions_client.list_state_machines.return_value = self.state_machine_list_no_next_token

        # noinspection PyPackageRequirements
        self.assertDictEqual(
            get_all_state_machines(self.region),
            self.state_machine_list_no_next_token
        )

        # assert the boto3 stepfunctions client was called with expected params
        m_client.assert_called_with('stepfunctions', region_name=self.region)

        # assert the stepfunctions client called list_state_machines with expected arguments
        mock_stepfunctions_client.list_state_machines.assert_called_with(maxResults=self.max_results)

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_get_all_state_machines_next_token_pagination(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client

        # 2 state machines returned, the first state machine has the key nextToken that causes us to begin iterating 
        # through pages of list_state_machines responses
        mock_stepfunctions_client.list_state_machines.side_effect = [
            self.state_machine_list_with_next_token_1,
            self.state_machine_list_no_next_token
        ]
        expected = [
            mock.call(maxResults=self.max_results),
            mock.call(maxResults=self.max_results, nextToken=self.next_token)
        ]

        # Assert we get the expected state machine list after 1 pagination iteration
        # noinspection PyPackageRequirements
        self.assertDictEqual(
            get_all_state_machines(self.region),
            self.state_machine_list_after_successful_pagination
        )

        # assert the boto3 stepfunctions client was called with expected params
        m_client.assert_called_with('stepfunctions', region_name=self.region)

        # assert the list_state_machines calls were called, and in the expected order
        mock_stepfunctions_client.list_state_machines.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_is_iow_state_machine_filter_happy_path(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client
        mock_stepfunctions_client.list_tags_for_resource.return_value = self.tags_list_for_valid_state_machine_arn_1

        # assert the return value is true, since list_tags_for_resource returned a valid response
        # noinspection PyPackageRequirements
        self.assertTrue(
            is_iow_state_machine_filter(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        )

        # assert the boto3 stepfunctions client was called with expected params
        m_client.assert_called_with('stepfunctions', region_name=self.region)

        # assert the stepfunctions client called list_tags_for_resource with expected arguments
        mock_stepfunctions_client.list_tags_for_resource.assert_called_with(resourceArn=self.valid_state_machine_arn_1)

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_is_iow_state_machine_filter_empty_tags_response(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client
        mock_stepfunctions_client.list_tags_for_resource.return_value = self.tags_list_empty_tags

        # assert the return value is False, since list_tags_for_resource returned a response with no 'Tags' key
        # noinspection PyPackageRequirements
        self.assertFalse(
            is_iow_state_machine_filter(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        )

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_is_iow_state_machine_filter_no_tags_response(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client
        mock_stepfunctions_client.list_tags_for_resource.return_value = self.tags_list_no_tags

        # assert the return value is False, since list_tags_for_resource returned a response with no tags in the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            is_iow_state_machine_filter(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        )

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_is_iow_state_machine_filter_no_wma_org_key_response(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client
        mock_stepfunctions_client.list_tags_for_resource.return_value = self.tags_list_no_wma_org_key

        # assert the return value is False, since list_tags_for_resource returned a response with no wma:organization key in
        # the Tags dict
        # noinspection PyPackageRequirements
        self.assertFalse(
            is_iow_state_machine_filter(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        )

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    def test_is_iow_state_machine_filter_no_iow_value_response(self, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client
        mock_stepfunctions_client.list_tags_for_resource.return_value = self.tags_list_no_iow_value

        # assert the return value is False, since list_tags_for_resource returned a response with a valid wma:organization
        # key, but the value is not "IOW"
        # noinspection PyPackageRequirements
        self.assertFalse(
            is_iow_state_machine_filter(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        )

    @mock.patch('cloudwatch_monitoring.state_machine.boto3.client', autospec=True)
    @mock.patch('cloudwatch_monitoring.state_machine.is_iow_state_machine_filter', autospec=True)
    @mock.patch('cloudwatch_monitoring.state_machine.get_all_state_machines', autospec=True)
    def test_create_state_machine_widgets(self, m_all_state_machines, m_filter, m_client):
        mock_stepfunctions_client = mock.Mock()
        m_client.return_value = mock_stepfunctions_client

        # return values
        m_all_state_machines.return_value = self.state_machine_list_after_successful_pagination
        m_filter.side_effect = [
            True, False, True
        ]

        # expected calls
        expected_is_iow_state_machine_filter_calls = [
            mock.call(self.valid_state_machine_arn_2, self.deploy_stage, self.region),
            mock.call(self.invalid_state_machine_arn, self.deploy_stage, self.region),
            mock.call(self.valid_state_machine_arn_1, self.deploy_stage, self.region)
        ]

        # we do not expect the invalid state machine would have resulted in a widget
        expected_state_machine_list = [
            {
                'type': 'metric',
                'x': 0,
                'y': 0,
                'height': 6,
                'width': 12,
                'properties': {
                    "metrics": [
                        ["AWS/States", "ExecutionsStarted", "StateMachineArn", self.valid_state_machine_arn_2],
                        [".", "ExecutionsSucceeded", ".", "."],
                        [".", "ExecutionsFailed", ".", "."],
                        [".", "ExecutionsTimedOut", ".", "."]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": self.region,
                    "stat": "Sum",
                    "period": 60,
                    "title": "Shrink Capture DB State Machine"
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
                        ["AWS/States", "ExecutionsStarted", "StateMachineArn", self.valid_state_machine_arn_1],
                        [".", "ExecutionsSucceeded", ".", "."],
                        [".", "ExecutionsFailed", ".", "."],
                        [".", "ExecutionsTimedOut", ".", "."]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": self.region,
                    "stat": "Sum",
                    "period": 60,
                    "title": "Grow Capture DB State Machine"
                }
            }
        ]

        positioning = Positioning()
        # Make sure the resultant widget list is correct
        # noinspection PyPackageRequirements
        self.assertListEqual(
            create_state_machine_widgets(self.region, self.deploy_stage, positioning),
            expected_state_machine_list
        )

        # assert our helper methods were called the expected number of times and in the proper order
        m_all_state_machines.assert_called_once_with(self.region)
        m_filter.assert_has_calls(expected_is_iow_state_machine_filter_calls, any_order=False)