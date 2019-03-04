from django.test import TestCase, TransactionTestCase
from ..models import *
from accounts.models import User
from datetime import time
from .test_entities import AbstractTestEntities

class TestViewModel(AbstractTestEntities):
    pass
