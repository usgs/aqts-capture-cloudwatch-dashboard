"""
Module for holding test resources

"""

concurrent_lambdas_metrics_list = [
    ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'label': 'DV stat Transformer'}],
    ['...', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', {'label': 'Error Handler'}],
    ['...', 'aqts-capture-raw-load-DEV-iowCapture', {'label': 'Raw Loader'}],
    ['...', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'label': 'Capture Trigger'}],
    ['...', 'aqts-capture-ts-corrected-DEV-preProcess', {'label': 'TS corrected preprocessor'}],
    ['...', 'aqts-capture-ts-description-DEV-processTsDescription', {'label': 'TS descriptions preprocessor'}],
    ['...', 'aqts-ts-type-router-DEV-determineRoute', {'label': 'TS type router'}],
    ['...', 'aqts-capture-ts-loader-DEV-loadTimeSeries', {'label': 'DV TS loader'}],
    ['...', 'aqts-capture-ts-field-visit-DEV-preProcess', {'label': 'Field visit preprocessor'}],
    ['...', 'aqts-capture-field-visit-transform-DEV-transform', {'label': 'Field visit transformer'}],
    ['...', 'aqts-capture-discrete-loader-DEV-loadDiscrete', {'label': 'Discrete GW loader'}],
    ['...', 'aqts-capture-field-visit-metadata-DEV-preProcess', {'label': 'Field visit metadata preprocessor'}],
    ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}],
    ['...', 'aqts-capture-raw-load-DEV-iowCaptureSmall', {'label': 'Raw Load Small'}],
    ['...', 'aqts-capture-raw-load-DEV-iowCaptureExtraSmall', {'label': 'Raw Load Extra Small'}]
]

duration_of_transform_db_lambdas_metrics_list = [
     ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'label': 'DV stat Transformer'}],
     ['...', 'aqts-capture-raw-load-DEV-iowCapture', {'label': 'Raw Loader'}],
     ['...', 'aqts-capture-ts-corrected-DEV-preProcess', {'label': 'TS corrected preprocessor'}],
     ['...', 'aqts-capture-ts-description-DEV-processTsDescription', {'label': 'TS descriptions preprocessor'}],
     ['...', 'aqts-ts-type-router-DEV-determineRoute', {'label': 'TS type router'}],
     ['...', 'aqts-capture-ts-loader-DEV-loadTimeSeries', {'label': 'DV TS loader'}],
     ['...', 'aqts-capture-ts-field-visit-DEV-preProcess', {'label': 'Field visit preprocessor'}],
     ['...', 'aqts-capture-field-visit-transform-DEV-transform', {'label': 'Field visit transformer'}],
     ['...', 'aqts-capture-discrete-loader-DEV-loadDiscrete', {'label': 'Discrete GW loader'}],
     ['...', 'aqts-capture-field-visit-metadata-DEV-preProcess', {'label': 'Field visit metadata preprocessor'}],
     ['...', 'aqts-capture-raw-load-DEV-iowCaptureMedium', {'label': 'Raw Load Medium'}],
     ['...', 'aqts-capture-raw-load-DEV-iowCaptureSmall', {'label': 'Raw Load Small'}],
     ['...', 'aqts-capture-raw-load-DEV-iowCaptureExtraSmall', {'label': 'Raw Load Extra Small'}]
]

expected_lambda_widget_list = [
    # title widget for custom lambdas
    {'type': 'text', 'height': 1, 'width': 24, 'properties': {'markdown': '# Lambda Status'}},

    # error handler activity
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
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
    },

    # concurrent lambdas
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            'metrics': concurrent_lambdas_metrics_list,
            'view': 'timeSeries',
            'stacked': True,
            'region': 'us-south-10',
            'period': 60,
            'stat': 'Average',
            'title': 'Concurrent Lambdas (Average per minute)'}
    },

    # average duration of transform db lambdas
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            'metrics': duration_of_transform_db_lambdas_metrics_list,
            'view': 'timeSeries',
            'stacked': False,
            'region': 'us-south-10',
            'period': 300,
            'stat': 'Average',
            'title': 'Duration of Transformation DB Lambdas (Average)'}
    },

    # max duration of transform db lambdas
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            'metrics': duration_of_transform_db_lambdas_metrics_list,
            'view': 'timeSeries',
            'stacked': False,
            'region': 'us-south-10',
            'period': 300,
            'stat': 'Maximum',
            'title': 'Duration of Transformation DB Lambdas (Maximum)'
        }
    },

    # title widget for generic IOW lambdas
    {
        'type': 'text',
        'height': 1,
        'width': 24,
        'properties': {
            'markdown': "# Status of each 'IOW' tagged lambda in the account"
        }
    },

    # error handler numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Error Handler',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # error handler concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler',{'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Error Handler Concurrent Executions',
            'period': 300,
            'stat': 'Sum',
            'stacked': False
        }
    },

    # error handler duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-error-handler-DEV-aqtsErrorHandler', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Error Handler Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # error handler memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-error-handler-DEV-aqtsErrorHandler' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Error Handler Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # capture trigger numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Capture Trigger',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # capture trigger concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Capture Trigger Concurrent Executions',
            'period': 300,
            'stat': 'Sum',
            'stacked': False
        }
    },

    # capture trigger duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-trigger-DEV-aqtsCaptureTrigger', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Capture Trigger Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # capture trigger memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-trigger-DEV-aqtsCaptureTrigger' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Capture Trigger Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # DV stat transformer numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'DV stat Transformer',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # DV stat transformer concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'DV stat Transformer Concurrent Executions',
            'period': 300,
            'stat': 'Sum',
            'stacked': False
        }
    },

    # DV stat transformer duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-dvstat-transform-DEV-transform', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'DV stat Transformer Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # DV stat transformer memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-dvstat-transform-DEV-transform' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "DV stat Transformer Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # field visit transformer numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-transform', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Field visit transformer',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # field visit transformer concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-transform', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Field visit transformer Concurrent Executions',
            'period': 300,
            'stat': 'Sum',
            'stacked': False
        }
    },

    # field visit transformer duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-transform', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Field visit transformer Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # field visit transformer memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-field-visit-transform-DEV-transform' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Field visit transformer Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # RDB loader numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'etl-discrete-groundwater-rdb-DEV-loadRdb', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Load RDB Files',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # RDB loader concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'etl-discrete-groundwater-rdb-DEV-loadRdb', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Load RDB Files Concurrent Executions',
            'period': 300, 'stat': 'Sum',
            'stacked': False
        }
    },

    # RDB loader duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'etl-discrete-groundwater-rdb-DEV-loadRdb', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Load RDB Files Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # RDB loader memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/etl-discrete-groundwater-rdb-DEV-loadRdb' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Load RDB Files Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # transform db pruner numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-pruner-DEV-pruneTimeSeries', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Prune Old Data',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # transform db pruner concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-pruner-DEV-pruneTimeSeries', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Prune Old Data Concurrent Executions',
            'period': 300, 'stat': 'Sum',
            'stacked': False
        }
    },

    # transform db pruner duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-pruner-DEV-pruneTimeSeries', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Prune Old Data Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # transform db pruner memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-pruner-DEV-pruneTimeSeries' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Prune Old Data Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # ecosystem switch - grow db numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-ecosystem-switch-DEV-growDb', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'Grow DB',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # ecosystem switch - grow db concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-ecosystem-switch-DEV-growDb', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Grow DB Concurrent Executions',
            'period': 300, 'stat': 'Sum',
            'stacked': False
        }
    },

    # ecosystem switch - grow db duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-ecosystem-switch-DEV-growDb', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'Grow DB Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # ecosystem switch - grow db memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/aqts-capture-ecosystem-switch-DEV-growDb' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "Grow DB Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    },

    # misc/lookup not added yet for this function - numeric stats
    {
        'type': 'metric',
        'height': 6,
        'width': 4,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Invocations', 'FunctionName', 'function_DEV_name_not_added_to_lookups_yet', {'stat': 'Sum'}],
                ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
                ['.', 'Duration', '.', '.'],
                ['.', 'ConcurrentExecutions', '.', '.'],
                ['.', 'Throttles', '.', '.']
            ],
            'view': 'singleValue',
            'region': 'us-south-10',
            'title': 'function_DEV_name_not_added_to_lookups_yet',
            'period': 300,
            'stacked': False,
            'stat': 'Average'
        }
    },

    # misc/lookup not added yet for this function - concurrent executions graph
    {
        'type': 'metric',
        'height': 6,
        'width': 8,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'function_DEV_name_not_added_to_lookups_yet', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
                ['.', 'Invocations', '.', '.'],
                ['.', 'Errors', '.', '.'],
                ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'function_DEV_name_not_added_to_lookups_yet Concurrent Executions',
            'period': 300,
            'stat': 'Sum',
            'stacked': False
        }
    },

    # misc/lookup not added yet for this function - duration graph
    {
        'type': 'metric',
        'height': 6,
        'width': 6,
        'properties': {
            'metrics': [
                ['AWS/Lambda', 'Duration', 'FunctionName', 'function_DEV_name_not_added_to_lookups_yet', {'yAxis': 'left'}],
                ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
            ],
            'view': 'timeSeries',
            'region': 'us-south-10',
            'title': 'function_DEV_name_not_added_to_lookups_yet Duration',
            'period': 300,
            'stat': 'Average',
            'stacked': False
        }
    },

    # misc/lookup not added yet for this function - memory usage
    {
        "type": "log",
        'height': 6,
        'width': 6,
        "properties": {
            "query": f"SOURCE '/aws/lambda/function_DEV_name_not_added_to_lookups_yet' | filter @type=\"REPORT\" | avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
            "region": 'us-south-10',
            "title": "function_DEV_name_not_added_to_lookups_yet Memory Usage",
            "view": "timeSeries",
            "stacked": False
        }
    }
]

expected_nwcapture_db_status_widget = {
    'type': 'metric',
    'height': 6,
    'width': 12,
    'properties': {
        'metrics': [
            ['AWS/RDS','CPUUtilization', 'DBClusterIdentifier', 'nwcapture-dev'],
            ['.', 'DatabaseConnections', '.', '.', {'yAxis': 'right'}]
        ],
        'view': 'timeSeries',
        'stacked': False,
        'region': 'us-south-10',
        'title': 'Nwcapture DB Status',
        'period': 300,
        'stat': 'Average'
    }
}

expected_observations_db_status_widget = {
    'type': 'metric',
    'height': 6,
    'width': 12,
    'properties': {
        'metrics': [
            ['AWS/RDS', 'CPUUtilization', 'DBInstanceIdentifier', 'observations-dev'],
            ['.', 'DatabaseConnections', '.', '.', {'yAxis': 'right'}]
        ],
        'view': 'timeSeries',
        'stacked': False,
        'region': 'us-south-10',
        'title': 'Observations DB Status',
        'period': 300,
        'stat': 'Average'
    }
}

expected_status_db_widget_list = [
    {
        'type': 'text',
        'height': 1,
        'width': 24,
        'properties': {
            "markdown": "# Database Status"
        }
    },
    expected_nwcapture_db_status_widget,
    expected_observations_db_status_widget
]

expected_queue_list = [
    {
        'type': 'text',
        'height': 1,
        'width': 24,
        'properties': {
            "markdown": "# Queue Status"
        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "aqts-capture-trigger-queue-DEV"],
                [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesDeleted", ".", "."],
                [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "period": 60,
            "title": "Capture Trigger Queue",
            "stat": "Average",

        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "aqts-capture-error-queue-DEV"],
                [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesDeleted", ".", "."],
                [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "period": 60,
            "title": "Error Queue",
            "stat": "Average",
        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "a-neat-valid-queue-DEV"],
                [".", "ApproximateAgeOfOldestMessage", ".", ".", {"yAxis": "right"}],
                [".", "NumberOfMessagesReceived", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesSent", ".", ".", {"stat": "Sum"}],
                [".", "NumberOfMessagesDeleted", ".", "."],
                [".", "ApproximateNumberOfMessagesDelayed", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "period": 60,
            "title": "a-neat-valid-queue-DEV",
            "stat": "Average",
        }
    }
]

expected_state_machine_list = [
    {
        'type': 'text',
        'height': 1,
        'width': 24,
        'properties': {
            "markdown": "# State Machine Status"
        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/States", "ExecutionsStarted", "StateMachineArn", "arn:aws:states:us-west-2:807615458658:stateMachine:aqts-ecosystem-switch-shrink-capture-db-DEV"],
                [".", "ExecutionsSucceeded", ".", "."],
                [".", "ExecutionsFailed", ".", "."],
                [".", "ExecutionsTimedOut", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "stat": "Sum",
            "period": 60,
            "title": "Shrink Capture DB State Machine"
        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/States", "ExecutionsStarted", "StateMachineArn", "arn:aws:states:us-west-2:807615458658:stateMachine:aqts-ecosystem-switch-grow-capture-db-DEV"],
                [".", "ExecutionsSucceeded", ".", "."],
                [".", "ExecutionsFailed", ".", "."],
                [".", "ExecutionsTimedOut", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "stat": "Sum",
            "period": 60,
            "title": "Grow Capture DB State Machine"
        }
    },
    {
        'type': 'metric',
        'height': 6,
        'width': 12,
        'properties': {
            "metrics": [
                ["AWS/States", "ExecutionsStarted", "StateMachineArn", "arn:aws:states:us-west-2:807615458658:stateMachine:a-neat-state-machine-DEV"],
                [".", "ExecutionsSucceeded", ".", "."],
                [".", "ExecutionsFailed", ".", "."],
                [".", "ExecutionsTimedOut", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": "us-south-10",
            "stat": "Sum",
            "period": 60,
            "title": "a-neat-state-machine-DEV"
        }
    }
]
