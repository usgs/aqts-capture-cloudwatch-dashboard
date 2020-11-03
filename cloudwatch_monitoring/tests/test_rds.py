"""
Tests for the rds module.

"""
from unittest import TestCase

from ..positioning import Positioning
from ..rds import (create_rds_widgets, generate_db_status_widget)


class TestCreateRDSWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'

        self.expected_nwcapture_db_status_widget = {
            'type': 'metric',
            'x': 0,
            'y': 0,
            'height': 6,
            'width': 24,
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

        self.expected_observations_db_status_widget = {
            'type': 'metric',
            'x': 0,
            'y': 0,
            'height': 6,
            'width': 24,
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

        self.expected_status_db_widget_list = [
            {
                'type': 'metric',
                 'x': 0,
                 'y': 0,
                 'height': 6,
                 'width': 24,
                'properties': {
                    'metrics': [
                        ['AWS/RDS', 'CPUUtilization', 'DBClusterIdentifier', 'nwcapture-dev'],
                        ['.', 'DatabaseConnections', '.', '.', {'yAxis': 'right'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': False,
                    'region': 'us-south-10',
                    'title': 'Nwcapture DB Status',
                    'period': 300,
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
                        ['AWS/RDS', 'CPUUtilization', 'DBInstanceIdentifier', 'observations-dev'],
                        ['.', 'DatabaseConnections', '.', '.', {'yAxis': 'right'}]
                    ],
                    'view': 'timeSeries',
                    'stacked': False,
                    'region': 'us-south-10',
                    'title': 'Observations DB Status',
                    'period': 300,
                    'stat': 'Average'}
            }
        ]

    def test_generate_db_status_widget_observations(self):
        positioning = Positioning()
        self.assertDictEqual(
            generate_db_status_widget(self.region, self.deploy_stage, positioning, 'observations'),
            self.expected_observations_db_status_widget
        )

    def test_generate_db_status_widget_nwcapture(self):
        positioning = Positioning()
        self.assertDictEqual(
            generate_db_status_widget(self.region, self.deploy_stage, positioning, 'nwcapture'),
            self.expected_nwcapture_db_status_widget
        )

    def test_create_rds_widgets(self):
        # more of a test that positioning works
        positioning = Positioning()
        self.assertListEqual(
            create_rds_widgets(self.region, self.deploy_stage, positioning),
            self.expected_status_db_widget_list
        )
