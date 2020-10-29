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
        self.function_name = 'neat-lambda-function-in-DEV-account'
        self.marker = 'some string'
        self.function_list = {
            'Functions': [
                {'FunctionName': self.function_name}
            ]
        }
        self.function_list_with_next_marker = {
            'Functions': [
                {'FunctionName': self.function_name}
            ],
            'NextMarker': self.marker
        }
        self.function_list_single_good_function = {
            'FunctionName': self.function_name
        }
        self.get_function = {
            'Configuration': {
                'FunctionName': self.function_name
            },
            'Tags': {
                'wma:organization': 'IOW'
            }
        }

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata(self, m_client):
        # mock_lambda_client = mock.MagicMock()
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client

        # only one function returned from list_functions
        mock_lambda_client.list_functions.return_value = self.function_list

        # noinspection PyPackageRequirements
        get_all_lambda_metadata(self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        # assert the lambda client called list_functions with expected arguments
        mock_lambda_client.list_functions.assert_called_with(MaxItems=self.max_items)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata_next_marker(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client

        # 2 functions returned, the first function has the key Marker that causes us to begin iterating through pages
        # of list_function responses
        mock_lambda_client.list_functions.side_effect = [
            self.function_list_with_next_marker,
            self.function_list
        ]

        expected = [
            mock.call(MaxItems=self.max_items),
            mock.call(MaxItems=self.max_items, Marker=self.marker)
        ]

        # noinspection PyPackageRequirements
        get_all_lambda_metadata(self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        mock_lambda_client.list_functions.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_asset_filter(self, m_client):
        mock_lambda_client = mock.MagicMock()
        m_client.return_value = mock_lambda_client

        # noinspection PyPackageRequirements
        is_iow_asset_filter(self.function_list_single_good_function, self.deploy_stage, self.region)

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with('lambda', region_name=self.region)

        # assert the lambda client called get_function with expected arguments
        mock_lambda_client.get_function.assert_called_with(FunctionName=self.function_name)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    @mock.patch('cloudwatch_monitoring.lambdas.create_lambda_widgets', autospec=True)
    @mock.patch('cloudwatch_monitoring.lambdas.is_iow_asset_filter', autospec=True)
    @mock.patch('cloudwatch_monitoring.lambdas.get_all_lambda_metadata', autospec=True)
    def test_create_lambda_widgets(self, m_all_lambdas, m_filter, m_create, m_client):
        mock_lambda_client = mock.MagicMock()
        m_client.return_value = mock_lambda_client

        # mock the return values from the mock lambda client
        mock_lambda_client.list_functions.return_value = self.function_list
        mock_lambda_client.get_function.return_value = self.get_function

        # mock the return values from the function calls
        m_all_lambdas.return_value = self.function_list

        # noinspection PyPackageRequirements
        create_lambda_widgets(self.region, self.deploy_stage)

        # assert the get_all_lambda_metadata function was called with expected arguments
        m_all_lambdas.assert_called_with(self.region)
        # assert the is_iow_asset_filter function was called with expected arguments
        m_filter.assert_called_with(self.function_list_single_good_function, self.deploy_stage, self.region)

        expected_widget_list = [
            {
                'type': 'metric',
                'x': 0,
                'y': 0,
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'neat-lambda-function-in-DEV-account'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'neat-lambda-function-in-DEV-account',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average'
                }
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 3,
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
                        ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': True,
                    'region': 'us-south-10',
                    'period': 60,
                    'stat': 'Average',
                    'title': 'Concurrent Lambdas (Average per minute)'
                }
            },
            {
                'type': 'metric',
                'x': 0,
                'y': 3,
                'height': 6,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', 'Resource', 'aqts-capture-error-handler-DEV-aqtsErrorHandler'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': False,
                    'region': 'us-south-10',
                    'title': 'Error Handler Activity',
                    'period': 60,
                    'stat': 'Average'
                }
            }
        ]

        # assert the widget list is what it should be, note the misleading name of the assertCountEqual test name
        # doc here: https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertCountEqual
        self.assertListEqual(
            create_lambda_widgets(self.region, self.deploy_stage),
            expected_widget_list
        )
