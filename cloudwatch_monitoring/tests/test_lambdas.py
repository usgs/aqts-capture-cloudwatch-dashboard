"""
Tests for the lambdas module.

"""
from unittest import TestCase, mock

from ..positioning import Positioning
from ..lambdas import (LambdaAPICalls, create_lambda_widgets, lambda_properties, generate_custom_lambda_metrics)


class TestCreateLambdaWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'
        self.client_type = 'lambda'
        self.max_items = 10
        self.valid_function_name_1 = 'aqts-capture-field-visit-transform-DEV-transform'
        self.valid_function_name_2 = 'aqts-capture-trigger-DEV-aqtsCaptureTrigger'
        self.valid_function_name_3 = 'aqts-capture-ecosystem-switch-DEV-growDb'
        self.valid_function_name_4 = 'function_DEV_name_not_added_to_lookups_yet'
        self.valid_function_name_5 = 'aqts-capture-dvstat-transform-DEV-transform'
        self.valid_function_name_6 = 'aqts-capture-error-handler-DEV-aqtsErrorHandler'
        self.valid_function_name_7 = 'aqts-capture-pruner-DEV-pruneTimeSeries'
        self.valid_function_name_8 = 'etl-discrete-groundwater-rdb-DEV-loadRdb'
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

        self.function_list_after_successful_pagination = {
            'Functions': [
                {'FunctionName': self.valid_function_name_2},
                {'FunctionName': self.bad_function_name},
                {'FunctionName': self.valid_function_name_1},
                {'FunctionName': self.bad_function_name}
            ],
            'NextMarker': self.marker
        }

        self.function_list_after_successful_pagination_2 = {
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

        self.full_function_list = {
            'Functions': [
                {'FunctionName': self.valid_function_name_2},
                {'FunctionName': self.bad_function_name},
                {'FunctionName': self.valid_function_name_3},
                {'FunctionName': self.bad_function_name},
                {'FunctionName': self.valid_function_name_1},
                {'FunctionName': self.valid_function_name_4},
                {'FunctionName': self.valid_function_name_5},
                {'FunctionName': self.valid_function_name_6},
                {'FunctionName': self.valid_function_name_7},
                {'FunctionName': self.valid_function_name_8},
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

        self.valid_function_4 = {
            'FunctionName': self.valid_function_name_4
        }

        self.valid_function_5 = {
            'FunctionName': self.valid_function_name_5
        }

        self.valid_function_6 = {
            'FunctionName': self.valid_function_name_6
        }

        self.valid_function_7 = {
            'FunctionName': self.valid_function_name_7
        }

        self.valid_function_8 = {
            'FunctionName': self.valid_function_name_8
        }

        self.bad_function = {
            'FunctionName': self.bad_function_name
        }

        # happy path
        self.get_function_1 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_1
            },
            'Tags': {
                'wma:organization': 'IOW'
            }
        }

        # sad path, no tags
        self.get_function_2 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_2
            }
        }

        # sad path, no wma:organization key
        self.get_function_3 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_3
            },
            'Tags': {
                'wma:notTheRightTagKey': 'IOW'
            }
        }

        # sad path, no 'IOW' value in the wma:organization tag
        self.get_function_4 = {
            'Configuration': {
                'FunctionName': self.valid_function_name_4
            },
            'Tags': {
                'wma:organization': 'notIOWTag'
            }
        }

        self.concurrent_lambdas_metrics_list = [
            ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform',
             {'label': 'DV stat Transformer'}],
            ['...', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', {'label': 'Error Handler'}],
            ['...', 'aqts-capture-raw-load-DEV-iowCapture', {'label': 'Raw Loader'}],
            ['...', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'label': 'Capture Trigger'}],
            ['...', 'aqts-capture-ts-corrected-DEV-preProcess', {'label': 'TS corrected preprocessor'}],
            ['...', 'aqts-capture-ts-description-DEV-processTsDescription',
             {'label': 'TS descriptions preprocessor'}],
            ['...', 'aqts-ts-type-router-DEV-determineRoute', {'label': 'TS type router'}],
            ['...', 'aqts-capture-ts-loader-DEV-loadTimeSeries', {'label': 'DV TS loader'}],
            ['...', 'aqts-capture-ts-field-visit-DEV-preProcess', {'label': 'Field visit preprocessor'}],
            ['...', 'aqts-capture-field-visit-transform-DEV-transform', {'label': 'Field visit transformer'}],
            ['...', 'aqts-capture-discrete-loader-DEV-loadDiscrete', {'label': 'Discrete GW loader'}],
            ['...', 'aqts-capture-field-visit-metadata-DEV-preProcess',
             {'label': 'Field visit metadata preprocessor'}],
            ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}],
            ['...', 'aqts-capture-raw-load-DEV-iowCaptureSmall', {'label': 'Raw Load Small'}],
            ['...', 'aqts-capture-raw-load-DEV-iowCaptureExtraSmall', {'label': 'Raw Load Extra Small'}]
        ]

        self.duration_of_transform_db_lambdas_metrics_list = [
             ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform',
              {'label': 'DV stat Transformer'}],
             ['...', 'aqts-capture-raw-load-DEV-iowCapture', {'label': 'Raw Loader'}],
             ['...', 'aqts-capture-ts-corrected-DEV-preProcess', {'label': 'TS corrected preprocessor'}],
             ['...', 'aqts-capture-ts-description-DEV-processTsDescription', {'label': 'TS descriptions preprocessor'}],
             ['...', 'aqts-ts-type-router-DEV-determineRoute', {'label': 'TS type router'}],
             ['...', 'aqts-capture-ts-loader-DEV-loadTimeSeries', {'label': 'DV TS loader'}],
             ['...', 'aqts-capture-ts-field-visit-DEV-preProcess', {'label': 'Field visit preprocessor'}],
             ['...', 'aqts-capture-field-visit-transform-DEV-transform', {'label': 'Field visit transformer'}],
             ['...', 'aqts-capture-discrete-loader-DEV-loadDiscrete', {'label': 'Discrete GW loader'}],
             ['...', 'aqts-capture-field-visit-metadata-DEV-preProcess',
              {'label': 'Field visit metadata preprocessor'}],
             ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}],
             ['...', 'aqts-capture-raw-load-DEV-iowCaptureSmall', {'label': 'Raw Load Small'}],
             ['...', 'aqts-capture-raw-load-DEV-iowCaptureExtraSmall', {'label': 'Raw Load Extra Small'}]]

    def test_lambda_properties(self):
        expected_properties = {
            'name': 'aqts-capture-dvstat-transform-DEV-transform',
            'label': 'DV stat Transformer'
        }

        self.assertDictEqual(
            lambda_properties('dvstat_transform', self.deploy_stage),
            expected_properties
        )

    def test_generate_custom_lambda_metrics_concurrent_lambdas(self):
        self.assertListEqual(
            generate_custom_lambda_metrics(self.deploy_stage, 'ConcurrentExecutions', 'concurrent_lambdas'),
            self.concurrent_lambdas_metrics_list
        )

    def test_generate_custom_lambda_metrics_duration_of_transform_db_lambdas(self):
        self.assertListEqual(
            generate_custom_lambda_metrics(self.deploy_stage, 'Duration', 'duration_of_transform_db_lambdas'),
            self.duration_of_transform_db_lambdas_metrics_list
        )

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

        # only one function returned from list_functions
        mock_lambda_client.list_functions.return_value = self.function_list_no_page_marker

        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_lambda_metadata(),
            self.function_list_no_page_marker
        )

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the lambda client called list_functions with expected arguments
        mock_lambda_client.list_functions.assert_called_with(MaxItems=self.max_items)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_get_all_lambda_metadata_next_marker_pagination(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

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

        # Assert we get the expected function list after 1 pagination iteration
        # noinspection PyPackageRequirements
        self.assertDictEqual(
            api_calls.get_all_lambda_metadata(),
            self.function_list_after_successful_pagination
        )

        # assert the boto3 lambda client was called with expected params
        m_client.assert_called_with(self.client_type, region_name=self.region)

        # assert the list_function calls were called, and in the expected order
        mock_lambda_client.list_functions.assert_has_calls(expected, any_order=False)

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_lambda_filter_happy_path(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        mock_lambda_client.get_function.return_value = self.get_function_1
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

        # assert the return value is true, since get_function returned a valid response
        # noinspection PyPackageRequirements
        self.assertTrue(
            api_calls.is_iow_lambda_filter(self.valid_function_1)
        )

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_lambda_filter_no_tags(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        mock_lambda_client.get_function.return_value = self.get_function_2
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since get_function returned a response with no 'Tags' key
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_lambda_filter(self.valid_function_2)
        )

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_lambda_filter_no_wma_organization_key(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        mock_lambda_client.get_function.return_value = self.get_function_3
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since get_function returned a response with no wma:organizatoin key
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_lambda_filter(self.valid_function_3)
        )

    @mock.patch('cloudwatch_monitoring.lambdas.boto3.client', autospec=True)
    def test_is_iow_lambda_filter_no_iow_value_for_wma_organization_key(self, m_client):
        mock_lambda_client = mock.Mock()
        m_client.return_value = mock_lambda_client
        mock_lambda_client.get_function.return_value = self.get_function_4
        api_calls = LambdaAPICalls(self.region, self.deploy_stage)

        # assert the return value is False, since get_function returned a response with no 'IOW' value in the
        # wma:organization key
        # noinspection PyPackageRequirements
        self.assertFalse(
            api_calls.is_iow_lambda_filter(self.valid_function_4)
        )

    @mock.patch('cloudwatch_monitoring.lambdas.LambdaAPICalls', autospec=True)
    def test_create_lambda_widgets(self, m_api_calls):
        # return values
        m_api_calls.return_value.get_all_lambda_metadata.return_value = self.full_function_list
        m_api_calls.return_value.is_iow_lambda_filter.side_effect = [
            True, False, True, False, True, True, True, True, True, True
        ]

        # expected calls
        expected_is_iow_lambda_filter_calls = [
            mock.call(self.valid_function_2),
            mock.call(self.bad_function),
            mock.call(self.valid_function_3),
            mock.call(self.bad_function),
            mock.call(self.valid_function_1),
            mock.call(self.valid_function_4),
            mock.call(self.valid_function_5),
            mock.call(self.valid_function_6),
            mock.call(self.valid_function_7),
            mock.call(self.valid_function_8),
        ]

        expected_widget_list = [
            {
                'type': 'metric',
                'height': 6,
                'width': 12,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', 'Resource', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', ],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': False,
                    'region': 'us-south-10',
                    'title': 'Error Handler Activity',
                    'period': 60,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 6,
                'width': 12,
                'properties': {
                    'metrics': self.concurrent_lambdas_metrics_list,
                    'view': 'timeSeries',
                    'stacked': True,
                    'region': 'us-south-10',
                    'period': 60,
                    'stat': 'Average',
                    'title': 'Concurrent Lambdas (Average per minute)',
                }
            },
            {
                'type': 'metric',
                'height': 6,
                'width': 12,
                'properties': {
                    'metrics': self.duration_of_transform_db_lambdas_metrics_list,
                    'view': 'timeSeries', 'stacked': False,
                    'region': 'us-south-10', 'period': 300,
                    'stat': 'Average',
                    'title': 'Duration of Transformation DB Lambdas (Average)'
                }
            },
            {
                'type': 'metric',
                'height': 6,
                'width': 12,
                'properties': {
                    'metrics': self.duration_of_transform_db_lambdas_metrics_list,
                    'view': 'timeSeries', 'stacked': False,
                    'region': 'us-south-10', 'period': 300,
                    'stat': 'Maximum',
                    'title': 'Duration of Transformation DB Lambdas (Maximum)'
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Error Handler',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Capture Trigger',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'DV stat Transformer',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-transform'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Field visit transformer',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'etl-discrete-groundwater-rdb-DEV-loadRdb'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Load RDB Files',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-pruner-DEV-pruneTimeSeries'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Prune Old Data',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-ecosystem-switch-DEV-growDb'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'Grow DB',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            },
            {
                'type': 'metric',
                'height': 3,
                'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'function_DEV_name_not_added_to_lookups_yet'],
                        ['.', 'Invocations', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Duration', '.', '.'],
                        ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                        ['.', 'Throttles', '.', '.']
                    ],
                    'view': 'singleValue',
                    'region': 'us-south-10',
                    'title': 'function_DEV_name_not_added_to_lookups_yet',
                    'period': 300,
                    'stacked': False,
                    'stat': 'Average',
                }
            }
        ]

        positioning = Positioning()
        # Make sure the resultant widget list is correct
        # noinspection PyPackageRequirements
        self.assertListEqual(
            create_lambda_widgets(self.region, self.deploy_stage, positioning),
            expected_widget_list
        )

        # assert our helper functions were called the expected number of times and in the proper order
        m_api_calls.return_value.get_all_lambda_metadata.assert_called_once()
        m_api_calls.return_value.is_iow_lambda_filter.assert_has_calls(expected_is_iow_lambda_filter_calls, any_order=False)
