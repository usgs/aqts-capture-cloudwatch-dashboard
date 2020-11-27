"""
Module for holding test widget resources

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

custom_lambda_title_widget = {
    'type': 'text',
    'height': 1,
    'width': 24,
    'properties': {
        'markdown': '# Lambda Status'
    }
}

iow_lambda_title = {
    'type': 'text',
    'height': 1,
    'width': 24,
    'properties': {
        'markdown': "# Status of each 'IOW' tagged lambda in the account"
    }
}

error_handler_activity_widget = {
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
}

concurrent_lambdas_widget = {
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
}

average_duration_of_transform_db_lambdas_widget = {
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
}

max_duration_of_transform_db_lambdas = {
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
}

error_handler_numeric_stats_widget = {
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
}

error_handler_concurrent_executions_widget = {
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
}

error_handler_duration_widget = {
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
}

error_handler_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-error-handler-DEV-aqtsErrorHandler' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Error Handler Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

capture_trigger_numeric_stats_widget = {
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
}

capture_trigger_concurrent_executions_widget = {
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
}

capture_trigger_duration_widget = {
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
}

capture_trigger_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-trigger-DEV-aqtsCaptureTrigger' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Capture Trigger Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

dvstat_transform_numeric_stats_widget = {
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
}

dvstat_transform_concurrent_executions_widget = {
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
}

dvstat_transform_duration_widget = {
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
}

dvstat_transform_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-dvstat-transform-DEV-transform' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "DV stat Transformer Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

field_visit_transform_numeric_stats_widget = {
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
}

field_visit_transform_concurrent_executions_widget = {
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
}

field_visit_transform_duration_widget = {
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
}

field_visit_transform_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-field-visit-transform-DEV-transform' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Field visit transformer Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

field_visit_transform_es_logger_numeric_stats_widget = {
    'type': 'metric',
    'height': 6,
    'width': 4,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'Invocations', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-es-logs-plugin', {'stat': 'Sum'}],
            ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
            ['.', 'Duration', '.', '.'],
            ['.', 'ConcurrentExecutions', '.', '.'],
            ['.', 'Throttles', '.', '.']
        ],
        'view': 'singleValue',
        'region': 'us-south-10',
        'title': 'Field visit transformer ES logger',
        'period': 300,
        'stacked': False,
        'stat': 'Average'
    }
}

field_visit_transform_es_logger_concurrent_executions_widget = {
    'type': 'metric',
    'height': 6,
    'width': 8,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-es-logs-plugin', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
            ['.', 'Invocations', '.', '.'],
            ['.', 'Errors', '.', '.'],
            ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
        ],
        'view': 'timeSeries',
        'region': 'us-south-10',
        'title': 'Field visit transformer ES logger Concurrent Executions',
        'period': 300,
        'stat': 'Sum',
        'stacked': False
    }
}

field_visit_transform_es_logger_duration_widget = {
    'type': 'metric',
    'height': 6,
    'width': 6,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'Duration', 'FunctionName', 'aqts-capture-field-visit-transform-DEV-es-logs-plugin', {'yAxis': 'left'}],
            ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
        ],
        'view': 'timeSeries',
        'region': 'us-south-10',
        'title': 'Field visit transformer ES logger Duration',
        'period': 300,
        'stat': 'Average',
        'stacked': False
    }
}

field_visit_transform_es_logger_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-field-visit-transform-DEV-es-logs-plugin' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Field visit transformer ES logger Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

rdb_loader_numeric_stats_widget = {
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
}

rdb_loader_concurrent_executions_widget = {
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
}

rdb_loader_duration_widget = {
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
}

rdb_loader_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/etl-discrete-groundwater-rdb-DEV-loadRdb' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Load RDB Files Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

pruner_numeric_stats_widget = {
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
}

pruner_concurrent_executions_widget = {
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
}

pruner_duration_widget = {
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
}

pruner_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-pruner-DEV-pruneTimeSeries' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Prune Old Data Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

grow_db_numeric_stats_widget = {
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
}

grow_db_concurrent_executions_widget = {
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
}

grow_db_duration_widget = {
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
}

grow_db_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/aqts-capture-ecosystem-switch-DEV-growDb' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "Grow DB Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

misc_function_numeric_stats_widget = {
    'type': 'metric',
    'height': 6,
    'width': 4,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'Invocations', 'FunctionName', 'function-name-not-added-to-lookups-yet-DEV-descriptor', {'stat': 'Sum'}],
            ['.', 'Errors', '.', '.', {'stat': 'Sum'}],
            ['.', 'Duration', '.', '.'],
            ['.', 'ConcurrentExecutions', '.', '.'],
            ['.', 'Throttles', '.', '.']
        ],
        'view': 'singleValue',
        'region': 'us-south-10',
        'title': 'function-name-not-added-to-lookups-yet-DEV-descriptor',
        'period': 300,
        'stacked': False,
        'stat': 'Average'
    }
}

misc_function_concurrent_executions_widget = {
    'type': 'metric',
    'height': 6,
    'width': 8,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'ConcurrentExecutions', 'FunctionName', 'function-name-not-added-to-lookups-yet-DEV-descriptor', {'stat': 'Maximum', 'label': 'ConcurrentExecutions (max)'}],
            ['.', 'Invocations', '.', '.'],
            ['.', 'Errors', '.', '.'],
            ['.', 'Throttles', '.', '.', {'stat': 'Average'}]
        ],
        'view': 'timeSeries',
        'region': 'us-south-10',
        'title': 'function-name-not-added-to-lookups-yet-DEV-descriptor Concurrent Executions',
        'period': 300,
        'stat': 'Sum',
        'stacked': False
    }
}

misc_function_duration_widget = {
    'type': 'metric',
    'height': 6,
    'width': 6,
    'properties': {
        'metrics': [
            ['AWS/Lambda', 'Duration', 'FunctionName', 'function-name-not-added-to-lookups-yet-DEV-descriptor', {'yAxis': 'left'}],
            ['...', {'yAxis': 'right', 'stat': 'Maximum'}]
        ],
        'view': 'timeSeries',
        'region': 'us-south-10',
        'title': 'function-name-not-added-to-lookups-yet-DEV-descriptor Duration',
        'period': 300,
        'stat': 'Average',
        'stacked': False
    }
}

misc_function_memory_usage_widget = {
    "type": "log",
    'height': 6,
    'width': 6,
    "properties": {
        "query": f"SOURCE '/aws/lambda/function-name-not-added-to-lookups-yet-DEV-descriptor' | filter @type=\"REPORT\" | max(@memorySize) as allocatedMemory, avg(@maxMemoryUsed) as mean_MemoryUsed, max(@maxMemoryUsed) as max_MemoryUsed by bin(5min)",
        "region": 'us-south-10',
        "title": "function-name-not-added-to-lookups-yet-DEV-descriptor Memory Usage",
        "view": "timeSeries",
        "stacked": False
    }
}

expected_lambda_widget_list = [

    # title
    custom_lambda_title_widget,

    # custom widgets
    error_handler_activity_widget,
    concurrent_lambdas_widget,
    average_duration_of_transform_db_lambdas_widget,
    max_duration_of_transform_db_lambdas,

    # title
    iow_lambda_title,

    # autogenerated widgets
    error_handler_numeric_stats_widget,
    error_handler_concurrent_executions_widget,
    error_handler_duration_widget,
    error_handler_memory_usage_widget,

    capture_trigger_numeric_stats_widget,
    capture_trigger_concurrent_executions_widget,
    capture_trigger_duration_widget,
    capture_trigger_memory_usage_widget,

    dvstat_transform_numeric_stats_widget,
    dvstat_transform_concurrent_executions_widget,
    dvstat_transform_duration_widget,
    dvstat_transform_memory_usage_widget,

    field_visit_transform_numeric_stats_widget,
    field_visit_transform_concurrent_executions_widget,
    field_visit_transform_duration_widget,
    field_visit_transform_memory_usage_widget,

    field_visit_transform_es_logger_numeric_stats_widget,
    field_visit_transform_es_logger_concurrent_executions_widget,
    field_visit_transform_es_logger_duration_widget,
    field_visit_transform_es_logger_memory_usage_widget,

    rdb_loader_numeric_stats_widget,
    rdb_loader_concurrent_executions_widget,
    rdb_loader_duration_widget,
    rdb_loader_memory_usage_widget,

    pruner_numeric_stats_widget,
    pruner_concurrent_executions_widget,
    pruner_duration_widget,
    pruner_memory_usage_widget,

    grow_db_numeric_stats_widget,
    grow_db_concurrent_executions_widget,
    grow_db_duration_widget,
    grow_db_memory_usage_widget,

    misc_function_numeric_stats_widget,
    misc_function_concurrent_executions_widget,
    misc_function_duration_widget,
    misc_function_memory_usage_widget
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
