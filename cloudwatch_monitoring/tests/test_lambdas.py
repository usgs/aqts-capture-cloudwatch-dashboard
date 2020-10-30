"""
Tests for the lambdas module.

"""
from unittest import TestCase, mock

from ..lambdas import create_lambda_widgets
from ..lambdas import get_all_lambda_metadata
from ..lambdas import is_iow_asset_filter


class TestCreateLambdaWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.max_items = 10
        self.valid_function_name_1 = 'lambda-function-in-DEV-account'
        self.valid_function_name_2 = 'another-lambda-function-in-DEV-account'
        self.valid_function_name_3 = 'sweet_DEV_function_name'
        self.bad_function_name = 'some-function-name-with-no-valid-TIER-specified'
        self.marker = 'some huge string'

        self.function_list_with_page_marker_1 = {
            'Functions': [
                {'FunctionName': self.valid_function_name_2},
                {'FunctionName': self.bad_function_name}
            ],
            'NextMarker': self.marker
        }

        self.function_list_with_page_marker_2 = {
            'Functions': [
                {'FunctionName': self.valid_function_name_3},
                {'FunctionName': self.bad_function_name}
            ],
            'NextMarker': self.marker
        }

        self.function_list_no_page_marker = {
            'Functions': [
                {'FunctionName': self.valid_function_name_1},
                {'FunctionName': self.bad_function_name}
            ]
        }

        self.full_function_list = {
            'Functions': [
                {'FunctionName': self.valid_function_name_2},
                {'FunctionName': self.bad_function_name},
                {'FunctionName': self.valid_function_name_3},
                {'FunctionName': self.bad_function_name},
                {'FunctionName': self.valid_function_name_1},
                {'FunctionName': self.bad_function_name}
            ],
            'NextMarker': self.marker
        }

        self.valid_function_1 = {
            'FunctionName': self.valid_function_name_1
        }

        self.valid_function_2 = {
            'FunctionName': self.valid_function_name_2
        }

        self.valid_function_3 = {
            'FunctionName': self.valid_function_name_3
        }

        self.bad_function = {
            'FunctionName': self.bad_function_name
        }

        self.get_function_1 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_1
            },
            'Tags': {
                'wma:organization': 'IOW'
            }
        }

        self.get_function_2 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_2
            },
            'Tags': {
                'wma:organization': 'IOW'
            }
        }

        self.get_function_3 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_3
            },
            'Tags': {
                'wma:organization': 'IOW'
            }
        }

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client

        # only one function returned from list_functions
        mock_lambda_client.list_functions.return_value = self.function_list_no_page_marker

        # noinspection PyPackageRequirements
        get_all_lambda_metadata(self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        # assert the lambda client called list_functions with expected arguments
        mock_lambda_client.list_functions.assert_called_with(MaxItems=self.max_items)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata_next_marker_pagination(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client

        # 2 functions returned, the first function has the key Marker that causes us to begin iterating through pages
        # of list_function responses
        mock_lambda_client.list_functions.side_effect = [
            self.function_list_with_page_marker_1,
            self.function_list_no_page_marker
        ]
        expected = [
            mock.call(MaxItems=self.max_items),
            mock.call(MaxItems=self.max_items, Marker=self.marker)
        ]

        # noinspection PyPackageRequirements
        get_all_lambda_metadata(self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        # assert the list_function calls were called, and in the expected order
        mock_lambda_client.list_functions.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_asset_filter(self, m_client):
        mock_lambda_client = mock.MagicMock()
        m_client.return_value = mock_lambda_client

        # noinspection PyPackageRequirements
        is_iow_asset_filter(self.valid_function_1, self.deploy_stage, self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        # assert the lambda client called get_function with expected arguments
        mock_lambda_client.get_function.assert_called_with(FunctionName=self.valid_function_name_1)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    @mock.patch('cloudwatch_monitoring.lambdas.is_iow_asset_filter', autospec=True)
    @mock.patch('cloudwatch_monitoring.lambdas.get_all_lambda_metadata', autospec=True)
    def test_create_lambda_widgets(self, m_all_lambdas, m_filter, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client

        # return values
        m_all_lambdas.return_value = self.full_function_list
        m_filter.side_effect = [
            True, False, True, False, True, False
        ]

        # expected calls
        expected_is_iow_asset_filter_calls = [
            mock.call(self.valid_function_2, self.deploy_stage, self.region),
            mock.call(self.bad_function, self.deploy_stage, self.region),
            mock.call(self.valid_function_3, self.deploy_stage, self.region),
            mock.call(self.bad_function, self.deploy_stage, self.region),
            mock.call(self.valid_function_1, self.deploy_stage, self.region),
            mock.call(self.bad_function, self.deploy_stage, self.region)
        ]

        expected_widget_list = [
            {
                'type': 'metric',
                'x': 0,
                'y': 0,
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'another-lambda-function-in-DEV-account'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'another-lambda-function-in-DEV-account',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                },
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 3,
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'sweet_DEV_function_name'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'sweet_DEV_function_name',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                },
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 6,
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'lambda-function-in-DEV-account'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'lambda-function-in-DEV-account',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                },
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 9,
                'height': 6,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'label': 'DV stat Transformer'}],
                        ['...', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', {'label': 'Error Handler'}],
                        ['...', 'aqts-capture-raw-load-DEV-iowCapture', {'label': 'Raw Loader'}],
                        ['...', 'aqts-capture-stattype-router-DEV-determineRoute', {'label': 'Statistic type router'}],
                        ['...', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'label': 'Capture trigger'}],
                        ['...', 'aqts-capture-ts-corrected-DEV-preProcess', {'label': 'TS corrected preprocessor'}],
                        ['...', 'aqts-capture-ts-description-DEV-processTsDescription', {'label': 'TS descriptions preprocessor'}],
                        ['...', 'aqts-ts-type-router-DEV-determineRoute', {'label': 'TS type router'}],
                        ['...', 'aqts-capture-ts-loader-DEV-loadTimeSeries', {'label': 'DV TS loader'}],
                        ['...', 'aqts-capture-ts-field-visit-DEV-preProcess', {'label': 'Field visit preprocessor'}],
                        ['...', 'aqts-capture-field-visit-transform-DEV-transform', {'label': 'Field visit transformer'}],
                        ['...', 'aqts-capture-discrete-loader-DEV-loadDiscrete', {'label': 'Discrete GW loader'}],
                        ['...', 'aqts-capture-field-visit-metadata-DEV-preProcess', {'label': 'Field visit metadata preprocessor'}],
                        ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}],
                    ],
                    'view': 'timeSeries',
                    'stacked': True,
                    'region': 'us-south-10',
                    'period': 60,
                    'stat': 'Average',
                    'title': 'Concurrent Lambdas (Average per minute)',
                },
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 9,
                'height': 6,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', 'Resource', 'aqts-capture-error-handler-DEV-aqtsErrorHandler',],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': False,
                    'region': 'us-south-10',
                    'title': 'Error Handler Activity',
                    'period': 60,
                    'stat': 'Average',
                },
            }
        ]

        # Make sure the resultant widget list is correct
        # noinspection PyPackageRequirements
        self.assertListEqual(
            create_lambda_widgets(self.region, self.deploy_stage),
            expected_widget_list
        )

        # assert our helper functions were called the expected number of times and in the proper order
        m_all_lambdas.assert_called_once_with(self.region)
        m_filter.assert_has_calls(expected_is_iow_asset_filter_calls, any_order=False)
