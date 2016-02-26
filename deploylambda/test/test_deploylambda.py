from unittest import TestCase
from ..deploylambda import DeployLambda

__author__ = 'matt-land'


class TestDeployLambda(TestCase):
    def test_update_metadata(self):
        d = DeployLambda()
        d.update_metadata("hackathoncolors")
