"""
module containing lookup key-value mappings for various IOW cloud assets.

"""

# not necessarily a complete dictionary of all IOW lambda assets
# add to this list when you need to add a lambda to a custom widget
dashboard_lambdas = {
    'dvstat_transform': {
        'repo_name': 'aqts-capture-dvstat-transform',
        'descriptor': 'transform',
        'label': 'DV stat Transformer'
    },
    'error_handler': {
        'repo_name': 'aqts-capture-error-handler',
        'descriptor': 'aqtsErrorHandler',
        'label': 'Error Handler'
    },
    'raw_load': {
        'repo_name': 'aqts-capture-raw-load',
        'descriptor': 'iowCapture',
        'label': 'Raw Loader'
    },
    'capture_trigger': {
        'repo_name': 'aqts-capture-trigger',
        'descriptor': 'aqtsCaptureTrigger',
        'label': 'Capture trigger'
    },
    'ts_corrected': {
        'repo_name': 'aqts-capture-ts-corrected',
        'descriptor': 'preProcess',
        'label': 'TS corrected preprocessor'
    },
    'ts_description': {
        'repo_name': 'aqts-capture-ts-description',
        'descriptor': 'processTsDescription',
        'label': 'TS descriptions preprocessor'
    },
    'ts_type_router': {
        'repo_name': 'aqts-ts-type-router',
        'descriptor': 'determineRoute',
        'label': 'TS type router'
    },
    'ts_loader': {
        'repo_name': 'aqts-capture-ts-loader',
        'descriptor': 'loadTimeSeries',
        'label': 'DV TS loader'
    },
    'ts_field_visit': {
        'repo_name': 'aqts-capture-ts-field-visit',
        'descriptor': 'preProcess',
        'label': 'Field visit preprocessor'
    },
    'field_visit_transform': {
        'repo_name': 'aqts-capture-field-visit-transform',
        'descriptor': 'transform',
        'label': 'Field visit transformer'
    },
    'discrete_loader': {
        'repo_name': 'aqts-capture-discrete-loader',
        'descriptor': 'loadDiscrete',
        'label': 'Discrete GW loader'
    },
    'field_visit_metadata': {
        'repo_name': 'aqts-capture-field-visit-metadata',
        'descriptor': 'preProcess',
        'label': 'Field visit metadata preprocessor'
    },
    'raw_load_medium': {
        'repo_name': 'aqts-capture-raw-load',
        'descriptor': 'iowCaptureMedium',
        'label': 'Raw Load Medium'
    },
    'raw_load_small': {
        'repo_name': 'aqts-capture-raw-load',
        'descriptor': 'iowCaptureSmall',
        'label': 'Raw Load Small'
    },
    'raw_load_extra_small': {
        'repo_name': 'aqts-capture-raw-load',
        'descriptor': 'iowCaptureExtraSmall',
        'label': 'Raw Load Extra Small'
    }
}

# list of custom lambda widgets and the lambdas they include
custom_lambda_widgets = {
    'concurrent_lambdas': [
        'dvstat_transform',
        'error_handler',
        'raw_load',
        'capture_trigger',
        'ts_corrected',
        'ts_description',
        'ts_type_router',
        'ts_loader',
        'ts_field_visit',
        'field_visit_transform',
        'discrete_loader',
        'field_visit_metadata',
        'raw_load_medium',
        'raw_load_small',
        'raw_load_extra_small'
    ]
}

error_handler_activity = {
    'error_handler_activity': 'error_handler'
}

# May not need lookups for this, but we do sometimes change the database properties from tier to tier, and those
# properties sometimes deviate from convention.
# for example: 'observations-prod-external-2' vs. 'nwcapture-prod-external'
# Add tier/db specific properties here
rds_instances = {
    'nwcapture': {
        'identifier_type': 'DBClusterIdentifier',
        'DEV': {
            'identifier': 'nwcapture-dev',
        },
        'TEST': {
            'identifier': 'nwcapture-test',
        },
        'QA': {
            'identifier': 'nwcapture-qa',
        },
        'PROD-EXTERNAL': {
            'identifier': 'nwcapture-prod-external',
        }
    },
    'observations': {
        'identifier_type': 'DBInstanceIdentifier',
        'DEV': {
            'identifier': 'observations-dev',
        },
        'TEST': {
            'identifier': 'observations-test',
        },
        'QA': {
            'identifier': 'observations-qa',
        },
        'PROD-EXTERNAL': {
            'identifier': 'observations-prod-external-2',
        }
    }
}
