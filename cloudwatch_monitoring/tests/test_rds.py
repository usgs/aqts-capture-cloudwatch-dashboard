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

    def test_generate_db_status_widget(self):
        print('first rds test')
        # fill in the blanks

    def test_create_rds_widgets(self):
        print('second rds test')
        # fill in the blanks
