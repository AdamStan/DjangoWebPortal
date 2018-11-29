from django.test import TestCase
from ..models import *
from ..add_data import add_entities
from ..algorithm import *

class TestAlgorithm(TestCase):
    """
    Run add_entities at start because django set up default temporary table when it starts testing
    """
    def setUp(self):
        add_entities()

    def test_create_plans(self):
        pass

