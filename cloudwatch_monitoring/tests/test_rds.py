"""
Tests for the rds module.

"""
from unittest import TestCase

from .test_widgets import (expected_nwcapture_db_status_widget, expected_observations_db_status_widget,
                           expected_status_db_widget_list)
from ..rds import (create_rds_widgets, generate_db_status_widget)


class TestCreateRDSWidgets(TestCase):

    def setUp(self):
        self.deploy_stage = 'DEV'
        self.region = 'us-south-10'

    def test_generate_db_status_widget_observations(self):
        self.assertDictEqual(
            generate_db_status_widget(self.region, self.deploy_stage, 'observations'),
            expected_observations_db_status_widget
        )

    def test_generate_db_status_widget_nwcapture(self):
        self.assertDictEqual(
            generate_db_status_widget(self.region, self.deploy_stage, 'nwcapture'),
            expected_nwcapture_db_status_widget
        )

    def test_create_rds_widgets(self):
        # do widgets, including the title widget, appear in the expected order
        self.assertListEqual(
            create_rds_widgets(self.region, self.deploy_stage),
            expected_status_db_widget_list
        )
