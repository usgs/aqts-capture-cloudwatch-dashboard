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
    },
    'grow_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'growObsDb',
        'label': 'Grow Obs DB'
    },
    'restore_db_cluster': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'restoreDbCluster',
        'label': 'Restore DB Cluster'
    },
    'grow_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'growDb',
        'label': 'Grow DB'
    },
    'shrink_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'shrinkObsDb',
        'label': 'Shrink Obs Db'
    },
    'execute_grow': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'executeGrow',
        'label': 'Execute Grow'
    },
    'execute_shrink': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'executeShrink',
        'label': 'Execute Shrink'
    },
    'stop_capture_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'StopCaptureDb',
        'label': 'Stop Capture DB'
    },
    'start_capture_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'StartCaptureDb',
        'label': 'Start Capture DB'
    },
    'modify_schema_owner': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'modifySchemaOwner',
        'label': 'Modify Schema Owner'
    },
    'troubleshoot': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'troubleshoot',
        'label': 'Troubleshoot'
    },
    'control_db_utilization': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'ControlDbUtil',
        'label': 'Control DB CPU Utilization'
    },
    'modify_postgres': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'modifyPostgres',
        'label': 'Modify Postgres'
    },
    'create_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'createObservationsDb',
        'label': 'Create Observations DB'
    },
    'prune_data': {
        'repo_name': 'aqts-capture-pruner',
        'descriptor': 'pruneTimeSeries',
        'label': 'Prune Old Data'
    },
    'shrink_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'shrinkDb',
        'label': 'Shrink DB'
    },
    'delete_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'deleteObservationsDb',
        'label': 'Delete Observations DB'
    },
    'modify_obs_postgres': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'modifyObPostgres',
        'label': 'Modify Observations DB Postgres'
    },
    'delete_capture_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'deleteCaptureDb',
        'label': 'Delete Capture DB'
    },
    'start_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'StartObservationsDb',
        'label': 'Start Observations DB'
    },
    'modify_obs_passwords': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'modifyObPasswords',
        'label': 'Modify Observations DB Passwords'
    },
    'enable_trigger': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'enableTrigger',
        'label': 'Enable Trigger'
    },
    'create_db_instance': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'createDbInstance',
        'label': 'Create DB Instance'
    },
    'copy_obs_db_snapshot': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'copyObDbSnapshot',
        'label': 'Copy Observations DB Snapshot'
    },
    'stop_observations_db': {
        'repo_name': 'aqts-capture-ecosystem-switch',
        'descriptor': 'StopObservationsDb',
        'label': 'Stop Observations DB'
    },
    'etl_discrete_gw_rdb': {
        'repo_name': 'etl-discrete-groundwater-rdb',
        'descriptor': 'loadRdb',
        'label': 'Load RDB Files'
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
    ],
    'duration_of_transform_db_lambdas': [
        'dvstat_transform',
        'raw_load',
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

# sqs queues
sqs_queues = {
    'aqts-capture-error-queue': {
        'title': 'Error Queue'
    },
    'aqts-capture-trigger-queue': {
        'title': 'Capture Trigger Queue'
    }
}

# State machine properties
state_machines = {
    'aqts-capture-state-machine': {
        'title': 'ETL State Machine'
    },
    'aqts-ecosystem-switch-shrink-capture-db': {
        'title': 'Shrink Capture DB State Machine'
    },
    'aqts-ecosystem-switch-grow-capture-db': {
        'title': 'Grow Capture DB State Machine'
    },
    'aqts-capture-ecosystem-switch-create-capture-db': {
        'title': 'Create Capture DB State Machine'
    },
    'aqts-capture-ecosystem-switch-create-obs-db': {
        'title': 'Create Observations DB State Machine'
    },
    'aqts-capture-load-test': {
        'title': 'ETL Load Test State Machine'
    }
}
