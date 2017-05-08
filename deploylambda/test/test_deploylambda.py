import os

import json
from unittest import TestCase
from ..deploylambda import DeployLambda

__author__ = 'matt-land'


class TestDeployLambda(TestCase):
    def test_update_metadata(self):
        d = DeployLambda()
        d.update_metadata("hackathoncolors")

    def test_build_metadata(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skeleton_config.json')) as data_file:
            skeleton = json.load(data_file)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), './new_config.json')) as data_file:
            new_config = json.load(data_file)
        data = DeployLambda._build_metadata(skeleton, new_config)
        self.assertEquals(8, data.__len__())